import sqlite3
import os

# Thiết lập đường dẫn đến database của mày
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "shop_data.db")

def fix_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Đang cập nhật Database...")
    
    # 1. Xóa bảng products cũ (Lưu ý: Việc này sẽ xóa các món mày đã thêm trước đó)
    cursor.execute("DROP TABLE IF EXISTS products")

    # 2. Tạo lại bảng products với cấu trúc chuẩn có label_id
    cursor.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label_id TEXT UNIQUE,      -- Cột định danh vị trí ô trên Menu
            name TEXT,                 -- Tên món ăn
            category TEXT,             -- Loại (Cà phê, Trà...)
            price INTEGER,             -- Giá bán
            image_name TEXT            -- Tên file ảnh lưu trong assets
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Đã cập nhật bảng products thành công!")

if __name__ == "__main__":
    fix_database()