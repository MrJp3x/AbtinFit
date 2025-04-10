from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QMessageBox, QFormLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class AddUserDialog(QDialog):
    def __init__(self, db_manager, parent=None, user_data=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.user_data = user_data
        self.setWindowTitle("➕ افزودن کاربر جدید" if not user_data else "✏️ ویرایش کاربر")
        self.setFixedSize(500, 500)
        self._init_ui()
        if user_data:
            self._populate_fields()

    def _init_ui(self):
        layout = QVBoxLayout()

        # فیلدهای فرم
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.phone = QLineEdit()
        self.phone.setInputMask("99999999999")
        self.age = QLineEdit()
        self.gender = QComboBox()
        self.gender.addItems(["مرد", "زن"])
        self.birth_date = QLineEdit()
        self.birth_date.setPlaceholderText("مثال: 1378-01-01")

        # استایل
        widget_style = """
            QLineEdit, QComboBox {
                font-size: 13px;
                padding: 8px;
                min-width: 250px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            QLabel {
                font-size: 14px;
                min-width: 120px;
            }
        """
        self.setStyleSheet(widget_style)

        # فرم لایه‌بندی
        form_layout = QFormLayout()
        form_layout.setFormAlignment(Qt.AlignRight)
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setHorizontalSpacing(20)

        # افزودن فیلدها
        form_layout.addRow(QLabel("نام:"), self.first_name)
        form_layout.addRow(QLabel("نام خانوادگی:"), self.last_name)
        form_layout.addRow(QLabel("شماره تلفن (11 رقمی):"), self.phone)
        form_layout.addRow(QLabel("سن:"), self.age)
        form_layout.addRow(QLabel("جنسیت:"), self.gender)
        form_layout.addRow(QLabel("تاریخ تولد (YYYY-MM-DD):"), self.birth_date)

        # دکمه تأیید
        self.submit_btn = QPushButton("✅ تأیید و ذخیره")
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 25px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.submit_btn.clicked.connect(self._submit)

        layout.addLayout(form_layout)
        layout.addWidget(self.submit_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def _populate_fields(self):
        self.first_name.setText(self.user_data["first_name"])
        self.last_name.setText(self.user_data["last_name"])
        self.phone.setText(self.user_data["phone"])
        self.age.setText(str(self.user_data["age"]))
        self.gender.setCurrentText(self.user_data["gender"])
        self.birth_date.setText(self.user_data["birth_date"])

    def _submit(self):
        data = {
            "first_name": self.first_name.text().strip(),
            "last_name": self.last_name.text().strip(),
            "phone": self.phone.text().strip(),
            "age": self.age.text().strip(),
            "gender": self.gender.currentText(),
            "birth_date": self.birth_date.text().strip()
        }

        # اعتبارسنجی
        errors = []
        if not data["first_name"]:
            errors.append("نام الزامی است")
        if not data["last_name"]:
            errors.append("نام خانوادگی الزامی است")
        if len(data["phone"]) != 11 or not data["phone"].isdigit():
            errors.append("شماره تلفن باید ۱۱ رقمی باشد")
        if not data["age"].isdigit():
            errors.append("سن باید عدد باشد")
        if not data["birth_date"]:
            errors.append("تاریخ تولد الزامی است")

        if errors:
            QMessageBox.warning(self, "خطا", "\n".join(errors))
            return

        try:
            if self.user_data:
                success = self.db_manager.update_user(self.user_data["id"], **data)
                msg = "ویرایش کاربر با موفقیت انجام شد!"
            else:
                success = self.db_manager.add_user(**data)
                msg = "کاربر با موفقیت ثبت شد!"

            if success:
                QMessageBox.information(self, "موفق", msg)
                self.accept()  # تغییر از close() به accept() برای فعال کردن رفرش
        except Exception as e:
            QMessageBox.critical(self, "خطا", f"خطا در عملیات:\n{str(e)}")