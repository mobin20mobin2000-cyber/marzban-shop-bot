# ==========================================================
# Zeus Shop VPN PRO
# database.py
# Part 1/4
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
# ساخت جداول
# ==========================================================

def init_db():

    db = get_db()
    cursor = db.cursor()


    # کاربران

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER UNIQUE NOT NULL,

        username TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # سفارش‌ها

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER NOT NULL,

        plan TEXT,

        volume INTEGER,

        days INTEGER,

        price INTEGER,

        coupon TEXT,

        status TEXT DEFAULT 'pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # سرویس‌ها

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER NOT NULL,

        order_id INTEGER,

        username TEXT,

        subscription_url TEXT,

        volume INTEGER,

        days INTEGER,

        expire_date TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # رسید پرداخت

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receipts(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER NOT NULL,

        file_id TEXT,

        status TEXT DEFAULT 'pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # کد تخفیف

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coupons(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        code TEXT UNIQUE NOT NULL,

        percent INTEGER NOT NULL,

        max_use INTEGER DEFAULT 1,

        used INTEGER DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # پشتیبانی

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
# کاربران
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
    # ==========================================================
# سفارش‌ها
# Part 2/4
# ==========================================================


# ==========================================================
# ساخت سفارش جدید
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
# دریافت سفارش با آیدی سفارش
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
# تایید پرداخت
# ==========================================================

def approve_payment(
    order_id
):

    update_order_status(
        order_id,
        "approved"
    )




# ==========================================================
# رد پرداخت
# ==========================================================

def reject_payment(
    order_id
):

    update_order_status(
        order_id,
        "rejected"
    )




# ==========================================================
# سفارش‌های در انتظار
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
# سفارش‌های تایید شده
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
# حذف سفارش
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
# سرویس‌ها
# Part 3/4
# ==========================================================


# ==========================================================
# ذخیره سرویس ساخته شده
# ==========================================================

def save_service(
    telegram_id,
    order_id,
    username,
    subscription_url,
    volume,
    days,
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
# رسید پرداخت
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
# رسیدهای در انتظار
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
# تغییر وضعیت رسید
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
# پشتیبانی
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
# همه پیام‌های پشتیبانی
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
# کد تخفیف
# Part 4/4
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




# ==========================================================
# دریافت کد تخفیف
# ==========================================================

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




# ==========================================================
# بررسی اعتبار کد تخفیف
# ==========================================================

def check_coupon(
    code
):

    coupon = get_coupon(code)


    if not coupon:

        return None



    if coupon["used"] >= coupon["max_use"]:

        return None



    return coupon




# ==========================================================
# استفاده از کد تخفیف
# ==========================================================

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




# ==========================================================
# لیست کدهای تخفیف
# ==========================================================

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


    coupons = cursor.fetchall()


    db.close()


    return coupons




# ==========================================================
# حذف کد تخفیف
# ==========================================================

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
# آمار داشبورد
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
# جستجوی کاربران
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
# آمار کامل
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
# END database.py
# Zeus Shop VPN PRO
# ==========================================================
