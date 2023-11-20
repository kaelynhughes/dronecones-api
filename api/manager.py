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
    # get all orders, or a specific number
    # if we want to get only a few at a time, we may need to have this be a bit more involved
    # so that we don't end up returning the same few records over and over
    # this will be used in account management as well

@bp.route("/users", methods=["GET"])
def users():
    db = get_db()
    error = None
    query = """
        SELECT username, is_active, user_type, id 
        FROM user 
        """
    usersResp = db.execute(query).fetchall()
    users = [dict(row) for row in usersResp]

    if users is None:
        error = "No users were found"

    if error:
        return json.dumps({"error": error})
    else:
        return json.dumps({"users": users})

@bp.route("/product", methods=["PUT", "POST", "DELETE"])
def accounting():
    if request.method == "PUT":
        db = get_db()
        data = request.get_json()
        display_name = data["display_name"]
        price_per_unit = data["price_per_unit"]
        product_type = data["product_type"]
        stock = data["stock"] if "stock" in data else 0
        id = data["id"]

        if not id:
            error = "Product id is required"
        
        query = """
            SELECT *
            FROM product 
            WHERE id = ?
            """
        existing_product = db.execute(query, (id,)).fetchone()
        if not existing_product:
            error = f"Couldn't find product with id {id}"
        else:
            try:
                query = """
                    UPDATE product
                    SET display_name = ?, price_per_unit = ?, product_type = ?, stock = ?
                    WHERE id = ?
                    """
                db.execute(
                    query,
                    (display_name, price_per_unit, product_type, stock, id),
                )
                db.commit()
                return json.dumps({"success": id})
            except:
                error = f"An error occurred while updating the product with id {id}."
        return json.dumps({"error": error})

    if request.method == "DELETE":
        db = get_db()
        error = None
        body = request.get_json()
        id = body["id"]

        if not id:
            error = "Product id is required"

        query = """
            SELECT *
            FROM product 
            WHERE id = ?
            """
        
        existing_product = db.execute(query, (id,)).fetchone()
        if not existing_product:
            error = "Product does not exist in database"

        if error is None:
            try:
                query = """
                    DELETE FROM product
                    WHERE id = ?
                    """
                db.execute(
                    query, (id,)
                )
                db.commit()
            except db.IntegrityError:
                error = f"An error occurred while deleting the product with id {id}"
            else:
                return json.dumps({"deleted_product": id})

        return json.dumps({"error": error})


    if request.method == "POST":
        data = request.get_json()
        display_name = data["display_name"]
        price_per_unit = data["price_per_unit"]
        product_type = data["product_type"]
        stock = data["stock"] if "stock" in data else 0
        db = get_db()
        error = None

        if not display_name:
            error = "Product name is required."
        elif not price_per_unit:
            error = "Price per unit is required."
        elif not product_type:
            error = "Product type is required."

        if error is None:
            try:
                query = """
                    INSERT INTO product (display_name, stock, price_per_unit, product_type)
                    VALUES (?, ?, ?, ?)
                    """
                id = db.execute(query, (display_name, stock, price_per_unit, product_type)).lastrowid
                db.commit()
            except:
                error = "Sorry, something went wrong saving the product."
            else:
                return json.dumps({"success": id})
        return json.dumps({"error": error})
