from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SmsPanel(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("پنل ارسال پیامک (در حال توسعه)")
        layout.addWidget(label)
        self.setLayout(layout)