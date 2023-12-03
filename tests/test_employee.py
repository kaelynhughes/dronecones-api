import pytest
import json
from api.db import get_db


def test_drones(client, app):
    response = client.get("/employee/2/drones")
    assert response.status_code == 200
    drones = json.loads(response.data).pop("drones")
    assert len(drones) == 3
    

def test_earnings(client, app):
    # response = client.get("/employee/2/earnings")
    # assert response.status_code == 200
    # earnings = json.loads(response.data)
    # assert "error" in earnings

    response = client.post('/customer/1/checkout', json={
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
        }
    ]
    }
    )
    assert response.status_code == 200

    # response = client.get("/employee/2/drones")
    # assert response.status_code == 200
    # drones = json.loads(response.data).pop("drones")
    # assert len(drones) == 2

    # something up with earnings
    # earnings cannot handle orders with multiple cones or multiple drones?
    response = client.get("/employee/2/earnings")
    assert response.status_code == 200
    earnings = json.loads(response.data)
    assert "earnings" in earnings

def test_drone(client, app):
    response = client.post("/employee/2/drone", json={"display_name": "drone_test", "drone_size": 1, "serial_number": "4", "is_active": 1})
    assert response.status_code == 200
    response = client.get("/employee/2/drones")
    assert response.status_code == 200
    drones = json.loads(response.data).pop("drones")
    assert len(drones) == 4

def test_history(client, app):
    response = client.get("/employee/2/history")
    assert response.status_code == 200
