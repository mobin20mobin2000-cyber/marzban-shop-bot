# =========================
# database.py
# Zeus Shop VPN PRO
# =========================

import sqlite3
from datetime import datetime


DATABASE = "zeus.db"



# =========================
# اتصال دیتابیس
# =========================


def get_db():

    db = sqlite3.connect(
        DATABASE
    )

    db.row_factory = sqlite3.Row

    return db



# =========================
# ساخت جدول‌ها
# =========================


def init_db():

    db = get_db()

    cursor = db.cursor()



    # کاربران

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER UNIQUE,

        username TEXT,

        status TEXT DEFAULT 'active',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # سفارش‌ها

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        plan TEXT,

        volume INTEGER,

        days INTEGER,

        price INTEGER,

        payment_status TEXT DEFAULT 'pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # سرویس‌ها

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        order_id INTEGER,

        marzban_username TEXT,

        subscription_url TEXT,

        expire_date TEXT,

        status TEXT DEFAULT 'active',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # لاگ ادمین

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        admin_id INTEGER,

        action TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # تنظیمات

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings(

        key TEXT PRIMARY KEY,

        value TEXT

    )
    """)



    db.commit()

    db.close()
    # =========================
# کاربران
# =========================


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
            telegram_id
        )

    )


    user = cursor.fetchone()


    db.close()


    return user





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





# =========================
# جستجوی
# =========================
# سفارش‌ها
# =========================


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
            order_id
        )

    )


    order = cursor.fetchone()


    db.close()


    return order





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
            telegram_id
        )

    )


    order = cursor.fetchone()


    db.close()


    return order





def user_orders(

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

        """,

        (
            telegram_id
        )

    )


    orders = cursor.fetchall()


    db.close()


    return orders





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


    orders = cursor.fetchall()


    db.close()


    return orders





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
            order_id
        )

    )


    db.commit()

    db.close()





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
            order_id
        )

    )


    db.commit()

    db.close()





# =========================
# سرویس‌ها
# =========================


def save_subscription(

    telegram_id,

    order_id,

    marzban_username,

    subscription_url,

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

            marzban_username,

            subscription_url,

            expire_date

        )

        VALUES (?,?,?,?,?)

        """,

        (

            telegram_id,

            order_id,

            marzban_username,

            subscription_url,

            expire_date

        )

    )


    db.commit()

    db.close()





def get_subscription(

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
            telegram_id
        )

    )


    service = cursor.fetchone()


    db.close()


    return service





def all_subscriptions():


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





def delete_subscription(

    subscription_id

):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(

        """
        DELETE FROM subscriptions

        WHERE id=?

        """,

        (
            subscription_id
        )

    )


    db.commit()

    db.close()





def update_expire_date(

    subscription_id,

    expire_date

):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(

        """
        UPDATE subscriptions

        SET expire_date=?

        WHERE id=?

        """,

        (

            expire_date,

            subscription_id

        )

    )


    db.commit()

    db.close()
    # =========================
# آمار فروش
# =========================


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


    result = cursor.fetchone()[0]


    db.close()


    return result





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





def subscriptions_count():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(

        """
        SELECT COUNT(*)

        FROM subscriptions

        WHERE status='active'

        """

    )


    result = cursor.fetchone()[0]


    db.close()


    return result





def get_stats():


    return {


        "users":

            users_count(),



        "sales":

            sales_count(),



        "subscriptions":

            subscriptions_count(),



        "income":

            total_sales()

    }





# =========================
# لاگ ادمین
# =========================


def add_log(

    admin_id,

    action

):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(

        """
        INSERT INTO logs

        (

            admin_id,

            action

        )

        VALUES (?,?)

        """,

        (

            admin_id,

            action

        )

    )


    db.commit()

    db.close()





def get_logs():


    db = get_db()

    cursor = db.cursor()


    cursor.execute(

        """
        SELECT *

        FROM logs

        ORDER BY id DESC

        """

    )


    logs = cursor.fetchall()


    db.close()


    return logs





# =========================
# تنظیمات ربات
# =========================


def set_setting(

    key,

    value

):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(

        """
        INSERT INTO settings

        (

            key,

            value

        )

        VALUES (?,?)

        ON CONFLICT(key)

        DO UPDATE SET value=excluded.value

        """,

        (

            key,

            value

        )

    )


    db.commit()

    db.close()





def get_setting(

    key

):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(

        """
        SELECT value

        FROM settings

        WHERE key=?

        """,

        (

            key

        )

    )


    result = cursor.fetchone()


    db.close()



    if result:

        return result["value"]


    return None





# =========================
# پاکسازی و حذف
# =========================


def delete_user(

    telegram_id

):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(

        """
        DELETE FROM users

        WHERE telegram_id=?

        """,

        (

            telegram_id

        )

    )


    db.commit()

    db.close()
