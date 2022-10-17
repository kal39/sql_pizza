'''
Before the first time you run this, please replace user and password with your own database's user and password, and run this file.
'''

import pymysql as sql
import datetime

verbose = False  # if this is true PizzaDatabase will print out every sql command before executing it, useful for debugging

class PizzaDatabase:
    # constructor, connects to database "pizza" if it id_exists; if not it will create and initialise it
    def __init__(self):
        self.db = sql.connect(host="localhost", user="tom", password="1243")
        self.cursor = self.db.cursor()

        if not self.__sql_database_id_exists():
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
    
    # returns a list of all ids
    def get_ids(self, table):
        self.__execute(f"SELECT id FROM {table} ORDER BY id;")
        return [i[0] for i in self.cursor.fetchall()]

    def get_pizza(self, id):
        self.__execute(f"SELECT pizza.name, ingredient.id FROM ingredient JOIN pizza_to_ingredient ON ingredient.id = pizza_to_ingredient.ingredient JOIN pizza ON pizza.id = pizza_to_ingredient.pizza WHERE pizza.id = '{id}';")
        info = self.cursor.fetchall()
        return {"name": info[0][0], "ingredients": [p[1] for p in info]}

    def get_ingredient(self, id):
        self.__execute("SELECT name, category, price FROM ingredient WHERE id = '" + str(id) + "';")
        ingredient = self.cursor.fetchone()
        return {"name": ingredient[0], "category": ingredient[1], "price": ingredient[2]}

    def get_side_dish(self, id):
        self.__execute(f"SELECT name, price FROM side_dish WHERE id= {id};")
        side_dish = self.cursor.fetchone()
        return {"name": side_dish[0], "price": side_dish[1]}

    def get_customer(self, id):
        if (not self.id_exists('customer', id)): return None
        self.__execute(f"SELECT name, address, postcode, phone_number FROM customer WHERE id = '{id}';")
        customer = self.cursor.fetchone()
        return {"name": customer[0], "address": customer[1], "postcode": customer[2], "phone_number": customer[3]}

    def get_order(self, id):
        if (not self.id_exists('order_info', id)): return None
        self.__execute(f"SELECT customer, time FROM order_info WHERE id = '{id}';")
        order = self.cursor.fetchone()
        return {"customer": order[0], "time": order[1]}

    def get_deliveryman(self, id):
        if (not self.id_exists('deliveryman', id)): return None
        self.__execute(f"SELECT name, postcode, time FROM deliveryman WHERE id = '{id}';")
        deliveryman = self.cursor.fetchone()
        return {"name": deliveryman[0], "postcode": deliveryman[1], "time": deliveryman[2]}
    
    def get_coupon(self, customer_id):
        self.__execute(f"SELECT accumulation FROM customer WHERE id = {customer_id};")
        pizza_number = self.cursor.fetchone()[0]
        if (pizza_number >= 10):
            try:
                self.cursor.execute(f"UPDATE customer SET accumulation = accumulation - 10 WHERE id = {customer_id}")
                self.cursor.execute("INSERT INTO coupon() VALUES();")
                self.db.commit()
                self.__execute("SELECT last_insert_id();")
                return self.cursor.fetchone()[0]
            except sql.Error as error:
                self.db.rollback()
                print("ERROR in getting coupon: " + str(error))
                return -1
        else: return -1

    def get_order_time(self, order_id):
        if (not self.id_exists('order_info', order_id)):
            print("Order does not exist.")
            return
        self.__execute(f"SELECT time FROM order_info WHERE id = {order_id};")
        return self.cursor.fetchone()[0]

    def is_pizza_vegan(self, pizza_name):
        '''
        This function shows how we tag if a pizza is vegetarian or not.

        Args:
            pizza_name: The name of pizza we want to tag.
        
        Returns:
            If it is vagetarian, it will return a tag to add after the pizza's name in menu.
        '''

        self.__execute(f"SELECT ingredient.category FROM ingredient JOIN pizza_to_ingredient ON ingredient.id = pizza_to_ingredient.ingredient JOIN pizza ON pizza.id = pizza_to_ingredient.pizza WHERE pizza.name = '" + pizza_name + "';")
        category = [c[0] for c in self.cursor.fetchall()]
        for each in category:
            if each != 'VEGETARIAN': return ""
        return '(VEGETARIAN)'

    def exists(self, table, col, str):
        self.__execute(f"SELECT {col} FROM {table} WHERE {col} = '{str}' LIMIT 1;")
        return self.cursor.fetchone() != None

    def id_exists(self, table, str): return self.exists(table, "id", str)

    def create_customer(self, customer_name, address, postcode, phoneNo):
        self.__execute(f"INSERT INTO customer(name, address, postcode, phone_number) values ('{customer_name}', '{address}', '{postcode}', '{phoneNo}');")
        self.__execute("SELECT last_insert_id();")
        return self.cursor.fetchone()[0]

    def place_order(self, customer_id, pizzas, side_dishes):
        try:
            self.cursor.execute(f"INSERT INTO order_info(customer) VALUES ({customer_id});")
            self.cursor.execute("SELECT last_insert_id();")
            order_id = self.cursor.fetchone()[0]

            for id in pizzas:
                self.cursor.execute(f"INSERT INTO order_to_pizza(order_info, pizza) VALUES ({order_id}, {id});")
                self.cursor.execute(f"UPDATE customer SET accumulation = accumulation + 1 WHERE id = {customer_id}")
            for id in side_dishes:
                self.cursor.execute(f"INSERT INTO order_to_side_dish(order_info, side_dish) VALUES ({order_id}, {id});")
            self.cursor.execute(f"UPDATE order_info SET time = NOW() WHERE id = {order_id};")
            self.db.commit()
            return order_id
        except sql.Error as error:
            self.db.rollback()
            print("ERROR in placing order: " + str(error))

    def delete_order(self, order_id):
        try:
            self.cursor.execute(f"DELETE FROM order_to_pizza WHERE order_info = {order_id};")
            self.cursor.execute(f"DELETE FROM order_to_side_dish WHERE order_info = {order_id};")
            self.cursor.execute(f"DELETE FROM order_info WHERE id = {order_id};")
            self.db.commit()
        except sql.Error as error:
            self.db.rollback()
            print("ERROR in canceling order: " + str(error))

    def check_coupon(self, coupon_id):
        if (not self.id_exists('coupon', coupon_id)): return False
        else: return True

    def set_deliveryman_time(self, id, time): self.__execute(f"UPDATE deliveryman SET time = '{time.strftime('%Y-%m-%d %H:%M:%S')}' WHERE id = {id};")

    def delete_coupon(self, coupon_id): self.__execute(f"DELETE FROM coupon WHERE id = {coupon_id};")

    def print_pizza(self, pizza_id):
        pizza = self.get_pizza(pizza_id)
        print("  - P" + str(pizza_id) + ": " + pizza["name"].title() + " " + self.is_pizza_vegan(pizza["name"]))
        price = 0
        for ingredient_name in pizza["ingredients"]:
            ingredient = self.get_ingredient(ingredient_name)
            price += ingredient["price"]*1.4
            print("    - " + ingredient["name"] + " : €" + str("%.2f" % (ingredient["price"]*1.4)))
        print("    Price: €" + str("%.2f" % (price*1.09)) + " (incl. 9% VAT)\n")

    def print_side_dish(self, side_dish_id):
        side_dish = self.get_side_dish(side_dish_id)
        print("  - D" + str(side_dish_id) + ": " + side_dish["name"].title())
        print("    Price: €" + str("%.2f" % side_dish["price"]) + " (incl. 9% VAT)\n")

    def print_order(self, pizzas, side_dishes):
        price = 0.
        print("- Pizza:")
        for pizza_id in pizzas:
            pizza = self.get_pizza(pizza_id)
            temp = price
            for ingredient_name in pizza["ingredients"]:
                ingredient = self.get_ingredient(ingredient_name)
                price += ingredient["price"]*1.4*1.09
            print(f"  - {pizza['name']}     €{'%.2f' % (price-temp)}")

        if(side_dishes != []):
            print("- Desert & Drink:")
            for side_id in side_dishes:
                side_dish = self.get_side_dish(side_id)
                print(f"  - {side_dish['name']}     €{'%.2f' % side_dish['price']}")
            price += self.get_side_dish(side_id)["price"]
        return price

    def print_deliverymen(self):
        ids = self.get_ids('deliveryman')
        for id in ids:
            deliveryman = self.get_deliveryman(id)
            print(f"{deliveryman['name']}:")
            print(f"  area: {deliveryman['postcode']}")
            if(deliveryman['time'] is None) or (datetime.datetime.now() > deliveryman['time']): print(f"  available: YES")
            else: print(f"  available: NO (will be available at {deliveryman['time']})")

    # "private" function, executes sql command
    # replaces newlines and tabs with spaces
    # can run many commands at once, if they are separated with a ";"
    # if "verbose" is set to true it will print the command before running it, pretty useful for debugging
    def __execute(self, command):
        for line in command.replace("\n", " ").replace("\t", " ").split(";"):
            if (len(line) == 0): continue
            try:
                if verbose: print("RUNNING: " + line)
                self.cursor.execute(line)
                self.db.commit()
            except sql.Error as error:
                print("ERROR: " + str(error))

    # "private" function, check if the "pizza" database id_exists
    def __sql_database_id_exists(self):
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
    def __populate_sql_database(self): self.__execute(open("database_population_command.sql", "r").read())


# for testing purposes (this will reset the database to the initial state)
if __name__ == "__main__":
    db = PizzaDatabase()
    db.reset()
    #db.place_order(1,[1,2,3],[2]) # For presentation
