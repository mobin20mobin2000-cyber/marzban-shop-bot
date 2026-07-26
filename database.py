# =========================
# database.py
# Zeus Shop VPN PRO
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

        coupon TEXT,

        payment_status TEXT DEFAULT 'pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # اشتراک‌ها

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER,

        order_id INTEGER,

        marzban_username TEXT,

        subscription_url TEXT,

        expire_date TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # کد تخفیف

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coupons(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        code TEXT UNIQUE,

        percent INTEGER,

        max_use INTEGER,

        used INTEGER DEFAULT 0,

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
# کاربران امروز
# =========================


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
    # =========================
# سفارش‌ها
# =========================


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





# =========================
# دریافت سفارش با آیدی
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
# آخرین سفارش کاربر
# =========================


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
# سفارش‌های تایید شده
# =========================


def approved_orders():


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        SELECT *

        FROM orders

        WHERE payment_status='approved'

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
# حذف سفارش
# =========================


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
# کدهای تخفیف
# =========================


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





# =========================
# دریافت کد تخفیف
# =========================


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





# =========================
# بررسی کد تخفیف
# =========================


def check_coupon(

    code

):

    coupon = get_coupon(

        code

    )



    if coupon is None:

        return None




    if coupon["used"] >= coupon["max_use"]:

        return None




    return coupon





# =========================
# افزایش استفاده کد
# =========================


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





# =========================
# لیست کدهای تخفیف
# =========================


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





# =========================
# حذف کد تخفیف
# =========================


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





# =========================
# سرویس کاربر
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



    service = cursor.fetchone()



    db.close()



    return service





# =========================
# همه سرویس‌ها
# =========================


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





# =========================
# تعداد سرویس‌ها
# =========================


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





# =========================
# تعداد فروش موفق
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





# =========================
# درآمد کل
# =========================


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



    total = cursor.fetchone()[0]



    db.close()



    return total or 0





# =========================
# پرداخت‌های منتظر
# =========================


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
    # =========================
# جستجوی کاربران
# =========================


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





# =========================
# آمار کامل داشبورد
# =========================


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





# =========================
# تست دیتابیس
# =========================


def test_database():


    try:


        db = get_db()

        db.close()



        return True



    except Exception as e:


        print(

            "DATABASE ERROR:",

            e

        )


        return False





# =========================
# پایان database.py
# Zeus Shop VPN PRO
# =========================
