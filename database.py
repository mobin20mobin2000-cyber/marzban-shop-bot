# ==========================================================
# database.py
# Zeus Shop VPN PRO
# Part 1
# Database Core + Users
# ==========================================================

import sqlite3


DATABASE = "zeus.db"


# ==========================================================
# اتصال دیتابیس
# ==========================================================

def get_db():

    db = sqlite3.connect(
        DATABASE
    )

    db.row_factory = sqlite3.Row

    return db



# ==========================================================
# ساخت جدول‌ها
# ==========================================================

def init_db():

    db = get_db()
    cursor = db.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER UNIQUE,

        username TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        plan TEXT,

        volume INTEGER,

        days INTEGER,

        price INTEGER,

        coupon TEXT,

        payment_status TEXT DEFAULT 'pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        order_id INTEGER,

        username TEXT,

        subscription_url TEXT,

        volume INTEGER,

        days INTEGER,

        expire_date TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receipts(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        file_id TEXT,

        status TEXT DEFAULT 'pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS support(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        message TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coupons(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        code TEXT UNIQUE,

        percent INTEGER,

        max_use INTEGER,

        used INTEGER DEFAULT 0

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
        "SELECT COUNT(*) FROM users"
    )


    count = cursor.fetchone()[0]


    db.close()

    return count
    # ==========================================================
# Orders
# Part 2
# ==========================================================


def create_order(
    telegram_id,
    plan,
    volume,
    days,
    price,
    coupon=None
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
            price,
            coupon
        )

        VALUES (?,?,?,?,?,?)
        """,

        (
            telegram_id,
            plan,
            volume,
            days,
            price,
            coupon
        )
    )


    db.commit()


    order_id = cursor.lastrowid


    db.close()


    return order_id





# ==========================================================
# دریافت سفارش
# ==========================================================


def get_order(
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
# آخرین سفارش کاربر
# ==========================================================


def last_order(
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
# تغییر وضعیت سفارش
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

        SET payment_status=?

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
# سفارش‌های منتظر
# ==========================================================


def pending_orders():

    db = get_db()
    cursor = db.cursor()


    cursor.execute(
        """
        SELECT *

        FROM orders

        WHERE payment_status='pending'

        ORDER BY id DESC
        """
    )


    data = cursor.fetchall()


    db.close()


    return data





# ==========================================================
# تایید پرداخت
# ==========================================================


def approve_payment(
    order_id
):

    db = get_db()
    cursor = db.cursor()


    cursor.execute(
        """
        UPDATE orders

        SET payment_status='approved'

        WHERE id=?
        """,

        (
            order_id,
        )
    )


    db.commit()
    db.close()





# ==========================================================
# رد پرداخت
# ==========================================================


def reject_payment(
    order_id
):

    db = get_db()
    cursor = db.cursor()


    cursor.execute(
        """
        UPDATE orders

        SET payment_status='rejected'

        WHERE id=?
        """,

        (
            order_id,
        )
    )


    db.commit()
    db.close()





# ==========================================================
# Receipt
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





def get_receipts():

    db = get_db()
    cursor = db.cursor()


    cursor.execute(
        """
        SELECT *

        FROM receipts

        ORDER BY id DESC
        """
    )


    data = cursor.fetchall()


    db.close()


    return data
    # ==========================================================
# Subscriptions
# Part 3
# ==========================================================


# ==========================================================
# ذخیره سرویس
# ==========================================================

def save_service(
    telegram_id,
    username,
    subscription_url,
    volume,
    days,
    order_id=None,
    expire_date=None
):

    db = get_db()
    cursor = db.cursor()


    cursor.execute(
        """
        INSERT INTO subscriptions
        (
            telegram_id,
            order_id,
            username,
            subscription_url,
            volume,
            days,
            expire_date
        )

        VALUES (?,?,?,?,?,?,?)
        """,

        (
            telegram_id,
            order_id,
            username,
            subscription_url,
            volume,
            days,
            expire_date
        )
    )


    db.commit()
    db.close()





# ==========================================================
# دریافت سرویس کاربر
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
# همه سرویس‌ها
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
# تعداد سرویس‌ها
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





def get_support_messages():

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
# آمار
# ==========================================================


def sales_count():

    db = get_db()
    cursor = db.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)

        FROM orders

        WHERE payment_status='approved'
        """
    )


    count = cursor.fetchone()[0]


    db.close()


    return count





def pending_count():

    db = get_db()
    cursor = db.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)

        FROM orders

        WHERE payment_status='pending'
        """
    )


    count = cursor.fetchone()[0]


    db.close()


    return count





def total_sales():

    db = get_db()
    cursor = db.cursor()


    cursor.execute(
        """
        SELECT SUM(price)

        FROM orders

        WHERE payment_status='approved'
        """
    )


    result = cursor.fetchone()[0]


    db.close()


    return result or 0
    # ==========================================================
# Coupons
# Part 4
# ==========================================================


def create_coupon(
    code,
    percent,
    max_use
):

    db = get_db()
    cursor = db.cursor()


    cursor.execute(
        """
        INSERT INTO coupons
        (
            code,
            percent,
            max_use
        )

        VALUES (?,?,?)
        """,

        (
            code.upper(),
            percent,
            max_use
        )
    )


    db.commit()
    db.close()





def get_coupon(
    code
):

    db = get_db()
    cursor = db.cursor()


    cursor.execute(
        """
        SELECT *

        FROM coupons

        WHERE code=?
        """,

        (
            code.upper(),
        )
    )


    coupon = cursor.fetchone()


    db.close()


    return coupon





def check_coupon(
    code
):

    coupon = get_coupon(
        code
    )


    if not coupon:

        return None



    if coupon["used"] >= coupon["max_use"]:

        return None



    return coupon





def use_coupon(
    code
):

    db = get_db()
    cursor = db.cursor()


    cursor.execute(
        """
        UPDATE coupons

        SET used = used + 1

        WHERE code=?
        """,

        (
            code.upper(),
        )
    )


    db.commit()
    db.close()





def all_coupons():

    db = get_db()
    cursor = db.cursor()


    cursor.execute(
        """
        SELECT *

        FROM coupons

        ORDER BY id DESC
        """
    )


    data = cursor.fetchall()


    db.close()


    return data





def delete_coupon(
    code
):

    db = get_db()
    cursor = db.cursor()


    cursor.execute(
        """
        DELETE FROM coupons

        WHERE code=?
        """,

        (
            code.upper(),
        )
    )


    db.commit()
    db.close()





# ==========================================================
# Dashboard Stats
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





def subscriptions_count():

    return services_count()





def get_stats():

    return {

        "users":
            users_count(),

        "today_users":
            today_users_count(),

        "sales":
            sales_count(),

        "subscriptions":
            subscriptions_count(),

        "income":
            total_sales(),

        "pending":
            pending_count()
    }





# ==========================================================
# تست دیتابیس
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
# END DATABASE
# Zeus Shop VPN PRO
# ==========================================================
