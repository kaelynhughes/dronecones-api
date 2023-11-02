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
    drones = db.execute(query, (owner_id,)).fetchall()

    if drones is None:
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
        display_name = request.form["display_name"]
        drone_size = request.form["drone_size"]
        serial_number = request.form["serial_number"]
        owner_id = request.form["owner_id"]
        is_active = 1
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
                    "INSERT INTO drone (serial_number, display_name, drone_size, owner_id, is_active) VALUES (?, ?, ?, ?, ?)",
                    (serial_number, display_name, drone_size, owner_id, is_active),
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
        serial_number = request.form["serial_number"]

        if not serial_number:
            error = "Serial Number is required"

        if error is None:
            try:
                db.execute(
                    "Delete From drone where serial_number = ?",  # will never fail because of how sql delete works
                    (serial_number),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Couldn't delete drone with serial {serial_number} because it does not exist."
            else:
                return json.dumps({"deleted drone with serial ": serial_number})
        return json.dumps({"error": error})

        # delete a drone's record

    if request.method == "PUT":
        db = get_db()
        serial_number = request.form["serial_number"]
        display_name = request.form["display_name"]
        is_active = request.form["is_active"]

        if not serial_number:
            error = "Serial Number is required"
        elif not display_name:
            error = "Display Name is required."
        elif not is_active:
            error = "Active State is required."

        try:
            db.execute(
                "UPDATE drone SET display_name = ?, is_active = ? WHERE serial_number = ?",
                (display_name, is_active, serial_number),
            )
            db.commit()
        except db.IntegrityError:
            error = f"Couldn't find drone with serial {serial_number} because it does not exist."
        else:
            return json.dumps({"Updated drone with serial ": serial_number})
        return json.dumps({"error": error})
        # update a drone's record - change info, deactivate
