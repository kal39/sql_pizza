'''
Before the first time you run this, run these in mysql:

CREATE USER tom IDENTIFIED BY '1243';
GRANT ALL PRIVILEGES ON pizza.* to 'tom'@'%';
FLUSH PRIVILEGES;

You can check the structure of any tables by using this in mysql:
DESC table_name;
Because I don't know why it cannot be shown in terminal if add this line in here :X
'''

from os import stat
import pymysql as sql

verbose = False # if this is true PizzaDatabase will print out every sql command before executing it, useful for debugging

class PizzaDatabase:
	# constructor, connects to database "pizza" if it exists; if not it will create and initialise it
	def __init__(self):
		self.db = sql.connect(host="localhost", user="tom", password="1243")
		self.cursor = self.db.cursor()

		if not self.__sql_database_exists():
			self.__create_sql_database()
			self.__populate_sql_database()
		
		self.execute("USE pizza;")
	
	# deconstructor, probably unnecessary, but who knows, might be good to have
	def __del__(self): self.db.close()
	
	# executes sql command
	# replaces newlines and tabs with spaces
	# can run many commands at once, if they are separated with a ";"
	# if "verbose" is set to true it will print the command before running it, pretty useful for debugging
	def execute(self, command):
		for line in command.replace("\n", " ").replace("\t", " ").split(";"):
			if(len(line) == 0): continue
			try:
				if verbose: print("RUNNING: " + line)
				self.cursor.execute(line)
				self.db.commit()
			except sql.Error as error:
				print("ERROR: " + str(error))
	
	# resets the sql database to its the state specified in the .sql files
	def reset(self):
		self.__destroy_sql_database()
		self.__create_sql_database()
		self.__populate_sql_database()
	
	def get_pizza_info(self, pizza_id):
		self.execute(f"SELECT pizza.name, ingredient.name FROM ingredient JOIN pizza_to_ingredient ON ingredient.id = pizza_to_ingredient.ingredient JOIN pizza ON pizza.id = pizza_to_ingredient.pizza WHERE pizza.id = '{pizza_id}';")
		info = self.cursor.fetchall()
		return {"name": info[0][0], "ingredients": [p[1] for p in info]}

	def get_ingredient(self, ingredient_name):
		self.execute("SELECT category, price FROM ingredient WHERE name = '" + ingredient_name + "';")
		ingredient = self.cursor.fetchall()
		return {"name": ingredient_name, "category": ingredient[0][0], "price": ingredient[0][1]} if len(ingredient) == 1 else None 

	# returns a list of all pizza names
	def get_all_pizzas(self):
		self.execute("SELECT * FROM pizza ORDER BY id;")
		return {s[0]:s[1] for s in self.cursor.fetchall()}

	def get_all_sidedishes(self):
		self.execute("SELECT * FROM side_dish;")
		return [s for s in self.cursor.fetchall()]

	def get_sidedish(self,id):
		self.execute(f"SELECT * FROM side_dish WHERE id= {id};")
		return self.cursor.fetchone()

	def get_sidedish(self, did):
		self.execute(f"SELECT * FROM side_dish WHERE id = {did};")
		return self.cursor.fetchone()

	def get_cus_info(self, cus_id):
		if(not self.is_exist(table = 'customer',col = 'id', str = cus_id)):
			return None
		else:
			self.execute(f"SELECT * FROM customer WHERE id = '{cus_id}';")
			return self.cursor.fetchone()

	def get_total_price(self, items):
		price = 0
		for pizza_id in items[0]:
			pizza = self.get_pizza_info(pizza_id)
			for ingredient_name in pizza["ingredients"]:
				ingredient = self.get_ingredient(ingredient_name)
				price += ingredient["price"]*1.4*1.09
		for did in items[1]:
			price += self.get_sidedish(did)[2]
		return price

	def get_order_time(self,order_id):
		if(not self.is_exist('order_info','id',order_id)):
			print("Order does not exist.")
			return 
		self.execute(f"SELECT time FROM order_info WHERE id = {order_id};")
		return self.cursor.fetchone()[0]

	def get_coupon(self):
		self.execute("INSERT INTO coupon() VALUES();") 
		self.execute("SELECT id FROM coupon WHERE status = 0 LIMIT 1;")
		return self.cursor.fetchone()[0]

	def is_vegan(self,pizza_name):
		self.execute(f"SELECT ingredient.category FROM ingredient JOIN pizza_to_ingredient ON ingredient.id = pizza_to_ingredient.ingredient JOIN pizza ON pizza.id = pizza_to_ingredient.pizza WHERE pizza.name = '" + pizza_name + "';")
		category = [c[0] for c in self.cursor.fetchall()]
		for each in category:
			if each != 'VEGETARIAN': return ""
		return '(VEGETARIAN)'

	def is_exist(self, table, col, str):
		self.execute(f"SELECT {col} FROM {table} WHERE {col} = '{str}' LIMIT 1;")
		return self.cursor.fetchone() != None

	def create_customer(self, customer_name, address, postcode, phoneNo):
		try:
			self.execute(f"INSERT INTO customer(name, address, postcode, phone_number) values ('{customer_name}', '{address}', '{postcode}', '{phoneNo}');")
			self.execute("SELECT last_insert_id();")
			return self.cursor.fetchone()[0]
		except sql.Error as error:
			print("ERROR: " + str(error))
			return False

	def create_order(self, cus_id):
		try:
			self.execute(f"INSERT INTO order_info(customer) VALUES ({cus_id});")
			self.execute("SELECT last_insert_id();")
			return self.cursor.fetchone()[0]
		except sql.Error as error:
			print("ERROR: " + str(error))
	
	def check_coupon(self, coupon_id):
		if(not self.is_exist('coupon','id',coupon_id)):
			return False
		else:
			self.execute(f"SELECT status FROM coupon WHERE id = {coupon_id}")
			status = self.cursor.fetchone()[0]
			if(status == 1):
				return True
			else:
				return False

	def send_coupon(self, coupon_id):
		self.execute(f"UPDATE coupon SET status = 1 WHERE id = {coupon_id};")

	def delete_coupon(self, coupon_id):
		self.cursor.execute(f"DELETE FROM coupon WHERE id = {coupon_id};")

	def set_order(self, items, order_ID):
		try:
			for pizza_id in items[0]:
				self.cursor.execute(f"INSERT INTO order_to_pizza(order_info, pizza) VALUES ({order_ID}, {pizza_id});")
			for sidedish_id in items[1]:
				print(sidedish_id)
				self.cursor.execute(f"INSERT INTO order_to_side_dish(order_info, side_dish) VALUES ({order_ID}, {sidedish_id});")
			self.cursor.execute(f"UPDATE order_info SET time = NOW() WHERE id = {order_ID};")
			self.db.commit() # They should commit together, instead of one by one.
			return True
		except sql.Error as error:
			print("ERROR: " + str(error))
			return False
	
	def delete_order(self, order_id):
		try:
			self.cursor.execute(f"DELETE FROM order_to_pizza WHERE order_info = {order_id};")
			self.cursor.execute(f"DELETE FROM order_to_side_dish WHERE order_info = {order_id};")
			self.cursor.execute(f"DELETE FROM order_info WHERE id = {order_id};")
			self.db.commit() # They should commit together, instead of one by one.
		except sql.Error as error:
			print("ERROR: " + str(error))

	# "private" function, check if the "pizza" database exists
	def __sql_database_exists(self):
		self.execute("SHOW DATABASES LIKE 'pizza';")
		return self.cursor.fetchone() != None

	# "private" function, creates the "pizza" database
	def __create_sql_database(self):
		self.execute("CREATE DATABASE pizza;")
		self.execute("USE pizza;")
		self.execute(open("database_creation_command.sql", "r").read())
	
	# "private" function, destroys the "pizza" database
	def __destroy_sql_database(self): self.execute("DROP DATABASE pizza;")

	# "private" function, inserts all the samples from "database_population_command.sql"
	def __populate_sql_database(self): self.execute(open("database_population_command.sql", "r").read())

# for testing purposes (this will reset the database to the initial state)
if __name__ == "__main__":
	db = PizzaDatabase()
	db.reset()

	#print(db.is_exist('pizza','id','1'))
	#print(db.is_exist('pizza','id','11'))
	#print(db.is_exist(table = 'pizza',col='name',str = 'ham'))

	#print(db.get_cus_info(1))
	#print(db.get_all_pizzas())
	# print(db.get_ingredients_for("Vegan Fungi"))
	#print(db.get_all_pizzas())
	# print(db.get_pizza_info(1))

	#cus_id = db.create_customer("cat","123","321","345")
	#print(cus_id)
	#id = db.create_order(1)
	#print(id)
	#items = [[1,2,3],[2]]
	#print(db.set_order(items,id))
	#print(type(db.get_total_price(items)))
	#print(db.get_order_time(1))

