import json

from flask import (
    Blueprint,
    request,
)

from api.db import get_db
from werkzeug.security import generate_password_hash

bp = Blueprint("customer", __name__, url_prefix="/customer")


@bp.route("/menu", methods=["GET"])
def menu():
    db = get_db()
    error = None
    query = """
        SELECT display_name, price_per_unit, id, product_type, stock 
        FROM product 
        WHERE product_type = 'Cone' AND NOT stock = 0
        """
    conesResp = db.execute(query).fetchall()
    cones = [dict(row) for row in conesResp]

    query = """
        SELECT display_name, price_per_unit, id, product_type, stock
        FROM product
        WHERE product_type = 'IceCream' AND NOT stock = 0
        """
    icecreamResp = db.execute(query).fetchall()
    icecream = [dict(row) for row in icecreamResp]

    query = """
        SELECT display_name, price_per_unit, id, product_type,stock
        FROM product
        WHERE product_type = 'Topping' AND NOT stock = 0
        """
    toppingsResp = db.execute(query).fetchall()
    toppings = [dict(row) for row in toppingsResp]

    if len(cones) == 0 and len(icecream) == 0 and len(toppings) == 0:
        error = "No menu available yet - check back later!"
    elif len(cones) == 0 or len(icecream) == 0 or len(toppings) == 0:
        error = "Looks like this store is running low on stock. Check again later!"

    if error:
        return json.dumps({"error": error})
    else:
        return json.dumps({"cones": cones, "icecream": icecream, "toppings": toppings})


@bp.route("/<int:customer_id>/checkout", methods=["GET", "POST"])
def checkout(customer_id):
    if request.method == "GET":
        db = get_db()
        query = """
                SELECT id
                FROM full_order
                WHERE customer_id = ?
                ORDER BY id DESC
                LIMIT 1
                """
        order_id = db.execute(query, (customer_id,)).fetchone()
        if not order_id:
            return {
                "error": "We can't find any previous orders for you. Try making one now!"
            }

        try:
            query = """
                    SELECT *
                    FROM ordered_cone
                    WHERE order_id = ?
                    """
            ordered_cone = db.execute(query, (order_id[0],)).fetchall()
            ordered_cone_list = [dict(row) for row in ordered_cone]
        except Exception:
            return {"error": "Something went wrong on our end. Sorry!"}, 400

        return json.dumps({"ordered cone": ordered_cone_list})

    if request.method == "POST":
        db = get_db()
        body = request.get_json()
        # error handling - checking data formation
        try:
            total_price = body["total_price"]
            employee_cut = body["employee_cut"]
            profit = body["profit"]
            order_time = body["order_time"]
            cones = body["cones"]
        except KeyError:
            return (
                {
                    "error": "Something went wrong - we don't have all the information we need to place your order!"
                },
                400,
            )

        for full_cone in cones:
            if "cone" not in full_cone or "scoop_1" not in full_cone:
                return {
                    "error": "Something went wrong - at least one of the cones you ordered is missing parts!"
                }, 400

        # putting stuff in the database
        query = """
            SELECT id
            FROM drone
            WHERE is_active = 1 AND drone_size = ?
            LIMIT 1
            """

        drone_id = db.execute(query, (str(len(cones)),)).fetchone()
        if not drone_id:
            return json.dumps({"error": "No drones are active. Try again later!"})

        query = """
            INSERT INTO full_order (total_price, employee_cut, profit, customer_id, order_time)
            VALUES (?, ?, ?, ?, ?)
            """
        full_order_id = db.execute(
            query,
            (
                total_price,
                employee_cut,
                profit,
                customer_id,
                order_time,
            ),
        ).lastrowid

        for full_cone in cones:
            for product, product_id in full_cone.items():
                if (
                    product_id
                ):  # might want to add later to check to see if stock can handle
                    query = """ 
                    SELECT stock, display_name
                    FROM product
                    WHERE id = ?
                    """
                    product_stock = db.execute(query, (product_id,)).fetchone()
                    if not product_stock:
                        return {
                            "error": "Looks like one of the elements of your order doesn't exist anymore - try ordering something else!"
                        }, 400
                    if product_stock["stock"] <= 0:
                        return json.dumps(
                            {
                                "error": f"We are out of stock of {product_stock['display_name']}."
                            }
                        )
                    query = """ 
                    UPDATE product
                    SET stock = stock - 1
                    WHERE id = ?
                    """
                    db.execute(query, (product_id,))

            query = """
                INSERT INTO ordered_cone (cone, scoop_1, scoop_2, scoop_3, topping_1, topping_2, topping_3, order_id, drone_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """

            db.execute(
                query,
                (
                    full_cone["cone"],
                    full_cone["scoop_1"],
                    full_cone["scoop_2"] if "scoop_2" in full_cone else None,
                    full_cone["scoop_3"] if "scoop_3" in full_cone else None,
                    full_cone["topping_1"] if "topping_1" in full_cone else None,
                    full_cone["topping_2"] if "topping_2" in full_cone else None,
                    full_cone["topping_3"] if "topping_3" in full_cone else None,
                    full_order_id,
                    drone_id[0],
                ),
            )

        db.commit()

    return json.dumps(
        {"full_order_id": full_order_id}
    )  # will want to return more here later


@bp.route("/<int:customer_id>/history", methods=["GET"])
def history(customer_id):
    if request.method == "GET":
        db = get_db()
        query = """
                SELECT id, total_price, order_time
                FROM full_order
                WHERE customer_id = ?
                ORDER BY id DESC
                LIMIT 10
                """
        orders = db.execute(query, (customer_id,)).fetchall()
        orders_dict = [dict(row) for row in orders]
        for order in orders_dict:
            query = """
                    SELECT id, cone, scoop_1, scoop_2, scoop_3, topping_1, topping_2, topping_3
                    FROM ordered_cone
                    WHERE order_id = ?
                    """
            ordered_cone = db.execute(query, (order["id"],)).fetchall()
            ordered_cone_dict = [dict(row) for row in ordered_cone]
            order["cones"] = ordered_cone_dict

        return json.dumps({"orders_history": orders_dict})


@bp.route("/<int:customer_id>/account", methods=["GET", "PUT"])
def account(customer_id):
    if request.method == "GET":
        db = get_db()
        query = """
            SELECT id, username, password, user_type
            FROM user
            WHERE id = ?
            """
        info = db.execute(query, (customer_id,)).fetchall()
        customer = [dict(row) for row in info]
        if not customer:
            return {"error": "No customer exists at this ID!"}, 404
        return json.dumps({"customer": customer})

    if request.method == "PUT":
        db = get_db()
        # update the relevant info about the user
        body = request.get_json()
        msg = ""
        if "username" in body:
            query = """
                UPDATE user
                SET username = ?
                WHERE id = ?
                """
            db.execute(query, (body["username"], customer_id))
            msg += "Username has been updated. "

        if "password" in body:
            query = """
                UPDATE user
                SET password = ?
                WHERE id = ?
                """
            db.execute(query, (generate_password_hash(body["password"]), customer_id))
            msg += "Password has been updated. "

        if "is_active" in body:
            query = """
                UPDATE user
                SET is_active = ?
                WHERE id = ?
                """
            db.execute(query, (body["is_active"], customer_id))
            msg += "Activity has been updated."
        return json.dumps({"success": msg})
