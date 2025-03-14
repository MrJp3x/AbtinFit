from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
from ui.user_panel import UserPanel
from ui.sms_panel import SmsPanel
from ui.settings_panel import SettingsPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("سامانه مدیریت کاربران و پیامک")  # عنوان پنجره
        self.setGeometry(100, 100, 800, 600)  # موقعیت و اندازه‌ی اولیه

        # ویجت مرکزی
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # لایه‌ی اصلی (QHBoxLayout برای داشتن سایدبار و محتوای اصلی)
        main_layout = QHBoxLayout(central_widget)

        # سایدبار (دکمه‌های تغییر صفحه)
        sidebar = QVBoxLayout()
        self.btn_users = QPushButton("مدیریت کاربران")
        self.btn_sms = QPushButton("ارسال پیامک")
        self.btn_settings = QPushButton("تنظیمات")

        # اضافه کردن دکمه‌ها به سایدبار
        sidebar.addWidget(self.btn_users)
        sidebar.addWidget(self.btn_sms)
        sidebar.addWidget(self.btn_settings)
        sidebar.addStretch()  # پرکردن فضای باقی‌مانده

        # QStackedWidget برای نمایش صفحات مختلف
        self.stack = QStackedWidget()
        self.user_panel = UserPanel()
        self.sms_panel = SmsPanel()
        self.settings_panel = SettingsPanel()

        # اضافه کردن پنل‌ها به QStackedWidget
        self.stack.addWidget(self.user_panel)
        self.stack.addWidget(self.sms_panel)
        self.stack.addWidget(self.settings_panel)

        # اضافه کردن سایدبار و QStackedWidget به لایه‌ی اصلی
        main_layout.addLayout(sidebar, 1)  # سایدبار 1 واحد از فضا را بگیرد
        main_layout.addWidget(self.stack, 4)  # QStackedWidget، چهار برابر سایدبار فضا بگیرد

        # اتصال دکمه‌ها به تغییر صفحات
        self.btn_users.clicked.connect(lambda: self.stack.setCurrentWidget(self.user_panel))
        self.btn_sms.clicked.connect(lambda: self.stack.setCurrentWidget(self.sms_panel))
        self.btn_settings.clicked.connect(lambda: self.stack.setCurrentWidget(self.settings_panel))

