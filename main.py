import sys
from PyQt5 import QtWidgets
from logic.login import LoginWindow
from logic.signup import SignupWindow
from logic.ds import DSWindow
# Import thêm MenuWindow nếu bạn đã tách nó ra

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Tạo QStackedWidget để chứa các trang
    widget = QtWidgets.QStackedWidget()
    
    # Khởi tạo các cửa sổ và truyền 'widget' vào để các cửa sổ tự chuyển trang được
    login_screen = LoginWindow(widget)
    signup_screen = SignupWindow(widget)
    ds_screen = DSWindow(widget) 
    
    widget.addWidget(login_screen)   # Index 0
    widget.addWidget(signup_screen)  # Index 1
    widget.addWidget(ds_screen)  # Index 2
    
    widget.show()
    sys.exit(app.exec_())