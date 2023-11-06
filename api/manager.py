import json
from flask import Blueprint, request, jsonify
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

    if not orders:
        error = "No orders found"
    elif len(orders) == 0:
        error = "Empty table"

    if error:
        return jsonify({"error": error})
    else:
        return jsonify({"orders": [dict(row) for row in orders]})

@bp.route("/product/<product_id>", methods=["GET", "PUT", "POST"])
def accounting(product_id):
    db = get_db()
    
    if request.method == "GET":
        query = """
            SELECT display_name, stock, price_per_unit
            FROM product
            WHERE id = ?
        """
        item = db.execute(query, (product_id,)).fetchone()
        
        if not item:
            return jsonify({"error": "Product not found"})
        else:
            return jsonify({"item": dict(item)})

    if request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"})

        # Validate and retrieve data from the JSON request
        display_name = data.get("display_name")
        stock = data.get("stock")
        price_per_unit = data.get("price_per_unit")
        product_type = data.get("product_type")

        if not display_name or not price_per_unit or not product_type:
            return jsonify({"error": "Missing required data fields"})

        try:
            query = """
                REPLACE INTO product (display_name, stock, price_per_unit, product_type)
                VALUES (?, ?, ?, ?)
            """
            db.execute(query, (display_name, stock, price_per_unit, product_type))
            db.commit()
            return jsonify({"success": f"{display_name} has been updated."})
        except Exception as e:
            return jsonify({"error": f"Error saving product: {str(e)}"})

    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"})

        display_name = data.get("display_name")
        stock = data.get("stock") if "stock" in data else 0
        price_per_unit = data.get("price_per_unit")
        product_type = data.get("product_type")

        if not display_name or not price_per_unit or not product_type:
            return jsonify({"error": "Missing required data fields"})

        try:
            query = """
                INSERT INTO product (display_name, stock, price_per_unit, product_type)
                VALUES (?, ?, ?, ?)
            """
            db.execute(query, (display_name, stock, price_per_unit, product_type))
            db.commit()
            return jsonify({"success": f"{product_type} added successfully."})
        except Exception as e:
            return jsonify({"error": f"Error saving product: {str(e)}"})

@bp.route("/user/<user_id>", methods=["GET", "PUT"])
def user(user_id):
    db = get_db()

    if request.method == "GET":
        search = request.args.get("search")

        if not search:
            return jsonify({"error": "Missing search term"})

        query = """
            SELECT *
            FROM user
            WHERE username = ?
        """
        user = db.execute(query, (search,)).fetchall()

        if not user:
            return jsonify({"error": "User not found"})
        else:
            user_list = [dict(row) for row in user]
            return jsonify({"user": user_list})

    if request.method == "PUT":
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data provided"})

        username = data.get("username")
        password = data.get("password")
        user_type = data.get("user_type")
        is_active = data.get("is_active")

        if not username or not password or not user_type or is_active is None:
            return jsonify({"error": "Missing required data fields"})

        try:
            query = """
                REPLACE INTO user (username, password, user_type, is_active)
                VALUES (?, ?, ?, ?)
            """
            db.execute(query, (username, password, user_type, is_active))
            db.commit()
            return jsonify({"success": f"Active value set to {is_active}"})
        except Exception as e:
            return jsonify({"error": f"Error saving user: {str(e)}"})
