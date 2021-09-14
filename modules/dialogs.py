from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QIcon


class MsgError(QMessageBox):
    def __init__(self, msg):
        super().__init__()
        self.setMinimumWidth(700)
        self.setIcon(QMessageBox.Critical)
        self.setText(msg)
        self.setWindowTitle("Error")
        self.setWindowIcon(QIcon('icons/arrow-up.png'))


class MsgAlert(QMessageBox):
    def __init__(self, msg):
        super().__init__()
        self.setMinimumWidth(700)
        self.setIcon(QMessageBox.Warning)
        self.setText(msg)
        self.setWindowTitle("Error")
        self.setWindowIcon(QIcon('icons/arrow-up.png'))

