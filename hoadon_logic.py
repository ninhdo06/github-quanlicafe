import os
from PyQt5 import QtWidgets, uic, QtCore
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class BillWindow(QtWidgets.QWidget):
    def __init__(self, data, total_amount, table_name):
        super().__init__()
        # Load file hoadon.ui của mày
        uic.loadUi(os.path.join(BASE_DIR, 'view', 'hoadon.ui'), self)
        
        self.setWindowTitle(f"Hóa đơn - {table_name}")
        
        # 1. Cập nhật thông tin chung
        self.label_time.setText(f"Thời gian: {datetime.now().strftime('%H:%M %d/%m/%Y')}")
        self.total_money.setText(total_amount)
        
        # 2. Đổ dữ liệu vào table_bill
        self.table_bill.setRowCount(0)
        for row_data in data:
            row_idx = self.table_bill.rowCount()
            self.table_bill.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table_bill.setItem(row_idx, col_idx, item)

        # 3. Kết nối nút bấm
        self.btn_close.clicked.connect(self.close)
        self.btn_print.clicked.connect(self.print_fake) # Chức năng in giả lập

    def print_fake(self):
        QtWidgets.QMessageBox.information(self, "Thông báo", "Đang kết nối máy in... \nHóa đơn đã được gửi đi!")
        self.close()