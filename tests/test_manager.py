import pytest
import json
from api.db import get_db


def test_orders(client):
    # Test the /manager/orders endpoint
    response = client.get("/manager/orders")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "orders" in data


def test_users(client):
    # Test the /manager/users endpoint
    response = client.get("/manager/users")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_product_get(client):
    # Test the /manager/product GET endpoint
    data = {"id": 1}  # assuming product ID 1 exists
    response = client.get("/manager/product", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "product" in data


def test_product_errors_get(client):
    # no id error
    data = {}  # assuming product ID 1 exists
    response = client.get("/manager/product", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data

    # no product with id error
    data = {"id": 100}  # assuming product ID 1 exists
    response = client.get("/manager/product", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "No product has been registered with id 100" in data["error"]


def test_product_put(client):
    # Test the /manager/product PUT endpoint
    data = {
        "id": 1,
        "display_name": "New Name",
        "stock": 50,
        "price_per_unit": 10
    }
    response = client.put("/manager/product", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Updated stock with id " in data


def test_product_errors_put(client):
    # no id passed
    data = {}
    response = client.put("/manager/product", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data

    # incorrect data type passed
    data = {
        "id": "1",
        "display_name": "New Name"
    }
    response = client.put("/manager/product", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data


def test_product_post(client):
    # Test the /manager/product POST endpoint
    data = {
        "display_name": "New Product",
        "price_per_unit": 20,
        "product_type": "Cone",
        "stock": 100
    }
    response = client.post("/manager/product", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "success" in data


def test_product_errors_post(client):
    # Test the /manager/product POST endpoint
    data = {
        "display_name": "New Product"
    }
    response = client.post("/manager/product", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data

    data = {
        "display_name": "New Product",
        "price_per_unit": "incorrect data",
        "product_type": "Cone",
        "stock": 100
    }
    response = client.post("/manager/product", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data


def test_product_delete(client):
    # Test the /manager/product DELETE endpoint
    data = {"id": 1}  # assuming product ID 1 exists
    response = client.delete("/manager/product", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "deleted_product" in data


def test_product_errors_delete(client):
    # Test the /manager/product DELETE endpoint
    data = {}  # assuming product ID 1 exists
    response = client.delete("/manager/product", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data


def test_user_get(client):
    # Test the /manager/user GET endpoint
    data = {"id": 1}  # assuming user ID 1 exists
    response = client.get("/manager/user", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "product" in data


def test_user_errors_get(client):
    # Test the /manager/user GET endpoint
    data = {}  # assuming user ID 1 exists
    response = client.get("/manager/user", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data

    data = {"id": "bad"}  # assuming user ID 1 exists
    response = client.get("/manager/user", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data

    data = {"id": 100}  # assuming user ID 1 exists
    response = client.get("/manager/user", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data


def test_user_put(client):
    # Test the /manager/user PUT endpoint
    data = {"id": 1, "is_active": 0}  # assuming user ID 1 exists
    response = client.put("/manager/user", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Updated user with id " in data


def test_user_errors_put(client):
    # Test the /manager/user PUT endpoint
    data = {}  # assuming user ID 1 exists
    response = client.put("/manager/user", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data

    data = {"id": "bad"}  # assuming user ID 1 exists
    response = client.put("/manager/user", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data

    data = {"id": 100}  # assuming user ID 1 exists
    response = client.put("/manager/user", json=data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data


def test_history(client):
    # Test the /manager/history endpoint
    response = client.get("/manager/history")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "orders_history" in data