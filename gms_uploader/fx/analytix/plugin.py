import yaml
import pkgutil
import pandas as pd
from pathlib import Path
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QGuiApplication
import qdarktheme


class FX:
    def __init__(self):
        # self.conf = None
        # path = Path("d:/PycharmProjects", "GMS-uploader", "gms_uploader", "fx", "analytix", "conf.yaml")
        # with path.open('r', encoding='utf-8') as handle:
        #     self.conf = yaml.safe_load(handle)
        self.conf = yaml.safe_load(pkgutil.get_data(__name__, "conf.yaml"))
        self.dialog = QFileDialog()
        style = qdarktheme.load_stylesheet("light")
        self.dialog.setStyleSheet(style)

        self.from_file = False
        self.from_clipboard = False

        self._set_importers()

    def _set_importers(self):
        self.from_file = self.conf['importers']['import_from_file']
        self.from_clipboard = self.conf['importers']['import_from_clipboard']

    def _load_file(self, path: Path) -> pd.DataFrame:
        print("load file")
        return pd.read_csv(path, sep=';', dtype=self.conf['import_dtypes'])

    def _translate_fieldnames_values(self, df) -> pd.DataFrame:
        df_mod = df.dropna(subset=['Prov ID'])
        df_mod = df_mod.rename(columns=self.conf['translate_fieldnames'])
        df_mod['region_letter'] = df_mod['order_code'].map(self.conf['order_code_to_region_letter'])
        df_mod['region'] = df_mod['region_letter'].map(self.conf['region_letter_to_region'])
        df_mod['patient_sex'] = df_mod['patient_sex'].map(self.conf['translate_values']['patient_sex'])
        return df_mod

    def get_from_file(self) -> pd.DataFrame:
        file_obj = self._get_file()
        df = self._load_file(file_obj)
        df_mod = self._translate_fieldnames_values(df)
        return df_mod

    def _get_file(self) -> Path:
        """
        Set filepath to textfile where pseudo_ids should be stored
        :return: pathlib object
        """

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file, _ = self.dialog.getOpenFileName(self.dialog, "Open", "",
                                              "Semicolon-separated CSV (*.csv *.xls)",
                                              options=options)

        if file:
            return Path(file)

    def get_from_clipboard(self) -> pd.DataFrame:
        print("get_from_clipboard")
        clipboard = QGuiApplication.clipboard()
        mime_data = clipboard.mimeData()

        matrix = list()
        rows = mime_data.text().split("\n")
        for i, r in enumerate(rows):
            matrix.append(r.split("\t"))

        return matrix



def main():
    fx = FX()
    file_obj = Path("D:/data/10ec662cc9844675ac14608ed1c82837.csv")
    df = fx._load_file(file_obj)
    df_mod = fx._translate_fieldnames_values(df)

    print(df_mod)


if __name__ == '__main__':
    main()

    # file_obj = Path("D:/data/10ec662cc9844675ac14608ed1c82837.csv")
    # df = fx._load_file(file_obj)
    # df_mod = fx._translate_fieldnames_values(df)
    #
    # print(df_mod)
