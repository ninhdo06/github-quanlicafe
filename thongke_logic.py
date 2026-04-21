import sqlite3
import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from logic.checkhoadon import Ui_MainWindow   # ← Sửa thành checkhoadon

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "shop_data.db")


class RevenueWindow(QtWidgets.QMainWindow):
    def __init__(self, parent_widget):
        super().__init__()
        self.widget = parent_widget
        
        # Sử dụng UI có bảng table_stats
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Kết nối các nút
        self.ui.btn_ban_2.clicked.connect(lambda: self.widget.setCurrentIndex(2))   # Danh sách bàn
        self.ui.btn_ban.clicked.connect(self.load_history)                          # Hóa đơn
        self.ui.btn_tk.clicked.connect(lambda: self.widget.setCurrentIndex(5))                           # Thống kê

        # Load dữ liệu ngay khi mở màn
        self.load_history()

    def load_history(self):
        """Load danh sách hóa đơn vào bảng"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                SELECT order_time, items, total 
                FROM orders_history 
                ORDER BY order_id DESC
            """)
            rows = cur.fetchall()
            conn.close()

            if hasattr(self.ui, 'table_stats'):
                table = self.ui.table_stats
                table.setRowCount(0)

                header = table.horizontalHeader()
                header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

                for row_data in rows:
                    row_idx = table.rowCount()
                    table.insertRow(row_idx)
                    for col_idx, data in enumerate(row_data):
                        if col_idx == 2:   # Cột doanh thu
                            val = f"{int(data):,}" if data else "0"
                        else:
                            val = str(data)
                        
                        item = QtWidgets.QTableWidgetItem(val)
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        table.setItem(row_idx, col_idx, item)

                print(f"✅ Đã load {len(rows)} hóa đơn.")
            else:
                QMessageBox.warning(self, "Lỗi", "Không tìm thấy bảng table_stats!")

        except Exception as e:
            print(f"Lỗi load hóa đơn: {e}")
            QMessageBox.critical(self, "Lỗi", f"Không tải được dữ liệu:\n{e}")