'''
Before the first time you run this, run these in mysql:

CREATE USER tom IDENTIFIED BY '1243';
GRANT ALL PRIVILEGES ON pizza.* to 'tom'@'%';
FLUSH PRIVILEGES;

You can check the structure of any tables by using this in mysql:
DESC table_name;
Because I don't know why it cannot be shown in terminal if add this line in here :X
'''
import pymysql as sql

def create_tables(cursor):
    cursor.execute("""
		CREATE TABLE pizza(
        	id INT PRIMARY KEY AUTO_INCREMENT,
        	name VARCHAR(50) NOT NULL UNIQUE
		);
	""")
    cursor.execute("""
		CREATE TABLE ingredient(
			id INT PRIMARY KEY AUTO_INCREMENT,
			name VARCHAR(30) NOT NULL UNIQUE,
			category ENUM('VEGETARIAN', 'MEAT', 'FISH'),
			price FLOAT NOT NULL
		);
	""")
    cursor.execute("""
		CREATE TABLE pizza_to_ingredient(
			pizza INT,
			ingredient INT,
			FOREIGN KEY(pizza) REFERENCES pizza(id),
			FOREIGN KEY(ingredient) REFERENCES ingredient(id)
		);
	""")
    cursor.execute("""
		CREATE TABLE side_dish(
			id INT PRIMARY KEY AUTO_INCREMENT,
			name VARCHAR(50) NOT NULL UNIQUE,
			price FLOAT NOT NULL
		);
	""")
    cursor.execute("""
		CREATE TABLE customer(
			id INT PRIMARY KEY AUTO_INCREMENT,
			name VARCHAR(50),
			address VARCHAR(128) NOT NULL,
			postcode VARCHAR(6) NOT NULL,
			phone_number VARCHAR(12)
		);
	""")
    cursor.execute("""
		CREATE TABLE deliveryman(
			id INT PRIMARY KEY AUTO_INCREMENT,
			name VARCHAR(50),
			postcode VARCHAR(6) NOT NULL,
			time DATETIME
		);
	""")
    cursor.execute("""
		CREATE TABLE order_info(
			id INT PRIMARY KEY AUTO_INCREMENT,
			customer INT NOT NULL,
			time DATETIME,
			FOREIGN KEY (customer) REFERENCES customer(id)
		);
	""")
    cursor.execute("""
		CREATE TABLE order_to_pizza(
			order_info INT NOT NULL,
			pizza INT NOT NULL,
			FOREIGN KEY(order_info) REFERENCES order_info(id),
			FOREIGN KEY(pizza) REFERENCES pizza(id)
		);
	""")
    cursor.execute("""
		CREATE TABLE order_to_side_dish(
			order_info INT NOT NULL,
			side_dish INT NOT NULL,
			FOREIGN KEY(order_info) REFERENCES order_info(id),
			FOREIGN KEY(side_dish) REFERENCES side_dish(id)
		);
	""")
    cursor.execute("""
		CREATE TABLE coupon(
			id INT PRIMARY KEY AUTO_INCREMENT,
			status INT DEFAULT 0
		);
	""") # status: 0 - not given, 1 - is given, delete after using it 

