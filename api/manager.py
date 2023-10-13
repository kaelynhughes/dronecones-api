import json

from flask import (
    Blueprint,
    request,
)

from api.db import get_db

bp = Blueprint("manager", __name__, url_prefix="/manager")


@bp.route("/orders", methods=["GET"])
def orders():
    db = get_db()
    error = None
    query = """
        SELECT *
        FROM ordered_cone
        """
    orders = db.execute(query).fetchall()
    print(orders)
    # get all orders, or a specific number
    # if we want to get only a few at a time, we may need to have this be a bit more involved
    # so that we don't end up returning the same few records over and over
    # this will be used in account management as well

    if orders is None:
        error = "Not implemented"
    elif len(orders == 0):
        error = "Empty table"

    if error:
        return json.dumps({"error": error})
    else:
        return json.dumps({"orders": orders})


@bp.route("/product", methods=["GET"])
def accounting():
    if request.method == "GET":
        db = get_db()
        error = None
        # get info on one specific product
        query = """
            SELECT display_name, stock, price_per_unit
            FROM product
            WHERE id = {search}
            """
        # Idea is each item from table will be grabbed incrementally
        item = db.execute(query).fetchone()
        print(item)

        if item is None:
            error = "Not implemented"
        elif len(item == 0):
            error = "Empty table"

        if error:
            return json.dumps({"error": error})
        else:
            return json.dumps({"item": item})

    if request.method == "PUT":
        db = get_db()
        error = None
        query = """
            SELECT stock
            FROM product
            WHERE product_type = {item_to_change}
            """
        stock = db.execute(query).fetchone()

        if stock is None:
            error = "Not implemented"
        elif len(user) == 0:
            error = "Empty table"

        if error:
            return json.dumps({"error": error})
        else:
            return json.dumps({"stock": {user_input}})
        # update record on one specific product

    if request.method == "POST":
        # add a new product
        db = get_db()
        error = None
        query = """
            SELECT *
            FROM product
            """
        menu = db.execute(query).fetchall()
        if new_item not in menu:
            menu.append(new_item)
        else:
            error = "Item already in menu"

        if error:
            return json.dumps({"error": error})
        else:
            return json.dumps({"menu": menu})


@bp.route("/user", methods=["GET", "PUT"])
def user():
    if request.method == "GET":
        db = get_db()
        # get more info about a specific user
        error = None
        query = """
            SELECT username
            FROM user
            WHERE username = '{search term}'    
            """
        # The idea is to find a specific user, right? Hence the {search term}
        user = db.execute(query).fetchall()
        print(user)

        if user is None:
            error = "Not implemented"
        elif len(user) == 0:
            error = "Empty table"

        if error:
            return json.dumps({"error": error})
        else:
            return json.dumps({"user": user})

    if request.method == "PUT":
        db = get_db()
        error = None
        query = """
            SELECT is_active
            FROM user
            WHERE username = {search_term}
            """
        user = db.execute(query).fetchone()

        if user is None:
            error = "Not implemented"
        elif len(user) == 0:
            error = "Empty table"

        # update a user's info - this will be used to ban them

        if error:
            return json.dumps({"error": error})
        else:
            if user.is_active == 0:
                return json.dumps({"is_active": 1})
            else:
                return json.dumps({"is_active": 0})
