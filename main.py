import sys
import os
from PyQt5 import QtWidgets, QtCore


# Thiết lập đường dẫn hệ thống
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Import các màn hình cũ
from logic.login import LoginWindow
from logic.signup import SignupWindow
from logic.ds import DSWindow
from logic.menu import MenuWindow
from logic.thongke import CotWindow
from logic.shop_data import create_table

# 1. IMPORT THÊM MÀN HÌNH THỐNG KÊ (HÓA ĐƠN)
# Mày nhớ phải tạo file thongke_logic.py trong thư mục logic nhé
from logic.thongke_logic import RevenueWindow
if __name__ == "__main__":
    # 1. Tạo database/bảng nếu chưa có
    create_table()
    
    app = QtWidgets.QApplication(sys.argv)
    
    # 2. Tạo khung StackedWidget tổng
    widget = QtWidgets.QStackedWidget()
    widget.carts = {}
    for i in range(1, 11):
        widget.carts[str(i)] = []
    # 3. Khởi tạo các màn hình
    login_screen = LoginWindow(widget)
    signup_screen = SignupWindow(widget)
    ds_screen = DSWindow(widget)
    menu_screen = MenuWindow(widget)
    cot_screen = CotWindow(widget)
    # KHỞI TẠO MÀN HÌNH THỐNG KÊ
    tk_screen = RevenueWindow(widget) 
    
    # 4. Thêm vào Stack theo thứ tự Index
    widget.addWidget(login_screen)   # Index 0
    widget.addWidget(signup_screen)  # Index 1
    widget.addWidget(ds_screen)      # Index 2 (Danh sách bàn)
    widget.addWidget(menu_screen)    # Index 3 (Chọn món)
    widget.addWidget(tk_screen)      # Index 4 (Hóa đơn/Thống kê)
    widget.addWidget(cot_screen)     # Index5 cot
    
    # 5. Cấu hình hiển thị cho cái khung tổng
    widget.setMinimumSize(1100, 750)
    widget.setWindowTitle("Hệ thống Quản lý Cafe")
    
    # 6. ÉP HIỆN LOGIN ĐẦU TIÊN
    widget.setCurrentIndex(0) 
    widget.show()

    sys.exit(app.exec_())