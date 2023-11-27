import pytest
import json
from api.db import get_db


def test_drones(client, app):
    response = client.get("/employee/2/drones")
    assert response.status_code == 200


def test_earnings(client, app):
    response = client.get("/employee/2/earnings")
    assert response.status_code == 200


def test_drone(client, app):
    response = client.get("employee/2/drone")
    assert response.status_code == 200


def test_history(client, app):
    response = client.get("employee/2/history")
    assert response.status_code == 200
