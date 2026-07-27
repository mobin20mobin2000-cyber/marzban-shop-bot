# ==========================================================
# Zeus Shop VPN PRO
# database.py
# Part 1/4
# ==========================================================

import sqlite3


DATABASE = "zeus.db"


# ==========================================================
# Database Connection
# ==========================================================

def get_db():

    db = sqlite3.connect(
        DATABASE
    )

    db.row_factory = sqlite3.Row

    return db



# ==========================================================
# Initialize Database
# ==========================================================

def init_db():

    db = get_db()

    cursor = db.cursor()


    # Users

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER UNIQUE,

        username TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # Orders

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        plan TEXT,

        volume INTEGER,

        days INTEGER,

        price INTEGER,

        status TEXT DEFAULT 'pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # Services

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        username TEXT,

        subscription_url TEXT,

        volume INTEGER,

        days INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # Receipts

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receipts(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        file_id TEXT,

        status TEXT DEFAULT 'pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # Support

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS support(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        message TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    db.commit()

    db.close()



# ==========================================================
# Users
# ==========================================================


def add_user(
    telegram_id,
    username=None
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        INSERT OR IGNORE INTO users
        (
            telegram_id,
            username
        )
        VALUES (?,?)
        """,
        (
            telegram_id,
            username
        )
    )


    db.commit()

    db.close()



def get_user(
    telegram_id
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE telegram_id=?
        """,
        (
            telegram_id,
        )
    )


    user = cursor.fetchone()

    db.close()


    return user



def users_count():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users
        """
    )


    count = cursor.fetchone()[0]


    db.close()


    return count
    # ==========================================================
# Orders
# Part 2/4
# ==========================================================


# ==========================================================
# Create Order
# ==========================================================

def create_order(
    telegram_id,
    plan,
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
            telegram_id,
            plan,
            volume,
            days,
            price
        )
        VALUES (?,?,?,?,?)
        """,
        (
            telegram_id,
            plan,
            volume,
            days,
            price
        )
    )


    db.commit()


    order_id = cursor.lastrowid


    db.close()


    return order_id



# ==========================================================
# Get Order By User
# ==========================================================

def get_order(
    telegram_id
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT *
        FROM orders
        WHERE telegram_id=?
        ORDER BY id DESC
        LIMIT 1
        """,
        (
            telegram_id,
        )
    )


    order = cursor.fetchone()


    db.close()


    return order



# ==========================================================
# Get Order By ID
# ==========================================================

def get_order_by_id(
    order_id
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT *
        FROM orders
        WHERE id=?
        """,
        (
            order_id,
        )
    )


    order = cursor.fetchone()


    db.close()


    return order



# ==========================================================
# Update Order Status
# ==========================================================

def update_order_status(
    telegram_id,
    status
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        UPDATE orders

        SET status=?

        WHERE telegram_id=?

        """,
        (
            status,
            telegram_id
        )
    )


    db.commit()

    db.close()



# ==========================================================
# Approve Payment
# ==========================================================

def approve_payment(
    telegram_id
):

    update_order_status(
        telegram_id,
        "approved"
    )



# ==========================================================
# Reject Payment
# ==========================================================

def reject_payment(
    telegram_id
):

    update_order_status(
        telegram_id,
        "rejected"
    )



# ==========================================================
# Pending Orders
# ==========================================================

def pending_orders():

    db = get_db()

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
# Approved Orders
# ==========================================================

def approved_orders():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT *

        FROM orders

        WHERE status='approved'

        ORDER BY id DESC
        """
    )


    orders = cursor.fetchall()


    db.close()


    return orders



# ==========================================================
# Delete Order
# ==========================================================

def delete_order(
    order_id
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        DELETE FROM orders

        WHERE id=?
        """,
        (
            order_id,
        )
    )


    db.commit()

    db.close()
    # ==========================================================
# Services
# Part 3/4
# ==========================================================


# ==========================================================
# Save Service
# ==========================================================

def save_service(
    telegram_id,
    username,
    subscription_url,
    volume,
    days
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        INSERT INTO subscriptions
        (
            telegram_id,
            username,
            subscription_url,
            volume,
            days
        )

        VALUES (?,?,?,?,?)

        """,
        (
            telegram_id,
            username,
            subscription_url,
            volume,
            days
        )
    )


    db.commit()

    db.close()



# ==========================================================
# Get User Service
# ==========================================================

def get_user_service(
    telegram_id
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT *

        FROM subscriptions

        WHERE telegram_id=?

        ORDER BY id DESC

        LIMIT 1

        """,
        (
            telegram_id,
        )
    )


    service = cursor.fetchone()


    db.close()


    return service



# ==========================================================
# All Services
# ==========================================================

def all_services():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT *

        FROM subscriptions

        ORDER BY id DESC

        """
    )


    services = cursor.fetchall()


    db.close()


    return services



# ==========================================================
# Service Count
# ==========================================================

def services_count():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)

        FROM subscriptions

        """
    )


    count = cursor.fetchone()[0]


    db.close()


    return count





# ==========================================================
# Receipts
# ==========================================================


def save_receipt(
    telegram_id,
    file_id
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        INSERT INTO receipts
        (
            telegram_id,
            file_id
        )

        VALUES (?,?)

        """,
        (
            telegram_id,
            file_id
        )
    )


    db.commit()

    db.close()



