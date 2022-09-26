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
	def __del__(self):
		self.db.close()
	
	# executes sql command; replaces newlines and tabs with spaces;
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
	
	# returns a list of all pizzas
	def get_pizzas(self):
		self.execute("SELECT name FROM pizza")
		return list(map(lambda item: item[0], self.cursor.fetchall()))
	
	# returns a list of ingredients for 
	def get_ingredients_for(self, pizza_name):
		self.execute("SELECT ingredient.name FROM ingredient INNER JOIN pizza_to_ingredient ON ingredient.id = pizza_to_ingredient.ingredient INNER JOIN pizza ON pizza.id = pizza_to_ingredient.pizza WHERE pizza.name = '" + pizza_name + "';")
		return list(map(lambda item: item[0], self.cursor.fetchall()))
	
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
	def __destroy_sql_database(self):
		self.execute("DROP DATABASE pizza;")

	# "private" function, inserts all the samples from "database_population_command.sql"
	def __populate_sql_database(self):
		self.execute(open("database_population_command.sql", "r").read())

# for testing purposes (this will reset the database to the initial state)
if __name__ == "__main__":
	db = PizzaDatabase()
	db.reset()
	# print(db.get_pizzas())
	# print(db.get_ingredients_for("Vegan Fungi"))
