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


@bp.route("/product", methods=["GET", "PUT", "POST"])
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
        # grab data
        data = request.get_json()
        displayName = data["display_name"]
        stock = data["stock"]
        pricePerUnit = data["price_per_unit"]
        productType = data["product_type"]

        # initiating variable
        db = get_db()
        error = None

        # check data entries
        if not displayName:
            error = "Display name missing."
        elif not stock:
            error = "Stock missing."
        elif not pricePerUnit:
            error = "Price per unit missing."
        elif not productType:
            error = "Product type missing."

        # continue if no errors
        if error is None:
            try:
                query = """
                    REPLACE INTO product (display_name, stock, price_per_unit, product_type)
                    VALUES (?, ?, ?, ?)
                    """
                db.execute(query, (displayName, stock, pricePerUnit, productType))
                db.commit()
            except:
                error = "Error saving values"
            else:
                return json.dumps({"success": f"{displayName} has been updated."})
        else:
            return json.dumps({"error": error})
        # update record on one specific product

    if request.method == "POST":
        # grab data
        data = request.get_json()
        displayName = data["display_name"]
        stock = data["stock"] if "stock" in data else 0
        pricePerUnit = data["price_per_unit"]
        productType = data["product_type"]

        # initiating variable
        db = get_db()
        error = None

        # check data entries
        if not displayName:
            error = "Product name is required."
        elif not pricePerUnit:
            error = "Price per unti is required."
        elif not productType:
            error = "Product type is required."

        # continue if no errors
        if error is None:
            try:
                query = """
                    INSERT INTO product (display_name, stock, price_per_unit, product_type)
                    VALUES (?, ?, ?, ?)
                    """
                db.execute(query, (displayName, stock, pricePerUnit, productType))
                db.commit()
            except:
                error = "Error saving product."
            else:
                return json.dumps({"success": f"{productType} added successfully."})
        else:
            return json.dumps({"error": error})


@bp.route("/user", methods=["GET", "PUT"])
def user():
    if request.method == "GET":
        # grab data
        data = request.get_json
        search = data["search"]

        db = get_db()
        error = None

        if not search:
            return json.dumps({"error": "Missing search term."})

        # get more info about a specific user
        query = """
            SELECT *
            FROM user
            WHERE username = ?  
            """
        # The idea is to find a specific user, right? Hence the {search term}
        user = db.execute(query, (search)).fetchall()
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
        # grab data
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        userType = data["user_type"]
        isActive = data["is_active"]

        # initiating variable
        db = get_db()
        error = None

        # check data entries
        if not username:
            error = "Username missing."
        elif not password:
            error = "Password missing."
        elif not userType:
            error = "User type missing."
        elif not isActive:
            error = "Active value missing."

        # continue if no errors
        if error is None:
            try:
                query = """
                    REPLACE INTO user (username, password, user_type, is_active)
                    VALUES (?, ?, ?, ?)
                    """
                db.execute(query, (username, password, userType, isActive))
                db.commit()
            except:
                error = "Error saving value"
            else:
                return json.dumps({"success": f"Active value set to {isActive}"})
        else:
            return json.dumps({"error": error})
        # update a user's info - this will be used to ban them
