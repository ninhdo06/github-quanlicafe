# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 600)
        self.vboxlayout = QtWidgets.QVBoxLayout(Form)
        self.vboxlayout.setObjectName("vboxlayout")
        
        # Tên quán
        self.label_shop = QtWidgets.QLabel(Form)
        self.label_shop.setAlignment(QtCore.Qt.AlignCenter)
        self.label_shop.setObjectName("label_shop")
        self.vboxlayout.addWidget(self.label_shop)
        
        # Địa chỉ
        self.label_address = QtWidgets.QLabel(Form)
        self.label_address.setAlignment(QtCore.Qt.AlignCenter)
        self.label_address.setObjectName("label_address")
        self.vboxlayout.addWidget(self.label_address)
        
        # Thời gian
        self.label_time = QtWidgets.QLabel(Form)
        self.label_time.setAlignment(QtCore.Qt.AlignCenter)
        self.label_time.setObjectName("label_time")
        self.vboxlayout.addWidget(self.label_time)
        
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.HLine)
        self.frame.setObjectName("frame")
        self.vboxlayout.addWidget(self.frame)
        
        # Bảng hóa đơn
        self.table_bill = QtWidgets.QTableWidget(Form)
        self.table_bill.setObjectName("table_bill")
        self.table_bill.setColumnCount(4)
        self.table_bill.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_bill.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_bill.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_bill.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_bill.setHorizontalHeaderItem(3, item)
        self.vboxlayout.addWidget(self.table_bill)
        
        # Phần tính tiền
        self.vboxlayout1 = QtWidgets.QVBoxLayout()
        self.hboxlayout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(Form)
        self.label.setText("Tổng tiền:")
        self.total_money = QtWidgets.QLabel(Form)
        self.total_money.setAlignment(QtCore.Qt.AlignRight)
        self.hboxlayout.addWidget(self.label)
        self.hboxlayout.addWidget(self.total_money)
        self.vboxlayout1.addLayout(self.hboxlayout)
        
        self.vboxlayout.addLayout(self.vboxlayout1)
        
        # Nút bấm
        self.hboxlayout3 = QtWidgets.QHBoxLayout()
        self.btn_print = QtWidgets.QPushButton(Form)
        self.btn_print.setText("In hóa đơn")
        self.hboxlayout3.addWidget(self.btn_print)
        self.btn_close = QtWidgets.QPushButton(Form)
        self.btn_close.setText("Đóng")
        self.hboxlayout3.addWidget(self.btn_close)
        self.vboxlayout.addLayout(self.hboxlayout3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Hóa đơn thanh toán"))
        self.label_shop.setText(_translate("Form", "☕ Lê La Coffee"))
        self.label_shop.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.label_address.setText(_translate("Form", "Địa chỉ: Hà Nội"))
        self.table_bill.horizontalHeaderItem(0).setText(_translate("Form", "Món"))
        self.table_bill.horizontalHeaderItem(1).setText(_translate("Form", "SL"))
        self.table_bill.horizontalHeaderItem(2).setText(_translate("Form", "Giá"))
        self.table_bill.horizontalHeaderItem(3).setText(_translate("Form", "TT"))