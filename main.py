from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import sqlite3
from shop_data import create_table, register_user, check_login

#Cua so login
class Signin_w(QMainWindow):
    def __init__(self):
        super(Signin_w, self).__init__()
        uic.loadUi('fixed.ui', self)
        self.b1.clicked.connect(self.loginapp)
        self.b2.clicked.connect(self.signup_x)
    def signup_x(self) :
        widget.setCurrentIndex(1)
    def loginapp(self):
        un = self.name.text()
        psw = self.password.text()
        if len(un) == 0 or len(psw) == 0:
            self.error.setText("Nhap day du thong tin.")
            return
        conn = sqlite3.connect("shop_data.db")
        cur = conn.cursor()
        cur.execute("SELECT password FROM login_info WHERE username = ?", (un,))
        result = cur.fetchone()
        if result is None:
            self.error.setText("Username không tồn tại")
        elif result[0] == psw:
            widget.setCurrentIndex(2)
        else:
            self.error.setText("Sai mật khẩu")
        conn.close()
class Signup_w(QMainWindow): 
    def __init__(self): 
        super(Signup_w, self).__init__()
        uic.loadUi('taomoi.ui', self)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.cf_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.b3.clicked.connect(self.signup) 
    def signup(self): 
        un = self.name.text() 
        psw = self.password.text() 
        cf = self.cf_password.text() 

        if len(un) == 0 or len(psw) == 0 or len(cf) == 0:
            self.error.setText("Nhap day du thong tin.")
        elif psw != cf: 
            self.error.setText("Sai mat khau.") 
        else: 
            try:
                with sqlite3.connect("shop_data.db") as conn:
                    cur = conn.cursor()
                    cur.execute(
                        'INSERT INTO login_info (username, password) VALUES (?,?)',
                        (un, psw)
                    )

                self.error.setText("Đăng ký thành công")
                widget.setCurrentIndex(0)

            except sqlite3.IntegrityError:
                self.error.setText("Username đã tồn tại")
class chinh_w(QMainWindow):
    def __init__(self):
        super(chinh_w, self).__init__()
        uic.loadUi('anh.ui', self)
#xuli
app= QApplication(sys.argv)
create_table()
widget= QtWidgets.QStackedWidget()
Signin_f= Signin_w()
Signup_f= Signup_w()
chinh_f = chinh_w()
widget.addWidget(Signin_f)
widget.addWidget(Signup_f)
widget.addWidget(chinh_f)
widget.setCurrentIndex(0)
widget.show()
app.exec()