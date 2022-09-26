INSERT INTO pizza(name) values ('Perfect Pepperoni');
INSERT INTO pizza(name) values ('Margarita');
INSERT INTO pizza(name) values ('Fungi');
INSERT INTO pizza(name) values ('Ham');
INSERT INTO pizza(name) values ('Salami');
INSERT INTO pizza(name) values ('Vegan Fungi');

INSERT INTO ingredient(name, category, price) values ('Mozzarella',      'MEAT',       1.25);
INSERT INTO ingredient(name, category, price) values ('Pepperoni',       'MEAT',       1.25);
INSERT INTO ingredient(name, category, price) values ('Pizza Seasoning', 'VEGETARIAN', 0);
INSERT INTO ingredient(name, category, price) values ('Mushroom',        'VEGETARIAN', 1.25);
INSERT INTO ingredient(name, category, price) values ('Ham',             'MEAT',       1.25);
INSERT INTO ingredient(name, category, price) values ('Salami',          'MEAT',       1.25);
INSERT INTO ingredient(name, category, price) values ('Vegan Cheese',    'VEGETARIAN', 2);

INSERT INTO pizza_to_ingredient(pizza, ingredient) values(1, 1);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(1, 2);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(2, 1);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(2, 3);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(3, 1);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(3, 4);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(4, 1);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(4, 5);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(5, 1);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(5, 6);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(6, 4);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(6, 3);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(6, 7);

INSERT INTO side_dish(name, price) values ('Thick Shake Cherry', 4.75);
INSERT INTO side_dish(name, price) values ('Thick Shake Banana', 4.75);
INSERT INTO side_dish(name, price) values ('Coco Churros',       3.95);
INSERT INTO side_dish(name, price) values ('Dutch Pancake',      2.99);

INSERT INTO customer(name, address, postcode, phone_number) values ('Jerry', 'PHS1', '6229EN', '123456789');

INSERT INTO deliveryman(name, postcode) values ('Tom', '6229EN');