CREATE TABLE pizza(
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE ingredient(
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE,
	category ENUM('VEGETARIAN', 'MEAT', 'FISH'),
	price FLOAT NOT NULL
);

CREATE TABLE pizza_to_ingredient(
	pizza INT NOT NULL,
	ingredient INT NOT NULL,
	FOREIGN KEY(pizza) REFERENCES pizza(id),
	FOREIGN KEY(ingredient) REFERENCES ingredient(id)
);

CREATE TABLE side_dish(
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE,
	price FLOAT NOT NULL
);

CREATE TABLE customer(
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50),
	address VARCHAR(128) NOT NULL,
	postcode VARCHAR(6) NOT NULL,
	phone_number VARCHAR(12),
	accumulation INT DEFAULT 0
);

CREATE TABLE deliveryman(
	id INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50),
	postcode VARCHAR(4) NOT NULL,
	time DATETIME
);

CREATE TABLE order_info(
	id INT PRIMARY KEY AUTO_INCREMENT,
	customer INT NOT NULL,
	time DATETIME,
	FOREIGN KEY (customer) REFERENCES customer(id)
);

CREATE TABLE order_to_pizza(
	order_info INT NOT NULL,
	pizza INT NOT NULL,
	FOREIGN KEY(order_info) REFERENCES order_info(id),
	FOREIGN KEY(pizza) REFERENCES pizza(id)
);

CREATE TABLE order_to_side_dish(
	order_info INT NOT NULL,
	side_dish INT NOT NULL,
	FOREIGN KEY(order_info) REFERENCES order_info(id),
	FOREIGN KEY(side_dish) REFERENCES side_dish(id)
);

CREATE TABLE coupon(
	id INT PRIMARY KEY AUTO_INCREMENT,
	status INT DEFAULT 0
);