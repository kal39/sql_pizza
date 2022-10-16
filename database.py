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

verbose = False  # if this is true PizzaDatabase will print out every sql command before executing it, useful for debugging


class PizzaDatabase:
    # constructor, connects to database "pizza" if it exists; if not it will create and initialise it
    def __init__(self):
        self.db = sql.connect(host="localhost", user="tom", password="1243")
        self.cursor = self.db.cursor()

        if not self.__sql_database_exists():
            self.__create_sql_database()
            self.__populate_sql_database()

        self.__execute("USE pizza;")

    # deconstructor, probably unnecessary, but who knows, might be good to have
    def __del__(self): self.db.close()

    # resets the sql database to its the state specified in the .sql files
    def reset(self):
        self.__destroy_sql_database()
        self.__create_sql_database()
        self.__populate_sql_database()

    def get_pizza(self, id):
        self.__execute(
            f"SELECT pizza.name, ingredient.id FROM ingredient JOIN pizza_to_ingredient ON ingredient.id = pizza_to_ingredient.ingredient JOIN pizza ON pizza.id = pizza_to_ingredient.pizza WHERE pizza.id = '{id}';")
        info = self.cursor.fetchall()
        return {"name": info[0][0], "ingredients": [p[1] for p in info]}

    def get_ingredient(self, id):
        self.__execute(
            "SELECT name, category, price FROM ingredient WHERE id = '" + str(id) + "';")
        ingredient = self.cursor.fetchone()
        return {"name": ingredient[0], "category": ingredient[1], "price": ingredient[2]}

    def get_side_dish(self, id):
        self.__execute(f"SELECT name, price FROM side_dish WHERE id= {id};")
        side_dish = self.cursor.fetchone()
        return {"name": side_dish[0], "price": side_dish[1]}

    def get_customer(self, id):
        if (not self.exists(table='customer', col='id', str=id)):
            return None
        self.__execute(
            f"SELECT name, address, postcode, phone_number FROM customer WHERE id = '{id}';")
        customer = self.cursor.fetchone()
        return {"name": customer[0], "address": customer[1], "postcode": customer[2], "phone_number": customer[3]}

    def get_order(self, id):
        if (not self.exists(table='order_info', col='id', str=id)):
            return None
        self.__execute(
            f"SELECT customer, time FROM order_info WHERE id = '{id}';")
        order = self.cursor.fetchone()
        return {"customer": order[0], "time": order[1]}

    def get_deliveryman(self, id):
        if (not self.exists(table='deliveryman', col='id', str=id)):
            return None
        self.__execute(
            f"SELECT name, postcode, time FROM deliveryman WHERE id = '{id}';")
        deliveryman = self.cursor.fetchone()
        return {"name": deliveryman[0], "postcode": deliveryman[1], "time": deliveryman[2]}

    # returns a list of all pizza ids
    def get_all_pizza_ids(self):
        self.__execute("SELECT id FROM pizza;")
        return [i[0] for i in self.cursor.fetchall()]

    def get_all_side_dish_ids(self):
        self.__execute("SELECT id FROM side_dish;")
        return [i[0] for i in self.cursor.fetchall()]

    def get_all_order_ids(self):
        self.__execute("SELECT id FROM order_info;")
        return [i[0] for i in self.cursor.fetchall()]

    def get_all_deliverymen_ids(self):
        self.__execute("SELECT id FROM deliveryman;")
        return [i[0] for i in self.cursor.fetchall()]

    def get_order_time(self, order_id):
        if (not self.exists('order_info', 'id', order_id)):
            print("Order does not exist.")
            return
        self.__execute(f"SELECT time FROM order_info WHERE id = {order_id};")
        return self.cursor.fetchone()[0]

    def get_coupon(self, customer_id):
        self.__execute(
            f"SELECT accumulation FROM customer WHERE id = {customer_id};")
        pizza_number = self.cursor.fetchone()[0]
        if (pizza_number >= 10):
            self.__execute(
                f"UPDATE customer SET accumulation = accumulation - 10 WHERE id = {customer_id}")
            self.__execute("INSERT INTO coupon() VALUES();")
            self.__execute("SELECT id FROM coupon WHERE status = 0 LIMIT 1;")
            return self.cursor.fetchone()[0]
        else:
            return -1

    def is_vegan(self, pizza_name):
        self.__execute(f"SELECT ingredient.category FROM ingredient JOIN pizza_to_ingredient ON ingredient.id = pizza_to_ingredient.ingredient JOIN pizza ON pizza.id = pizza_to_ingredient.pizza WHERE pizza.name = '" + pizza_name + "';")
        category = [c[0] for c in self.cursor.fetchall()]
        for each in category:
            if each != 'VEGETARIAN':
                return ""
        return '(VEGETARIAN)'

    def exists(self, table, col, str):
        self.__execute(
            f"SELECT {col} FROM {table} WHERE {col} = '{str}' LIMIT 1;")
        return self.cursor.fetchone() != None

    def create_customer(self, customer_name, address, postcode, phoneNo):
        self.__execute(
            f"INSERT INTO customer(name, address, postcode, phone_number) values ('{customer_name}', '{address}', '{postcode}', '{phoneNo}');")
        self.__execute("SELECT last_insert_id();")
        return self.cursor.fetchone()[0]

    def place_order(self, customer_id, pizzas, side_dishes):
        self.__execute(
            f"INSERT INTO order_info(customer) VALUES ({customer_id});")
        self.__execute("SELECT last_insert_id();")
        order_id = self.cursor.fetchone()[0]

        for id in pizzas:
            self.__execute(
                f"INSERT INTO order_to_pizza(order_info, pizza) VALUES ({order_id}, {id});")
            self.__execute(
                f"UPDATE customer SET accumulation = accumulation + 1 WHERE id = {customer_id}")
        for id in side_dishes:
            self.__execute(
                f"INSERT INTO order_to_side_dish(order_info, side_dish) VALUES ({order_id}, {id});")
        self.__execute(
            f"UPDATE order_info SET time = NOW() WHERE id = {order_id};")

        self.db.commit()
        return order_id

    def delete_order(self, order_id):
        self.__execute(
            f"DELETE FROM order_to_pizza WHERE order_info = {order_id};")
        self.__execute(
            f"DELETE FROM order_to_side_dish WHERE order_info = {order_id};")
        self.__execute(f"DELETE FROM order_info WHERE id = {order_id};")
        self.db.commit()

    def check_coupon(self, coupon_id):
        if (not self.exists('coupon', 'id', coupon_id)):
            return False
        self.__execute(f"SELECT status FROM coupon WHERE id = {coupon_id}")
        status = self.cursor.fetchone()[0]
        if (status == 1):
            return True
        else:
            return False

    def set_deliveryman_time(self, id):
        self.__execute(f"UPDATE deliveryman SET time = NOW() WHERE id = {id};")

    def delete_coupon(self, coupon_id):
        self.__execute(f"DELETE FROM coupon WHERE id = {coupon_id};")

    def send_coupon(self, coupon_id):
        self.__execute(f"UPDATE coupon SET status = 1 WHERE id = {coupon_id};")

    def print_pizza(self, pizza_id):
        pizza = self.get_pizza(pizza_id)
        print("  - P" + str(pizza_id) + ": " +
              pizza["name"].title() + " " + self.is_vegan(pizza["name"]))
        price = 0
        for ingredient_name in pizza["ingredients"]:
            ingredient = self.get_ingredient(ingredient_name)
            price += ingredient["price"]*1.4
            print("    - " + ingredient["name"] + " : €" +
                  str("%.2f" % (ingredient["price"]*1.4)))
        print("    Price: €" + str("%.2f" %
              (price*1.09)) + " (incl. 9% VAT)\n")

    def print_side_dish(self, side_dish_id):
        side_dish = self.get_side_dish(side_dish_id)
        print("  - D" + str(side_dish_id) + ": " + side_dish["name"])
        print("    Price: €" + str("%.2f" %
              side_dish["price"]) + " (incl. 9% VAT)\n")

    # "private" function, executes sql command
    # replaces newlines and tabs with spaces
    # can run many commands at once, if they are separated with a ";"
    # if "verbose" is set to true it will print the command before running it, pretty useful for debugging
    def __execute(self, command):
        for line in command.replace("\n", " ").replace("\t", " ").split(";"):
            if (len(line) == 0):
                continue
            try:
                if verbose:
                    print("RUNNING: " + line)
                self.cursor.execute(line)
                self.db.commit()
            except sql.Error as error:
                print("ERROR: " + str(error))

    # "private" function, check if the "pizza" database exists
    def __sql_database_exists(self):
        self.__execute("SHOW DATABASES LIKE 'pizza';")
        return self.cursor.fetchone() != None

    # "private" function, creates the "pizza" database
    def __create_sql_database(self):
        self.__execute("CREATE DATABASE pizza;")
        self.__execute("USE pizza;")
        self.__execute(open("database_creation_command.sql", "r").read())

    # "private" function, destroys the "pizza" database
    def __destroy_sql_database(self): self.__execute("DROP DATABASE pizza;")

    # "private" function, inserts all the samples from "database_population_command.sql"
    def __populate_sql_database(self): self.__execute(
        open("database_population_command.sql", "r").read())


# for testing purposes (this will reset the database to the initial state)
if __name__ == "__main__":
    db = PizzaDatabase()
    db.reset()
