import os
import sqlite3
import unittest
from flask import Flask

# Your Flask application initialization
app = Flask(__name__, instance_relative_config=True)
# ... (other app configurations)

# Function to initialize the database with initial data
def initialize_database():
    db_path = os.path.join(app.instance_path, "api.sqlite")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    insert_statements = [
        "INSERT INTO product (display_name, stock, price_per_unit, product_type) VALUES ('Waffle', 10, 100, 'Cone')",
        "INSERT INTO product (display_name, stock, price_per_unit, product_type) VALUES ('Cake', 10, 100, 'Cone')",
        "INSERT INTO product (display_name, stock, price_per_unit, product_type) VALUES ('ChocolateDipped', 10, 100, 'Cone')",
        "INSERT INTO product (display_name, stock, price_per_unit, product_type) VALUES ('M&Ms', 10, 100, 'Topping')",
        "INSERT INTO product (display_name, stock, price_per_unit, product_type) VALUES ('Sprinkles', 10, 100, 'Topping')",
        "INSERT INTO product (display_name, stock, price_per_unit, product_type) VALUES ('Oreos', 10, 100, 'Topping')",
        "INSERT INTO product (display_name, stock, price_per_unit, product_type) VALUES ('Vanilla', 10, 100, 'IceCream')",
        "INSERT INTO product (display_name, stock, price_per_unit, product_type) VALUES ('Chocolate', 10, 100, 'IceCream')",
        "INSERT INTO product (display_name, stock, price_per_unit, product_type) VALUES ('Mint', 10, 100, 'IceCream')",
    ]

    for statement in insert_statements:
        cursor.execute(statement)
        conn.commit()

    conn.close()

class MyAppTestCase(unittest.TestCase):
    def setUp(self):
        # Run the database initialization before each test
        initialize_database()
        # Initialize the Flask test client
        self.app = app.test_client()

    def tearDown(self):
        # Clean up after each test if needed
        pass

    # Your test methods go here
    def test_menu(self):
        # Example test
        response = self.app.get('/customer/menu')
        print(response)
        self.assertEqual(response.status_code, 200)
        # ...

if __name__ == '__main__':
    unittest.main()
