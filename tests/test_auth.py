import pytest
import json
from api.db import get_db


def test_login_valid_user(client):
    response = client.post("/auth/register", json={"username": "test_user", "password": "test_password", "user_type": "Employee"})
    assert response.status_code == 200

    response = client.post("/auth/login", json={"username": "test_user", "password": "test_password"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "id" in data
    assert "user_type" in data
    assert "is_active" in data

def test_login_incorrect_username(client):
    response = client.post("/auth/login", json={"username": "non_existing_user", "password": "test_password"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data

def test_login_incorrect_password(client):
    response = client.post("/auth/login", json={"username": "test_user", "password": "incorrect_password"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data

def test_login_missing_credentials(client):
    response = client.post("/auth/login", json={})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data

def test_register_valid_user(client):
    response = client.post("/auth/register", json={"username": "new_user", "password": "new_password", "user_type": "Customer"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "success" in data
    assert isinstance(data["success"], int)

def test_register_existing_user(client, app):
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO user (username, password, user_type, is_active) VALUES (?, ?, ?, ?)",
                   ("existing_user", "existing_password", "Manager", 1))
        db.commit()

    response = client.post("/auth/register", json={"username": "existing_user", "password": "existing_password", "user_type": "Manager"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data
    assert "is not available" in data["error"]

def test_register_missing_data(client):
    response = client.post("/auth/register", json={})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data
    assert "Bad data" in data["error"]