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
    print(cones)

    query = """
        SELECT display_name, price_per_unit, id, product_type, stock
        FROM product
        WHERE product_type = 'IceCream' AND NOT stock = 0
        """
    icecreamResp = db.execute(query).fetchall()
    icecream = [dict(row) for row in icecreamResp]
    print(icecream)

    query = """
        SELECT display_name, price_per_unit, id, product_type,stock
        FROM product
        WHERE product_type = 'Topping' AND NOT stock = 0
        """
    toppingsResp = db.execute(query).fetchall()
    toppings = [dict(row) for row in toppingsResp]
    print(toppings)

    if menu is None:
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
        error = None
        if not order_id:
            error = "No orders"

        if not error:
            query = """
                    SELECT *
                    FROM ordered_cone
                    WHERE order_id = ?
                    """
            ordered_cone = db.execute(query, (order_id[0],)).fetchall()
            ordered_cone_list = [dict(row) for row in ordered_cone]

            return json.dumps({"ordered cone": ordered_cone_list})
        else:
            return json.dumps({"error": error})
        # get most recent order

    if request.method == "POST":
        db = get_db()
        body = request.get_json()
        # create a full_order and then a ordered cone
        total_price = body["total_price"]
        employee_cut = body["employee_cut"]
        profit = body["profit"]
        order_time = body["order_time"]

        cones = body["cones"]
        error = None
        for full_cone in cones:
            cone = full_cone["cone"]
            scoop_1 = full_cone["scoop_1"]
            scoop_2 = full_cone["scoop_2"]
            scoop_3 = full_cone["scoop_3"]
            topping_1 = full_cone["topping_1"]
            topping_2 = full_cone["topping_2"]
            topping_3 = full_cone["topping_3"]

            if not total_price:
                error = "total_price is required."
            elif not employee_cut:
                error = "employee_cut is required."
            elif not profit:
                error = "profit is required."
            elif not order_time:
                error = "order_time is required."  # may be a back end thing
            elif not cone:
                error = "cone is required."
            elif not full_cone:
                error = "products dictionary is required."
            elif not scoop_1:
                error = "scoop_1 is required."

        if not error:
            query = """
                SELECT id
                FROM drone
                WHERE is_active = 1 AND drone_size = ?
                LIMIT 1
                """

            drone_id = db.execute(query, (str(len(cones)),)).fetchone()
            if not drone_id:
                error = "No drones are active"
                return json.dumps({"error": error})  # hot fix make look better later

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
                        SELECT stock
                        FROM product
                        WHERE id = ?
                        """
                        product_stock = db.execute(query, (product_id,)).fetchone()
                        if product_stock["stock"] <= 0:
                            error = f"We are out of stock of product {product_id}."
                            return json.dumps({"error": error})
                        query = """ 
                        UPDATE product
                        SET stock = stock - 1
                        WHERE id = ?
                        """
                        db.execute(query, (product_id,))
                        # maybe return the stocks in json?

                query = """
                    INSERT INTO ordered_cone (cone, scoop_1, scoop_2, scoop_3, topping_1, topping_2, topping_3, order_id, drone_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """

                db.execute(
                    query,
                    (
                        full_cone["cone"],
                        full_cone["scoop_1"],
                        full_cone["scoop_2"],
                        full_cone["scoop_3"],
                        full_cone["topping_1"],
                        full_cone["topping_2"],
                        full_cone["topping_3"],
                        full_order_id,
                        drone_id[0],
                    ),
                )

        db.commit()

        return json.dumps(
            {"full_order_id": full_order_id}
        )  # will want to return more here later

    return json.dumps({"error": error})


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
            print(order)
            query = """
                    SELECT id, cone, scoop_1, scoop_2, scoop_3, topping_1, topping_2, topping_3
                    FROM ordered_cone
                    WHERE order_id = ?
                    """
            ordered_cone = db.execute(query, (order["id"],)).fetchall()
            ordered_cone_dict = [dict(row) for row in ordered_cone]
            order["ordered_cone_dict"] = ordered_cone_dict

        return json.dumps({"full orders": orders_dict})


@bp.route("/<int:customer_id>/account", methods=["GET", "PATCH"])
def account(customer_id):
    if request.method == "GET":
        db = get_db()
        query = """
            SELECT id, username, password, user_type
            FROM user
            WHERE id = ?
            """
        info = db.execute(query, customer_id).fetchone()
        print(info)
        return json.dumps({info})

    if request.method == "PATCH":
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
            msg += " username has been updated"

        if "password" in body:
            query = """
                UPDATE user
                SET password = ?
                WHERE id = ?
                """
            db.execute(query, (generate_password_hash(body["password"])))
            msg += " password has been updated"

        if "is_active" in body:
            query = """
                UPDATE user
                SET is_active = ?
                WHERE id = ?
                """
            db.execute(query, (body["is_active"], customer_id))
            msg += " activity has been updated"
        return json.dumps({"success": msg})
