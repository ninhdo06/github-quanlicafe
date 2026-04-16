import sys
from PyQt5 import QtWidgets
from logic.login import LoginWindow
from logic.signup import SignupWindow
from logic.ds import DSWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Tạo QStackedWidget để chứa các trang
    widget = QtWidgets.QStackedWidget()
    
    # Khởi tạo các cửa sổ và truyền 'widget' vào để các cửa sổ tự chuyển trang được
    login_screen = LoginWindow(widget)
    signup_screen = SignupWindow(widget)
    ds_screen = DSWindow(widget) 
    
    # Thêm các trang vào widget theo thứ tự index
    widget.addWidget(login_screen)   # Index 0
    widget.addWidget(signup_screen)  # Index 1
    widget.addWidget(ds_screen)      # Index 2 (Đây là màn hình sau khi Login)
    
    # Thiết lập kích thước mặc định và hiển thị
    widget.setMinimumSize(800, 600)
    widget.setWindowTitle("Hệ thống Quản lý Cafe")
    widget.show()
    
    # Chạy ứng dụng
    sys.exit(app.exec_())