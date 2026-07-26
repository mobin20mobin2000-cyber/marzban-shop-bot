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
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        telegram_id INTEGER UNIQUE,

        username TEXT,

        is_blocked INTEGER DEFAULT 0,

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

        coupon TEXT,

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

        status TEXT DEFAULT 'active',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)



    # کدهای تخفیف

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coupons (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        code TEXT UNIQUE,

        percent INTEGER,

        max_use INTEGER DEFAULT 1,

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
        WHERE is_blocked=0
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
        WHERE is_blocked=0
        """
    )


    count = cursor.fetchone()[0]


    db.close()


    return count





def today_users():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users

        WHERE DATE(created_at)
        =
        DATE('now')
        """
    )


    count = cursor.fetchone()[0]


    db.close()


    return count





def block_user(
    telegram_id
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        UPDATE users

        SET is_blocked=1

        WHERE telegram_id=?

        """,

        (
            telegram_id,
        )
    )


    db.commit()

    db.close()





def unblock_user(
    telegram_id
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        UPDATE users

        SET is_blocked=0

        WHERE telegram_id=?

        """,

        (
            telegram_id,
        )
    )


    db.commit()

    db.close()





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





def all_orders():

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        SELECT *

        FROM orders

        ORDER BY id DESC

        """
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
# وضعیت پرداخت
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

        WHERE payment_status='pending'

        """
    )


    count = cursor.fetchone()[0]


    db.close()


    return count
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

        AND status='active'

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

        WHERE status='active'

        """
    )


    count = cursor.fetchone()[0]


    db.close()


    return count





def user_subscriptions(
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

        """,

        (
            telegram_id,
        )
    )


    result = cursor.fetchall()


    db.close()


    return result





def disable_subscription(
    subscription_id
):

    db = get_db()

    cursor = db.cursor()


    cursor.execute(
        """
        UPDATE subscriptions

        SET status='expired'

        WHERE id=?

        """,

        (
            subscription_id,
        )
    )


    db.commit()

    db.close()
    # =========================
# کد تخفیف
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
            code,
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
            code,
        )
    )


    coupon = cursor.fetchone()


    db.close()


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
            code,
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


    coupons = cursor.fetchall()


    db.close()


    return coupons





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
            code,
        )
    )


    db.commit()

    db.close()





# =========================
# داشبورد مدیریت
# =========================


def get_stats():

    return {

        "users":
            users_count(),


        "today_users":
            today_users(),


        "sales":
            sales_count(),


        "income":
            total_sales(),


        "subscriptions":
            subscriptions_count(),


        "pending":
            pending_count()

    }





def full_dashboard():

    stats = get_stats()


    return f"""
👑 Zeus Shop VPN

━━━━━━━━━━━━━━

👥 کل کاربران:
{stats['users']}

🆕 کاربران امروز:
{stats['today_users']}

🛒 فروش موفق:
{stats['sales']}

💰 درآمد:
{stats['income']:,} تومان

🌐 سرویس فعال:
{stats['subscriptions']}

⏳ پرداخت در انتظار:
{stats['pending']}

━━━━━━━━━━━━━━
"""
