from PyQt5 import QtWidgets, QtCore
from datetime import datetime
from logic.hoadon_ui import Ui_Form 

class HoadonWindow(QtWidgets.QWidget):
    def __init__(self, items, total_amount, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # Cửa sổ popup
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowCloseButtonHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowTitle("Hóa đơn thanh toán")

        # 1. Cập nhật thời gian
        now = datetime.now()
        self.ui.label_time.setText(f"Thời gian: {now.strftime('%H:%M %d/%m/%Y')}")

        # 2. Đổ dữ liệu vào bảng
        self.ui.table_bill.setRowCount(0)
        self.ui.table_bill.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        for item in items:
            row_pos = self.ui.table_bill.rowCount()
            self.ui.table_bill.insertRow(row_pos)
            self.ui.table_bill.setItem(row_pos, 0, QtWidgets.QTableWidgetItem(item['name']))
            self.ui.table_bill.setItem(row_pos, 1, QtWidgets.QTableWidgetItem(str(item['qty'])))
            self.ui.table_bill.setItem(row_pos, 2, QtWidgets.QTableWidgetItem(f"{item['price']:,}"))
            self.ui.table_bill.setItem(row_pos, 3, QtWidgets.QTableWidgetItem(f"{item['total']:,}"))

        # 3. Hiển thị tổng tiền (chỉ dùng những gì có sẵn trong UI)
        self.ui.total_money.setText(f"{total_amount:,} VND")

        # 4. Thông báo thành công
        QtWidgets.QMessageBox.information(self, "Thanh toán", "Thanh toán thành công!")

        # 5. Kết nối nút
        self.ui.btn_close.clicked.connect(self.close)
        self.ui.btn_print.clicked.connect(self.print_invoice)

    def print_invoice(self):
        """Giả lập in hóa đơn"""
        QtWidgets.QMessageBox.information(self, "In hóa đơn", 
            "Đã gửi lệnh in đến máy in nhiệt thành công!\nCảm ơn quý khách!")
        self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    test_items = [
        {'name': 'Cafe Đen', 'qty': 2, 'price': 25000, 'total': 50000},
        {'name': 'Bạc Xỉu', 'qty': 1, 'price': 35000, 'total': 35000}
    ]
    win = HoadonWindow(test_items, 85000)
    win.show()
    sys.exit(app.exec_())