import pandas as pd
from PySide6.QtGui import QIcon, Qt
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QProgressBar, QDialog, QHeaderView, QTableWidgetItem
from gms_uploader.ui.uploader_dialog import Ui_Dialog as UI_Dialog_Uploader
from gms_uploader.modules.upload.support_classes import ParamikoFileUploadWorker, Boto3FileUploadWorker, \
    MsgUploadComplete
import paramiko
import boto3
from botocore.exceptions import ClientError
from gms_uploader.modules.pseudo_id.pseudo_id import PseudoIDManager
from pathlib import Path
import json


class ConnectionTester:
    def __init__(self):
        path = 'D:/Dokument/accounts/gms-uploader/ngp.json'
        self.cred = None
        with open(path, "r") as fh:
            self.cred = json.load(fh)

    def _get_sftp_connection(self):

        t = paramiko.Transport((self.cred['target_host'], 22))
        t.banner_timeout = 10
        t.connect(username=self.cred['usr'], password=self.cred['psw'])
        sftp = paramiko.SFTPClient.from_transport(t)

        return sftp

    def _get_s3_connection(self):
        if self.cred is not None:
            s3_client = boto3.client(
                service_name='s3',
                endpoint_url=self.cred['endpoint']
            )


class Item:
    def __init__(self, lid: str, pseudo_id: str, files: list):
        self.lid = lid
        self.pseudo_id = pseudo_id
        self.dir = dir
        self.files = files
        self.fnames = self._get_filenames()
        self.uploaded = self._get_uploaded_defaults()

    def _get_filenames(self):
        return [file.name for file in self.files]

    def contains_filename(self, fname: str) -> bool:
        if fname in self.fnames:
            return True

        return False

    def _get_uploaded_defaults(self) -> dict:
        uploaded = {}
        for fname in self.fnames:
            uploaded[fname] = False

        return uploaded

    def set_file_uploaded(self, fname: str):
        self.uploaded[fname] = True

    def upload_complete(self) -> bool:
        res = list(self.uploaded.values())
        if all(res):
            return True

        return False


class Uploader(QDialog, UI_Dialog_Uploader):
    def __init__(self, cred: dict,
                 tag: str,
                 df: pd.DataFrame,
                 metafile: Path,
                 completefile: Path,
                 pidm: PseudoIDManager):

        super(Uploader, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Upload")
        self.setWindowIcon(QIcon(':/gms_logo'))

        self.cred = cred
        self.tag = tag
        self.df = df.copy(deep=True)
        self.metafile = metafile
        self.completefile = completefile
        self.pidm = pidm

        self.items = self._create_items()
        self.fname2lid = {}
        self.allfiles = []

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
        for lid in self.items:
            for file in self.items[lid].files:
                fname = str(file.name)
                fsize = str(round(self.bytes_to_megabytes(file.stat().st_size), 2)) + " MB"

                self.fname2lid[fname] = self.items[lid].lid
                self.allfiles.append(file)

                self.progress_bars[fname] = QProgressBar()
                self.progress_bars[fname].setRange(0, 100)
                self.progress_bars[fname].setValue(0)
                self.progress_bars[fname].setAlignment(Qt.AlignRight)

                self.tableWidget.insertRow(row_no)

                name_item = QTableWidgetItem(fname)
                name_item.setFlags(Qt.ItemIsEnabled)
                size_item = QTableWidgetItem(fsize)
                size_item.setFlags(Qt.ItemIsEnabled)
                self.tableWidget.setItem(row_no, 0, name_item)
                self.tableWidget.setItem(row_no, 1, size_item)
                self.tableWidget.setCellWidget(row_no, 2, self.progress_bars[fname])

                row_no += 1

        self.pushButton_start.clicked.connect(self.start)
        self.pushButton_close.clicked.connect(self.close)
        self.pushButton_stop.clicked.connect(self.stop)

    def verify_connection(self):
        pass

    def _get_pidlids(self):
        pidlids = []
        for lid in self.items:
            if self.items[lid].pseudo_id is not None:
                pidlids.append((self.items[lid].pseudo_id, lid))

        return pidlids

    def _create_items(self) -> dict:
        items = {}
        for _, row in self.df.iterrows():
            _files = []
            _lid = row['internal_lab_id']
            _pseudo_id = row['pseudo_id']

            if row['fastq']:
                _list = row["fastq"]
                for filename in _list:
                    _files.append(Path(row["seq_path"], filename))

            if row['fast5']:
                _list = row["fast5"]
                for filename in _list:
                    _files.append(Path(row["seq_path"], filename))

            items[row['internal_lab_id']] = Item(_lid, _pseudo_id, _files)

        items['metafile'] = Item('metafile', None, [self.metafile])
        items['completefile'] = Item('completefile', None, [self.completefile])

        return items

    def upload_file(self):
        if len(self.allfiles) > 0:
            file = self.allfiles.pop(0)
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

        if not self.is_paused and len(self.allfiles) > 0:
            lid = self.fname2lid[filename]
            self.items[lid].set_file_uploaded(filename)
            self.upload_file()

        elif len(self.allfiles) == 0:
            lid = self.fname2lid[filename]
            self.items[lid].set_file_uploaded(filename)

            self.pushButton_stop.setDisabled(True)
            self.pushButton_close.setDisabled(False)

            if self._all_uploads_done():
                pidlids = self._get_pidlids()
                self.pidm.write_pidlids_to_csv(pidlids, self.tag)
                msg = MsgUploadComplete(f"Upload of data with tag {self.tag} is complete.\n "
                                        f"Pseudo_ids are stored in the pseudo_id_file.")

                msg.exec()

            else:
                msg = MsgUploadComplete(f"Upload of data with tag {self.tag} is complete \n "
                                        f"but files were not listed as uploaded. The pseudo_id_file \n"
                                        f"was not updated.")

                msg.exec()

    def _all_uploads_done(self):
        res = []
        for name in self.items:
            res.append(self.items[name].upload_complete())

        if all(res):
            return True

        return False

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
        print(f"report_progress {filename} {pct}")
        self.progress_bars[filename].setValue(pct)

    def bytes_to_megabytes(self, bytes):
        return bytes/(1024*1024)

    def get_worker(self, cred, tag, file):
        if cred['protocol'] == "SFTP":
            return ParamikoFileUploadWorker(cred, tag, file)
        elif cred['protocol'] == "S3":
            return Boto3FileUploadWorker(cred, tag, file)
        else:
            return None
