from PyQt5 import QtCore,QtGui,QtWidgets, uic
from PyQt5.QtWidgets import * 
from PyQt5.uic import loadUi
import sys
import sqlite3
from database import create_table, register_user, check_login

#Cua so login
class Login_w(QMainWindow):
    def __init__(self):
        super(Login_w, self).__init__()
        uic.loadUi('login.ui', self)
        self.login.clicked.connect(self.signin)
        self.b2.clicked.connect(self.reg_form)
    
    def reg_form(self) :
        widget.setCurrentIndex(1) 

    def signin(self) :
        un = self.user_name.text()
        psw = self.password.text()
        if check_login(un, psw) :
            widget.setCurrentIndex(2)
        else:
            QMessageBox.warning(self, "Loi", "Sai tai khoan hoac mat khau")


class tao_moi(QMainWindow) :
    def __init__(self):
        super(tao_moi, self).__init__()
        uic.loadUi('taomoi.ui', self)
        self.b3.clicked.connect(self.signup)
    
    def signup(self) :
        un = self.dn_m.text()
        psw = self.mk_m.text()
        if register_user(un, psw) :
            QMessageBox.information(self, "Ok", "Dang ky thanh cong")
            widget.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "loi", "tai khoan da ton tai")

class chinh_w(QMainWindow) :
    def __init__(self):
        super(chinh_w, self).__init__()
        uic.loadUi('chinh.ui', self)
#Xuli:
app=QApplication(sys.argv)
create_table()
widget=QtWidgets.QStackedWidget()
Login_f= Login_w()
tao_f = tao_moi()
chinh_f = chinh_w()
widget.addWidget(Login_f)
widget.addWidget(tao_f)
widget.addWidget(chinh_f)
widget.setCurrentIndex(0)
widget.show()
widget.setFixedHeight(700)
widget.setFixedWidth(690)
app.exec()
