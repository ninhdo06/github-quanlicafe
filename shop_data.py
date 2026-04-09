import sqlite3
import hashlib

DB_NAME = "shop_data.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        hashed_pw = hash_password(password)

        cursor.execute(
            "INSERT INTO login_info (username, password) VALUES (?, ?)",
            (username, hashed_pw)
        )

        conn.commit()
        return True

    except:
        return False

    finally:
        conn.close()

def check_login(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    hashed_pw = hash_password(password)

    cursor.execute(
        "SELECT * FROM login_info WHERE username=? AND password=?",
        (username, hashed_pw)
    )

    result = cursor.fetchone()
    conn.close()

    return result is not None

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, username FROM login_info")
    data = cursor.fetchall()

    conn.close()
    return data