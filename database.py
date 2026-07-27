# ==========================================================
# Zeus Shop VPN PRO
# database.py
# Part 1/4
# ==========================================================


import sqlite3
from datetime import datetime



DB_NAME = "zeus.db"





# ==========================================================
# Database Connection
# ==========================================================


def get_db():

    db = sqlite3.connect(
        DB_NAME
    )

    db.row_factory = sqlite3.Row

    return db





# ==========================================================
# Initialize Database
# ==========================================================


def init_db():


    db = get_db()

    cursor = db.cursor()



    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY,

        username TEXT,

        created TEXT

    )

    """)




    cursor.execute("""

    CREATE TABLE IF NOT EXISTS orders(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        volume TEXT,

        days INTEGER,

        price INTEGER,

        status TEXT,

        discount TEXT,

        created TEXT

    )

    """)




    cursor.execute("""

    CREATE TABLE IF NOT EXISTS receipts(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        order_id INTEGER,

        file_id TEXT,

        status TEXT,

        created TEXT

    )

    """)




    cursor.execute("""

    CREATE TABLE IF NOT EXISTS services(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        username TEXT,

        subscription_url TEXT,

        volume TEXT,

        days INTEGER,

        status TEXT,

        created TEXT

    )

    """)




    cursor.execute("""

    CREATE TABLE IF NOT EXISTS discounts(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        code TEXT UNIQUE,

        percent INTEGER,

        active INTEGER

    )

    """)



    db.commit()

    db.close()
    # ==========================================================
# Users & Orders
# Part 2/4
# ==========================================================



# ==========================================================
# Add User
# ==========================================================


def add_user(

    user_id,

    username

):


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        INSERT OR IGNORE INTO users

        (

            id,

            username,

            created

        )

        VALUES

        (?,?,?)

        """,

        (

            user_id,

            username,

            datetime.now().isoformat()

        )

    )



    db.commit()

    db.close()







# ==========================================================
# Create Order
# ==========================================================


def create_order(

    user_id,

    volume,

    days,

    price,

    discount=""

):


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        INSERT INTO orders

        (

            user_id,

            volume,

            days,

            price,

            status,

            discount,

            created

        )

        VALUES

        (?,?,?,?,?,?,?)

        """,

        (

            user_id,

            volume,

            days,

            price,

            "pending",

            discount,

            datetime.now().isoformat()

        )

    )



    order_id = cursor.lastrowid



    db.commit()

    db.close()



    return order_id







# ==========================================================
# Last User Order
# ==========================================================


def last_order(

    user_id

):


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        SELECT *

        FROM orders

        WHERE user_id=?

        ORDER BY id DESC

        LIMIT 1

        """,

        (

            user_id,

        )

    )



    order = cursor.fetchone()



    db.close()



    return order







# ==========================================================
# Get Order
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
# Update Order
# ==========================================================


def update_order
# ==========================================================
# Receipts & Services
# Part 3/4
# ==========================================================



# ==========================================================
# Save Receipt
# ==========================================================


def save_receipt(

    user_id,

    order_id,

    file_id

):


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        INSERT INTO receipts

        (

            user_id,

            order_id,

            file_id,

            status,

            created

        )

        VALUES

        (?,?,?,?,?)

        """,

        (

            user_id,

            order_id,

            file_id,

            "pending",

            datetime.now().isoformat()

        )

    )



    db.commit()

    db.close()







# ==========================================================
# Update Receipt Status
# ==========================================================


def update_receipt_status(

    order_id,

    status

):


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        UPDATE receipts

        SET status=?

        WHERE order_id=?

        """,

        (

            status,

            order_id

        )

    )



    db.commit()

    db.close()







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


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        INSERT INTO services

        (

            user_id,

            username,

            subscription_url,

            volume,

            days,

            status,

            created

        )

        VALUES

        (?,?,?,?,?,?,?)

        """,

        (

            user_id,

            username,

            subscription_url,

            volume,

            days,

            "active",

            datetime.now().isoformat()

        )

    )



    db.commit()

    db.close()







# ==========================================================
# Get User Service
# ==========================================================


def get_user_service(

    user_id

):


    db = get_db()

    cursor =
    # ==========================================================
# Discount + Admin + Test
# Part 4/4
# ==========================================================



# ==========================================================
# Add Discount
# ==========================================================


def add_discount(

    code,

    percent

):


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        INSERT OR REPLACE INTO discounts

        (

            code,

            percent,

            active

        )

        VALUES

        (?,?,?)

        """,

        (

            code.upper(),

            percent,

            1

        )

    )



    db.commit()

    db.close()







# ==========================================================
# Get Discount
# ==========================================================


def get_discount(

    code

):


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        SELECT *

        FROM discounts

        WHERE code=?

        AND active=1

        """,

        (

            code.upper(),

        )

    )



    discount = cursor.fetchone()



    db.close()



    return discount







# ==========================================================
# Disable Discount
# ==========================================================


def disable_discount(

    code

):


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        """

        UPDATE discounts

        SET active=0

        WHERE code=?

        """,

        (

            code.upper(),

        )

    )



    db.commit()

    db.close()







# ==========================================================
# Statistics
# ==========================================================


def get_stats():


    db = get_db()

    cursor = db.cursor()



    cursor.execute(

        "SELECT COUNT(*) FROM users"

    )

    users = cursor.fetchone()[0]





    cursor.execute(

        "SELECT COUNT(*) FROM orders"

    )

    orders = cursor.fetchone()[0]





    cursor.execute(

        "SELECT COUNT(*) FROM services"

    )

    services = cursor.fetchone()[0]





    cursor.execute(

        """

        SELECT SUM(price)

        FROM orders

        WHERE status='paid'

        """

    )


    income = cursor.fetchone()[0]



    if income is None:

        income = 0





    db.close()



    return {


        "users":

        users,


        "orders":

        orders,


        "services":

        services,


        "income":

        income

    }









# ==========================================================
# Pending Orders
# ==========================================================


def get_pending_orders():


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
# Database Test
# ==========================================================


def test_database():


    try:


        db = get_db()

        cursor = db.cursor()


        cursor.execute(

            "SELECT 1"

        )


        result = cursor.fetchone()


        db.close()



        if result:


            print(

                "✅ Database Connected"

            )


            return True



        return False



    except Exception as error:



        print(

            "❌ Database Error:",

            error

        )


        return False
