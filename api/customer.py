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
        SELECT display_name, price_per_unit 
        FROM product 
        WHERE product_type = 'cone' AND NOT stock = 0
        """
    cones = db.execute(query).fetchall()
    print(cones)

    query = """
        SELECT display_name, price_per_unit
        FROM product
        WHERE product_type = 'flavor' AND NOT stock = 0
        """
    icecream = db.execute(query).fetchall()
    print(icecream)

    query = """
        SELECT display_name, price_per_unit
        FROM product
        WHERE product_type = 'topping' AND NOT stock = 0
        """
    toppings = db.execute(query).fetchall()
    print(toppings)

    if menu is None:
        error = "No menu available yet - check back later!"
    elif len(cones) == 0 or len(icecream) == 0 or len(toppings) == 0:
        error = "Looks like this store is running low on stock. Check again later!"

    if error:
        return json.dumps({"error": error})
    else:
        return json.dumps({"cones": cones, "icecream": icecream, "toppings": toppings})


@bp.route("/<user_id>/checkout", methods=["GET", "POST"])
def checkout(user_id):
    if request.method == "GET":
        db = get_db()
        query = """
                SELECT id
                FROM full_order
                WHERE customer_id = ?
                ORDER BY id DESC
                LIMIT 1
                """
        order_id = db.execute(query, (user_id,)).fetchone()[0]

        query = """
                SELECT *
                FROM ordered_cone
                WHERE order_id = ?
                """
        ordered_cone = db.execute(query, (order_id,)).fetchall()
        ordered_cone_list = [dict(row) for row in ordered_cone]

        return json.dumps({"ordered cone": ordered_cone_list})
        # get most recent order

    if request.method == "POST":
        db = get_db()
        body = request.get_json()
        # create a full_order and then a ordered cone
        total_price = body["total_price"]
        employee_cut = body["employee_cut"]
        profit = body["profit"]
        order_time = body["order_time"]

        products = body["products"]
        cone = products["cone"]
        scoop_1 = products["scoop_1"]
        scoop_2 = products["scoop_2"]
        scoop_3 = products["scoop_3"]
        topping_1 = products["topping_1"]
        topping_2 = products["topping_2"]
        topping_3 = products["topping_3"]

        error = None
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
        elif not products:
            error = "products dictionary is required."
        elif not scoop_1:
            error = "scoop_1 is required."

        if not error:
            for product, product_id in products.items():
                if product_id:
                    query = """
                    UPDATE product
                    SET stock = stock - 1
                    WHERE id = ?
                    """
                    db.execute(query, (product_id,))
                    print("removed stock " + str(product_id)) # maybe return the stocks in json?

            query = """
                INSERT INTO full_order (total_price, employee_cut, profit, customer_id, order_time)
                VALUES (?, ?, ?, ?, ?)
                """
            full_order_id = db.execute(
                query, (total_price, employee_cut, profit, user_id, order_time,)
            ).lastrowid


            query = """
                SELECT id
                FROM drone
                WHERE is_active = 1
                LIMIT 1
                """
            drone_id = db.execute(query).fetchone()
            query = """
                INSERT INTO ordered_cone (cone, scoop_1, scoop_2, scoop_3, topping_1, topping_2, topping_3, order_id, drone_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """

            order = db.execute(
                query,
                (
                    cone,
                    scoop_1,
                    scoop_2,
                    scoop_3,
                    topping_1,
                    topping_2,
                    topping_3,
                    full_order_id,
                    drone_id[0],
                ),
            )
            db.commit()

            return json.dumps(
                {"success": order.fetchall()}
            )  # will want to return more here later

        return json.dumps({"error": error})


@bp.route("/<user_id>/history", methods=["GET"])
def history(user_id):
    if request.method == "GET":
        db = get_db()
        query = """
                SELECT *
                FROM full_order
                WHERE customer_id = ?
                """
        order_id = db.execute(query, (user_id,)).fetchall()
        order_id = [dict(row) for row in order_id]

        return json.dumps({"full orders": order_id})
        


@bp.route("/<user_id>/account", methods=["GET", "PATCH"])
def account(user_id):
    if request.method == "GET":
        db = get_db()
        query = """
            SELECT id, username, password, user_type
            FROM user
            WHERE id = ?
            """
        info = db.execute(query, user_id).fetchone()
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
            db.execute(query, (body["username"], user_id))
            msg += " username has been updated"

        if "password" in body:
            query = """
                UPDATE user
                SET password = ?
                WHERE id = ?
                """
            db.execute(query, (generate_password_hash(body["password"])))
            msg += " password has been updated"
        return json.dumps(msg)
