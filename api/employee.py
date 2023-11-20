import json

from flask import (
    Blueprint,
    request,
    session,
)

from api.db import get_db

bp = Blueprint("employee", __name__, url_prefix="/employee/<int:owner_id>")
# bp = Blueprint("employee", __name__, url_prefix="/employee")


@bp.route("/drones", methods=["GET"])
def drones(owner_id):
    # session.get("user_id")
    db = get_db()
    error = None
    query = """
    SELECT id, display_name, serial_number, is_active, drone_size, created
    FROM drone
    WHERE owner_id = ?
    """
    drones = db.execute(query, (owner_id,)).fetchall()

    if drones is None:
        error = "This feature is not available yet - check back later!"
    elif len(drones) == 0:
        error = "No drones have been registered!"
    else:
        drones_dict = [dict(drone) for drone in drones]
        for (
            drone
        ) in (
            drones_dict
        ):  # change to have front in pass in a list of drones instead of looping through yourself.
            drone["created"] = str(drone["created"])
            num_orders = 0
            employee_cut = 0
            drone_id = drone["id"]
            query = """
            SELECT order_id
            FROM ordered_cone
            WHERE drone_id = ?
            """
            orders = db.execute(query, (drone_id,)).fetchall()
            if drones is None:
                error = "This feature is not available yet - check back later!"
            elif len(orders) == 0:
                drone["earnings"] = 0
                drone["num_orders"] = 0
            else:
                for order in orders:
                    # print(order["order_id"])
                    full_order_id = order["order_id"]
                    query = """
                    SELECT employee_cut
                    FROM full_order
                    WHERE id = ?
                    """
                    full_order = db.execute(query, (full_order_id,)).fetchone()
                    if drones is None:
                        error = "This feature is not available yet - check back later!"
                    elif len(full_order) == 0:
                        error = "full order table has not be set up correclty!"
                    else:
                        employee_cut += full_order["employee_cut"]
                        num_orders += 1

            drone["earnings"] = employee_cut
            drone["num_orders"] = num_orders
            drone["is_active"] = drone["is_active"] == 1

    if error:
        return json.dumps({"error": error})
    else:
        # Convert the rows to a list of dictionaries

        # Return the JSON-serializable data
        return json.dumps({"drones": drones_dict})
    # return list of all drones and their immediately relevant info
    # response should look like: {'drones': [ {name: Drone2, size: number, id: 10394825, isActive: true } ]}


@bp.route("/earnings", methods=["GET"])
def earnings(owner_id):
    db = get_db()
    error = None
    # serial_number = body["display_name"]

    query = """
    SELECT id
    FROM drone
    WHERE owner_id = ?
    """
    drones = db.execute(query, (owner_id,)).fetchall()
    
    if drones is None:
        error = "This feature is not available yet - check back later!"
    elif len(drones) == 0:
        error = "No drones have been registered!"
    else:
        employee_cut = 0
        for (
            drone
        ) in (
            drones
        ):  # change to have front in pass in a list of drones instead of looping through yourself.
            # print(drone["serial_number"])
            drone_id = drone["id"]
            query = """
            SELECT order_id
            FROM ordered_cone
            WHERE drone_id = ?
            """
            orders = db.execute(query, (drone_id,)).fetchall()
            if orders is None:
                error = "This feature is not available yet - check back later!"
            elif len(orders) == 0:
                error = "No orders have been submitted!" #make sure this is working correctly
            else:
                for order in orders:
                    full_order_id = order["order_id"]
                    query = """
                    SELECT employee_cut
                    FROM full_order
                    WHERE id = ?
                    """
                    full_order = db.execute(query, (full_order_id,)).fetchone()
                    if full_order is None:
                        error = "This feature is not available yet - check back later!"
                    elif len(full_order) == 0:
                        error = "full order table has not be set up correclty!"
                    else:
                        employee_cut += full_order["employee_cut"]

    if error:
        return json.dumps({"error": error})
    else:
        # Convert the rows to a list of dictionaries
        return json.dumps({"earnings": employee_cut})
        # return a single value with total earnings
        # example: {'earnings': 56600} for $566.00


