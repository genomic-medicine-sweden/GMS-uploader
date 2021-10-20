from abc import ABC, abstractmethod
from NGPIris.hcp import HCPManager
import paramiko


class UploadManager(ABC):
    @abstractmethod
    def upload_file(self):
        pass


class S3UploadManager(UploadManager):
    def __init__(self, cred: dict, tag: str):

        self.hcpm = HCPManager(cred['endpoint'],
                          cred['aws_access_key_id'],
                          cred['aws_secret_access_key'],
                          bucket=cred['bucket'])

    def upload_file(self, file, tag, callback=None):
        self.hcpm.upload_file(file, tag, metadata={'tag': tag}, callback=callback)


class SFTPUploadManager(UploadManager):

    def __init__(self, cred: dict, tag: str):

        self.hcpm = HCPManager(cred['endpoint'],
                          cred['aws_access_key_id'],
                          cred['aws_secret_access_key'],
                          bucket=cred['bucket'])

        self.t = paramiko.Transport((cred['host'], 22))
        self.t.banner_timeout = 10
        self.t.connect(username=cred['usr'], password=cred['psw'])

        # get the SFTP client object.
        self.sftp = paramiko.SFTPClient.from_transport(self.t)

        # upload local file to remote server path.

    def upload_file(self, file, tag):
        self.sftp.put(file, tag)

    def close_conn(self):
        # close the connection.
        self.t.close()

    def create_subfolder(self):
        pass


