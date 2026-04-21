# logic/themmon.py
import os
import sqlite3
import shutil
from datetime import datetime
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox

# Thiết lập đường dẫn động
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DB_PATH = os.path.join(BASE_DIR, "database", "shop_data.db")

class ThemMonWindow(QtWidgets.QMainWindow):
    def __init__(self, parent_menu=None):
        super().__init__()
        self.parent_menu = parent_menu
        self.image_path = ""

        # 1. Load giao diện từ file .ui
        ui_path = os.path.join(BASE_DIR, 'view', 'themmon.ui')
        uic.loadUi(ui_path, self)

        # 2. TỰ ĐỘNG ĐỔ TẤT CẢ LABEL TỪ GIAO DIỆN MENU VÀO COMBOBOX
        if hasattr(self, 'cb_label'):
            self.cb_label.clear()
            try:
                # Import file test.py (nơi chứa toàn bộ object giao diện menu)
                from logic.test import Ui_MainWindow
                temp_ui = Ui_MainWindow()
                
                # Tìm tất cả các thuộc tính có tên bắt đầu bằng "label_"
                all_labels = [attr for attr in dir(temp_ui) if attr.startswith("label_")]
                
                # Sắp xếp danh sách theo số thứ tự (label_1, label_2, label_10...) 
                # để mày tìm cho dễ, không bị lộn xộn theo bảng chữ cái
                all_labels.sort(key=lambda x: int(x.split('_')[1]) if x.split('_')[1].isdigit() else 0)
                
                if all_labels:
                    self.cb_label.addItems(all_labels)
                else:
                    # Nếu không tìm thấy label_ nào thì dùng tạm list dự phòng
                    labels = [f"label_{i}" for i in range(1, 101)]
                    self.cb_label.addItems(labels)
                    
            except Exception as e:
                print(f"Lỗi quét label: {e}")
                # Nếu lỗi import thì tự đổ 100 cái cho chắc ăn
                labels = [f"label_{i}" for i in range(1, 101)]
                self.cb_label.addItems(labels)

        # 3. Kết nối sự kiện nút bấm
        # Nút "Thêm ảnh"
        if hasattr(self, 'btnThemAnh'):
            self.btnThemAnh.clicked.connect(self.choose_image)
        
        # Nút "Thêm món" (Lưu)
        if hasattr(self, 'btnThemAnh_2'):
            self.btnThemAnh_2.clicked.connect(self.save_product)

    def choose_image(self):
        """Mở hộp thoại chọn ảnh cho món mới"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Chọn ảnh món", "", "Images (*.png *.jpg *.jpeg *.webp)"
        )
        if file_path:
            self.image_path = file_path
            pixmap = QtGui.QPixmap(file_path)
            # Hiển thị ảnh xem trước, giữ tỉ lệ khung hình
            if hasattr(self, 'preview'):
                self.preview.setPixmap(pixmap.scaled(self.preview.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
                self.preview.setScaledContents(True)

    def save_product(self):
        """Lưu món mới, copy ảnh vào assets và đồng bộ với Menu"""
        # Lấy dữ liệu từ giao diện
        ten = self.tenSanPham.text().strip()
        loai = self.loaiSanPham.currentText()
        gia_text = self.giaBan.text().strip()
        
        # FIX LỖI: Lấy label_id từ ComboBox cb_label mày đã thêm trong Designer
        if hasattr(self, 'cb_label'):
            label_id = self.cb_label.currentText()
        else:
            QMessageBox.critical(self, "Lỗi UI", "Không tìm thấy ô chọn vị trí (cb_label)!")
            return

        # 1. Kiểm tra thông tin đầu vào
        if not ten or not gia_text or not self.image_path:
            QMessageBox.warning(self, "Thiếu thông tin", "Mày phải nhập đủ Tên, Giá và chọn Ảnh món!")
            return

        try:
            # Xử lý định dạng giá (bỏ dấu chấm/phẩy nếu có)
            gia = int(gia_text.replace(',', '').replace('.', ''))
            
            # 2. XỬ LÝ ẢNH CHUYÊN NGHIỆP: Đặt tên ảnh theo label_id để Menu tự nhận
            ext = os.path.splitext(self.image_path)[1] # Lấy đuôi file .jpg, .png...
            new_image_name = f"{label_id}{ext}"
            target_assets_path = os.path.join(ASSETS_DIR, new_image_name)
            
            # Đảm bảo thư mục assets tồn tại
            if not os.path.exists(ASSETS_DIR):
                os.makedirs(ASSETS_DIR)
                
            # Copy ảnh vào folder assets (ghi đè nếu đã có ảnh cũ ở label đó)
            shutil.copy(self.image_path, target_assets_path)

            # 3. LƯU VÀO DATABASE
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Sử dụng INSERT OR REPLACE: Nếu label_id đã tồn tại món cũ, nó sẽ xóa và đè món mới lên
            cursor.execute("""
                INSERT OR REPLACE INTO products (label_id, name, category, price, image_name)
                VALUES (?, ?, ?, ?, ?)
            """, (label_id, ten, loai, gia, new_image_name))
            
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Thành công", f"Đã cập nhật món '{ten}' vào vị trí {label_id}!")

            # 4. ĐỒNG BỘ VỚI MENU: Gọi hàm cập nhật lại giao diện Menu ngay lập tức
            # Giả sử màn hình Menu là widget thứ 3 trong StackedWidget
            if self.parent_menu and hasattr(self.parent_menu, 'widget'):
                menu_screen = self.parent_menu.widget.widget(3)
                if hasattr(menu_screen, 'update_menu_from_db'):
                    menu_screen.update_menu_from_db()

            self.close() 

        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Giá bán phải là số nguyên!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Hệ thống", f"Không thể lưu: {str(e)}")