@bp.route("/drone", methods=["POST", "DELETE", "PUT"])
def drone(owner_id):
    if request.method == "POST":
        body = request.get_json()

        display_name = body["display_name"]
        drone_size = body["drone_size"]
        serial_number = body["serial_number"]
        is_active = body["is_active"]

        db = get_db()
        error = None

        if not serial_number or type(serial_number) is not str:
            error = "Serial Number is required and must be a string."
        elif not display_name or type(display_name) is not str:
            error = "Display Name is required and must be a string."
        elif not drone_size or type(is_active) is not int:
            error = "Drone Size is required."
        elif not is_active or type(is_active) is not int:
            error = "Active status is required and must be an integer."

        # register a drone

        if error is None:
            try:
                query = """
                    INSERT INTO drone (serial_number, display_name, drone_size, owner_id, is_active)
                    VALUES (?, ?, ?, ?, ?)
                    """
                id = db.execute(
                    query,
                    (serial_number, display_name, drone_size, owner_id, is_active),
                ).lastrowid
                db.commit()
            except db.IntegrityError:
                error = f"Drone {display_name} is already registered."
            else:
                return json.dumps({"Drone_id": id})
        # if we don't end up being able to register, return the error
        return json.dumps({"error": error})

    if request.method == "DELETE":
        db = get_db()
        error = None
        body = request.get_json()

        serial_number = body["serial_number"]

        if not serial_number:
            error = "Serial Number is required"

        query = """
            SELECT *
            FROM drone 
            WHERE serial_number = ?
            """
        existing_drone = db.execute(query, (serial_number,)).fetchone()
        if not existing_drone:
            error = f"Couldn't find drone with serial {serial_number} because it does not exist."
        print(existing_drone)
        if error is None:
            try:
                query = """
                    DELETE FROM drone
                    WHERE serial_number = ?
                    """
                db.execute(
                    query, (serial_number,)  # will never fail becuase of how sql works
                )
                db.commit()
            except db.IntegrityError:
                error = f"An error occurred while deleting the drone with serial {serial_number}"
            else:
                return json.dumps({"deleted drone with serial ": serial_number})
        return json.dumps({"error": error})

        # delete a drone's record

    if request.method == "PUT":
        db = get_db()
        body = request.get_json()

        serial_number = body["serial_number"]
        display_name = body["display_name"]
        is_active = body["is_active"]
        drone_size = body["drone_size"]

        if not serial_number or type(serial_number) is not str:
            error = "Serial Number is required and must be a string."
        elif not display_name or type(display_name) is not str:
            error = "Display Name is required and must be a string."
        elif not is_active or type(is_active) is not int:
            error = "Active State is required and must be a integer."
        elif not drone_size or type(is_active) is not int:
            error = "Drone Size is required and must be a integer."

        query = """
            SELECT *
            FROM drone 
            WHERE serial_number = ?
            """
        existing_drone = db.execute(query, (serial_number,)).fetchone()
        if not existing_drone:
            error = f"Couldn't find drone with serial {serial_number} because it does not exist."
        else:
            try:
                query = """
                    UPDATE drone
                    SET display_name = ?, is_active = ?, drone_size = ?
                    WHERE serial_number = ?
                    """
                db.execute(
                    query,
                    (display_name, is_active, drone_size, serial_number),
                )
                db.commit()
                return json.dumps({"Updated drone with serial ": serial_number})
            except:
                error = f"An error occurred while updating the drone with serial {serial_number}."
        return json.dumps({"error": error})
        # update a drone's record - change info, deactivate


@bp.route("/history", methods=["GET"])
def history(owner_id):
    if request.method == "GET":
        db = get_db()
        error = None

        query = """
        SELECT id
        FROM drone
        WHERE owner_id = ?
        """
        drones = db.execute(query, (owner_id,)).fetchall()

        order_list = []
        if drones is None:
            error = "This feature is not available yet - check back later!"
        elif len(drones) == 0:
            error = "No drones have been registered!"
        else:
            drone_ids = []
            for drone in drones:  # change to have front in pass in a list of drones instead of looping through yourself.
                drone_ids.append(drone["id"])

            placeholders = ', '.join(['?'] * len(drone_ids))
            query = f"""
            SELECT DISTINCT order_id
            FROM ordered_cone
            WHERE drone_id IN ({placeholders})
            ORDER BY id DESC
            LIMIT 50
            """ # added distinct so it shouldn't replicate orders bc we are doing an ordered cone and there are multiple ordered cones in an order
            orders = db.execute(query, drone_ids).fetchall()
            #ordered_cone_dict = [dict(row) for row in orders]
            full_order_ids_dict = [dict(row) for row in orders]

            if orders is None:
                error = "Full Orders table is not set up yet"
            else:
                for order_id_line in full_order_ids_dict:
                    full_order_id = order_id_line["order_id"]
                    query = """
                    SELECT id, employee_cut, order_time
                    FROM full_order
                    WHERE id = ?
                    """
                    full_order = db.execute(query, (full_order_id,)).fetchall()

                    if full_order is None:
                        error = "This feature is not available yet - check back later!"
                    elif len(full_order) == 0:
                        error = "full order table has not be set up correclty!"
                    else:
                        full_order_dict = [dict(row) for row in full_order]
                        for order in full_order_dict:
                            query = """
                                    SELECT *
                                    FROM ordered_cone
                                    WHERE order_id = ?
                                    """ 
                            ordered_cones = db.execute(query, (full_order_id,)).fetchall()

                            if ordered_cones is None:
                                error = "This feature is not available yet - check back later!"
                            elif len(ordered_cones) == 0:
                                error = "Ordered Cone table has not be set up correctly!"
                            else:
                                ordered_cone_dict = [dict(row) for row in ordered_cones]
                                order["cones"] = ordered_cone_dict
                                order_list.append(order)
                        #order_list.append(order)



    if error:
        return json.dumps({"error": error})
    else:
        return json.dumps({"orders_history": order_list})