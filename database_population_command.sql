INSERT INTO pizza(name) values ('perfect pepperoni');
INSERT INTO pizza(name) values ('margaritha');
INSERT INTO pizza(name) values ('fungi');
INSERT INTO pizza(name) values ('ham');
INSERT INTO pizza(name) values ('salami');
INSERT INTO pizza(name) values ('tonno');
INSERT INTO pizza(name) values ('americana');
INSERT INTO pizza(name) values ('hawaii');
INSERT INTO pizza(name) values ('vegan fungi');
INSERT INTO pizza(name) values ('vegan margaritha');

INSERT INTO ingredient(name, category, price) values ('Mozzarella',      'MEAT',       1.25);
INSERT INTO ingredient(name, category, price) values ('Pepperoni',       'MEAT',       1.25);
INSERT INTO ingredient(name, category, price) values ('Minced Beef',     'MEAT',       1.5);
INSERT INTO ingredient(name, category, price) values ('Ham',             'MEAT',       1.25);
INSERT INTO ingredient(name, category, price) values ('Salami',          'MEAT',       1.25);
INSERT INTO ingredient(name, category, price) values ('Tuna',            'FISH',       2);
INSERT INTO ingredient(name, category, price) values ('Pizza Seasoning', 'VEGETARIAN', 0);
INSERT INTO ingredient(name, category, price) values ('Mushroom',        'VEGETARIAN', 1.25);
INSERT INTO ingredient(name, category, price) values ('Onion',           'VEGETARIAN', 1);
INSERT INTO ingredient(name, category, price) values ('Pineapple',       'VEGETARIAN', 1.5);
INSERT INTO ingredient(name, category, price) values ('Vegan Cheese',    'VEGETARIAN', 2);

INSERT INTO pizza_to_ingredient(pizza, ingredient) values(1, 1);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(1, 2);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(2, 1);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(2, 7);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(3, 1);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(3, 7);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(3, 8);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(4, 1);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(4, 4);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(5, 1);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(5, 5);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(6, 1);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(6, 6);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(6, 9);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(7, 1);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(7, 2);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(7, 3);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(7, 4);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(8, 1);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(8, 3);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(8, 10);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(9, 7);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(9, 8);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(9, 11);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(10, 7);
INSERT INTO pizza_to_ingredient(pizza, ingredient) values(10, 11);

INSERT INTO side_dish(name, price) values ('thick shake cherry', 4.75);
INSERT INTO side_dish(name, price) values ('thick shake banana', 4.75);
INSERT INTO side_dish(name, price) values ('thick shake iced coffee', 4.75);

INSERT INTO side_dish(name, price) values ('chocolate lavacake',       3.95);
INSERT INTO side_dish(name, price) values ('dutch pancake',      2.99);

INSERT INTO customer(name, address, postcode, phone_number) values ('Jerry', 'PHS1', '6229EN', '123456789');

INSERT INTO deliveryman(name, postcode) values ('Tom', '6229');
INSERT INTO deliveryman(name, postcode) values ('Kurt', '6228');
INSERT INTO deliveryman(name, postcode) values ('Albert', '6229');