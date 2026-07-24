# =========================
# database.py
# Zeus Shop VPN
# =========================

import sqlite3


DATABASE = "zeus.db"



# =========================
# اتصال دیتابیس
# =========================

def get_db():

    db = sqlite3.connect(
        DATABASE
    )

    return db



# =========================
# ساخت جدول‌ها
# =========================

def init_db():

    db = get_db()

    cursor = db.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER UNIQUE,

        username TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (

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



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        order_id INTEGER,

        marzban_username TEXT,

        subscription_url TEXT,

        expire_date TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

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
            telegram_id,
        )
    )


    result = cursor.fetchone()


    db.close()


    return result



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


    result = cursor.fetchall()


    db.close()


    return result



def users_count():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)

        FROM users
        """
    )


    result = cursor.fetchone()[0]


    db.close()


    return result
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
            order_id,
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
            telegram_id,
        )
    )


    orders = cursor.fetchall()


    db.close()


    return orders




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
            order_id,
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
            order_id,
        )
    )


    db.commit()

    db.close()




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
    # =========================
# اشتراک‌ها
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
            telegram_id,
        )
    )


    subscription = cursor.fetchone()


    db.close()


    return subscription




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


    subscriptions = cursor.fetchall()


    db.close()


    return subscriptions




def subscriptions_count():

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




def delete_subscription(
    telegram_id
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        DELETE FROM subscriptions

        WHERE telegram_id=?

        """,
        (
            telegram_id,
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
