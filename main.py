import database
import datetime
from sys import platform

if platform == "linux": import readline

doc = """
available commands:
- menu
  Prints available pizzas, drinks and desserts
- order item1 item2 ...
  Place a new order. Add items splitted by a single space.
- cancel order_id1 order_id2 ...
  Cancel an existing order.
- delivery
  Check all deliverymen's status.
- reset
  Rest the database to the initial state
- help
  Show this message.
- quit
  Quit the app.
"""

# takes in a list of ids and checks if they are all valid
# if valid, the ids are converted into ids usable directly in the database
def parse_order(db, ids):
    pizzas = []
    side_dishes = []

    for id in ids:
        if id[0] == 'p' and db.id_exists('pizza', id[1:]):
            pizzas.append(id[1:])
        elif id[0] == 'd' and db.id_exists('side_dish', id[1:]):
            side_dishes.append(id[1:])
        else:
            print(f"invalid id '{id}'")
            return ([], [])

    if pizzas == []:
        print("order at least one pizza")
        return ([], [])

    print("Ordering:")

    for id in pizzas:  db.print_pizza(id)
    for id in side_dishes: db.print_side_dish(id)

    return (pizzas, side_dishes)

def setup_customer(db):
    while (True):  # loop until valid customer has been made
        if input("Do you have an customer ID? (y/n) > ").strip().lower() == 'y':
            id = input("Your customer ID > ").strip()
            customer = db.get_customer(id)
            if customer != None:
                print(f"- Your information: name: {customer['name']}, address: {customer['address']}, postcode: {customer['postcode']}, phone number: {customer['phone_number']}.")
                return id
            else:
                print("ID does not exist.")
                continue
        while(True):
            name = input("Name > ").strip()
            address = input("Address > ").strip()
            postcode = input("Postcode > ").strip()
            phone = input("Phone number > ").strip()
            if(not postcode[:4].isdigit()): print("Invalid postcode. Please write postcode like 1234XX.")
            elif(not db.exists('deliveryman', 'postcode', postcode[:4])): print(f"Cannot deliver to postal code {postcode}. Please try another address.")
            else: break
        customer_id = db.create_customer(name, address, postcode, phone)
        print("- Registered successfully! Your customer id is", customer_id)
        return customer_id

def cancel_order(db, id):
    if db.id_exists("order_info", id):
        if datetime.datetime.now() + datetime.timedelta(minutes=-5) > db.get_order_time(id):
            print(f"Cannot cancel order {id} because for more than 5 minutes have passed.")
        else:
            db.delete_order(id)
            print(f"Cancelled order {id}")
    else:
        print("Order doesn't exist. Please try again.")

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

def coupon(db, customer_id):
    coupon_id = db.get_coupon(customer_id)
    if coupon_id != -1:
        print("- You've ordered more than 10 pizzas. Here's a coupon id:", coupon_id)
        print("- You can use it for 10% discount next time.")
        db.send_coupon(coupon_id)

# Since one of requirement is 'make sure that you show how you calculate the pizza prices', it's better to keep this.
def show_order(db, pizzas, side_dishes, discount):
    print("Your order detail: ")
    original = db.print_order(pizzas, side_dishes)
    print(f'- Total price: € {("%.2f" % (original * discount))} (original price: € {("%.2f" % original)})')

def setup_delivery(db, postcode):
    fastest_delivery = {"time": None, "id": None}
    cooking_time = datetime.datetime.now() + datetime.timedelta(minutes=10)

    # find the deliveryman available the earliest
    for deliveryman_id in db.get_ids('deliveryman'):
        deliveryman = db.get_deliveryman(deliveryman_id)
        if deliveryman["postcode"] == postcode:
            if deliveryman["time"] == None or deliveryman["time"] < cooking_time:  deliveryman["time"] = cooking_time

            if fastest_delivery["time"] == None or deliveryman["time"] < fastest_delivery["time"]:
                fastest_delivery["time"] = deliveryman["time"]
                fastest_delivery["id"] = deliveryman_id

    db.set_deliveryman_time(fastest_delivery["id"], fastest_delivery["time"] + datetime.timedelta(minutes=30))
    return fastest_delivery["time"]

# This thread will get orders from the terminal
if __name__ == "__main__":
    db = database.PizzaDatabase()

    while True:
        input_str = input("Enter command (\"help\" for available commands)\n > ").strip().lower()

        command = input_str.split(" ", 1)[0]
        args = input_str.split(" ")[1:] if len(input_str.split(" ", 1)) > 1 else []

        match command:
            case "menu":
                print("- Pizzas:")
                for pizza_id in db.get_ids('pizza'): db.print_pizza(pizza_id)
                print("- Drinks & Deserts:")
                for side_dish_id in db.get_ids('side_dish'): db.print_side_dish(side_dish_id)

            case "order":
                (pizzas, side_dishes) = parse_order(db, args)
                if pizzas == []:  continue
                customer_id = setup_customer(db)
                order_id = db.place_order(customer_id, pizzas, side_dishes)
                discount = check_coupon(db)
                print("+-----------------------------------------------------------+")
                print("- Your order id is:", order_id)
                show_order(db, pizzas, side_dishes, discount)
                print("+-----------------------------------------------------------+")
                coupon(db, customer_id)

                postcode = db.get_customer(customer_id)["postcode"][:4]
                delivery_start_time = setup_delivery(db, postcode)

                if delivery_start_time == None:
                    print(f"cannot deliver to postal code {postcode}. Please try another address.")
                    db.delete_order(order_id)
                else: print("- Your order will be out for delivery at", delivery_start_time)
            case "cancel":
                for order in args: cancel_order(db, order)
            case "reset":
                print("Resting database...")
                db.reset()
                print("done")
            case "delivery":  db.print_deliverymen()
            case "help": print(doc)
            case "quit": exit(0)
            case _: print("Unknown command \"" + command + "\"")