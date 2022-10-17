# Databases - Course Project
Group 7:
Ankie - i6272224
Kai - i6275822


## If this is the first you run this program:
Step 1: go to `database.py`, find the first line of `__init__` function, and replace `user` and `password` with your own user and password of your local 'mysql'.  
Step 2: run `database.py`. If you run it in terminal, you can use `python database.py`.  
***Warning: if you have a database called 'pizza', running this will cover your 'pizza' database.***  

## To use the program
Run `python main.py` in terminal.  
Available commands:
- `menu`  
  Prints available pizzas, drinks and desserts  
  Example: `- P1: Perfect Pepperoni`
  `P1` is id that you use to order.
- `order item1 item2 ...`  
  Place a new order. Add items by their id, and splitting the, by a single space.  
  Example: `order p1 p2 p3 d2`  
- `cancel order_id1 order_id2 ...`  
  Cancel existing orders.  
  Example: `cancel 1 2`  
- `status order_id1 order_id2 ...`
  Check the status of orders;
  Example: `status 1 3`
- `delivery`  
  Check all deliverymen's status.  
- `reset`  
  Rest the database to the initial state  
- `help`  
  Show this message.  
- `quit`  
  Quit the app.  

## Diagrams and other documents:
### [ER schema](docs/ERschema.pdf)
### [ER diagram](docs/ERdiagram.pdf) 
### [schema/table structure](docs/schema.pdf)  
### [presentation video](docs/video_present.mp4)
**This video only shows the core part of our project. For more detail please take a look of:**
### [detailed presentation in text](docs/present.md)  
If you don't know how to read .md file:  
Visit to our GitHub repository: https://github.com/kal39/sql_pizza


