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
    owner_id = session.get('user_id')
    db = get_db()
    error = None
    query= """
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
        db = get_db()
        # register a drone

    if request.method == "DELETE":
        db = get_db()
        # delete a drone's record

    if request.method == "PUT":
        db = get_db()
        # update a drone's record - change info, deactivate
