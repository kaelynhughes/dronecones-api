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
    query = """
    SELECT id, display_name, serial_number, is_active, drone_size, created
    FROM drone
    WHERE owner_id = ?
    """
    drones = db.execute(query, (owner_id,)).fetchall()

    if drones is None:
        return {"error": "This feature is not available yet - check back later!"}
    elif len(drones) == 0:
        return {"error": "No drones have been registered!"}
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
                return {
                    "error": "This feature is not available yet - check back later!"
                }, 404
            elif len(orders) == 0:
                drone["earnings"] = 0
                drone["num_orders"] = 0
            else:
                for order in orders:
                    full_order_id = order["order_id"]
                    query = """
                    SELECT employee_cut
                    FROM full_order
                    WHERE id = ?
                    """
                    full_order = db.execute(query, (full_order_id,)).fetchone()
                    if drones is None:
                        return {
                            "error": "This feature is not available yet - check back later!"
                        }  # , 404
                    elif len(full_order) == 0:
                        {
                            "error": "Full order table has not been set up correctly!"
                        }  # , 404
                    else:
                        employee_cut += full_order["employee_cut"]
                        num_orders += 1

            drone["earnings"] = employee_cut
            drone["num_orders"] = num_orders
            drone["is_active"] = drone["is_active"] == 1

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
        return {
            "error": "This feature is not available yet - check back later!"
        }  # , 404
    elif len(drones) == 0:
        return {"error": "No drones have been registered!"}
    else:
        drones_dict = [dict(drone) for drone in drones]
        print(drones_dict)
        employee_cut = 0
        for drone in drones_dict:
            # change to have front in pass in a list of drones instead of looping through yourself.
            try:
                drone_id = drone["id"]
                query = """
                SELECT DISTINCT order_id
                FROM ordered_cone
                WHERE drone_id = ?
                """
                orders = db.execute(query, (drone_id,)).fetchall()
                if orders is None:
                    return {
                        "error": "This feature is not available yet - check back later!"
                    }, 404

                for order in orders:
                    full_order_id = order["order_id"]
                    query = """
                    SELECT employee_cut
                    FROM full_order
                    WHERE id = ?
                    """
                    full_order = db.execute(query, (full_order_id,)).fetchone()
                    if full_order is None:
                        return {
                            "error": "This feature is not available yet - check back later!"
                        }  # , 404
                    elif len(full_order) == 0:
                        return {
                            "error": "full order table has not be set up correctly!"
                        }  # , 404
                    else:
                        employee_cut += full_order["employee_cut"]
            except Exception:
                return {
                    "error": "An unknown error occurred on our end. Sorry!"
                }  # , 500

    # Convert the rows to a list of dictionaries
    if employee_cut == 0:
        return {"error": "No orders have been submitted!"}
    return json.dumps({"earnings": employee_cut})
    # return a single value with total earnings
    # example: {'earnings': 56600} for $566.00