# ==========================================================
# Get Pending Receipts
# ==========================================================

def pending_receipts():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT *

        FROM receipts

        WHERE status='pending'

        ORDER BY id DESC

        """
    )


    receipts = cursor.fetchall()


    db.close()


    return receipts



# ==========================================================
# Update Receipt Status
# ==========================================================

def update_receipt_status(
    telegram_id,
    status
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        UPDATE receipts

        SET status=?

        WHERE telegram_id=?

        """,
        (
            status,
            telegram_id
        )
    )


    db.commit()

    db.close()





# ==========================================================
# Support
# ==========================================================


def save_support_message(
    telegram_id,
    message
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        INSERT INTO support
        (
            telegram_id,
            message
        )

        VALUES (?,?)

        """,
        (
            telegram_id,
            message
        )
    )


    db.commit()

    db.close()



# ==========================================================
# All Support Messages
# ==========================================================

def all_support_messages():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT *

        FROM support

        ORDER BY id DESC

        """
    )


    messages = cursor.fetchall()


    db.close()


    return messages
    # ==========================================================
# Statistics
# Part 4/4
# ==========================================================


# ==========================================================
# Count Today Users
# ==========================================================

def today_users_count():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)

        FROM users

        WHERE DATE(created_at)=DATE('now')

        """
    )


    count = cursor.fetchone()[0]


    db.close()


    return count



# ==========================================================
# Sales Count
# ==========================================================

def sales_count():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)

        FROM orders

        WHERE status='approved'

        """
    )


    count = cursor.fetchone()[0]


    db.close()


    return count



# ==========================================================
# Total Income
# ==========================================================

def total_income():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT SUM(price)

        FROM orders

        WHERE status='approved'

        """
    )


    total = cursor.fetchone()[0]


    db.close()


    return total or 0



# ==========================================================
# Pending Payment Count
# ==========================================================

def pending_count():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)

        FROM orders

        WHERE status='pending'

        """
    )


    count = cursor.fetchone()[0]


    db.close()


    return count



# ==========================================================
# All Users
# ==========================================================

def all_users():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT *

        FROM users

        ORDER BY id DESC

        """
    )


    users = cursor.fetchall()


    db.close()


    return users



# ==========================================================
# Search Users
# ==========================================================

def search_users(
    text
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT *

        FROM users

        WHERE telegram_id LIKE ?

        OR username LIKE ?

        ORDER BY id DESC

        """,
        (
            f"%{text}%",
            f"%{text}%"
        )
    )


    users = cursor.fetchall()


    db.close()


    return users



# ==========================================================
# Dashboard Stats
# ==========================================================

def get_stats():

    return {


        "users":
        users_count(),


        "today_users":
        today_users_count(),


        "sales":
        sales_count(),


        "subscriptions":
        services_count(),


        "income":
        total_income(),


        "pending":
        pending_count()

    }



# ==========================================================
# Database Test
# ==========================================================

def test_database():

    try:

        db = get_db()

        db.close()

        return True


    except Exception as error:


        print(
            "DATABASE ERROR:",
            error
        )


        return False



# ==========================================================
# END database.py
# Zeus Shop VPN PRO
# ==========================================================
