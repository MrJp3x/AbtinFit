from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QTextEdit,
    QPushButton, QLabel, QHBoxLayout, QMessageBox,
    QListWidgetItem, QCheckBox
)
from PySide6.QtCore import Qt, QThread, Signal
from DataBase.database import DatabaseManager
from services.ippanel_service import IPPANELService


class SMSWorker(QThread):
    finished = Signal(bool, str)
    progress = Signal(int)

    def __init__(self, phone_numbers, message, api_key):
        super().__init__()
        self.phone_numbers = phone_numbers
        self.message = message
        self.api_key = api_key

    def run(self):
        try:
            sms_service = IPPANELService(self.api_key)
            total = len(self.phone_numbers)
            for i, number in enumerate(self.phone_numbers):
                sms_service.send_sms("+9810001", [number], self.message)
                self.progress.emit(int((i + 1) / total * 100))
            self.finished.emit(True, "پیام‌ها با موفقیت ارسال شدند!")
        except Exception as e:
            self.finished.emit(False, f"خطا: {str(e)}")


class SmsPanel(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.selected_users = []
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # لیست کاربران با چک‌باکس
        self.users_list = QListWidget()
        self._load_users()

        # ویرایشگر متن پیام
        self.message_editor = QTextEdit()
        self.message_editor.setPlaceholderText("متن پیام خود را وارد کنید...")
        self.message_editor.setMinimumHeight(150)

        # دکمه ارسال
        self.send_btn = QPushButton("📤 ارسال پیامک")
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 12px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.send_btn.clicked.connect(self._send_sms)

        # نوار پیشرفت
        self.progress_label = QLabel("آماده برای ارسال")
        self.progress_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(QLabel("انتخاب دریافت‌کنندگان:"))
        layout.addWidget(self.users_list)
        layout.addWidget(QLabel("متن پیام:"))
        layout.addWidget(self.message_editor)
        layout.addWidget(self.progress_label)
        layout.addWidget(self.send_btn)

        self.setLayout(layout)

    def _load_users(self):
        self.users_list.clear()
        users = self.db_manager.get_users()
        for user in users:
            item = QListWidgetItem()
            widget = QWidget()
            checkbox = QCheckBox(f"{user['first_name']} {user['last_name']} - {user['phone']}")

            # تغییر در اتصال سیگنال
            checkbox.toggled.connect(lambda checked, u=user: self._toggle_user(u, checked))

            layout = QHBoxLayout(widget)
            layout.addWidget(checkbox)
            layout.setContentsMargins(0, 0, 0, 0)
            widget.setLayout(layout)
            self.users_list.addItem(item)
            self.users_list.setItemWidget(item, widget)

    def _toggle_user(self, user, checked):
        """مدیریت وضعیت انتخاب کاربران"""
        print(f"User {user['id']} - Checked: {checked}")

        if checked:
            if user not in self.selected_users:
                self.selected_users.append(user)
        else:
            self.selected_users = [u for u in self.selected_users if u["id"] != user["id"]]

        # نمایش تعداد کاربران انتخاب شده
        self.progress_label.setText(f"{len(self.selected_users)} کاربر انتخاب شده")
        print(f"Selected users: {[u['id'] for u in self.selected_users]}")

    def _send_sms(self):
        """ارسال پیامک به کاربران انتخاب شده"""
        print(f"Attempting to send to {len(self.selected_users)} users")

        if not self.selected_users:
            QMessageBox.warning(self, "خطا", "لطفاً حداقل یک دریافت‌کننده انتخاب کنید!")
            return

        message = self.message_editor.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "خطا", "لطفاً متن پیام را وارد کنید!")
            return

        # دریافت API Key از تنظیمات (رمزگشایی شده)
        from DataBase.crypto_manager import CryptoManager
        crypto = CryptoManager()
        encrypted_api_key = "your_encrypted_api_key_here"  # باید از config بیاید
        api_key = crypto.decrypt(encrypted_api_key)

        phone_numbers = [u["phone"] for u in self.selected_users]

        # ایجاد نخ برای ارسال
        self.worker = SMSWorker(phone_numbers, message, api_key)
        self.worker.progress.connect(self._update_progress)
        self.worker.finished.connect(self._handle_result)
        self.send_btn.setEnabled(False)
        self.progress_label.setText("در حال ارسال...")
        self.worker.start()

    def _update_progress(self, value):
        self.progress_label.setText(f"پیشرفت: {value}%")

    def _handle_result(self, success, message):
        self.send_btn.setEnabled(True)
        if success:
            QMessageBox.information(self, "موفق", message)
            self.selected_users = []
            self.progress_label.setText("آماده برای ارسال")
        else:
            QMessageBox.critical(self, "خطا", message)
            self.progress_label.setText("خطا در ارسال")