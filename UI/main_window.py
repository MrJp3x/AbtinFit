import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QStackedWidget, QHBoxLayout, QApplication
)
from PySide6.QtGui import QFont
from UI.user_panel import UserPanel
from UI.sms_panel import SmsPanel
from UI.settings_panel import SettingsPanel
from DataBase.database import DatabaseManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self._init_ui()
        self.user_panel.user_added.connect(self.sms_panel.refresh_users)

    def _init_ui(self):
        self.setWindowTitle("نرم‌افزار مدیریت ماساژ")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # سایدبار
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #f5f5f5;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(15)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)

        # دکمه‌های سایدبار
        self.btn_users = QPushButton("👥 مدیریت کاربران")
        self.btn_sms = QPushButton("📤 ارسال پیامک")
        self.btn_settings = QPushButton("⚙️ تنظیمات")

        button_style = """
            QPushButton {
                text-align: right;
                padding: 15px;
                font-family: 'B Nazanin';
                font-size: 16px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """
        for btn in [self.btn_users, self.btn_sms, self.btn_settings]:
            btn.setStyleSheet(button_style)

        sidebar_layout.addWidget(self.btn_users)
        sidebar_layout.addWidget(self.btn_sms)
        sidebar_layout.addWidget(self.btn_settings)
        sidebar_layout.addStretch()

        # پنل‌های اصلی
        self.stacked_widget = QStackedWidget()
        self.user_panel = UserPanel(self.db_manager)
        self.sms_panel = SmsPanel(self.db_manager)
        self.settings_panel = SettingsPanel()

        self.stacked_widget.addWidget(self.user_panel)
        self.stacked_widget.addWidget(self.sms_panel)
        self.stacked_widget.addWidget(self.settings_panel)

        # اتصال دکمه‌ها
        self.btn_users.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_sms.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.btn_settings.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stacked_widget, stretch=1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("B Nazanin", 12)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())