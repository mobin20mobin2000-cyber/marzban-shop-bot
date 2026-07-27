# ==========================================================
# Zeus Shop VPN PRO
# database.py
# Part 1/8
# ==========================================================

import sqlite3
from contextlib import closing

DB_NAME = "zeus.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    with closing(get_connection()) as conn:
        cur = conn.cursor()

        # ================= USERS =================

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER UNIQUE NOT NULL,

            username TEXT,

            first_name TEXT,

            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ================= ORDERS =================

        cur.execute("""
        CREATE TABLE IF NOT EXISTS orders(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            plan TEXT NOT NULL,

            volume INTEGER,

            days INTEGER,

            price INTEGER,

            receipt TEXT,

            status TEXT DEFAULT 'pending',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ================= SERVICES =================

        cur.execute("""
        CREATE TABLE IF NOT EXISTS services(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER UNIQUE,

            username TEXT,

            subscription_url TEXT,

            expire_date TEXT,

            volume INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        # ================= BROADCAST =================

        cur.execute("""
        CREATE TABLE IF NOT EXISTS broadcasts(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            message TEXT,

            success INTEGER,

            failed INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """)

        conn.commit()
        # ==========================================================
# Users
# ==========================================================

def add_user(user_id: int, username: str | None):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO users
        (user_id, username, created_at)
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            username,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    conn.commit()
    conn.close()


def get_user(user_id: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id,user_id,username,created_at
        FROM users
        WHERE user_id=?
        """,
        (user_id,),
    )

    row = cur.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "user_id": row[1],
        "username": row[2],
        "created_at": row[3],
    }


def get_all_users():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT user_id,username
        FROM users
        ORDER BY id ASC
        """
    )

    rows = cur.fetchall()

    conn.close()

    return [
        {
            "user_id": r[0],
            "username": r[1],
        }
        for r in rows
    ]


def count_users():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM users
        """
    )

    count = cur.fetchone()[0]

    conn.close()

    return count
    # ==========================================================
# Orders
# Part 3/8
# ==========================================================


def create_order(
    user_id,
    plan,
    volume,
    days,
    price
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO orders
        (
            user_id,
            plan,
            volume,
            days,
            price,
            status
        )

        VALUES (?, ?, ?, ?, ?, ?)
        """,

        (
            user_id,
            plan,
            volume,
            days,
            price,
            "pending"
        )
    )

    order_id = cur.lastrowid

    conn.commit()
    conn.close()

    return order_id


# ==========================================================


def last_order(user_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
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

    row = cur.fetchone()

    conn.close()

    if row is None:
        return None

    return
    # ==========================================================
# Services
# Part 4/8
# ==========================================================


def save_service(
    user_id,
    username,
    subscription_url,
    expire_date,
    volume
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO services
        (
            user_id,
            username,
            subscription_url,
            expire_date,
            volume
        )

        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user_id,
            username,
            subscription_url,
            expire_date,
            volume
        )
    )

    conn.commit()
    conn.close()


# ==========================================================


def get_user_service(user_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *

        FROM services

        WHERE user_id=?

        LIMIT 1
        """,
        (
            user_id,
        )
    )

    row = cur.fetchone()

    conn.close()

    if row is None:
        return None

    return dict(row)


# ==========================================================


def delete_service(user_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM services

        WHERE user_id=?
        """,
        (
            user_id,
        )
    )

    conn.commit()
    conn.close()


# ==========================================================


def get_all_services():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *

        FROM services

        ORDER BY id DESC
        """
    )

    rows = cur.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ==========================================================


def count_services():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)

        FROM services
        """
    )

    count = cur.fetchone()[0]

    conn.close()

    return count
    # ==========================================================
# Services
# ==========================================================

def save_service(user_id, username, subscription_url, volume, days):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO services
        (
            user_id,
            username,
            subscription_url,
            volume,
            days,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        username,
        subscription_url,
        volume,
        days,
        now()
    ))

    conn.commit()
    conn.close()


def get_user_service(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM services
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,))

    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    return dict(row)


def delete_service(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM services WHERE user_id=?",
        (user_id,)
    )

    conn.commit()
    conn.close()


def get
# ==========================================================
# Statistics
# Part 7/8
# ==========================================================


def get_stats():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    orders = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM services")
    services = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(SUM(price),0)
        FROM orders
        WHERE status='paid'
    """)
    income = cursor.fetchone()[0]

    conn.close()

    return {
        "users": users,
        "orders": orders,
        "services": services,
        "income": income
    }


# ==========================================================
# Broadcast History
# ==========================================================


def save_broadcast_history(
    message,
    success,
    failed
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO broadcasts
        (
            message,
            success,
            failed
        )

        VALUES (?, ?, ?)
    """, (
        message,
        success,
        failed
    ))

    conn.commit()
    conn.close()


def get_broadcast_history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM broadcasts
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def count_broadcasts():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM broadcasts")

    count = cursor.fetchone()[0]

    conn.close()

    return count
    # ==========================================================
# database.py
# Part 7/8
# Statistics & Backup
# ==========================================================

import shutil
from pathlib import Path


# ==========================================================
# Statistics
# ==========================================================

def get_stats():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders")
    orders = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM services")
    services = cur.fetchone()[0]

    cur.execute(
        """
        SELECT COALESCE(SUM(price),0)
        FROM orders
        WHERE status='paid'
        """
    )

    income = cur.fetchone()[0]

    conn.close()

    return {
        "users": users,
        "orders": orders,
        "services": services,
        "income": income,
    }


# ==========================================================
# Database Backup
# ==========================================================

def backup_database(destination="backup"):

    Path(destination).mkdir(
        exist_ok=True
    )

    filename = datetime.now().strftime(
        "zeus_%Y%m%d_%H%
    # ==========================================================
# Utilities
# Part 8/8
# ==========================================================

from datetime import datetime


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ==========================================================
# Counters
# ==========================================================

def count_orders():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM orders")

    value = cursor.fetchone()[0]

    conn.close()

    return value


def count_services():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM services")

    value = cursor.fetchone()[0]

    conn.close()

    return value


# ==========================================================
# Reset Database (Developer)
# ==========================================================

def clear_database():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM orders")
    cursor.execute("DELETE FROM services")
    cursor.execute("DELETE FROM broadcasts")

    conn.commit()
    conn.close()


# ==========================================================
# Initialize Database Automatically
# ==========================================================

init_db()


print("✅ Database Loaded Successfully")
