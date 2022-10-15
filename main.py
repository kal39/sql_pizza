from threading import Thread
from time import sleep

import database
import datetime

doc = """
available commands:
- menu
  Prints available pizzas, drinks and desserts
- order
  Place a new order.
- cancel
  Cancel an existing order
- reset
  Rest the database to the initial state
- help
  Show this message.
- quit
  Quite the app.
"""

db = database.PizzaDatabase()
running = False  # the input and system threads will stop whenever this is set to false

# This thread will get orders from the terminal
def input_thread_fn():
    global db, running  # this is a threaded function, so this is needed, idk why

    while running:
        input_str = input("Enter command (\"help\" for available commands)\n > ").strip().lower()

        command = input_str.split(" ", 1)[0]
        args = input_str.split(" ")[1:] if len(input_str.split(" ", 1)) > 1 else []

        match command:
            case "menu": # TODO: If we can use ID to order that would be more convenient.
                print("- Pizzas:")
                for pizza_id in db.get_all_pizza_ids(): db.print_pizza(pizza_id)
                print("- Drinks & Deserts:")
                for side_dish_id in db.get_all_side_dish_ids(): db.print_side_dish(side_dish_id)

            case "order":
                (pizzas, side_dishes) = parse_order(db, args)
                if pizzas == []: continue
                customer_id = setup_customer(db)
                order_id = db.place_order(customer_id, pizzas, side_dishes)

                print("Your order id is:", order_id)
                arrival_time = (db.get_order_time(order_id) + datetime.timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")
                print("Your order is expected to arrive at", arrival_time)

            case "cancel":
                for order in args: cancel_order(db, order)
            case "reset":
                print("Resting database...")
                db.reset()
                print("done")
            case "help": print(doc)
            case "quit": running = False
            case _: print("Unknown command \"" + command + "\"")

# This thread will take care of sending out the deliverymen and other non-input stuff
def system_thread_fn():
    global db, running  # this is a threaded function, so this is needed, idk why

    while running:
        order_ids = db.get_all_order_ids()
        for id in order_ids:
            order = db.get_order(id)
            if datetime.datetime.now() + datetime.timedelta(minutes=-10) > order["time"]: deliver_order(db, id)

        sleep(1)  # only check for updates every second

# takes in a list of ids and checks if they are all valid
# if valid, the ids are converted into ids usable directly in the database
def parse_order(db, ids):
    pizzas = []
    side_dishes = []

    for id in ids: 
        if id[0] == 'p' and db.exits('pizza', 'id', id[1:]): pizzas.append(id[1:])
        elif id[0] == 'd' and db.exits('side_dish', 'id', id[1:]): side_dishes.append(id[1:])
        else:
            print(f"invalid id '{id}'")
            return ([], [])

    if pizzas == []:
        print("order at least one pizza")
        return ([], [])

    print("Ordering:")

    for id in pizzas: db.print_pizza(id)
    for id in side_dishes: db.print_side_dish(id)

    return (pizzas, side_dishes)

def setup_customer(db):
    while(True): # loop until valid customer has been made  
        if input("Do you have an customer ID? (y/n) > ").strip().lower() == 'y':
            id = input("Your customer ID > ").strip()
            customer = db.get_customer(id)
            if customer != None:
                print(f"name: {customer['name']}, address: {customer['address']}, postcode: {customer['postcode']}, phone number: {customer['phone_number']}.")
                return id
            else:
                print("ID does not exist.")
                continue
        name = input("Name > ").strip()
        address = input("Address > ").strip()
        postcode = input("Postcode > ").strip()
        phone = input("Phone number > ").strip()
        return db.create_customer(name, address, postcode, phone)

def cancel_order(db, id):
    if db.exits("order_info", "id", id):
        if datetime.datetime.now() + datetime.timedelta(minutes=-5) > db.get_order_time(id):
            print(f"Cannot cancel order {id} because for more than 5 minutes have passed.")
        else:
            db.delete_order(id)
            print(f"Cancelled order {id}")
    else:
        print("Order doesn't exist. Please try again.")

def deliver_order(db, id):
    for deliveryman_id in db.get_all_deliverymen_ids():
        deliveryman = db.get_deliveryman(deliveryman_id)
        if deliveryman["time"] == None or datetime.datetime.now() + datetime.timedelta(minutes=-20) > deliveryman["time"]:
            print(f"{deliveryman['name']} is now delivering order {id}, it will arrive in 20 minutes")
            db.delete_order(id)
            db.set_deliveryman_time(id)
            return

def check_coupon(db):
    while (True):
        coupon = input("Enter your coupon. If no enter 'n' > ").strip().lower()
        if (coupon[0] == 'n'):
            return 1
        elif (db.check_coupon(coupon)):
            db.delete_coupon(coupon)
            return 0.9
        else:
            print("Invalid coupon. Please try again.")

def coupon(db, items):
    if len(items[0]) >= 10:
        coupon_id = db.get_coupon()
        print("You've ordered over 10 pizzas. Here's a coupon id:", coupon_id)
        print("You can use it for 10% \discount next time.")
        db.send_coupon(coupon_id)

if __name__ == "__main__":
    print("Starting app")

    input_thread = Thread(target=input_thread_fn)
    system_thread = Thread(target=system_thread_fn)

    running = True

    input_thread.start()
    system_thread.start()

    input_thread.join()
    system_thread.join()