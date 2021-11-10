from PySide6.QtWidgets import QMessageBox, QDialog
from PySide6.QtGui import QIcon
from gms_uploader.ui.validation_dialog import Ui_Dialog as UI_Dialog_Validation


class ValidationDialog(QDialog, UI_Dialog_Validation):
    def __init__(self, test_list):
        super(ValidationDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Validation errors")
        self.setWindowIcon(QIcon('icons/GMS-logo.png'))
        self.textEdit.setReadOnly(True)
        self.textEdit.setPlainText("\n".join(test_list))
        self.pushButton.clicked.connect(self.close)


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
        self.setWindowTitle("Alert")
        self.setWindowIcon(QIcon('icons/arrow-up.png'))




