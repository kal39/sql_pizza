# Databases - Course Project

## If this is the first you run this program:
Step 1: go to `database.py`, find the first line of `__init__` function, and replace `user` and `password` with your own user and password of your local 'mysql'.  
Step 2: run `database.py`. If you run it in terminal, you can use `python database.py`.  
***Warning: if you have a database called 'pizza', running this will cover your 'pizza' database.***  

## Use the program
Run `python main.py` in terminal.  
Available commands:  
- `menu`  
  Prints available pizzas, drinks and desserts  
- `order item1 item2 ...`  
  Place a new order. Add items splitted by a single space.  
  Example: `order p1 p2 p3 d2`  
- `cancel order_id1 order_id2 ...`  
  Cancel an existing order.  
  Example: `cancel 1 2`  
- `delivery`  
  Check all deliverymen's status.  
- `reset`  
  Rest the database to the initial state  
- `help`  
  Show this message.  
- `quit`  
  Quit the app.  