from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableView, QPushButton,
    QLineEdit, QHBoxLayout, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt, QAbstractTableModel, Slot
from PySide6.QtGui import QFont
from UI.add_user_dialog import AddUserDialog


class UserTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = ["ID", "نام", "نام خانوادگی", "شماره تلفن", "سن", "جنسیت", "تاریخ تولد"]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        return None


class UserPanel(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()

        # جستجو
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 جستجو بر اساس نام یا نام خانوادگی...")
        self.search_input.setStyleSheet("font-size: 13px; padding: 8px;")
        self.search_input.textChanged.connect(self._load_users)

        # جدول کاربران
        self.table = QTableView()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableView {
                font-size: 13px;
                alternate-background-color: #f9f9f9;
            }
            QHeaderView::section {
                background-color: #e0e0e0;
                padding: 8px;
                font-size: 14px;
            }
        """)

        # دکمه‌های مدیریت
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("➕ افزودن کاربر")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        self.add_btn.clicked.connect(self._show_add_dialog)

        self.delete_btn = QPushButton("🗑️ حذف کاربر")
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        self.delete_btn.clicked.connect(self._delete_user)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.delete_btn)

        layout.addWidget(self.search_input)
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self._load_users()

    @Slot()
    def _load_users(self):
        users = self.db_manager.get_users()
        search_term = self.search_input.text().strip().lower()

        filtered = [
            [u["id"], u["first_name"], u["last_name"], u["phone"], u["age"], u["gender"], u["birth_date"]]
            for u in users if search_term in (u["first_name"] + u["last_name"]).lower()
        ]

        model = UserTableModel(filtered)
        self.table.setModel(model)

    def _show_add_dialog(self):
        dialog = AddUserDialog(self.db_manager, self)
        dialog.exec_()
        self._load_users()

    def _delete_user(self):
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "خطا", "لطفاً یک کاربر را انتخاب کنید!")
            return

        user_id = int(self.table.model()._data[selected[0].row()][0])
        self.db_manager.delete_user(user_id)
        self._load_users()