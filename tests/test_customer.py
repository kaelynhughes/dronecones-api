import pytest
import json
from api.db import get_db

def test_menu(client, app):
    with app.app_context():
        db = get_db()
        query = "INSERT INTO product (display_name, stock, price_per_unit, product_type) VALUES ('Waffle', 10, 100, 'Cone')"
        db.execute(query)
        query = "INSERT INTO product (display_name, stock, price_per_unit, product_type) VALUES ('M&Ms', 10, 100, 'Topping')"
        db.execute(query)
        query = "INSERT INTO product (display_name, stock, price_per_unit, product_type) VALUES ('Vanilla', 10, 100, 'IceCream')"
        db.execute(query)
        db.commit()
    client.post('manager/product', data={'display_name': 'waffle', 'stock': 10, 'price_per_unit': 100, 'product_type': 'cone'})
    response = client.get('/customer/menu')
    assert response.status_code == 200

    assert len(json.loads(response.data)) == 4