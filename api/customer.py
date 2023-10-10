import json

from flask import (
    Blueprint,
    request,
)

from api.db import get_db

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


@bp.route("checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "GET":
        db = get_db()
        # get most recent order

    if request.method == "POST":
        db = get_db()
        # save an order


@bp.route("/account", methods=["GET", "PATCH"])
def account():
    if request.method == "GET":
        db = get_db()
        # get all info for the account

    if request.method == "PATCH":
        db = get_db()
        # update the relevant info about the user
