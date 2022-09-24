'''
Before the first time you run this, run these in mysql:

CREATE USER tom IDENTIFIED BY '1243';
GRANT ALL PRIVILEGES ON pizza.* to 'tom'@'%';
FLUSH PRIVILEGES;

You can check the structure of any tables by using in mysql:
DESC table_name;
Because I don't know why it cannot be shown in termina :X
'''
import pymysql

def create_tables(cursor):
    create_pizza = """CREATE TABLE pizza(
        pid INT PRIMARY KEY AUTO_INCREMENT,
        pname VARCHAR(50) NOT NULL UNIQUE);"""
    cursor.execute(create_pizza)

    create_ingre = """CREATE TABLE ingredient(
        iid INT PRIMARY KEY AUTO_INCREMENT,
        iname VARCHAR(30) NOT NULL UNIQUE,
        category INT,
        price FLOAT NOT NULL);"""
    cursor.execute(create_ingre) # Category: 0 - veg, 1 -meat, 2 - seafood. In the future we only need to sum up to check if a pizza is vegan.

    create_p2i = """CREATE TABLE makepizza(
        pid INT,
        iid INT,
        FOREIGN KEY(pid) REFERENCES pizza(pid),
        FOREIGN KEY(iid) REFERENCES ingredient(iid));"""
    cursor.execute(create_p2i)

    create_food = """CREATE TABLE otherfood(
        fid INT PRIMARY KEY AUTO_INCREMENT,
        fname VARCHAR(50) NOT NULL UNIQUE,
        price FLOAT NOT NULL);"""
    cursor.execute(create_food)

    create_customer = """CREATE TABLE customer(
        cid INT PRIMARY KEY AUTO_INCREMENT,
        cname VARCHAR(50),
        address VARCHAR(128) NOT NULL,
        postcode VARCHAR(6) NOT NULL,
        phoneno VARCHAR(12));"""
    cursor.execute(create_customer)

    create_deliver = """CREATE TABLE deliveryman(
        did INT PRIMARY KEY AUTO_INCREMENT,
        dname VARCHAR(50),
        postcode VARCHAR(6) NOT NULL,
        time DATETIME);"""
    cursor.execute(create_deliver)

    # When using 'order' as name, it occured an error. I guess 'order' is a keyword somehow
    create_order = """CREATE TABLE orderInfo(
        oid INT PRIMARY KEY AUTO_INCREMENT,
        cid INT NOT NULL,
        time DATETIME,
        FOREIGN KEY (cid) REFERENCES customer(cid));"""
    cursor.execute(create_order)

    create_o2p = """CREATE TABLE orderpizza(
        oid INT NOT NULL,
        pid INT NOT NULL,
        FOREIGN KEY(pid) REFERENCES pizza(pid),
        FOREIGN KEY(oid) REFERENCES orderInfo(oid));"""
    cursor.execute(create_o2p)

    create_o2f = """CREATE TABLE orderfood(
        oid INT NOT NULL,
        fid INT NOT NULL,
        FOREIGN KEY(fid) REFERENCES otherfood(fid),
        FOREIGN KEY(oid) REFERENCES orderInfo(oid));"""
    cursor.execute(create_o2f)

    create_coupon = """CREATE TABLE coupon(
        couponid INT PRIMARY KEY AUTO_INCREMENT,
        status INT DEFAULT 0);"""
    cursor.execute(create_coupon)

def insert_samples(cursor):
    # These samples are copied from Domino
    # Insert some pizzas
    cursor.execute("INSERT INTO pizza(pname) values ('Perfect Pepperoni');")
    cursor.execute("INSERT INTO pizza(pname) values ('Margaritha');")
    cursor.execute("INSERT INTO pizza(pname) values ('Funghi');")
    cursor.execute("INSERT INTO pizza(pname) values ('Ham');")
    cursor.execute("INSERT INTO pizza(pname) values ('Salami');")
    cursor.execute("INSERT INTO pizza(pname) values ('Vegan Funghi');")

    # Insert some ingredients
    cursor.execute("INSERT INTO ingredient(iname, category,price) values ('Mozzarella',1,1.25);")
    cursor.execute("INSERT INTO ingredient(iname, category,price) values ('Pepperoni',1,1.25);")
    cursor.execute("INSERT INTO ingredient(iname, category,price) values ('Pizza Seasoning',0,0);")
    cursor.execute("INSERT INTO ingredient(iname, category,price) values ('Mushroom',0,1.25);")
    cursor.execute("INSERT INTO ingredient(iname, category,price) values ('Ham',0,1.25);")
    cursor.execute("INSERT INTO ingredient(iname, category,price) values ('Salami',0,1.25);")
    cursor.execute("INSERT INTO ingredient(iname, category,price) values ('Vegan Cheese',0,2);")


    # Insert some makepizzas
    cursor.execute("INSERT INTO makepizza(pid, iid) values(1,1)")
    cursor.execute("INSERT INTO makepizza(pid, iid) values(1,2)")
    cursor.execute("INSERT INTO makepizza(pid, iid) values(2,1)")
    cursor.execute("INSERT INTO makepizza(pid, iid) values(2,3)")
    cursor.execute("INSERT INTO makepizza(pid, iid) values(3,1)")
    cursor.execute("INSERT INTO makepizza(pid, iid) values(3,4)")
    cursor.execute("INSERT INTO makepizza(pid, iid) values(4,1)")
    cursor.execute("INSERT INTO makepizza(pid, iid) values(4,5)")
    cursor.execute("INSERT INTO makepizza(pid, iid) values(5,1)")
    cursor.execute("INSERT INTO makepizza(pid, iid) values(5,6)")
    cursor.execute("INSERT INTO makepizza(pid, iid) values(6,4)")
    cursor.execute("INSERT INTO makepizza(pid, iid) values(6,3)")
    cursor.execute("INSERT INTO makepizza(pid, iid) values(6,7)")
    # Execute this in mysql to see the complete price chart with names:
    # SELECT p.pid, p.pname, i.iid, i.iname, i.price FROM pizza p JOIN makepizza m ON p.pid = m.pid JOIN ingredient i ON i.iid = m.iid ORDER BY pid;

    # Insert some other foods
    cursor.execute("INSERT INTO otherfood(fname, price) values ('Thick Shake Cherry',4.75);")
    cursor.execute("INSERT INTO otherfood(fname, price) values ('Thick Shake Banana',4.75);")
    cursor.execute("INSERT INTO otherfood(fname, price) values ('Coco Churros',3.95);")
    cursor.execute("INSERT INTO otherfood(fname, price) values ('Dutch Pancake',2.99);")

    #Insert a customer
    cursor.execute("INSERT INTO customer(cname,address,postcode,phoneno) values ('Jerry','PHS1','6229EN','123456789');")

    #Insert a deliveryman
    cursor.execute("INSERT INTO deliveryman(dname, postcode) values ('Tom','6229EN');")

db = pymysql.connect(host = 'localhost', user='tom', password='1243')
cursor = db.cursor()
cursor.execute('DROP DATABASE IF EXISTS pizza;')
cursor.execute('CREATE DATABASE pizza;')
cursor.execute('USE pizza;')

create_tables(cursor)
try:
    insert_samples(cursor)
    db.commit()
except pymysql.Error as e:
    print(e)
    db.rollback()
 
db.close()