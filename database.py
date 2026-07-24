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

    return sqlite3.connect(
        DATABASE
    )


# =========================
# ساخت جدول‌ها
# =========================

def init_db():

    db = get_db()

    cursor = db.cursor()


    # کاربران

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER UNIQUE,

        username TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)


    # سفارش‌ها

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


    # اشتراک‌ها

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
# ثبت کاربر
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



# =========================
# دریافت کاربر
# =========================

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



# =========================
# ساخت سفارش
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



# =========================
# دریافت سفارش
# =========================

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



# =========================
# سفارش‌های در انتظار
# =========================

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



# =========================
# تایید پرداخت
# =========================

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



# =========================
# رد پرداخت
# =========================

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



# =========================
# ذخیره اشتراک مرزبان
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



# =========================
# دریافت اشتراک کاربر
# =========================

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



# =========================
# همه کاربران
# =========================

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



# =========================
# تعداد کاربران
# =========================

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
# تعداد سفارش‌ها
# =========================

def orders_count():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """

        SELECT COUNT(*)

        FROM orders

        """
    )


    count = cursor.fetchone()[0]


    db.close()


    return count



# =========================
# فروش تایید شده
# =========================

def sales_total():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """

        SELECT SUM(price)

        FROM orders

        WHERE payment_status='approved'

        """
    )


    total = cursor.fetchone()[0]


    db.close()


    return total or 0
