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
    
