from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class SmsPanel(QWidget):
    """SMS sending panel"""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel("SMS Sending Panel")
        layout.addWidget(label)

        self.setLayout(layout)
