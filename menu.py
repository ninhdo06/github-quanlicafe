import os
import sqlite3
import datetime
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QPixmap

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DB_PATH = os.path.join(BASE_DIR, "database", "shop_data.db")
from logic.test import Ui_MainWindow

class MenuWindow(QtWidgets.QMainWindow):
    def __init__(self, parent_widget=None):
        super().__init__()
        self.widget = parent_widget
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 1. Quản lý giỏ hàng: 
        # Vì bạn đã đưa bảng ra ngoài Tab, chúng ta dùng 1 danh sách duy nhất cho bàn hiện tại
        self.carts = {}
        self.current_table_num = "1" 
        self.current_cart = [] # Danh sách món ăn của bàn đang chọn

        # 2. Khởi tạo giao diện và dữ liệu
        self.update_menu_from_db()
        self.refresh_cart_display()
        self.load_table(self.current_table_num)
        # 3. Kết nối các nút chức năng
        # Nút chuyển về màn hình chính (nếu có)
        if hasattr(self.ui, 'pushButton'):
            self.ui.pushButton.clicked.connect(lambda: self.widget.setCurrentIndex(2))
        
        # Kết nối nút thanh toán mới
        if hasattr(self.ui, 'btn_thanhtoan_1'):
            # Ngắt kết nối cũ nếu có để tránh chạy 2 lần
            try: self.ui.btn_thanhtoan_1.clicked.disconnect()
            except: pass
            self.ui.btn_thanhtoan_1.clicked.connect(self.process_payment)

        # Tự động kết nối các nút món ăn trong các Tab
        self.auto_connect_menu_buttons()

    # ====================== THÊM MÓN ======================
     # ------------------ THÊM PHƯƠNG THỨC load_table ------------------
    def load_table(self, table_num):
        """Tải giỏ hàng của bàn table_num lên giao diện"""
        table_num = str(table_num)
        self.current_table_num = table_num
        
        # Nếu bàn chưa có giỏ hàng thì tạo mới
        if table_num not in self.carts:
            self.carts[table_num] = []
        
        # Trỏ current_cart vào đúng giỏ hàng của bàn
        self.current_cart = self.carts[table_num]
        
        # Cập nhật hiển thị bảng và tổng tiền
        self.refresh_cart_display()

    def make_add_to_cart(self, name, price):
        return lambda: self.add_to_cart(name, price)
    def add_to_cart(self, name, price):
        """Thêm món và cập nhật ngay lập tức"""
        found = False
        for item in self.current_cart:
            if item['name'] == name:
                item['qty'] += 1
                found = True
                break
        
        if not found:
            self.current_cart.append({'name': name, 'qty': 1, 'price': price})

        # Sau khi thay đổi dữ liệu, phải gọi hàm vẽ lại bảng và tính tổng
        self.carts[self.current_table_num] = self.current_cart
        self.refresh_cart_display()

    def refresh_cart_display(self):
        """Cập nhật dữ liệu lên bảng và nhãn tổng tiền"""
        table = self.ui.tableWidget 
        table.setRowCount(0)
        total_bill = 0

        for item in self.current_cart:
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(item['name']))
            table.setItem(row, 1, QTableWidgetItem(str(item['qty'])))
            table.setItem(row, 2, QTableWidgetItem(f"{item['price']:,}"))
            
            line_total = item['qty'] * item['price']
            table.setItem(row, 3, QTableWidgetItem(f"{line_total:,}"))
            total_bill += line_total

        # Cập nhật số tiền vào nhãn lblTotal_2 (hoặc lblTotal tùy file UI)
        # Kiểm tra xem label nào tồn tại để tránh crash
        label = getattr(self.ui, 'lblTotal_2', getattr(self.ui, 'lblTotal', None))
        if label:
            label.setText(f"TỔNG CỘNG: {total_bill:,} VNĐ")

    # ====================== THANH TOÁN ======================
    def connect_payment_buttons(self):
        payment_btns = [self.ui.btn_thanhtoan_1]
        for btn in payment_btns:
            if btn:
                btn.clicked.connect(self.process_payment)

    # ====================== THANH TOÁN ======================
    def process_payment(self):
        # 1. Kiểm tra giỏ hàng (Sử dụng self.current_cart để đồng bộ với bảng bên phải)
        if not self.current_cart:
            QMessageBox.warning(self, "Lỗi", "Chưa có món nào trong giỏ hàng!")
            return

        items_for_db = []
        total_val = 0

        for item in self.current_cart:
            item_total = item['qty'] * item['price']
            items_for_db.append(f"{item['name']} x{item['qty']}")
            total_val += item_total

        # 2. Lưu vào database
        try:
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS orders_history 
                (order_id TEXT, table_name TEXT, order_time TEXT, items TEXT, total REAL, username TEXT)
            """)

            order_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            cur.execute("""
                INSERT INTO orders_history 
                (order_id, table_name, order_time, items, total, username)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (order_id, f"Bàn {self.current_table_num}", 
                  datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
                  ", ".join(items_for_db), total_val, "Admin"))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Lỗi DB: {e}")
        self.current_cart.clear()
        self.carts[self.current_table_num] = self.current_cart   # đồng bộ lại
        # 3. Thông báo thành công (CHỈ HIỆN 1 LẦN)
        QMessageBox.information(self, "Thanh toán", 
                                f"Thanh toán bàn {self.current_table_num} thành công!\n"
                                f"Tổng tiền: {total_val:,} VNĐ")

        # 4. Giải phóng bàn (đổi màu bàn ở màn hình sơ đồ - Index 2)
        try:
            if self.widget:
                ds_screen = self.widget.widget(2)
                if hasattr(ds_screen, 'release_table'):
                    ds_screen.release_table(self.current_table_num)
        except Exception as e:
            print(f"Lỗi giải phóng bàn: {e}")

        # 5. Reset dữ liệu giỏ hàng
        self.current_cart = []
        # Nếu bạn vẫn dùng biến self.carts cho logic cũ, hãy reset nó luôn
        if hasattr(self, 'carts'):
            self.carts[self.current_table_num] = []
        
        self.refresh_cart_display()

        # 6. QUAY VỀ DANH SÁCH BÀN (Chuyển Index về 2)
        if self.widget:
            self.widget.setCurrentIndex(2)

    # ====================== CÁC HÀM KHÁC ======================
    def update_menu_from_db(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT label_id, name, price, image_name FROM products")
            rows = cur.fetchall()
            conn.close()

            for label_id, name, price, img_name in rows:
                num_part = ''.join(filter(str.isdigit, label_id))
                
                if hasattr(self.ui, label_id):
                    label_obj = getattr(self.ui, label_id)
                    img_path = os.path.join(ASSETS_DIR, img_name).replace('\\', '/')
                    if os.path.exists(img_path):
                        pixmap = QtGui.QPixmap(img_path)
                        scaled = pixmap.scaled(label_obj.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                        label_obj.setPixmap(scaled)
                        label_obj.setScaledContents(True)

                btn_name = f"pushButton_{num_part}"
                if hasattr(self.ui, btn_name):
                    btn_obj = getattr(self.ui, btn_name)
                    btn_obj.setText(f"{name}\n{price:,} VNĐ")
                    btn_obj.raise_()
                    try: btn_obj.clicked.disconnect()
                    except: pass
                    btn_obj.clicked.connect(self.make_add_to_cart(name, price))

        except Exception as e:
            print(f"Lỗi update menu: {e}")

    def load_images_from_assets(self):
        if not os.path.exists(ASSETS_DIR): return
        for file_name in os.listdir(ASSETS_DIR):
            name = os.path.splitext(file_name)[0]
            if hasattr(self.ui, name):
                obj = getattr(self.ui, name)
                if isinstance(obj, QtWidgets.QLabel):
                    pixmap = QPixmap(os.path.join(ASSETS_DIR, file_name))
                    if not pixmap.isNull():
                        scaled = pixmap.scaled(obj.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                        obj.setPixmap(scaled)
                        obj.setAlignment(QtCore.Qt.AlignCenter)

    def auto_connect_menu_buttons(self):
        """Quét và gán sự kiện cho các nút món ăn"""
        for btn in self.findChildren(QtWidgets.QPushButton):
            # Điều kiện: Nút có text chứa giá tiền (có dấu xuống dòng)
            if "\n" in btn.text():
                try:
                    text = btn.text().split("\n")
                    name = text[0].strip()
                    # Lấy số, bỏ dấu chấm
                    price = int(text[1].replace(".", "").replace(",", "").replace("VNĐ", "").strip())
                    
                    try: btn.clicked.disconnect()
                    except: pass
                    btn.clicked.connect(self.make_add_to_cart(name, price))
                except:
                    continue