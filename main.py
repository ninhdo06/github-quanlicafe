from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import sys
import sqlite3 as mdb
from database import create_table, register_user, check_login

#Cua so login
class Signin_w(QMainWindow):
    def __init__(self):
        super(Signin_w, self).__init__()
        uic.loadUi('fixed.ui', self)
        self.b1.clicked.connect(self.loginapp)
        self.b2.clicked.connect(self.signup_x)
    def signup_x(self) :
        widget.setCurrentIndex(1)
    def loginapp(self) :
        un = self.user_name.text()
        psw = self.password.text()
        if check_login(un, psw) : 
            widget.setCurrentIndex(2)
        else: 
            QMessageBox.warning(self, "Loi", "Sai tai khoan hoac mat khau")
class Signup_w(QMainWindow):
    def __init__(self):
        super(Signup_w, self).__init__()
        uic.loadUi('taomoi.ui', self)
        self.b3.clicked.connect(self.signup)
    def signup(self) : 
        un = self.nw_name.text() 
        psw = self.nw_pass.text() 
        if register_user(un, psw) : 
            QMessageBox.information(self, "Ok", "Dang ky thanh cong") 
            widget.setCurrentIndex(0)
        else: 
            QMessageBox.warning(self, "loi", "tai khoan da ton tai")
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