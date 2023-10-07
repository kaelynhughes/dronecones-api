DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS drone;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS full_order;
DROP TABLE IF EXISTS ordered_cone;
DROP TABLE IF EXISTS restock;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  user_type TEXT NOT NULL,
  is_active INTEGER
);

CREATE TABLE drone (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  display_name TEXT NOT NULL,
  is_active INTEGER NOT NULL,
  drone_size INTEGER NOT NULL,
  owner_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (owner_id) REFERENCES user (id)
);

CREATE TABLE product (
   id INTEGER PRIMARY KEY AUTOINCREMENT, 
   display_name TEXT NOT NULL,
   stock INTEGER NOT NULL,
   price_per_unit INTEGER NOT NULL,
   product_type TEXT NOT NULL
);

CREATE TABLE full_order (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    total_price INTEGER NOT NULL,
    employee_cut INTEGER,
    profit INTEGER,
    customer_id INTEGER NOT NULL,
    order_time TEXT NOT NULL
);

CREATE TABLE ordered_cone (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cone INTEGER NOT NULL,
    scoop_1 INTEGER NOT NULL,
    scoop_2 INTEGER,
    scoop_3 INTEGER,
    topping_1 INTEGER,
    topping_2 INTEGER,
    topping_3 INTEGER,
    order_id INTEGER NOT NULL,
    drone_id INTEGER NOT NULL,
    FOREIGN KEY (cone) REFERENCES product (id),
    FOREIGN KEY (scoop_1) REFERENCES product (id),
    FOREIGN KEY (scoop_2) REFERENCES product (id),
    FOREIGN KEY (scoop_3) REFERENCES product (id),
    FOREIGN KEY (topping_1) REFERENCES product (id),
    FOREIGN KEY (topping_2) REFERENCES product (id),
    FOREIGN KEY (topping_3) REFERENCES product (id),
    FOREIGN KEY (order_id) REFERENCES full_order (id),
    FOREIGN KEY (drone_id) REFERENCES drone (id)
);

CREATE TABLE restock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    restock_time TEXT NOT NULL,
    product INTEGER,
    cost INTEGER NOT NULL,
    FOREIGN KEY (product) REFERENCES product (id)
);