from pathlib import Path
import json


class CredManager:
    """ Class for managing credentials"""
    def __init__(self, settings):
        self.settings = settings
        self.credentials = {}
        self.load_credentials()

    def load_credentials(self):
        path = self.settings.get_value('entered_value', 'credentials_path')
        path_obj = None
        if path is not None:
            path_obj = Path(path)

        if path_obj is not None and path_obj.exists():
            files = path_obj.glob('*.json')

            for file in files:
                with open(file) as fh:
                    curr_cred = json.load(fh)
                    if self.validate_cred(curr_cred):
                        target_label = curr_cred['target_label']
                        self.credentials[target_label] = curr_cred

    def get_current_target_label(self):
        return self.settings.get_value("select_single", "target_label")

    def get_current_protocol(self):
        target_label = self.settings.get_value("select_single", "target_label")
        if target_label in self.credentials:
            return self.credentials[target_label]['protocol']
        else:
            return None

    def get_current_cred(self):
        target_label = self.settings.get_value('select_single', 'target_label')
        if target_label in self.credentials:
            return self.credentials[target_label]

    def validate_cred(self, cred):
        if not isinstance(cred, dict):
            return False
        if 'protocol' not in cred:
            return False
        if 'target_label' not in cred:
            return False

        if cred['protocol'] == "S3":
            if 'endpoint' not in cred:
                return False
            if 'aws_access_key_id' not in cred:
                return False
            if 'aws_secret_access_key' not in cred:
                return False
            if 'bucket' not in cred:
                return False

            return True

        elif cred['protocol'] == "SFTP":
            if 'target_host' not in cred:
                return False
            if 'base_path' not in cred:
                return False
            if 'usr' not in cred:
                return False
            if 'psw' not in cred:
                return False

            return True

        return False

    def get_current_cred_target_label(self):
        key = self.settings.get_value('select_single', 'target_label')
        if key in self.credentials_dict:
            return key

        return "None"

    def get_current_cred_protocol(self):
        key = self.settings.get_value('select_single', 'target_label')
        if key in self.credentials_dict:
            return self.credentials_dict[key]['protocol']

        return "None"

    def get_cred(self, key: str) -> dict:
        return self.credentials[key]

    def get_cred_keys(self) -> list:
        return list(self.credentials.keys())
