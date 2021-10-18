from PySide6.QtWidgets import QMessageBox, QDialog, QTableWidgetItem, QProgressBar, QHeaderView
from PySide6.QtGui import QIcon, Qt
from PySide6.QtCore import QThread
from gms_uploader.ui.validation_dialog import Ui_Dialog as UI_Dialog_Validation
from gms_uploader.ui.uploader_dialog import Ui_Dialog as UI_Dialog_Uploader
from gms_uploader.modules.upload import UploadWorker
from pathlib import Path
import json


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


class Uploader(QDialog, UI_Dialog_Uploader):
    def __init__(self, credentials_path, tag, bucket, meta_json, files_list):
        super(Uploader, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Upload")
        self.setWindowIcon(QIcon('icons/GMS-logo.png'))

        self.pushButton_cancel.setDisabled(True)

        self.credentials = json.loads(Path(credentials_path).read_text())

        self.lineEdit_tag.setReadOnly(True)
        self.lineEdit_endpoint.setReadOnly(True)
        self.lineEdit_bucket.setReadOnly(True)

        self.lineEdit_tag.setText(tag)
        self.lineEdit_endpoint.setText(self.credentials['endpoint'])
        self.lineEdit_bucket.setText(bucket)

        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["file", "size", "progress"])

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        self.progress_bars = {}

        for i, file in enumerate(files_list):

            file_obj = Path(file)
            filename = file_obj.name
            filesize = str(self.bytes_to_megabytes(file_obj.stat().st_size)) + " MB"

            self.progress_bars[file] = QProgressBar()
            self.progress_bars[file].setValue(50)
            self.progress_bars[file].setAlignment(Qt.AlignRight)

            self.tableWidget.insertRow(i)

            name_item = QTableWidgetItem(filename)
            name_item.setFlags(Qt.ItemIsEnabled)
            size_item = QTableWidgetItem(filesize)
            size_item.setFlags(Qt.ItemIsEnabled)
            self.tableWidget.setItem(i, 0, name_item)
            self.tableWidget.setItem(i, 1, size_item)
            self.tableWidget.setCellWidget(i, 2, self.progress_bars[file])

        self.thread = QThread()

        # meta_json, sample_seqs, tag, credentials_path, bucket

        print(meta_json, files_list, tag, credentials_path, bucket)

        self.worker = UploadWorker(meta_json, files_list, tag, credentials_path, bucket)
        self.worker.moveToThread(self.thread)

        # self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        # self.worker.progress.connect(self.upload_complete)

        # self.pushButton_terminate.clicked.connect(self.terminate)
        self.pushButton_start.clicked.connect(self.start)
        self.pushButton_close.clicked.connect(self.close)

    def bytes_to_megabytes(self, b):
        return b/(1024*2014)

    def stop(self):
        self.thread.terminate()

    def start(self):
        self.thread.start()


class ValidationDialog(QDialog, UI_Dialog_Validation):
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