def insert_samples(cursor):
    # These samples are copied from Domino
    # Insert some pizzas
    cursor.execute("INSERT INTO pizza(name) values ('Perfect Pepperoni');")
    cursor.execute("INSERT INTO pizza(name) values ('Margarita');")
    cursor.execute("INSERT INTO pizza(name) values ('Fungi');")
    cursor.execute("INSERT INTO pizza(name) values ('Ham');")
    cursor.execute("INSERT INTO pizza(name) values ('Salami');")
    cursor.execute("INSERT INTO pizza(name) values ('Vegan Fungi');")

    # Insert some ingredients
    cursor.execute("INSERT INTO ingredient(name, category, price) values ('Mozzarella',      'MEAT',       1.25);")
    cursor.execute("INSERT INTO ingredient(name, category, price) values ('Pepperoni',       'MEAT',       1.25);")
    cursor.execute("INSERT INTO ingredient(name, category, price) values ('Pizza Seasoning', 'VEGETARIAN', 0);")
    cursor.execute("INSERT INTO ingredient(name, category, price) values ('Mushroom',        'VEGETARIAN', 1.25);")
    cursor.execute("INSERT INTO ingredient(name, category, price) values ('Ham',             'MEAT',       1.25);")
    cursor.execute("INSERT INTO ingredient(name, category, price) values ('Salami',          'MEAT',       1.25);")
    cursor.execute("INSERT INTO ingredient(name, category, price) values ('Vegan Cheese',    'VEGETARIAN', 2);")

    # Insert some makepizzas
    cursor.execute("INSERT INTO pizza_to_ingredient(pizza, ingredient) values(1, 1);")
    cursor.execute("INSERT INTO pizza_to_ingredient(pizza, ingredient) values(1, 2);")
    cursor.execute("INSERT INTO pizza_to_ingredient(pizza, ingredient) values(2, 1);")
    cursor.execute("INSERT INTO pizza_to_ingredient(pizza, ingredient) values(2, 3);")
    cursor.execute("INSERT INTO pizza_to_ingredient(pizza, ingredient) values(3, 1);")
    cursor.execute("INSERT INTO pizza_to_ingredient(pizza, ingredient) values(3, 4);")
    cursor.execute("INSERT INTO pizza_to_ingredient(pizza, ingredient) values(4, 1);")
    cursor.execute("INSERT INTO pizza_to_ingredient(pizza, ingredient) values(4, 5);")
    cursor.execute("INSERT INTO pizza_to_ingredient(pizza, ingredient) values(5, 1);")
    cursor.execute("INSERT INTO pizza_to_ingredient(pizza, ingredient) values(5, 6);")
    cursor.execute("INSERT INTO pizza_to_ingredient(pizza, ingredient) values(6, 4);")
    cursor.execute("INSERT INTO pizza_to_ingredient(pizza, ingredient) values(6, 3);")
    cursor.execute("INSERT INTO pizza_to_ingredient(pizza, ingredient) values(6, 7);")
   
    # Execute this in mysql to see the complete price chart with names:
    # SELECT pizza.id, pizza.name, ingredient.id, ingredient.name, ingredient.category, ingredient.price, ingredient.price*1.4 as 'sell_price' FROM pizza JOIN pizza_to_ingredient ON pizza.id = pizza_to_ingredient.pizza JOIN ingredient ON ingredient.id = pizza_to_ingredient.ingredient ORDER BY pizza;

    # Insert some other foods
    cursor.execute("INSERT INTO side_dish(name, price) values ('Thick Shake Cherry', 4.75);")
    cursor.execute("INSERT INTO side_dish(name, price) values ('Thick Shake Banana', 4.75);")
    cursor.execute("INSERT INTO side_dish(name, price) values ('Coco Churros',       3.95);")
    cursor.execute("INSERT INTO side_dish(name, price) values ('Dutch Pancake',      2.99);")

    #Insert a customer
    cursor.execute("INSERT INTO customer(name, address, postcode, phone_number) values ('Jerry', 'PHS1', '6229EN', '123456789');")

    #Insert a deliveryman
    cursor.execute("INSERT INTO deliveryman(name, postcode) values ('Tom', '6229EN');")

if __name__ == "__main__":
	db = sql.connect(host="localhost", user="tom", password="1243")
	cursor = db.cursor()
	
	cursor.execute("DROP DATABASE IF EXISTS pizza;")
	cursor.execute("CREATE DATABASE pizza;")
	cursor.execute("USE pizza;")

	create_tables(cursor)
	try:
		insert_samples(cursor)
		db.commit()
	except sql.Error as e:
		print(e)
		db.rollback()
	
	db.close()
