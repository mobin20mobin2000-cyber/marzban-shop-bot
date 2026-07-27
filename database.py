# ==========================================================
# Zeus Shop VPN PRO
# database.py
# Part 1/4
# ==========================================================


import sqlite3
from datetime import datetime



DB_NAME = "zeus.db"




def get_db():

    return sqlite3.connect(
        DB_NAME
    )





# ==========================================================
# Create Tables
# ==========================================================


def init_db():


    db = get_db()

    cursor = db.cursor()



    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY,

        username TEXT,

        created TEXT

    )

    """)




    cursor.execute("""

    CREATE TABLE IF NOT EXISTS orders (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        volume TEXT,

        days INTEGER,

        price INTEGER,

        status TEXT DEFAULT 'pending',

        created TEXT

    )

    """)




    cursor.execute("""

    CREATE TABLE IF NOT EXISTS services (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        username TEXT,

        subscription_url TEXT,

        volume TEXT,

        days INTEGER,

        created TEXT

    )

    """)




    cursor.execute("""

    CREATE TABLE IF NOT EXISTS receipts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        file_id TEXT,

        created TEXT

    )

    """)




    cursor.execute("""

    CREATE TABLE IF NOT EXISTS discounts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        code TEXT UNIQUE,

        percent INTEGER,

        active INTEGER DEFAULT 1

    )

    """)



    db.commit()

    db.close()
    # ==========================================================
# Users & Orders
# Part 2/4
# ==========================================================



# ==========================================================
# Add User
# ==========================================================


def add_user(

    user_id,

    username

):


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """
        INSERT OR IGNORE INTO users
        (
            id,
            username,
            created
        )

        VALUES
        (?,?,?)
        """,

        (

            user_id,

            username,

            datetime.now().isoformat()

        )

    )


    db.commit()

    db.close()







# ==========================================================
# Create Order
# ==========================================================


def create_order(

    user_id,

    volume,

    days,

    price

):


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        INSERT INTO orders

        (

            user_id,

            volume,

            days,

            price,

            status,

            created

        )


        VALUES

        (?,?,?,?,?,?)

        """,

        (

            user_id,

            volume,

            days,

            price,

            "pending",

            datetime.now().isoformat()

        )

    )



    order_id = cursor.lastrowid



    db.commit()

    db.close()



    return order_id







# ==========================================================
# Last Order
# ==========================================================


def last_order(

    user_id

):


    db = get_db()

    db.row_factory = sqlite3.Row

    cursor = db.cursor()



    cursor.execute(

        """

        SELECT *

        FROM orders

        WHERE user_id=?

        ORDER BY id DESC

        LIMIT 1

        """,

        (

            user_id,

        )

    )


    order = cursor.fetchone()



    db.close()



    return order







# ==========================================================
# Update Order Status
# ==========================================================


def update_order_status(

    order_id,

    status

):


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        UPDATE orders

        SET status=?

        WHERE id=?

        """,

        (

            status,

            order_id

        )

    )


    db.commit()

    db.close()
    # ==========================================================
# Receipts & Services
# Part 3/4
# ==========================================================



# ==========================================================
# Save Receipt
# ==========================================================


def save_receipt(

    user_id,

    file_id

):


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        INSERT INTO receipts

        (

            user_id,

            file_id,

            created

        )

        VALUES

        (?,?,?)

        """,

        (

            user_id,

            file_id,

            datetime.now().isoformat()

        )

    )



    db.commit()

    db.close()







# ==========================================================
# Save Service
# ==========================================================


def save_service(

    user_id,

    username,

    subscription_url,

    volume,

    days

):


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        INSERT INTO services

        (

            user_id,

            username,

            subscription_url,

            volume,

            days,

            created

        )


        VALUES

        (?,?,?,?,?,?)

        """,

        (

            user_id,

            username,

            subscription_url,

            volume,

            days,

            datetime.now().isoformat()

        )

    )



    db.commit()

    db.close()







# ==========================================================
# Get User Service
# ==========================================================


def get_user_service(

    user_id

):


    db = get_db()

    db.row_factory = sqlite3.Row

    cursor = db.cursor()



    cursor.execute(

        """

        SELECT *

        FROM services

        WHERE user_id=?

        ORDER BY id DESC

        LIMIT 1

        """,

        (

            user_id,

        )

    )



    service = cursor.fetchone()



    db.close()



    return service







# ==========================================================
# Get All Services
# ==========================================================


def get_services():


    db = get_db()

    db.row_factory = sqlite3.Row

    cursor = db.cursor()



    cursor.execute(

        """

        SELECT *

        FROM services

        ORDER BY id DESC

        """

    )



    services = cursor.fetchall()



    db.close()



    return services
    # ==========================================================
# Discounts & Statistics
# Part 4/4
# ==========================================================



# ==========================================================
# Add Discount Code
# ==========================================================


def add_discount(

    code,

    percent

):


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        INSERT OR REPLACE INTO discounts

        (

            code,

            percent,

            active

        )

        VALUES

        (?,?,?)

        """,

        (

            code.upper(),

            percent,

            1

        )

    )



    db.commit()

    db.close()







# ==========================================================
# Check Discount
# ==========================================================


def get_discount(

    code

):


    db = get_db()

    db.row_factory = sqlite3.Row

    cursor = db.cursor()



    cursor.execute(

        """

        SELECT *

        FROM discounts

        WHERE code=?

        AND active=1

        """,

        (

            code.upper(),

        )

    )



    discount = cursor.fetchone()



    db.close()



    return discount







# ==========================================================
# Disable Discount
# ==========================================================


def disable_discount(

    code

):


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        UPDATE discounts

        SET active=0

        WHERE code=?

        """,

        (

            code.upper(),

        )

    )


    db.commit()

    db.close()







# ==========================================================
# Statistics
# ==========================================================


def get_stats():


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        "SELECT COUNT(*) FROM users"

    )

    users = cursor.fetchone()[0]





    cursor.execute(

        "SELECT COUNT(*) FROM orders"

    )

    orders = cursor.fetchone()[0]





    cursor.execute(

        "SELECT COUNT(*) FROM services"

    )

    services = cursor.fetchone()[0]





    cursor.execute(

        """

        SELECT SUM(price)

        FROM orders

        WHERE status='paid'

        """

    )


    income = cursor.fetchone()[0]



    if income is None:

        income = 0





    db.close()



    return {


        "users":

        users,


        "orders":

        orders,


        "services":

        services,


        "income":

        income

    }







# ==========================================================
# Get Pending Orders
# ==========================================================


def get_pending_orders():


    db = get_db()

    db.row_factory = sqlite3.Row

    cursor = db.cursor()



    cursor.execute(

        """

        SELECT *

        FROM orders

        WHERE status='pending'

        ORDER BY id DESC

        """

    )



    orders = cursor.fetchall()



    db.close()



    return orders
