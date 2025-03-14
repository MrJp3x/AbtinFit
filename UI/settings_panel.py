from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class SettingsPanel(QWidget):
    """Settings panel"""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel("Settings Panel")
        layout.addWidget(label)

        self.setLayout(layout)
