from audioop import add
from threading import Thread
from time import sleep
#import readline # importing this lets you use arrow keys and other stuff in input() 

import database

doc = """
available commands: available, order, reset, help, quit

- available
  Prints available pizzas, drinks and desserts
- order
  Place a new order.
  format:  order item_1_name item_1_count item_2_name item_2_count ... item_n_name item_n_count
  example: order margarita 2 orange_juice 2 cheese_cake 1
- reset
  Rest the database to the initial state
- help
  Show this message.
- quit
  Quite the app.
"""

db = database.PizzaDatabase()
running = False # the input and system threads will stop whenever this is set to false

# This thread will get orders from the terminal
def input_thread_fn():
	global db, running # this is a threaded function, so this is needed, idk why

	while running:
		input_str = input("Enter command (\"help\" for available commands)\n > ").strip()
		
		command = input_str.split(" ", 1)[0].lower()
		args =  input_str.split(" ")[1:] if len(input_str.split(" ", 1)) > 1 else []

		match command:
			case "menu": # TODO: If we can use ID to order that would be more convinient.
				print("- Pizza")
				for pizza_name in db.get_all_pizza_names():
					pizza = db.get_pizza(pizza_name)
					print("  - " + pizza["name"].title() + " " + db.is_vegan(pizza["name"]))
					price = 0
					for ingredient_name in pizza["ingredients"]:
						ingredient = db.get_ingredient(ingredient_name)
						price += ingredient["price"]*1.4
						print("    - " + ingredient["name"] + " : €" + str("%.2f" % (ingredient["price"]*1.4)))
					print("    Price: €" + str("%.2f" % (price*1.09)) + " (incl. 9% VAT)\n")
				print("- Drinks & Deserts")
				dd = db.get_all_sidedishes()
				for name in dd:
					print("  - "+name.title())
					print("    Price: €" + str("%.2f" % (dd[name]*1.09)) + " (incl. 9% VAT)\n")
			case "order":
				orders = order(db) # TODO: order in database
				set_order(db) # TODO: commit in database, set time, print order infos.
				cusID = set_cus_info(db)
			case "reset":
				print("Resting database...")
				db.reset()
				print("done")
			case "help": print(doc)
			case "quit": running = False
			case _: print("Unknown command \"" + command + "\"")

# This thread will take care of sending out the deliverymen and other non-input stuff
def system_thread_fn():
	global db, running # this is a threaded function, so this is needed, idk why

	while running:
		sleep(1) # only check for updates every second
		# TODO: implement

#Setting customer information without any checking
def set_cus_info(db):
	hasID = input("Do you have an customer ID? (y/n) > ").strip().lower()
	if hasID == 'y':
		id = input("Your customer ID > ").strip()
		info = db.get_cus_info(id)
		if info != None:
			print(f"Your name: {info[1]}, address: {info[2]}, postcode: {info[3]}, phone number:{info[4]}.")
			print("Login success!")
		else:
			print("ID does not exist. Please create a new one.")
	name = input("Your name > ").strip()
	address = input("Your address > ").strip()
	postcode = input("Postcode > ").strip()
	phoneNo = input("Your phone number > ").strip()
	id = db.add_customer(name,address,postcode,phoneNo)
	return id

def order(db):
	pizza_names = []
	sidedish_names = []
	while(True):
		command = input("Pizza, Desert & Drink, or Finishing ordering? (p/d/f) > ").strip().lower()
		match command:
			case "p":
				name = input("Enter pizza name > ").strip().lower()
				if db.is_exist(table = 'pizza', col = 'name', str = name):
					pizza_names.append(name)
				else:
					print("Pizza does not exist.")
			case "d":
				name = input("Enter desert or drink name > ").strip().lower()
				if db.is_exist(table = 'side_dish', col = 'name', str = name):
					sidedish_names.append(name)
				else:
					print("Desert or Drink does not exist.")
			case "f":
				if(len(pizza_names) > 0):
					break
				else:
					print("You have to order at least one pizza.")
	print(pizza_names)
	print(sidedish_names)
	return [pizza_names,sidedish_names]

def set_order(db):
	pass

if __name__ == "__main__":
	print("Starting app")

	input_thread = Thread(target = input_thread_fn)
	system_thread = Thread(target = system_thread_fn)

	running = True

	input_thread.start()
	system_thread.start()

	input_thread.join()
	system_thread.join()

	print("Exiting app")
