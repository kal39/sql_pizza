from email.policy import default
from threading import Thread
from time import sleep

import initialize

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

running = False # the input and system threads will stop whenever this is set to false

# This thread will get orders from the terminal
def input_thread_fn():
	global running

	while running:
		input_str = input("Enter command (\"help\" for available commands)\n > ").strip()
		
		command = input_str.split(" ", 1)[0]
		args =  input_str.split(" ")[1:] if len(input_str.split(" ", 1)) > 1 else []

		print("command: " + command + ", args: " + str(args))

		match command:
			case "pass": pass # TODO: implement
			case "order": pass # TODO: implement
			case "reset":
				print("Resting database... ", end="")
				initialize.init()
				print("done")
			case "help": print(doc)
			case "quit": running = False
			case _: print("Unknown command \"" + command + "\"")

# This thread will take care of sending out the deliverymen and other non-input stuff
def system_thread_fn():
	global running
	
	while running:
		sleep(1) # only check for updates every second

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
