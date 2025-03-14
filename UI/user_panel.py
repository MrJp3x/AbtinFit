from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class UserPanel(QWidget):
    """User management panel"""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel("User Management Panel")
        layout.addWidget(label)

        self.setLayout(layout)
