# ==========================================================
# Zeus Shop VPN PRO
# database.py
# Part 1/5
# ==========================================================


import sqlite3
from datetime import datetime



DB_NAME = "zeus.db"





# ==========================================================
# Database Connection
# ==========================================================


def get_db():

    return sqlite3.connect(
        DB_NAME
    )






# ==========================================================
# Init Database
# ==========================================================


def init_db():

    db = get_db()

    cursor = db.cursor()



    # Users

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users
        (
            id INTEGER PRIMARY KEY,
            username TEXT,
            created TEXT
        )
        """
    )



    # Orders

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            volume TEXT,
            days INTEGER,
            price INTEGER,
            status TEXT,
            created TEXT
        )
        """
    )



    # Receipts

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS receipts
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            order_id INTEGER,
            file_id TEXT,
            created TEXT
        )
        """
    )



    # Services

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS services
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            subscription_url TEXT,
            volume TEXT,
            days INTEGER,
            created TEXT
        )
        """
    )



    db.commit()

    db.close()



    print(
        "✅ Database Initialized"
    )
    # ==========================================================
# Users
# Part 2/5
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
# Get User
# ==========================================================


def get_user(

    user_id

):


    db = get_db()

    db.row_factory = sqlite3.Row


    cursor = db.cursor()



    cursor.execute(

        """
        SELECT *

        FROM users

        WHERE id=?

        """,

        (

            user_id,

        )

    )



    user = cursor.fetchone()



    db.close()



    return user
    # ==========================================================
# Orders
# Part 3/5
# ==========================================================



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
# Pending Orders
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
    # ==========================================================
# Receipts
# Part 4/5
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





    # گرفتن آخرین سفارش کاربر

    cursor.execute(

        """
        SELECT id

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





    order_id = None



    if order:


        order_id = order[0]







    cursor.execute(

        """
        INSERT INTO receipts
        (
            user_id,
            order_id,
            file_id,
            created
        )

        VALUES
        (?,?,?,?)

        """,

        (

            user_id,

            order_id,

            file_id,

            datetime.now().isoformat()

        )

    )



    db.commit()

    db.close()





    return True







# ==========================================================
# Get Receipt
# ==========================================================


def get_receipt(

    user_id

):


    db = get_db()

    db.row_factory = sqlite3.Row


    cursor = db.cursor()



    cursor.execute(

        """
        SELECT *

        FROM receipts

        WHERE user_id=?

        ORDER BY id DESC

        LIMIT 1

        """,

        (

            user_id,

        )

    )



    receipt = cursor.fetchone()



    db.close()



    return receipt
    # ==========================================================
# Services + Stats
# Part 5/5
# ==========================================================



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



    return True







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
# Statistics
# ==========================================================


def get_stats
