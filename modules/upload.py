from PySide6.QtCore import QObject, Signal
from HCPInterface.hcp import HCPManager
import json
from pathlib import Path


class UploadWorker(QObject):
    finished = Signal()
    progress = Signal(str, int)

    def __init__(self, meta_json, sample_seqs, tag, credentials_path, bucket):
        super(UploadWorker, self).__init__()

        self.meta_json = meta_json
        self.cred = json.loads(Path(credentials_path).read_text())
        self.sample_seqs = sample_seqs
        self.tag = tag
        self.credentials_path = credentials_path
        self.bucket = bucket
        self.current_upload = None

    def run(self):
        self.hcp_upload()
        self.finished.emit()

    def hcp_upload(self):
        hcpm = HCPManager(self.cred['endpoint'],
                          self.cred["aws_access_key_id"],
                          self.cred["aws_secret_access_key"])
        hcpm.attach_bucket(self.bucket)

        hcpm.upload_file(str(self.meta_json),
                         self.tag,
                         metadata={'dt_tag': self.tag, 'type': 'json'},
                         silent=True)

        for sample in self.sample_seqs:
            for file in self.sample_seqs[sample]:
                self.current_upload = file
                hcpm.upload_file(str(file),
                                 self.tag,
                                 metadata={'tag': self.tag, 'type': 'fastq', 'sample': sample}
                                 )
                self.update_progress(100)

    def update_progress(self, value):
        self.progress.emit(self.current_upload, value)






