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
    
    if error is None:
            return json.dumps(users)
    return json.dumps(error)

@bp.route("/product", methods=["GET", "PUT", "POST", "DELETE"])
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

        if not id or type(id) is not int:
            error = "Id is required and must be a integer."
        elif not display_name or type(display_name) is not str:
            error = "Display Name is required and must be a string."
        elif not stock or type(stock) is not int:
            error = "Stock is required and must be a integer."
        elif not price_per_unit or type(price_per_unit) is not int:
            error = "Price Per Unit is required and must be a integer."


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
                    UPDATE product
                    SET display_name = ?, stock = ?, price_per_unit = ?
                    WHERE id = ?
                    """
                db.execute(
                    query,
                    (display_name, stock, price_per_unit, id),
                )
                db.commit()
                return json.dumps({"success": id})
            except db.IntegrityError:
                error = f"An error occurred while updating the stock with id {id}."
        return json.dumps({"error": error})
        # update record on one specific product - can be used for restock

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
            except db.IntegrityError:
                error = "Sorry, something went wrong saving the product."
            else:
                return json.dumps({"success": id})
            
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
        body = request.get_json()

        id = body["id"]
        is_active = body["is_active"]

        if not id or type(id) is not int:
            error = "Id is required and must be a string."
        elif not is_active or type(is_active) is not int:
            error = "Display Name is required and must be a string."

        query = """
            SELECT *
            FROM user
            WHERE id = ?
            """
        existing_product = db.execute(query, (id,)).fetchone()
        if not existing_product:
            error = f"Couldn't find user with id {id} because it does not exist."
        else:
            try:
                query = """
                    UPDATE user
                    SET is_active = ?
                    WHERE id = ?
                    """
                db.execute(
                    query,
                    (is_active, id)
                )
                db.commit()
                return json.dumps({"Updated user with id ": id})
            except db.IntegrityError:
                error = f"An error occurred while updating the user with id {id}."
        return json.dumps({"error": error})
        # update a user's info - this will be used to ban them

@bp.route("/history", methods=["GET"])
def history():
    if request.method == "GET":
        db = get_db()
        error = None
        order_list = []

        query = """
                SELECT *
                FROM full_order
                ORDER BY id DESC
                LIMIT 50
                """
        orders = db.execute(query).fetchall()
        

        if orders is None:
                error = "This feature is not available yet - check back later!"
        else:
            full_order_dict = [dict(row) for row in orders]
            for order in full_order_dict:
                full_order_id = order["id"]
                query = """
                        SELECT *
                        FROM ordered_cone
                        WHERE order_id = ?
                        """ 
                ordered_cones = db.execute(query, (full_order_id,)).fetchall()

                if ordered_cones is None:
                    error = "This feature is not available yet - check back later!"
                else:
                    ordered_cone_dict = [dict(row) for row in ordered_cones]
                    order["cones"] = ordered_cone_dict
                    order_list.append(order)

        if error:
            return json.dumps({"error": error})
        else:
            return json.dumps({"orders_history": order_list})
