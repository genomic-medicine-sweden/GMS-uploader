from PySide6.QtWidgets import QMessageBox, QFileDialog, QListView, QAbstractItemView, QPushButton, QTreeView, QDialog
from PySide6.QtGui import QIcon
import os
from ui.validation_dialog import Ui_Dialog


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


class ValidationDialog(QDialog, Ui_Dialog):
    def __init__(self, test_list):
        super(ValidationDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Validation errors")
        self.setWindowIcon(QIcon('icons/GMS-logo.png'))
        self.textEdit.setReadOnly(True)
        self.textEdit.setPlainText("\n".join(test_list))
        self.pushButton.clicked.connect(self.close)


    #     btns = self.findChildren(QPushButton)
    #     self.openBtn = [x for x in btns if 'open' in str(x.text()).lower()][0]
    #     self.openBtn.clicked.disconnect()
    #     self.openBtn.clicked.connect(self.openClicked)
    #     self.tree = self.findChild(QTreeView)
    #
    # def openClicked(self):
    #     inds = self.tree.selectionModel().selectedIndexes()
    #     files = []
    #     for i in inds:
    #         if i.column() == 0:
    #             print(i)
    #             files.append(os.path.join(str(self.directory().absolutePath()), str(i.data().toString())))
    #
    #     self.selectedFiles = files
    #     self.hide()
    #
    # def filesSelected(self):
    #     return self.selectedFiles


