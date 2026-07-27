# ==========================================================
# Zeus Shop VPN PRO
# database.py
# Part 1/8
# ==========================================================


import sqlite3
from datetime import datetime



DB_NAME = "zeus.db"





# ==========================================================
# Connection
# ==========================================================


def get_connection():

    return sqlite3.connect(

        DB_NAME

    )









# ==========================================================
# Initialize Database
# ==========================================================


def init_db():


    conn = get_connection()

    cursor = conn.cursor()





    # =========================
    # Users Table
    # =========================


    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER UNIQUE,

        username TEXT,

        created_at TEXT

    )

    """)







    # =========================
    # Orders Table
    # =========================


    cursor.execute("""

    CREATE TABLE IF NOT EXISTS orders (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        volume TEXT,

        days INTEGER,

        price INTEGER,

        status TEXT DEFAULT 'pending',

        created_at TEXT

    )

    """)







    # =========================
    # Receipts Table
    # =========================


    cursor.execute("""

    CREATE TABLE IF NOT EXISTS receipts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        file_id TEXT,

        created_at TEXT

    )

    """)







    # =========================
    # Services Table
    # =========================


    cursor.execute("""

    CREATE TABLE IF NOT EXISTS services (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        username TEXT,

        subscription_url TEXT,

        volume TEXT,

        days INTEGER,

        created_at TEXT

    )

    """)







    # =========================
    # Broadcast Table
    # =========================


    cursor.execute("""

    CREATE TABLE IF NOT EXISTS broadcasts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        message TEXT,

        success INTEGER,

        failed INTEGER,

        created_at TEXT

    )

    """)







    conn.commit()

    conn.close()
    # ==========================================================
# Users Management
# Part 2/8
# ==========================================================





# ==========================================================
# Add User
# ==========================================================


def add_user(

    user_id,

    username

):


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        INSERT OR IGNORE INTO users
        (
            user_id,
            username,
            created_at
        )

        VALUES (?, ?, ?)

        """,

        (

            user_id,

            username,

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        )

    )





    conn.commit()

    conn.close()







# ==========================================================
# Get User By ID
# ==========================================================


def get_user(

    user_id

):


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        SELECT *

        FROM users

        WHERE user_id = ?

        """,

        (

            user_id,

        )

    )





    user = cursor.fetchone()


    conn.close()





    if user:


        return {

            "id": user[0],

            "user_id": user[1],

            "username": user[2],

            "created_at": user[3]

        }





    return None







# ==========================================================
# Get All Users
# Used For Broadcast System
# ==========================================================


def get_all_users():


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        SELECT user_id, username

        FROM users

        """

    )





    rows = cursor.fetchall()


    conn.close()





    users = []





    for row in rows:


        users.append(

            {

                "user_id": row[0],

                "username": row[1]

            }

        )





    return users







# ==========================================================
# Count Users
# ==========================================================


def count_users():


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        SELECT COUNT(*)

        FROM users

        """

    )





    count = cursor.fetchone()[0]


    conn.close()





    return count
    # ==========================================================
# Orders Management
# Part 3/8
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


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        INSERT INTO orders
        (
            user_id,
            volume,
            days,
            price,
            status,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?)

        """,

        (

            user_id,

            volume,

            days,

            price,

            "pending",

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        )

    )





    order_id = cursor.lastrowid





    conn.commit()

    conn.close()





    return order_id







# ==========================================================
# Get Last User Order
# ==========================================================


def last_order(

    user_id

):


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        SELECT *

        FROM orders

        WHERE user_id = ?

        ORDER BY id DESC

        LIMIT 1

        """,

        (

            user_id,

        )

    )





    order = cursor.fetchone()


    conn.close()





    if order:


        return {

            "id": order[0],

            "user_id": order[1],

            "volume": order[2],

            "days": order[3],

            "price": order[4],

            "status": order[5],

            "created_at": order[6]

        }





    return None







# ==========================================================
# Get Order By ID
# ==========================================================


def get_order(

    order_id

):


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        SELECT *

        FROM orders

        WHERE id = ?

        """,

        (

            order_id,

        )

    )





    order = cursor.fetchone()


    conn.close()





    if order:


        return {

            "id": order[0],

            "user_id": order[1],

            "volume": order[2],

            "days": order[3],

            "price": order[4],

            "status": order[5],

            "created_at": order[6]

        }





    return None







# ==========================================================
# Get Pending Orders
# ==========================================================


def get_pending_orders():


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        SELECT *

        FROM orders

        WHERE status = 'pending'

        ORDER BY id DESC

        """

    )





    rows = cursor.fetchall()


    conn.close()





    orders = []





    for order in rows:


        orders.append(

            {

                "id": order[0],

                "user_id": order[1],

                "volume": order[2],

                "days": order[3],

                "price": order[4],

                "status": order[5],

                "created_at": order[6]

            }

        )





    return orders
    # ==========================================================
# Receipts Management
# Part 4/8
# ==========================================================





# ==========================================================
# Save Receipt
# ==========================================================


def save_receipt(

    user_id,

    file_id

):


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        INSERT INTO receipts
        (
            user_id,
            file_id,
            created_at
        )

        VALUES (?, ?, ?)

        """,

        (

            user_id,

            file_id,

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        )

    )





    conn.commit()

    conn.close()







# ==========================================================
# Get User Receipts
# ==========================================================


