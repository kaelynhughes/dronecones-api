INSERT INTO product (display_name, stock, price_per_unit, product_type)
VALUES
    ('Waffle', 10, 100, 'Cone'),
    ('Cake', 10, 100, 'Cone'),
    ('ChocolateDipped', 10, 100, 'Cone'),
    ('M&Ms', 10, 100, 'Topping'),
    ('Sprinkles', 10, 100, 'Topping'),
    ('Oreos', 10, 100, 'Topping'),
    ('Vanilla', 10, 100, 'IceCream'),
    ('Chocolate', 10, 100, 'IceCream'),
    ('Mint', 10, 100, 'IceCream');

INSERT INTO user (username, password, user_type, is_active)
VALUES
    ('customer1', 'password', 'customer', 1),
    ('employee1', 'password', 'employee', 1);

INSERT INTO drone (serial_number, display_name, drone_size, is_active, owner_id)
VALUES
    (1, 'drone1', 1, 1, 2),
    (2, 'drone2', 2, 1, 2),
    (3, 'drone3', 3, 1, 2);
