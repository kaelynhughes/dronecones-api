import json

from flask import (
    Blueprint,
    request,
    session,
)

from api.db import get_db

bp = Blueprint("employee", __name__, url_prefix="/employee")


@bp.route("/drones", methods=["GET"])
def drones():
    owner_id = 1
    # session.get("user_id")
    db = get_db()
    error = None
    query = """
    SELECT display_name, id, is_active
    FROM drone
    WHERE id = ?
    """
    drones = db.execute(query, owner_id).fetchall()

    if drone is None:
        error = "This feature is not available yet - check back later!"
    elif len(drones) == 0:
        error = "No drones have been registered!"

    if error:
        return json.dumps({"error": error})
    else:
        return json.dumps({"drones": drones})
    # return list of all drones and their immediately relevant info
    # response should look like: {'drones': [ {name: Drone2, size: number, id: 10394825, isActive: true } ]}


@bp.route("/earnings", methods=["GET"])
def earnings():
    db = get_db()
    # return a single value with total earnings
    # example: {'earnings': 56600} for $566.00


@bp.route("/drone", methods=["POST", "DELETE", "PUT"])
def drone():
    if request.method == "POST":
        print(request.form["display_name"])
        display_name = request.form["display_name"]
        drone_size = request.form["drone_size"]
        owner_id = 1
        # session.get("user_id")
        db = get_db()
        error = None

        if not display_name:
            error = "Display Name is required."
        elif not drone_size:
            error = "Drone Size is required."
        # register a drone

        if error is None:
            try:
                db.execute(
                    "INSERT INTO drone (display_name, drone_size, owner_id) VALUES (?, ?, ?)",
                    (display_name, drone_size, owner_id),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Drone {display_name} is already registered."
            else:
                return json.dumps({"success": display_name})
        # if we don't end up being able to register, return the error
        return json.dumps({"error": error})

    if request.method == "DELETE":
        db = get_db()
        # delete a drone's record

    if request.method == "PUT":
        db = get_db()
        # update a drone's record - change info, deactivate