def get_user_receipts(

    user_id

):


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        SELECT *

        FROM receipts

        WHERE user_id = ?

        ORDER BY id DESC

        """,

        (

            user_id,

        )

    )





    rows = cursor.fetchall()


    conn.close()





    receipts = []





    for row in rows:


        receipts.append(

            {

                "id": row[0],

                "user_id": row[1],

                "file_id": row[2],

                "created_at": row[3]

            }

        )





    return receipts







# ==========================================================
# Get Last Receipt
# ==========================================================


def get_last_receipt(

    user_id

):


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        SELECT *

        FROM receipts

        WHERE user_id = ?

        ORDER BY id DESC

        LIMIT 1

        """,

        (

            user_id,

        )

    )





    receipt = cursor.fetchone()


    conn.close()





    if receipt:


        return {

            "id": receipt[0],

            "user_id": receipt[1],

            "file_id": receipt[2],

            "created_at": receipt[3]

        }





    return None
    # ==========================================================
# Services Management
# Part 5/8
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


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        INSERT INTO services
        (
            user_id,
            username,
            subscription_url,
            volume,
            days,
            created_at
        )

        VALUES (?, ?, ?, ?, ?, ?)

        """,

        (

            user_id,

            username,

            subscription_url,

            volume,

            days,

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        )

    )





    conn.commit()

    conn.close()







# ==========================================================
# Get User Service
# ==========================================================


def get_user_service(

    user_id

):


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        SELECT *

        FROM services

        WHERE user_id = ?

        ORDER BY id DESC

        LIMIT 1

        """,

        (

            user_id,

        )

    )





    service = cursor.fetchone()


    conn.close()





    if service:


        return {

            "id": service[0],

            "user_id": service[1],

            "username": service[2],

            "subscription_url": service[3],

            "volume": service[4],

            "days": service[5],

            "created_at": service[6]

        }





    return None







# ==========================================================
# Get All Services
# ==========================================================


def get_all_services():


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        SELECT *

        FROM services

        ORDER BY id DESC

        """

    )





    rows = cursor.fetchall()


    conn.close()





    services = []





    for service in rows:


        services.append(

            {

                "id": service[0],

                "user_id": service[1],

                "username": service[2],

                "subscription_url": service[3],

                "volume": service[4],

                "days": service[5],

                "created_at": service[6]

            }

        )





    return services
    # ==========================================================
# Order Status Management
# Part 6/8
# ==========================================================





# ==========================================================
# Update Order Status
# ==========================================================


def update_order_status(

    order_id,

    status

):


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        UPDATE orders

        SET status = ?

        WHERE id = ?

        """,

        (

            status,

            order_id

        )

    )





    conn.commit()

    conn.close()







# ==========================================================
# Get Orders By Status
# ==========================================================


def get_orders_by_status(

    status

):


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        SELECT *

        FROM orders

        WHERE status = ?

        ORDER BY id DESC

        """,

        (

            status,

        )

    )





    rows = cursor.fetchall()


    conn.close()





    orders = []





    for order in rows:


        orders.append(

            {

                "id": order[0],

                "user_id": order[1],

                "volume": order[2],

                "days": order[3],

                "price": order[4],

                "status": order[5],

                "created_at": order[6]

            }

        )





    return orders







# ==========================================================
# Count Orders By Status
# ==========================================================


def count_orders_status(

    status

):


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        SELECT COUNT(*)

        FROM orders
    # ==========================================================
# Statistics Management
# Part 7/8
# ==========================================================





# ==========================================================
# Get Bot Stats
# ==========================================================


def get_stats():


    conn = get_connection()

    cursor = conn.cursor()





    # تعداد کاربران

    cursor.execute(

        """
        SELECT COUNT(*)

        FROM users

        """

    )


    users = cursor.fetchone()[0]







    # تعداد سفارش‌ها

    cursor.execute(

        """
        SELECT COUNT(*)

        FROM orders

        """

    )


    orders = cursor.fetchone()[0]







    # تعداد سرویس‌ها

    cursor.execute(

        """
        SELECT COUNT(*)

        FROM services

        """

    )


    services = cursor.fetchone()[0]







    # درآمد کل پرداخت شده

    cursor.execute(

        """
        SELECT SUM(price)

        FROM orders

        WHERE status = 'paid'

        """

    )


    income = cursor.fetchone()[0]





    conn.close()





    if income is None:


        income = 0







    return {


        "users": users,


        "orders": orders,


        "services": services,


        "income": income


    }
    # ==========================================================
# Broadcast History Management
# Part 8/8
# ==========================================================





# ==========================================================
# Save Broadcast History
# ==========================================================


def save_broadcast_history(

    message,

    success,

    failed

):


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        INSERT INTO broadcasts
        (
            message,
            success,
            failed,
            created_at
        )

        VALUES (?, ?, ?, ?)

        """,

        (

            message,

            success,

            failed,

            datetime.now().strftime(

                "%Y-%m-%d %H:%M:%S"

            )

        )

    )





    conn.commit()

    conn.close()







# ==========================================================
# Get Broadcast History
# ==========================================================


def get_broadcast_history(

):


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        SELECT *

        FROM broadcasts

        ORDER BY id DESC

        LIMIT 20

        """

    )





    rows = cursor.fetchall()


    conn.close()





    history = []





    for item in rows:


        history.append(

            {

                "id": item[0],

                "message": item[1],

                "success": item[2],

                "failed": item[3],

                "created_at": item[4]

            }

        )





    return history







# ==========================================================
# Count Broadcasts
# ==========================================================


def count_broadcasts():


    conn = get_connection()

    cursor = conn.cursor()





    cursor.execute(

        """
        SELECT COUNT(*)

        FROM broadcasts

        """

    )





    count = cursor.fetchone()[0]


    conn.close()





    return count
