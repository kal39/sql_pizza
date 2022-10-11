'''
Before the first time you run this, run these in mysql:

CREATE USER tom IDENTIFIED BY '1243';
GRANT ALL PRIVILEGES ON pizza.* to 'tom'@'%';
FLUSH PRIVILEGES;

You can check the structure of any tables by using this in mysql:
DESC table_name;
Because I don't know why it cannot be shown in terminal if add this line in here :X
'''

from multiprocessing.util import is_exiting
import re
from tkinter.tix import Select
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
	
	def get_pizza(self, pizza_name):
		self.execute("SELECT ingredient.name FROM ingredient INNER JOIN pizza_to_ingredient ON ingredient.id = pizza_to_ingredient.ingredient INNER JOIN pizza ON pizza.id = pizza_to_ingredient.pizza WHERE pizza.name = '" + pizza_name + "';")
		return {"name": pizza_name, "ingredients": list(map(lambda item: item[0], self.cursor.fetchall()))}

	def get_ingredient(self, ingredient_name):
		self.execute("SELECT category, price FROM ingredient WHERE name = '" + ingredient_name + "';")
		ingredient = self.cursor.fetchall()
		return {"name": ingredient_name, "category": ingredient[0][0], "price": ingredient[0][1]} if len(ingredient) == 1 else None 

	# returns a list of all pizza names
	def get_all_pizza_names(self):
		self.execute("SELECT name FROM pizza")
		return list(map(lambda item: item[0], self.cursor.fetchall()))

	def get_all_sidedishes(self):
		self.execute("SELECT name, price from side_dish;")
		return {s[0]:s[1] for s in self.cursor.fetchall()}

	def is_vegan(self,pizza_name):
		self.execute("SELECT ingredient.category FROM ingredient INNER JOIN pizza_to_ingredient ON ingredient.id = pizza_to_ingredient.ingredient INNER JOIN pizza ON pizza.id = pizza_to_ingredient.pizza WHERE pizza.name = '" + pizza_name + "';")
		category = [c[0] for c in self.cursor.fetchall()]
		for each in category:
			if each != 'VEGETARIAN': return ""
		return '(VEGETARIAN)'

	def add_order(self, customer_id):
		if(not self.is_exist(table = 'customer',col = 'id', str = customer_id)):
			print('Customer does not exist.')
			return False
		try:
			self.execute(f"INSERT INTO order_info(customer) values ('{customer_id}');")
			self.db.commit()
			self.execute("SELECT last_insert_id();")
			return self.cursor.fetchone()
		except sql.Error as error:
			print("ERROR: " + str(error))
			return False

	def add_customer(self, customer_name, address, postcode, phoneNo):
		try:
			self.execute(f"INSERT INTO customer(name, address, postcode, phone_number) values ('{customer_name}', '{address}', '{postcode}', '{phoneNo}');")
			self.db.commit()
			self.execute("SELECT last_insert_id();")
			return self.cursor.fetchone()
		except sql.Error as error:
			print("ERROR: " + str(error))
			return False

	def is_exist(self, table, col, str):
		self.execute(f"SELECT {col} FROM {table} WHERE {col} = '{str}' LIMIT 1;")
		return self.cursor.fetchone() != None
	
	def order_pizzas(self,pizza_names):
		pass

	def get_cus_info(self, cus_id):
		if(not self.is_exist(table = 'customer',col = 'id', str = cus_id)):
			return None
		else:
			self.execute(f"SELECT * from customer where id = '{cus_id}';")
			return self.cursor.fetchone()

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

	print(db.get_cus_info(1))
	# print(db.get_pizzas())
	# print(db.get_ingredients_for("Vegan Fungi"))
