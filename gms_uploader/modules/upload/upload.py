import os
import threading
import paramiko
from PySide6.QtCore import QObject, Signal, Slot, QThread, QRunnable
from NGPIris.hcp import HCPManager
from pathlib import Path


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
        self.hcpm = HCPManager(cred['endpoint'],
                               cred['aws_access_key_id'],
                               cred['aws_secret_access_key'],
                               bucket=cred['bucket'])

        self.target = tag + "/" + self.filename

    def run(self):
        self.upload_file()
        self.finished.emit(self.filename)

    def upload_file(self):
        self.hcpm.upload_file(self.file,
                              self.target,
                              metadata={'tag': self.tag},
                              callback=NGPIrisCallbackPercentage(Path(self.file), self.progress))


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


