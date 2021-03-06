from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QComboBox, QLineEdit
from PySide6.QtGui import QStandardItem
from pathlib import Path

from gms_uploader.modules.dialogs.dialogs import MsgAlert


class SettingsManager:
    """ Class for managing settings"""
    def __init__(self, conf):
        self._qsettings = QSettings("Genomic Medicine Sweden", "GMS-uploader")
        self.conf = conf

        self.credentials_dict = {}

        # self._qsettings.clear()

        if not self._validate_settings():
            msg = MsgAlert("Incompatible saved settings: (re-)initializing...")
            msg.exec()

            self._init_settings()

    def get_valid_metadata_dir(self):
        metadata_dir = self.get_value('entered_value', 'metadata_output_path')

        if metadata_dir is None or metadata_dir == "None":
            self.metadata_dir = None

        try:
            md_obj = Path(metadata_dir)
        except:
            return None

        if md_obj.is_dir():
            return md_obj

        return None

    def get_ordered_fieldnames(self):
        return list(self.conf['model_fields'].keys())

    def get_cred_keys(self):
        return self.credentials_dict.keys()

    def get_current_cred_target_label(self):
        key = self.get_value('select_single', 'target_label')
        if key in self.credentials_dict:
            return key

        return "None"

    def get_current_cred_protocol(self):
        key = self.get_value('select_single', 'target_label')
        if key in self.credentials_dict:
            return self.credentials_dict[key]['protocol']

        return "None"

    def set_cred(self, key: str, value_dict: dict):
        self.credentials_dict[key] = value_dict

    def get_cred(self, key: str) -> dict:
        return self.credentials_dict[key]

    def update_setting(self, obj=None, item=None):
        if obj:
            if isinstance(obj, QLineEdit):
                name = obj.objectName()
                value = obj.text()
                self._entered_update(name, value)

            if isinstance(obj, QComboBox):
                value = obj.currentText()
                name = obj.objectName()
                self._single_update(name, value)

        elif item:
            if isinstance(item, QStandardItem):
                self._multi_update(item)

    def get_value(self, field_type, field):
        store_key = "/".join([field_type, field])
        return self._qsettings.value(store_key)

    def set_value(self, field_type, field, value):
        print("insettings", field_type, field, value)
        key = "/".join([field_type, field])
        self._qsettings.setValue(key, value)

    def _entered_update(self, name, value):
        store_key = "/".join(['entered_value', name])
        self._qsettings.setValue(store_key, value)

    def _single_update(self, name, value):
        store_key = "/".join(['select_single', name])
        self._qsettings.setValue(store_key, value)

    def _multi_update(self, obj):

        model = obj.model()
        name = model.objectName()

        checked_items = []
        for row in range(model.rowCount()):
            if str(model.data(model.index(row, 0))) == "1":
                checked_items.append(model.data(model.index(row, 1)))

        store_key = "/".join(['select_multi', name])
        self._qsettings.setValue(store_key, checked_items)

    def _init_settings(self):
        """
        If there is a qsettings and config settings don't match, clear qsettings and reset to
        default values from config.
        :return: None
        """
        self._qsettings.clear()

        for field_type in self.conf['settings_values']:
            for field in self.conf['settings_values'][field_type]:
                store_key = "/".join([field_type, field])

                if field_type == "select_single":
                    if self.conf['settings_values'][field_type][field] != "None":
                        for i, key in enumerate(self.conf['settings_values'][field_type][field]):
                            if self.conf['settings_values'][field_type][field][key]:
                                self._qsettings.setValue(store_key, key)
                    else:
                        self._qsettings.setValue(store_key, 'None')

                elif field_type == "select_multi":
                    checked_items = []
                    for key, checked in self.conf['settings_values'][field_type][field].items():
                        if checked:
                            checked_items.append(key)

                    self._qsettings.setValue(store_key, checked_items)

                else:
                    self._qsettings.setValue(store_key, self.conf['settings_values'][field_type][field])

    def _validate_settings(self):
        """
        Compares qsetting keys with keys in config file to make sure there is no mismatch.
        :return: True if ok, False otherwise
        """
        all_keys = self._qsettings.allKeys()
        for key in all_keys:
            field_type, field = key.split('/')
            if field_type not in self.conf['settings_values']:
                 return False
            if field not in self.conf['settings_values'][field_type]:
                return False

        for wtype in self.conf['settings_values']:
            for field in self.conf['settings_values'][wtype]:
                store_key = "/".join([wtype, field])
                if store_key not in all_keys:
                    return False

        return True

