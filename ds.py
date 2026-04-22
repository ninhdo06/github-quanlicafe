# logic/ds.py
import os
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMessageBox
from logic.themmon import ThemMonWindow # Nhớ import class này vào

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class DSWindow(QtWidgets.QMainWindow):
    def __init__(self, parent_widget):
        super().__init__()
        self.widget = parent_widget
        self.used_tables = set()  # Lưu các bàn đang dùng
        
        # 1. Load UI
        ui_path = os.path.join(BASE_DIR, 'view', 'danhsachban.ui')
        uic.loadUi(ui_path, self)
            
        # 2. Kết nối tất cả các nút bàn
        self.connect_table_buttons()
        
        # 3. Kết nối các nút sidebar và nút chức năng
        if hasattr(self, 'btn_logout'):
            self.btn_logout.clicked.connect(self.go_to_menu)
        if hasattr(self, 'btn_ban'):
            self.btn_ban.clicked.connect(self.go_to_hoadon)
        if hasattr(self, 'btn_tk'):
            self.btn_tk.clicked.connect(self.go_to_thongke)

        # --- PHẦN THÊM MỚI: Nút mở cửa sổ Thêm món ---
        # Đảm bảo trong Designer mày đã đặt ObjectName là btn_them_mon
        if hasattr(self, 'btn_them_mon'):
            self.btn_them_mon.clicked.connect(self.open_them_mon)
        # ----------------------------------------------

    def open_them_mon(self):
        """Hàm mở cửa sổ thêm món mới"""
        # Truyền self vào để sau khi lưu xong nó có thể tự refresh Menu
        self.them_mon_win = ThemMonWindow(parent_menu=self)
        self.them_mon_win.show()

    def connect_table_buttons(self):
        """Kết nối tất cả nút bàn 01 đến 10"""
        for i in range(1, 11):
            btn_name = f"btn_{i:02d}"  # btn_01, btn_02, ...
            if hasattr(self, btn_name):
                btn = getattr(self, btn_name)
                btn.clicked.connect(lambda checked, num=i: self.open_table(num))

    def open_table(self, table_num):
        """Xử lý khi bấm vào bàn"""
        menu_screen = self.widget.widget(3)          # lấy màn hình Menu
        menu_screen.load_table(str(table_num))       # 👈 Tải giỏ hàng của bàn đó
    
        # Đánh dấu bàn đang dùng (nếu chưa)
        if table_num not in self.used_tables:
            self.used_tables.add(table_num)
            self.update_table_status()
    
        # Đổi màu bàn thành đỏ
        btn_name = f"btn_{table_num:02d}"
        if hasattr(self, btn_name):
            btn = getattr(self, btn_name)
            btn.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 10px; padding: 10px;")
    
        # Chuyển sang màn hình Menu
        self.widget.setCurrentIndex(3)

    def update_table_status(self):
        """Cập nhật text Đang dùng: x/10"""
        count = len(self.used_tables)
        if hasattr(self, 'label_2'):
            self.label_2.setText(f"Đang dùng: {count}/10")

    def go_to_menu(self):
        self.widget.setCurrentIndex(3)

    def go_to_hoadon(self):
        self.widget.setCurrentIndex(4)
        tk_screen = self.widget.widget(4)
        if hasattr(tk_screen, 'load_history'):
            tk_screen.load_history()
    
    # Tùy chọn: Thông báo cho người dùng
    # QtWidgets.QMessageBox.information(self, "Hóa đơn", "Đang xem danh sách hóa đơn gần nhất")

    def go_to_thongke(self):
        self.widget.setCurrentIndex(5)

    def release_table(self, table_num):
        """Đưa bàn về trạng thái trống (màu nâu/gốc) sau khi thanh toán"""
        try:
            # Xử lý lấy số ID bàn từ chuỗi hoặc số
            table_id = int(''.join(filter(str.isdigit, str(table_num))))

            if table_id in self.used_tables:
                self.used_tables.remove(table_id)
            
            btn_name = f"btn_{table_id:02d}"
            if hasattr(self, btn_name):
                btn = getattr(self, btn_name)
                btn.setStyleSheet("background-color: #5a2d0c; color: white; border-radius: 10px; padding: 10px;")
            
            self.update_table_status()
        except Exception as e:
            print(f"Lỗi khi giải phóng bàn: {e}")
        


# ====================== PHẦN CODE TỰ ĐỘNG ======================
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        pass

    def retranslateUi(self, MainWindow):
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())