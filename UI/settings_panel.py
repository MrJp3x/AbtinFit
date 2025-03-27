from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("پنل تنظیمات (در حال توسعه)")
        layout.addWidget(label)
        self.setLayout(layout)