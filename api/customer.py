import json

from flask import (
    Blueprint,
    request,
)

from api.db import get_db

bp = Blueprint("customer", __name__, url_prefix="/customer")


@bp.route("/menu", methods="GET")
def menu():
    db = get_db()
    # get and return all menu items


@bp.route("checkout", methods=("GET", "POST"))
def checkout():
    if request.method == "GET":
        db = get_db()
        # get most recent order

    if request.method == "POST":
        db = get_db()
        # save an order


@bp.route("/account", methods=("GET", "PATCH"))
def account():
    if request.method == "GET":
        db = get_db()
        # get all info for the account

    if request.method == "PATCH":
        db = get_db()
        # update the relevant info about the user
