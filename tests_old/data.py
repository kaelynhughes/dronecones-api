import os
import sqlite3
from flask import Flask

app = Flask(__name__, instance_relative_config=True)

# Get the path to the database file in the "instance" folder
db_path = os.path.join(app.instance_path, "api.sqlite")
try:
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute the SQL queries to insert data
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
        
except sqlite3.Error as e:
    print(f"SQLite error: {e}")        

# Close the database connection
conn.close()
