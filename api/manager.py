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
        return {" error": "No users were found"}  # , 404

    return json.dumps(users)


@bp.route("/product", methods=["GET", "PUT", "POST", "DELETE"])
def accounting():  # does this need to be product()
    if request.method == "GET":
        db = get_db()
        body = request.get_json()

        error = None
        id = body["id"]

        if not id or type(id) is not int:
            return {"error": "Id is required and must be an integer."}

        query = """
        SELECT *
        FROM product
        WHERE id = ?
        """
        product = db.execute(query, (id,)).fetchall()

        if product is None:
            return {"error": "This feature is not available yet - check back later!"}

        if len(product) == 0:
            return {"error": f"No product has been registered with id {id}"}
        else:
            product_dict = [dict(row) for row in product]

        return json.dumps({"product": product_dict})

        # get info on one specific product

    # in 2.0, make this its own function that takes a product ID in the query string
    if request.method == "PUT":  # not tested
        db = get_db()
        body = request.get_json()
        if "id" not in body:
            return {"error": "We need a product ID to update your product!"}  # , 400
        id = body["id"]

        if type(id) is not int:
            return {"error": "ID must be an integer."}  # , 400

        try:
            query = """
                SELECT *
                FROM product 
                WHERE id = ?
                """
            existing_product = db.execute(query, (id,)).fetchone()
            # this is janky. change in 2.0 so we don't necessarily return stock
            if not existing_product:
                return {
                    "error": f"Couldn't find product with ID {id} because it does not exist."
                }  # , 400
            stock = existing_product["stock"]
        except db.IntegrityError:
            return {"error": f"We couldn't find a product with the ID {id}."}

        if "display_name" in body:
            display_name = body["display_name"]
            if type(display_name) is not str:
                return {"error": "Display name must be a string."}  # , 400
            try:
                query = """
                    UPDATE product
                    SET display_name = ?
                    WHERE id = ?
                    """
                db.execute(
                    query,
                    (display_name, id),
                )
                db.commit()
            except db.IntegrityError as ex:
                print(ex)
                return {
                    "error": "An unexpected database error occurred on our end while updating display name. Sorry!"
                }  # , 500
            except Exception as ex:
                print(ex)
                return {
                    "error": "An unexpected error occurred on our end while updating display name. Sorry!"
                }  # , 500

        if "stock" in body:
            stock = body["stock"]
            if type(stock) is not int:
                return {"error": "Stock must be a integer."}  # , 400
            try:
                query = """
                    UPDATE product
                    SET stock = ?
                    WHERE id = ?
                    """
                db.execute(
                    query,
                    (stock, id),
                )
                db.commit()
            except db.IntegrityError as ex:
                print(ex)
                return {
                    "error": "An unexpected database error occurred on our end while updating stock. Sorry!"
                }  # , 500
            except Exception as ex:
                print(ex)
                return {
                    "error": "An unexpected error occurred on our end while updating stock. Sorry!"
                }  # , 500

        if "price_per_unit" in body:
            price_per_unit = body["price_per_unit"]
            if type(price_per_unit) is not int:
                return {"error": "Price per unit must be a integer."}  # , 400
            try:
                query = """
                    UPDATE product
                    SET price_per_unit = ?
                    WHERE id = ?
                    """
                db.execute(
                    query,
                    (price_per_unit, id),
                )
                db.commit()
            except db.IntegrityError as ex:
                print(ex)
                return {
                    "error": "An unexpected database error occurred on our end while updating price per unit. Sorry!"
                }  # , 500
            except Exception as ex:
                print(ex)
                return {
                    "error": "An unexpected error occurred on our end while updating price per unit. Sorry!"
                }  # , 500

        # JANKY ALERT in 2.0 this should be updated to something like {"success": message} where message tells what was updated
        # also let it be known i find this return statement incredibly funny
        return json.dumps({"Updated stock with id ": stock})

        # update record on one specific product - can be used for restock

    if request.method == "POST":
        data = request.get_json()
        try:
            display_name = data["display_name"]
            price_per_unit = data["price_per_unit"]
            product_type = data["product_type"]
            stock = data["stock"] if "stock" in data else 0
        except KeyError:
            return {
                "error": "Looks like we're missing some of the information we need to create your product!"
            }  # , 400
        db = get_db()

        try:
            query = """
                INSERT INTO product (display_name, stock, price_per_unit, product_type)
                VALUES (?, ?, ?, ?)
                """
            id = db.execute(
                query, (display_name, stock, price_per_unit, product_type)
            ).lastrowid
            db.commit()
        except db.IntegrityError:
            error = "Sorry, something went wrong saving the product."
        else:
            return json.dumps({"success": id})

    if request.method == "DELETE":
        db = get_db()
        body = request.get_json()
        if "id" not in body:
            return {
                "error": "Looks like we're missing the ID of the product you want to delete!"
            }  # , 400
        id = body["id"]

        query = """
            SELECT *
            FROM product 
            WHERE id = ?
            """

        existing_product = db.execute(query, (id,)).fetchone()
        if not existing_product:
            return {"error": "Product does not exist in database"}  # , 404

        try:
            query = """
                DELETE FROM product
                WHERE id = ?
                """
            db.execute(query, (id,))
            db.commit()
        except db.IntegrityError:
            error = f"An error occurred while deleting the product with id {id}."
        else:
            return json.dumps({"deleted_product": id})


