from PySide6.QtGui import QIcon, Qt
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QProgressBar, QDialog, QHeaderView, QTableWidgetItem
from gms_uploader.ui.uploader_dialog import Ui_Dialog as UI_Dialog_Uploader
from gms_uploader.modules.upload.support_classes import ParamikoFileUploadWorker, NGPIrisFileUploadWorker, MsgUploadComplete
from pathlib import Path


class Uploader(QDialog, UI_Dialog_Uploader):
    def __init__(self, cred: dict, tag: str, files: dict):
        super(Uploader, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Upload")
        self.setWindowIcon(QIcon(':/gms_logo'))

        self.files = files
        self.cred = cred
        self.tag = tag
        self.files_list = []
        self.progress_bars = {}
        self.workers = {}
        self.threads = {}

        self.is_paused = False

        self.pushButton_stop.setDisabled(True)
        self.pushButton_delete_upload.setDisabled(True)

        self.lineEdit_tag.setReadOnly(True)
        self.lineEdit_target.setReadOnly(True)

        self.lineEdit_tag.setText(tag)
        self.lineEdit_target.setText(cred['target_label'])
        self.lineEdit_protocol.setText(cred['protocol'])

        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["file", "size", "progress"])

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        row_no = 0
        for sample in files:
            _files_list = files[sample]
            for file in _files_list:
                file_obj = Path(file)
                filename = str(file_obj.name)
                filesize = str(round(self.bytes_to_megabytes(file_obj.stat().st_size), 2)) + " MB"

                self.progress_bars[filename] = QProgressBar()
                self.progress_bars[filename].setValue(0)
                self.progress_bars[filename].setAlignment(Qt.AlignRight)

                self.tableWidget.insertRow(row_no)

                name_item = QTableWidgetItem(filename)
                name_item.setFlags(Qt.ItemIsEnabled)
                size_item = QTableWidgetItem(filesize)
                size_item.setFlags(Qt.ItemIsEnabled)
                self.tableWidget.setItem(row_no, 0, name_item)
                self.tableWidget.setItem(row_no, 1, size_item)
                self.tableWidget.setCellWidget(row_no, 2, self.progress_bars[filename])

                self.files_list.append(file)

                row_no += 1

        self.pushButton_start.clicked.connect(self.start)
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_stop.clicked.connect(self.stop)

    def upload_file(self):
        if len(self.files_list) > 0:
            file = self.files_list.pop(0)
            filename = file.name

            self.workers[filename] = self.get_worker(self.cred, self.tag, file)
            if self.workers[filename] is not None:
                self.threads[filename] = QThread()
                self.workers[filename].moveToThread(self.threads[filename])
                self.threads[filename].started.connect(self.workers[filename].run)
                self.workers[filename].progress.connect(self.report_progress)
                self.workers[filename].finished.connect(self.on_finished)
                self.threads[filename].start()

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def on_finished(self, filename):
        self.threads[filename].quit()
        self.workers[filename].deleteLater()
        self.threads[filename].deleteLater()

        print(f"file list len {len(self.files_list)}")

        if not self.is_paused and len(self.files_list) > 0:
            self.upload_file()

        elif len(self.files_list) == 0:
            self.pushButton_stop.setDisabled(True)
            self.pushButton_close.setDisabled(False)
            msg = MsgUploadComplete(f"Upload of data with tag {self.tag} is complete! ")
            msg.exec()

    def stop(self):
        self.pushButton_start.setDisabled(False)
        self.pushButton_stop.setDisabled(True)
        self.pushButton_close.setDisabled(False)
        self.pause()

    def start(self):
        self.pushButton_stop.setDisabled(False)
        self.pushButton_start.setDisabled(True)
        self.pushButton_delete_upload.setDisabled(True)
        self.pushButton_close.setDisabled(True)
        self.resume()
        self.upload_file()

    def report_progress(self, filename, pct):
        print(f"progress filename {filename}")
        self.progress_bars[filename].setValue(pct)

    def bytes_to_megabytes(self, bytes):
        return bytes/(1024*1024)

    def get_worker(self, cred, tag, file):
        if cred['protocol'] == "SFTP":
            return ParamikoFileUploadWorker(cred, tag, file)
        elif cred['protocol'] == "S3":
            return NGPIrisFileUploadWorker(cred, tag, file)
        else:
            return None
