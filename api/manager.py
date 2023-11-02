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


@bp.route("/product", methods=["GET", "PUT", "POST"])
def accounting():
    if request.method == "GET":
        db = get_db()
        # get info on one specific product

    if request.method == "PUT":
        db = get_db()
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
            except:
                error = "Sorry, something went wrong saving the product."
            else:
                return json.dumps({"success": f"Product successfully added!"})
        return json.dumps({"error": error})


@bp.route("/user", methods=["GET", "PUT"])
def user():
    if request.method == "GET":
        db = get_db()
        # get more info about a specific user

    if request.method == "PUT":
        db = get_db()
        # update a user's info - this will be used to ban them