@bp.route("/user", methods=["GET", "PUT"])
def user():
    if request.method == "GET":
        db = get_db()
        body = request.get_json()

        if "id" not in body:
            return {"error": "We need a user ID to get information on a user!"}  # , 400
        id = body["id"]

        if type(id) is not int:
            return {"error": "ID must be a int."}  # , 400
        try:
            query = """
            SELECT id, username, user_type, is_active
            FROM user
            WHERE id = ?
            """
            user = db.execute(query, (id,)).fetchall()
        except Exception as ex:
            print(ex)
            return {
                "error": f"Sorry, an unexpected error occurred on our end while fetching information for user {id}"
            }  # , 500

        if user is None:
            return {
                "error": "This feature is not available yet - check back later!"
            }  # , 400
        if len(user) == 0:
            return {"error": f"No user has been registered with id {id}"}  # , 404
        user_dict = [dict(row) for row in user]
        # 2.0 change this!! not a product
        return json.dumps({"product": user_dict})
        # get more info about a specific user

    if request.method == "PUT":
        db = get_db()
        body = request.get_json()

        if "id" not in body:
            return {
                "error": "We need the ID of the user you're trying to edit!"
            }  # , 400
        id = body["id"]
        if not id or type(id) is not int:
            return {"error": "ID is required and must be an integer."}  # , 400

        if "is_active" not in body:
            return {"error": "Looks like the activity status "}
        is_active = body["is_active"]
        if type(is_active) is not int:
            return {"error": "Activity status must be in integer form."}  # , 400

        try:
            query = """
                SELECT *
                FROM user
                WHERE id = ?
                """
            existing_user = db.execute(query, (id,)).fetchone()
            if not existing_user:
                return {
                    "error": f"Couldn't find user with id {id} because it does not exist."
                }  # , 404
            query = """
                UPDATE user
                SET is_active = ?
                WHERE id = ?
                """
            db.execute(query, (is_active, id))
            db.commit()
            return json.dumps({"Updated user with id ": id})
        except db.IntegrityError:
            return {"error": f"An error occurred while updating the user with ID {id}."}
        # update a user's info - this will be used to ban them


@bp.route("/history", methods=["GET"])
def history():
    if request.method == "GET":
        db = get_db()
        order_list = []

        query = """
                SELECT *
                FROM full_order
                ORDER BY id DESC
                LIMIT 50
                """
        orders = db.execute(query).fetchall()

        if orders is None:
            return {
                "error": "This feature is not available yet - check back later!"
            }  # , 500

        full_order_dict = [dict(row) for row in orders]
        for order in full_order_dict:
            try:
                full_order_id = order["id"]
                query = """
                        SELECT *
                        FROM ordered_cone
                        WHERE order_id = ?
                        """
                ordered_cones = db.execute(query, (full_order_id,)).fetchall()

                if ordered_cones is None:
                    return {
                        "error": "This feature is not available yet - check back later!"
                    }  # , 500
                ordered_cone_dict = [dict(row) for row in ordered_cones]
                order["cones"] = ordered_cone_dict
                order_list.append(order)
            except Exception as ex:
                print(ex)
                return {
                    "error": "Sorry, an unexpected error occurred on our end while processing your request!"
                }  # , 500

        return json.dumps({"orders_history": order_list})
