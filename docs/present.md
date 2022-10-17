# Presentation Content:  

## The choices we’ve made:  
+ Database API: **pymysql**  
+ Programming paradigm: **OOP**  
+ Database system: **MySQL**  

## The database we created:
Run in MySQL:
+ `use pizza;`
+ `show tables;`
+ `DESC pizza; DESC ingredient; DESC pizza_to_ingredient; DESC side_dish; DESC customer; DESC deliveryman; DESC order_info; DESC order_to_pizza; DESC order_to_side_dish; DESC coupon;`
+ `SELECT * FROM pizza;`
+ Pizzas information: `SELECT * FROM pizza JOIN pizza_to_ingredient ON pizza.id = pizza_to_ingredient.pizza JOIN ingredient ON ingredient.id = pizza_to_ingredient.ingredient;`

## Our program's functionality:
### `menu`: Prints available pizzas, drinks and desserts
+ Show at least 10 pizzas with 10 ingredients, 4 drinks and 2 deserts.
+ Show pizzas with their ingredients, and why it is vegetarian(`is_pizza_vegan()` in `database.py`)
+ Show how we calculate price: ingridients' prices * 1.4 * 1.09 (tax) (`print_pizza()` in `database.py`)

### `order [items]`: Place a new order. Add items splitted by a single space.
+ Order pizza, drink and desert
+ Store customer's information
+ Show comfirmation with the **products** ordered and the **estimated delivery time**
+ Show in MySQL: `SELECT * FROM customer;` (accumulation: total pizza number)
+ Place another order to let customer has more than 10 pizzas
+ show in MySQL: `SELECT * FROM customer;SELECT * FROM coupon;` (accumulation minored 10, coupon is sent)
+ Place another order with coupon, emphasize price
+ show in MySQL: `SELECT * FROM customer;SELECT * FROM coupon;` (accumulation increased, coupon is deleted after being used)

### `cancel [order id]`: Cancel existing orders.
+ Show in MySQL:  `SELECT * FROM order_info;` (time: when was the order placed)
+ Cancel an order that was placed five minutes ago
+ Cancel an order within five minutes

### `delivery`: Check all deliverymen's status.
+ Show in MySQL: `SELECT * FROM deliveryman;`
+ Postcode: match the fist 4 digit with customer's postcode
+ Run command `delivery`. 
  + (will be available at xxx): When a pizza is ordered, pizza will be cooked for 10 mins. If a delivery employee is available/will be available in this 10 mins, his time will be blocked after 20 mins after cooking time. Which is 30 mins after order is placed in total.
  + If there's no available delivery man for now, we will find the fastest one and block his time. The waiting time is added in **estimated delivery time** of the order.
+ Place an order out of available area: A delivery person cannot deliver outside the area which is not assigned to them
+ `setup_delivery()` in `main.py`