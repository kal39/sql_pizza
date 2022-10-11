from threading import Thread
from time import sleep
#import readline # importing this lets you use arrow keys and other stuff in input() # Not for Windows

import database
import datetime

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
				pizzas = db.get_all_pizzas()
				for pizza_id in pizzas:
					show_pizza(db, pizza_id)
				print("- Drinks & Deserts")
				for each in db.get_all_sidedishes():
					show_sidedish(each)
			case "order":
				items = order(db)
				cus_ID = set_cus_info(db)
				order_id = place_order(db, items, cus_ID) # commit in database, set time 
				print("Your order id is:", order_id)
				show_order(db,items,1) # TODO: coupon
				arrive_time = (db.get_order_time(order_id) +datetime.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")
				print("Your order is expected to arrive around", arrive_time)# 10 mins making, 20 mins delivering
			case "cancel":
				cancel_order(db)
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
			return id
		else:
			print("ID does not exist. Please create a new one.")
	name = input("Your name > ").strip()
	address = input("Your address > ").strip()
	postcode = input("Postcode > ").strip()
	phoneNo = input("Your phone number > ").strip()
	id = db.add_customer(name,address,postcode,phoneNo)
	return id

# Order from terminal
def order(db):
	pizza_IDs = []
	sidedish_IDs = []
	while(True):
		o = input("Enter food id, or 'f' to finish ordering > ").strip().lower()
		if o[0] == 'p':
			if db.is_exist(table = 'pizza',col = 'id', str = o[1:]):
				pizza_IDs.append(o[1:])
				show_pizza(db,pizza_id = o[1:])
				print("Added in order.\n")
			else:
				print("Pizza does not exist.")

		elif o[0] == 'd':
			if db.is_exist(table = 'side_dish',col = 'id', str = o[1:]):
				sidedish_IDs.append(o[1:]) 
				show_sidedish(db.get_sidedish(o[1:]))
				print("Added in order.\n")
			else:
				print("Drink or Desert does not exist.")
				
		elif o[0] == 'f':
			if(len(pizza_IDs) > 0):
				break
			else:
				print("You have to order at least one pizza.")
		else:
			print("Invalid input. Please try again.")
	return [pizza_IDs,sidedish_IDs]

# update in database
def place_order(db, orders, cus_id):
	if len(orders) < 1:
		print("You haven't order anything. Please use 'order' to order.")
	else:
		order_id = db.create_order(cus_id)
		if db.set_order(orders,order_id):
			print("Ordered successfully. \n")
			return order_id

def cancel_order(db):
	order_id = input("Enter your order ID > ")
	if db.is_exist(table = 'order_info',col = 'id', str =order_id):
		if((datetime.datetime.now() + datetime.timedelta(minutes=-5)) > db.get_order_time(order_id)):
			print("You CANNOT cancel because your order is placed for more than 5 minuts.")
		else:
			db.delete_order(order_id)
			print("Your order is canceled!")
	else:
		print("Order doesn't exist. Please try again.")

def show_pizza(db, pizza_id):
	pizza = db.get_pizza_info(pizza_id)
	print("  - P" + str(pizza_id) + ": "+pizza["name"].title() + " " + db.is_vegan(pizza["name"]))
	price = 0
	for ingredient_name in pizza["ingredients"]:
		ingredient = db.get_ingredient(ingredient_name)
		price += ingredient["price"]*1.4
		print("    - " + ingredient["name"] + " : €" + str("%.2f" % (ingredient["price"]*1.4)))
	print("    Price: €" + str("%.2f" % (price*1.09)) + " (incl. 9% VAT)\n")
				
def show_sidedish(info):
	print("  - D"+ str(info[0]) + ": "+ info[1].title())
	print("    Price: €" + str("%.2f" % info[2]) + " (incl. 9% VAT)\n")

def show_order(db, items, discount):
	print("Your order detail: ")
	print("- Pizza:")
	for pizza_id in items[0]:
		show_pizza(db,pizza_id)
	print("- Desert & Drink:")
	for did in items[1]:
		show_sidedish(db.get_sidedish(did))
	print("Total price: €", db.get_total_price(items,discount))
	
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
