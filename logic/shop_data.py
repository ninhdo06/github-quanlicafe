import sqlite3
from datetime import datetime

DB_NAME = "shop_data.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Bảng login
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Bảng lịch sử hóa đơn
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT,
            table_name TEXT,
            order_time TEXT,
            items TEXT,
            total INTEGER,
            username TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_order(table_name, orders_dict, total, username="Nhân viên"):
    """Lưu hóa đơn sau khi thanh toán"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    order_id = datetime.now().strftime("%Y%m%d%H%M%S")
    order_time = datetime.now().strftime("%d/%m/%Y %H:%M")
    items_str = " | ".join([f"{name} x{qty}" for name, (_, _, qty) in orders_dict.items()])

    cursor.execute("""
        INSERT INTO orders_history 
        (order_id, table_name, order_time, items, total, username)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (order_id, table_name, order_time, items_str, total, username))
    
    conn.commit()
    conn.close()
    return order_id