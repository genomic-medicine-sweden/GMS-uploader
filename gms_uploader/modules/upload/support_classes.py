import os
import threading
import paramiko
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QIcon
#from NGPIris.hcp import HCPManager
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
from boto3.s3.transfer import TransferConfig


class NGPIrisCallbackPercentage(object):
    def __init__(self, file, progress):
        self.file = str(file)
        self.filename = file.name
        self._size = float(os.path.getsize(self.file))
        self._seen_so_far = 0
        self._lock = threading.Lock()
        self.progress = progress

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = int((self._seen_so_far / self._size) * 100)
            self.progress.emit(self.filename, percentage)


class NGPIrisFileUploadWorker(QObject):
    finished = Signal(str)
    progress = Signal(str, int)

    def __init__(self, cred, tag, file):
        super(NGPIrisFileUploadWorker, self).__init__()

        self.tag = tag
        self.file = str(file)
        self.filename = file.name

        session = boto3.session.Session(aws_access_key_id=cred['aws_access_key_id'],
                                        aws_secret_access_key=cred['aws_secret_access_key'])

        s3_config = Config(s3={'addressing_style': 'path', 'payload_signing_enabled': True},
                           signature_version='s3v4')

        self.s3 = session.resource('s3',
                                   endpoint_url=cred['endpoint'],
                                   verify=False,  # Checks for SLL certificate. Disables because of already "secure" solution.
                                   config=s3_config)

        self.bucket = self.s3.Bucket(bucket=cred['bucket'])

        self.transfer_config = TransferConfig(multipart_threshold=10000000,
                                              max_concurrency=15,
                                              multipart_chunksize=10000000)

        self.target = tag + "/" + self.filename

    def run(self):
        self.upload_file()
        self.finished.emit(self.filename)

    def upload_file(self):
        self.bucket.upload_file(self.file,
                                self.target,
                                ExtraArgs={'Metadata': "test"},
                                Config=self.transfer_config,
                                Callback=NGPIrisCallbackPercentage(Path(self.file), self.progress))


        # self.hcpm.upload_file(self.file,
        #                       self.target,
        #                       metadata={'tag': self.tag},
        #                       callback=NGPIrisCallbackPercentage(Path(self.file), self.progress))


class ParamikoFileUploadWorker(QObject):
    finished = Signal(str)
    progress = Signal(str, int)

    def __init__(self, cred, tag, file):
        super(ParamikoFileUploadWorker, self).__init__()

        self.file = str(file)
        self.filename = file.name

        self.t = paramiko.Transport((cred['target_host'], 22))
        self.t.banner_timeout = 10
        self.t.connect(username=cred['usr'], password=cred['psw'])
        self.sftp = paramiko.SFTPClient.from_transport(self.t)

        target_path = cred['base_path'] + "/" + tag
        self.target = target_path + "/" + self.filename

        if not self.sftp_exists(target_path):
            self.sftp.mkdir(target_path)

    def run(self):
        self.upload_file()
        self.t.close()
        self.finished.emit(self.filename)

    def upload_file(self):

        self.sftp.put(self.file, self.target, callback=self.percentage_transferred)

    def percentage_transferred(self, bytes_transferred, bytes_total):

        pct = int((bytes_transferred / bytes_total) * 100)
        self.progress.emit(self.filename, pct)

    def sftp_exists(self, path):
        try:
            self.sftp.stat(path)
            return True
        except FileNotFoundError:
            return False


class MsgUploadComplete(QMessageBox):
    def __init__(self, msg):
        super().__init__()
        self.setMinimumWidth(700)
        self.setIcon(QMessageBox.Information)
        self.setText(msg)
        self.setWindowTitle("Upload Complete")
        self.setWindowIcon(QIcon('icons/arrow-up.png'))
