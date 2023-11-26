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

    username = body["username"]
    password = body["password"]
    db = get_db()
    error = None

    # execute does an SQL query
    # fetchone returns one row, as opposed to fetchall which fetches the first matching row
    user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()

    if user is None:
        error = "Incorrect username."
    elif not check_password_hash(user["password"], password):
        error = "Incorrect password."

    if error is None:
        session.clear()
        session["user_id"] = user["id"]
        user_type = user["user_type"]
        user_id = user["id"]
        active = user["is_active"]

    if not active:
        error = "This user has been deactivated.  Please contact us to appeal this ban."

    flash(error)
    response = {"error": error} if error else {"id": user_id, "user_type": user_type, "is_active": active}
    return json.dumps(response)


# localhost:5000/auth/register
@bp.route("/register", methods=["POST"])
def register():
    body = request.get_json()

    username = body["username"]
    password = body["password"]
    user_type = body["user_type"]
    db = get_db()
    error = None

    if not username:
        error = "Username is required."
    elif not password:
        error = "Password is required."

    if error is None:
        try:
            id = db.execute(
                "INSERT INTO user (username, password, user_type, is_active) VALUES (?, ?, ?, ?)",
                (username, generate_password_hash(password), user_type, 1),
            ).lastrowid
            db.commit()
        except db.IntegrityError:
            error = f"User {username} is already registered."
    response = {"error": error} if error else {"success": id}
    return json.dumps(response)
