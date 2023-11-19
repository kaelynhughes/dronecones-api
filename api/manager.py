import json

from flask import (
    Blueprint,
    request,
)

from api.db import get_db

bp = Blueprint("manager", __name__, url_prefix="/manager")


@bp.route("/orders", methods=["GET"])
def orders():
    if request.method == "GET":
        db = get_db()
        query = """
                SELECT *
                FROM full_order
                ORDER BY id DESC
                LIMIT 50
                """ 
        orders = db.execute(query).fetchall()
        full_order_dict = [dict(row) for row in orders]

        return json.dumps({"orders": full_order_dict})
        # get all orders, or a specific number
        # if we want to get only a few at a time, we may need to have this be a bit more involved
        # so that we don't end up returning the same few records over and over
        # this will be used in account management as well


@bp.route("/product", methods=["GET", "PUT", "POST"])
def accounting(): #does this need to be product()
    if request.method == "GET":
        db = get_db()
        body = request.get_json()

        error = None
        id = body["id"]

        if not id or type(id) is not int:
            error = "Id is required and must be a int."

        query = """
        SELECT *
        FROM product
        WHERE id = ?
        """
        product = db.execute(query, (id,)).fetchall()

        if not error:
            if product is None:
                error = "This feature is not available yet - check back later!"
            elif len(product) == 0:
                error = f"No product has been registered with id {id}"
            else:
                product_dict = [dict(row) for row in product]

        if error:
            return json.dumps({"error": error})
        else:
            return json.dumps({"product": product_dict})
    
        # get info on one specific product

    if request.method == "PUT": #not tested
        db = get_db()
        body = request.get_json()

        id = body["id"]
        display_name = body["display_name"]
        stock = body["stock"]
        price_per_unit = body["price_per_unit"]

        if not id or type(id) is int:
            error = "Id is required and must be a string."
        elif not display_name or type(display_name) is str:
            error = "Display Name is required and must be a string."
        elif not stock or type(stock) is int:
            error = "Stock is required."
        elif not price_per_unit or type(price_per_unit) is int:
            error = "Price Per Unit is required."

        query = """
            SELECT *
            FROM product 
            WHERE id = ?
            """
        existing_product = db.execute(query, (id,)).fetchone()
        if not existing_product:
            error = f"Couldn't find stock with id {id} because it does not exist."
        else:
            try:
                query = """
                    UPDATE stock
                    SET display_name = ?, stock = ?, price_per_unit = ?
                    WHERE id = ?
                    """
                db.execute(
                    query,
                    (display_name, stock, price_per_unit, id),
                )
                db.commit()
                return json.dumps({"Updated stock with id ": stock})
            except db.IntegrityError:
                error = f"An error occurred while updating the stock with id {id}."
        return json.dumps({"error": error})
        # update record on one specific product - can be used for restock

    if request.method == "POST":
        data = request.get_json()
        displayName = data["displayName"]
        pricePerUnit = data["pricePerUnit"]
        productType = data["productType"]
        stock = data["stock"] if "stock" in data else 0
        db = get_db()
        error = None

        if not displayName:
            error = "Product name is required."
        elif not pricePerUnit:
            error = "Price per unit is required."
        elif not productType:
            error = "Product type is required."

        if error is None:
            try:
                query = """
                    INSERT INTO product (display_name, stock, price_per_unit, product_type)
                    VALUES (?, ?, ?, ?)
                    """
                db.execute(query, (displayName, stock, pricePerUnit, productType))
                db.commit()
            except db.IntegrityError:
                error = "Sorry, something went wrong saving the product."
            else:
                return json.dumps({"success": f"Product successfully added!"})
        return json.dumps({"error": error})


@bp.route("/user", methods=["GET", "PUT"])
def user():
    if request.method == "GET":
        db = get_db()
        body = request.get_json()

        error = None
        id = body["id"]

        if not id or type(id) is not int:
            error = "Id is required and must be a int."

        query = """
        SELECT *
        FROM user
        WHERE id = ?
        """
        user = db.execute(query, (id,)).fetchall()

        if not error:
            if user is None:
                error = "This feature is not available yet - check back later!"
            elif len(user) == 0:
                error = f"No user has been registered with id {id}"
            else:
                user_dict = [dict(row) for row in user]

        if error:
            return json.dumps({"error": error})
        else:
            return json.dumps({"product": user_dict})
        # get more info about a specific user

    if request.method == "PUT":
        db = get_db()
        # update a user's info - this will be used to ban them
