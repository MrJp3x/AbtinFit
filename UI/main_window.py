from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QHBoxLayout
from user_panel import UserPanel
from sms_panel import SmsPanel
from settings_panel import SettingsPanel


class MainWindow(QMainWindow):
    """Main window of the application with a sidebar navigation"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SMS Management System")
        self.setGeometry(200, 100, 800, 600)  # Set initial window size

        # Main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Sidebar menu
        self.sidebar = QWidget()
        sidebar_layout = QVBoxLayout(self.sidebar)

        self.btn_users = QPushButton("Users")
        self.btn_sms = QPushButton("Send SMS")
        self.btn_settings = QPushButton("Settings")

        sidebar_layout.addWidget(self.btn_users)
        sidebar_layout.addWidget(self.btn_sms)
        sidebar_layout.addWidget(self.btn_settings)
        sidebar_layout.addStretch()  # Push buttons to the top

        # Stacked widget for switching panels
        self.stacked_widget = QStackedWidget()
        self.user_panel = UserPanel()
        self.sms_panel = SmsPanel()
        self.settings_panel = SettingsPanel()

        self.stacked_widget.addWidget(self.user_panel)
        self.stacked_widget.addWidget(self.sms_panel)
        self.stacked_widget.addWidget(self.settings_panel)

        # Add widgets to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget)

        # Connect buttons to functions
        self.btn_users.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.user_panel))
        self.btn_sms.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.sms_panel))
        self.btn_settings.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.settings_panel))

import sys
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
