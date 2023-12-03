import pytest
import json
from api.db import get_db


def test_drones(client, app):
    response = client.get("/employee/2/drones")
    assert response.status_code == 200
    drones = json.loads(response.data).pop("drones")
    assert len(drones) == 3


def test_no_drones_registered(client, app):
    # Request drones for an employee with no registered drones
    response = client.get("/employee/1/drones")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data
    #assert "No drones have been registered!" in response.json["error"]


def test_no_orders_earnings(client, app):
    # Request earnings for an employee with no orders
    response = client.get("/employee/2/earnings")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data


def test_earnings(client, app):
    response = client.get("/employee/2/earnings")
    assert response.status_code == 200
    earnings = json.loads(response.data)
    assert "error" in earnings

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
    )
    assert response.status_code == 200

    response = client.get("/employee/2/earnings")
    assert response.status_code == 200
    earnings = json.loads(response.data)
    assert "earnings" in earnings


def test_invalid_drone_data(client, app):
    # Test incomplete data for creating a drone
    response = client.post("/employee/2/drone", json={"display_name": "Incomplete Drone"})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "error" in data
    

def test_post_put_delete_drone(client, app):
    # Add a drone first
    response = client.post("/employee/2/drone", json={"display_name": "Drone to Delete", "drone_size": 1, "serial_number": "6", "is_active": 1})
    assert response.status_code == 200

    #check drone there
    response = client.get("/employee/2/drones")
    assert response.status_code == 200
    drones = json.loads(response.data).pop("drones")
    assert len(drones) == 4

    #check drone there
    response = client.put("/employee/2/drone", json={"serial_number": "6", "is_active": 0 })
    assert response.status_code == 200
    assert "success" in json.loads(response.data)

    # Delete the added drone
    response = client.delete("/employee/2/drone", json={"serial_number": "6"})
    assert response.status_code == 200
    # Check if the drone has been successfully deleted


def test_orders_history(client, app):
    # Request order history for an employee
    response = client.get("/employee/2/history")
    assert response.status_code == 200
    # Check the structure and content of the history returned
    # Add more assertions for specific data checks

