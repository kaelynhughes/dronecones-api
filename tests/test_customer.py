import pytest
import json
from api.db import get_db


def test_menu(client, app):
    # with app.app_context():
    #     db = get_db()
    #     query = "INSERT INTO product (display_name, stock, price_per_unit, product_type) VALUES ('Waffle', 10, 100, 'Cone')"
    #     db.execute(query)
    #     query = "INSERT INTO product (display_name, stock, price_per_unit, product_type) VALUES ('M&Ms', 10, 100, 'Topping')"
    #     db.execute(query)
    #     query = "INSERT INTO product (display_name, stock, price_per_unit, product_type) VALUES ('Vanilla', 10, 100, 'IceCream')"
    #     db.execute(query)
    #     db.commit()
    # client.post('manager/product', data={'display_name': 'waffle', 'stock': 10, 'price_per_unit': 100, 'product_type': 'cone'})
    response = client.get("/customer/menu")
    assert response.status_code == 200
    menu = json.loads(response.data)
    assert len(menu) == 3
    assert len(menu["cones"]) == 3
    assert len(menu["toppings"]) == 3
    assert len(menu["icecream"]) == 3


def test_checkout_post_get(client):
    # Test the /customer/<customer_id>/checkout GET endpoint
    response = client.get("/customer/1/checkout")
    assert response.status_code == 200
    assert "error" in json.loads(response.data)
    data = {
        "total_price": 500,
        "employee_cut": 100,
        "profit": 400,
        "order_time": "2023-11-19 10:30:00",
        "cones": [
            {
                "cone": 1,
                "scoop_1": 7,
                "scoop_2": 8,
                "scoop_3": 9,
                "topping_1": 4,
                "topping_2": 5,
                "topping_3": 6
            },
            {
                "cone": 2,
                "scoop_1": 8,
                "scoop_2": 9,
                "scoop_3": 7,
                "topping_1": 5,
                "topping_2": 6,
                "topping_3": 4
            }
        ]
    }
    response = client.post("/customer/1/checkout", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "full_order_id" in data

    response = client.get("/customer/1/checkout")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "ordered cone" in data


def test_history(client, app):
    response = client.get("/customer/1/history")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "orders_history" in data

def test_account_get_put(client):
    # Test the /customer/<customer_id>/account PUT endpoint
    data = {
        "username": "new_username",
        "password": "new_password",
        "is_active": 1
    }
    response = client.put("/customer/1/account", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "success" in data

    # Test the /customer/<customer_id>/account GET endpoint
    response = client.get("/customer/1/account")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "new_username" in data["customer"][0]["username"]