@bp.route("/drone", methods=["POST", "DELETE", "PUT"])
def drone(owner_id):
    if request.method == "POST":
        body = request.get_json()

        try:
            display_name = body["display_name"]
            drone_size = body["drone_size"]
            serial_number = body["serial_number"]
            is_active = body["is_active"]
        except KeyError:
            return {
                "error": "Looks like we're missing some of the information we need to save your drone!"
            }  # , 400

        db = get_db()

        if type(serial_number) is not str:
            return {"error": "Serial Number must be a string."}  # , 400
        elif type(display_name) is not str:
            return {"error": "Display Name must be a string."}  # , 400
        elif type(is_active) is not int:
            return {"error": "Drone Size must be a number."}  # , 400
        elif type(is_active) is not int:
            return {"error": "Active status must be an integer."}  # , 400

        # register a drone

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
            return {"error": f"Drone {display_name} is already registered."}  # , 409
        else:
            return json.dumps({"drone_id": id})

    if request.method == "DELETE":
        db = get_db()
        body = request.get_json()

        serial_number = body["serial_number"]

        if not serial_number:
            return {"error": "Serial number is required."}  # , 400

        query = """
            SELECT *
            FROM drone 
            WHERE serial_number = ?
            """
        existing_drone = db.execute(query, (serial_number,)).fetchone()
        if not existing_drone:
            return {
                "error": f"Couldn't find drone with serial number {serial_number} because it does not exist."
            }  # , 404
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
            return {
                "error": f"An error occurred while deleting the drone with serial {serial_number}"
            }  # , 500
        else:
            return json.dumps(
                {f"Deleted drone with serial number {serial_number}": serial_number}
            )

        # delete a drone's record

    if request.method == "PUT":
        db = get_db()
        body = request.get_json()

        if "serial_number" not in body:
            return {"error": "Serial number is required."}  # , 400

        serial_number = body["serial_number"]
        if type(serial_number) is not str:
            return {"error": "Serial number appears to be malformed."}  # , 400

        query = """
            SELECT *
            FROM drone 
            WHERE serial_number = ?
            """
        existing_drone = db.execute(query, (serial_number,)).fetchone()
        if not existing_drone:
            return {
                "error": f"Couldn't find drone with serial number {serial_number} because it does not exist."
            }  # , 404

        message = "Updated"
        if "display_name" in body:
            if type(body["display_name"]) is not str:
                return {"error": "Display name must be a string."}  # , 400
            try:
                query = """
                    UPDATE drone
                    SET display_name = ?
                    WHERE serial_number = ?
                    """
                db.execute(query, (body["display_name"], serial_number))
                db.commit()
                message += " display name"
            except Exception as ex:
                print(ex)
                return {
                    "error": "An unexpected error occurred on our end when updating display name."
                }  # , 500

        if "is_active" in body:
            if type(body["is_active"]) is not int:
                return {
                    "error": "Active status appears to have been sent incorrectly."
                }  # , 400

            try:
                query = """
                    UPDATE drone
                    SET is_active = ?
                    WHERE serial_number = ?
                    """
                db.execute(query, (body["is_active"], serial_number))
                db.commit()
                if len(message) > 7:
                    message += ","
                message += " active status"
            except Exception as ex:
                print(ex)
                return {
                    "error": "An unexpected error occurred on our end when updating activity status."
                }  # , 500

        if "drone_size" in body:
            if type(body["drone_size"]) is not int:
                return {
                    "error": "Drone size appears to have been sent incorrectly."
                }  # , 400

            try:
                query = """
                    UPDATE drone
                    SET drone_size = ?
                    WHERE serial_number = ?
                    """
                db.execute(query, (body["drone_size"], serial_number))
                db.commit()
                if len(message) > 7:
                    message += ","
                message += " drone size"
            except Exception as ex:
                print(ex)
                return {
                    "error": "An unexpected error occurred on our end when updating drone size."
                }  # , 500
        message += f" for drone with serial number {serial_number}."

        return json.dumps({"success": message})
        # update a drone's record - change info, deactivate


@bp.route("/history", methods=["GET"])
def history(owner_id):
    if request.method == "GET":
        db = get_db()

        query = """
        SELECT id
        FROM drone
        WHERE owner_id = ?
        """
        drones = db.execute(query, (owner_id,)).fetchall()

        order_list = []
        if drones is None:
            return {
                "error": "This feature is not available yet - check back later!"
            }  # , 404
        if len(drones) == 0:
            return {"error": "No drones have been registered!"}

        drone_ids = []
        for drone in drones:
            # change to have front in pass in a list of drones instead of looping through yourself.
            drone_ids.append(drone["id"])

        placeholders = ", ".join(["?"] * len(drone_ids))
        query = f"""
        SELECT DISTINCT order_id
        FROM ordered_cone
        WHERE drone_id IN ({placeholders})
        ORDER BY id DESC
        LIMIT 50
        """  # added distinct so it shouldn't replicate orders bc we are doing an ordered cone and there are multiple ordered cones in an order
        orders = db.execute(query, drone_ids).fetchall()
        if orders is None:
            return {"error": "Full Orders table is not set up yet"}  # , 404
        full_order_ids_dict = [dict(row) for row in orders]

        for order_id_line in full_order_ids_dict:
            full_order_id = order_id_line["order_id"]
            query = """
            SELECT id, employee_cut, order_time
            FROM full_order
            WHERE id = ?
            """
            full_order = db.execute(query, (full_order_id,)).fetchall()

            if full_order is None:
                return {
                    "error": "This feature is not available yet - check back later!"
                }, 404
            if len(full_order) == 0:
                return {
                    "error": "Full order table has not been set up correctly!"
                }  # , 404

            full_order_dict = [dict(row) for row in full_order]
            for order in full_order_dict:
                query = """
                        SELECT *
                        FROM ordered_cone
                        WHERE order_id = ?
                        """
                ordered_cones = db.execute(query, (full_order_id,)).fetchall()

                if ordered_cones is None:
                    return {
                        "error": "This feature is not available yet - check back later!"
                    }
                if len(ordered_cones) == 0:
                    return {
                        "error": "Ordered Cone table has not been set up correctly!"
                    }, 404

                ordered_cone_dict = [dict(row) for row in ordered_cones]
                order["cones"] = ordered_cone_dict
                order_list.append(order)

    return json.dumps({"orders_history": order_list})
