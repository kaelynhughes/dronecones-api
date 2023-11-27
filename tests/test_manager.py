import pytest
import json
from api.db import get_db


def test_orders(client, app):
    response = client.get("/manager/orders")
    assert response.status_code == 200


def test_users(client, app):
    response = client.get("/manager/users")
    assert response.status_code == 200


def test_product(client, app):
    response = client.get("/manager/product")
    assert response.status_code == 200


def test_user(client, app):
    response = client.get("/manager/user")
    assert response.status_code == 200


def test_history(client, app):
    response = client.get("/manager/history")
    assert response.status_code == 200
