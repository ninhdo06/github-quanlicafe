import sqlite3
import os
from datetime import datetime

# Thiết lập đường dẫn động đến database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "shop_data.db")

def create_table():
    """Khởi tạo toàn bộ cấu trúc Database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Bảng lưu thông tin tài khoản
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # 2. Bảng lịch sử hóa đơn
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

    # 3. Bảng sản phẩm (CẬP NHẬT: Thêm label_id và image_name)
    # Dùng label_id để biết món đó nằm ở ô nào (ví dụ: label_45)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label_id TEXT UNIQUE,
            name TEXT,
            category TEXT,
            price INTEGER,
            image_name TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def save_order(table_name, items_str, total, username="Nhân viên"):
    """Lưu hóa đơn vào lịch sử sau khi thanh toán"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    order_id = datetime.now().strftime("%Y%m%d%H%M%S")
    order_time = datetime.now().strftime("%d/%m/%Y %H:%M")

    cursor.execute("""
        INSERT INTO orders_history 
        (order_id, table_name, order_time, items, total, username)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (order_id, table_name, order_time, items_str, total, username))
    
    conn.commit()
    conn.close()
    return order_id

if __name__ == "__main__":
    create_table()
    print(f"✅ Database initialized at: {DB_PATH}")