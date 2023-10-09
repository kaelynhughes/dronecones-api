import json

from flask import (
    Blueprint,
    request,
)

from api.db import get_db

bp = Blueprint("manager", __name__, url_prefix="/manager")


@bp.route("/orders", methods="GET")
def orders():
    db = get_db()
    # get all orders, or a specific number
    # if we want to get only a few at a time, we may need to have this be a bit more involved
    # so that we don't end up returning the same few records over and over
    # this will be used in account management as well


@bp.route("/product", methods=("GET"))
def accounting():
    if request.method == "GET":
        db = get_db()
        # get info on one specific product

    if request.method == "PUT":
        db = get_db()
        # update record on one specific product

    if request.method == "POST":
        db = get_db()
        # add a new product


@bp.route("/user", methods=("GET", "PUT"))
def user():
    if request.method == "GET":
        db = get_db()
        # get more info about a specific user

    if request.method == "PUT":
        db = get_db()
        # update a user's info - this will be used to ban them
