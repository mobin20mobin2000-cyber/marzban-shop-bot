# =========================
# database.py
# Zeus Shop VPN
# =========================

import sqlite3


DB_NAME = "zeus.db"



# =========================
# اتصال به دیتابیس
# =========================

def connect():

    return sqlite3.connect(
        DB_NAME
    )



# =========================
# ساخت جدول‌ها
# =========================

def init_db():

    db = connect()

    cursor = db.cursor()



    # کاربران

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER UNIQUE,

        username TEXT,

        join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)



    # سفارش‌ها

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS orders (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        plan TEXT,

        volume INTEGER,

        days INTEGER,

        price INTEGER,

        status TEXT DEFAULT 'pending',

        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)



    # اشتراک‌ها

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS subscriptions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        order_id INTEGER,

        marzban_username TEXT,

        subscription_url TEXT,

        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)



    db.commit()

    db.close()




# =========================
# ثبت کاربر
# =========================

def add_user(
    user_id,
    username=None
):

    db = connect()

    cursor = db.cursor()


    cursor.execute(
        """

        INSERT OR IGNORE INTO users

        (
        user_id,
        username
        )

        VALUES (?,?)

        """,

        (
            user_id,
            username
        )

    )


    db.commit()

    db.close()




# =========================
# ساخت سفارش
# =========================

def create_order(

    user_id,
    plan,
    volume,
    days,
    price

):


    db = connect()

    cursor = db.cursor()



    cursor.execute(

        """

        INSERT INTO orders

        (

        user_id,
        plan,
        volume,
        days,
        price

        )

        VALUES (?,?,?,?,?)

        """,

        (

        user_id,
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




# =========================
# دریافت سفارش
# =========================

def get_order(order_id):


    db = connect()

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


    result = cursor.fetchone()


    db.close()


    return result




# =========================
# سفارش‌های منتظر تایید
# =========================

def pending_orders():


    db = connect()

    cursor = db.cursor()


    cursor.execute(

        """

        SELECT *

        FROM orders

        WHERE status='pending'

        ORDER BY id DESC

        """

    )


    result = cursor.fetchall()


    db.close()


    return result




# =========================
# تایید سفارش
# =========================

def approve_order(order_id):


    db = connect()

    cursor = db.cursor()



    cursor.execute(

        """

        UPDATE orders

        SET status='approved'

        WHERE id=?

        """,

        (
        order_id,
        )

    )


    db.commit()

    db.close()




# =========================
# رد سفارش
# =========================

def reject_order(order_id):


    db = connect()

    cursor = db.cursor()



    cursor.execute(

        """

        UPDATE orders

        SET status='rejected'

        WHERE id=?

        """,

        (
        order_id,
        )

    )


    db.commit()

    db.close()




# =========================
# ذخیره اشتراک مرزبان
# =========================

def save_subscription(

    user_id,

    order_id,

    marzban_username,

    subscription_url

):


    db = connect()

    cursor = db.cursor()



    cursor.execute(

        """

        INSERT INTO subscriptions

        (

        user_id,

        order_id,

        marzban_username,

        subscription_url

        )

        VALUES (?,?,?,?)

        """,

        (

        user_id,

        order_id,

        marzban_username,

        subscription_url

        )

    )



    db.commit()

    db.close()




# =========================
# گرفتن اشتراک کاربر
# =========================

def get_subscription(user_id):


    db = connect()

    cursor = db.cursor()



    cursor.execute(

        """

        SELECT *

        FROM subscriptions

        WHERE user_id=?

        ORDER BY id DESC

        LIMIT 1

        """,

        (
        user_id,
        )

    )



    result = cursor.fetchone()


    db.close()


    return result




# =========================
# آمار فروش
# =========================

def sales_stats():


    db = connect()

    cursor = db.cursor()



    cursor.execute(

        """

        SELECT COUNT(*), SUM(price)

        FROM orders

        WHERE status='approved'

        """

    )


    result = cursor.fetchone()


    db.close()


    return result
