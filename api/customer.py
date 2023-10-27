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
            error = "order_time is required." # may be a back end thing
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
                    SET stock - 1
                    WHERE id = ?
                    """
                    db.execute(query, (product_id,))

                query = """
                    INSERT INTO full_order (total_price, employee_cut, profit, customer_id, order_time)
                    VALUES (?, ?, ?, ?, ?)
                    """
                full_order_id = db.execute(query, (total_price, employee_cut, profit, user_id, order_time)) # not sure if id but need id returned somehow
                
                query = """
                    INSERT INTO ordered_cone (cone, scoop_1, scoop_2, scoop_3, profit, topping_1, topping_2, topping_3, order_id, drone_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                
                #will need to find availible drone.


        return json.dumps({"error": error})
        # will need to remove products from inventory as well

        # register a order

        # if error is None:
        #     try:
        #         query = """
        #             INSERT INTO drone (serial_number, display_name, drone_size, owner_id, is_active)
        #             VALUES (?, ?, ?, ?, ?)
        #             """
        #         db.execute(
        #             "INSERT INTO drone (serial_number, display_name, drone_size, owner_id, is_active) VALUES (?, ?, ?, ?, ?)",
        #             (serial_number, display_name, drone_size, owner_id, is_active),
        #         )
        #         db.commit()
        #     except db.IntegrityError:
        #         error = f"Drone {display_name} is already registered."
        #     else:
        #         return json.dumps({"success": display_name})
        # # if we don't end up being able to register, return the error
        # return json.dumps({"error": error})
        # save an order


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
