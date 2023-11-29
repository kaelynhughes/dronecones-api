import functools, json

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from api.db import get_db

# defines the first chunk of the URL after localhost
# helps us organize our endpoints
# this one specifies that its endpoints will follow the form localhost:5000/auth/[more stuff]
bp = Blueprint("auth", __name__, url_prefix="/auth")


# localhost:5000/auth/login
# first line associates the URL /login with the login function
# the user submitted a login form, so the method will be POST
@bp.route("/login", methods=["POST"])
def login():
    # request.form is a kind of dict mapping with form keys and values
    body = request.get_json()
    try:
        username = body["username"]
        password = body["password"]
    except KeyError:
        return {"error": "Bad data: username or password not provided."}, 400

    db = get_db()

    # execute does an SQL query
    # fetchone returns one row, as opposed to fetchall which fetches the first matching row
    user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()

    if user is None:
        return {"error": "Incorrect username."}, 401
    elif not check_password_hash(user["password"], password):
        return {"error": "Incorrect password."}, 401

    session.clear()
    try:
        session["user_id"] = user["id"]
        user_type = user["user_type"]
        user_id = user["id"]
        active = user["is_active"]
    except Exception:
        return {
            "error": "Looks like there's some malformed data on our end. Sorry!"
        }, 404

    if not active:
        return {
            "error": "This user has been deactivated.  Please contact us to appeal this ban."
        }, 401

    response = {"id": user_id, "user_type": user_type, "is_active": active}
    return json.dumps(response)


# localhost:5000/auth/register
@bp.route("/register", methods=["POST"])
def register():
    body = request.get_json()
    try:
        username = body["username"]
        password = body["password"]
        user_type = body["user_type"]
    except KeyError:
        return {
            "error": "Bad data: username, password, or user type not provided."
        }, 401
    db = get_db()

    try:
        id = db.execute(
            "INSERT INTO user (username, password, user_type, is_active) VALUES (?, ?, ?, ?)",
            (username, generate_password_hash(password), user_type, 1),
        ).lastrowid
        db.commit()
    except db.IntegrityError:
        return {"error": f"User {username} is already registered."}, 409
    response = {"success": id}
    return json.dumps(response, 201)
