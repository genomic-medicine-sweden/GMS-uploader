import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from modules.pandasmodel import PandasModel
from modules.delegates import CompleterDelegate, ComboBoxDelegate, DateAutoCorrectDelegate, CheckBoxDelegate
from modules.sortfilterproxymodel import MultiSortFilterProxyModel
import pandas as pd
from pathlib import Path
import yaml
import sys
import subprocess
from qt_material import apply_stylesheet
# import os


from ui.mw import Ui_MainWindow

__version__ = '0.0.5'
__title__ = 'uploader'


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.settings = QSettings("Region Västerbotten", "GMSDataUpload")

        self.setWindowIcon(QIcon('img/uploader_u.png'))
        self.setWindowTitle("GMSDataUpload")

        ff = Path('config', 'fields.yaml')

        with ff.open(encoding='utf8') as fp:
            self.conf = yaml.safe_load(fp)

        self.tableView_columns = list(self.conf['fields'].keys())

        self.df = pd.DataFrame(columns=self.tableView_columns)
        self.model = PandasModel(self.df, self.conf['fields'])
        self.sort_proxy_model = MultiSortFilterProxyModel()

        self.tableView_setup()

        # create settings models

        self.column_model = QStandardItemModel()
        self.criterion_model = QStandardItemModel()
        self.region_model = QStandardItemModel()
        self.instrument_model = QStandardItemModel()
        self.platform_model = QStandardItemModel()
        self.library_method_model = QStandardItemModel()

        self.populate_settings_models()

        # filter
        self.lineEdit_filter.textChanged.connect(self.filter)
        self.lineEdit_user.textChanged.connect(self.update_data_user)
        self.pushButton_delrow.clicked.connect(self.del_row)
        self.pushButton_fastp.clicked.connect(self.run_fastp)

        self.set_delegates()
        self.set_datatab_values()
        self.set_col_widths()

    def run_fastp(self):
        for index, row in self.df.iterrows():
            print(index)
            fastq1 = Path(row['fastq1'])
            fastq2 = Path(row['fastq2'])
            report_html = Path(fastq1.parent, row['internal_lab_id'] + '.html')
            out1 = Path(str(fastq1) + '.fastp.gz')
            out2 = Path(str(fastq2) + '.fastp.gz')
            print(out1, out2)
            subprocess.run(["opt/fastp.exe", "-i", fastq1, "-I", fastq2, "-o", out1, "-O", out2, "--html", report_html])

    def del_row(self):
        proxy_model = self.tableView.model()
        selection = self.tableView.selectionModel()
        view_rows = selection.selectedRows()
        df_rows = []
        for i in view_rows:
            si = proxy_model.mapToSource(i)
            print(si.row())
            df_rows.append(si.row())

        sorted_df_rows = sorted(df_rows, reverse=True)
        self.df = self.df.drop(sorted_df_rows)
        self.df = self.df.reset_index(drop=True)
        self.update_model()

    def populate_settings_models(self):
        self.populate_labs()
        self.populate_region()
        self.populate_criterion()
        self.populate_platform()
        self.populate_instrument()
        self.populate_library_method()
        self.populate_column()
        self.populate_server()
        self.populate_user()
        self.populate_path()

    def set_col_widths(self):
        i = 0
        for name in self.conf['fields']:
            self.tableView.setColumnWidth(i, self.conf['fields'][name]['col_width'])
            i = i + 1

    def set_datatab_values(self):
        self.update_data_lab()
        self.update_data_user()
        self.lineEdit_data_lab.setReadOnly(True)
        self.lineEdit_data_user.setReadOnly(True)

        # self.lineEdit_data_lab.setText(self.comboBox_lab.currentText())
        # self.lineEdit_data_user.setText(self.lineEdit_user.text())

    def filter(self):
        text = self.lineEdit_filter.text()
        search = QRegularExpression(text, QRegularExpression.CaseInsensitiveOption)
        self.sort_proxy_model.setFilterByColumns([0, 1, 2, 3], search)

    def checked_to_list(self, model):
        checked_list = ['']
        for r in range(model.rowCount()):
            item = model.item(r, 0)
            if item.checkState() == Qt.CheckState.Checked:
                checked_list.append(item.text())

        return checked_list

    def update_settings(self, checked_list, field):
        self.settings.setValue(field, checked_list)

    def update_data_lab(self):
        txt = self.comboBox_lab.currentText()
        self.lineEdit_data_lab.setText(txt)
        self.settings.setValue('lab_code', txt)

    def update_data_user(self):
        txt = self.lineEdit_user.text() or None

        if txt:
            self.lineEdit_data_user.setText(txt)
            self.settings.setValue('user', txt)

    def update_user(self):
        txt = self.lineEdit_user.text() or None
        if txt:
            self.settings.setValue('user', txt)

    def update_server(self):
        txt = self.lineEdit_server.text() or None
        self.settings.setValue('server', txt)

    def update_path(self):
        txt = self.lineEdit_path.text() or None
        self.settings.setValue('path', txt)

    def set_delegates(self):
        self.set_criterion_delegate()
        self.set_region_delegate()
        self.set_date_delegate()
        self.set_instrument_delegate()
        self.set_platform_delegate()
        self.set_library_delegate()
        self.set_checkbox_delegate()

    def set_checkbox_delegate(self):
        self.checkbox_delegate = CheckBoxDelegate(None)
        self.tableView.setItemDelegateForColumn(self.tableView_columns.index('mark'), self.checkbox_delegate)

    def set_criterion_delegate(self):
        checked_list = self.checked_to_list(self.criterion_model)
        self.criterion_delegate = ComboBoxDelegate(checked_list)
        self.tableView.setItemDelegateForColumn(self.tableView_columns.index('criterion'), self.criterion_delegate)
        self.update_settings(checked_list, 'criterion')

    def set_region_delegate(self):
        checked_list = self.checked_to_list(self.region_model)
        self.region_delegate = ComboBoxDelegate(checked_list)
        self.tableView.setItemDelegateForColumn(self.tableView_columns.index('region_code'), self.region_delegate)
        self.update_settings(checked_list, 'region_code')

    def set_date_delegate(self):
        self.date_delegate = DateAutoCorrectDelegate()
        self.tableView.setItemDelegateForColumn(self.tableView_columns.index('date'), self.date_delegate)

    def set_instrument_delegate(self):
        checked_list = self.checked_to_list(self.instrument_model)
        self.instrument_delegate = ComboBoxDelegate(checked_list)
        self.tableView.setItemDelegateForColumn(self.tableView_columns.index('instrument'), self.instrument_delegate)
        self.update_settings(checked_list, 'instrument')

    def set_platform_delegate(self):
        checked_list = self.checked_to_list(self.platform_model)
        self.platform_delegate = ComboBoxDelegate(checked_list)
        self.tableView.setItemDelegateForColumn(self.tableView_columns.index('platform'), self.platform_delegate)
        self.update_settings(checked_list, 'platform')

    def set_library_delegate(self):
        checked_list = self.checked_to_list(self.library_method_model)
        self.library_delegate = ComboBoxDelegate(checked_list)
        self.tableView.setItemDelegateForColumn(self.tableView_columns.index('library_method'), self.library_delegate)
        self.update_settings(checked_list, 'library_method')

    def tableView_setup(self):
        self.sort_proxy_model.setSourceModel(self.model)
        self.tableView.setModel(self.sort_proxy_model)
        self.tableView.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionsMovable(True)
        self.tableView.setSortingEnabled(True)
        self.pushButton_resetsort.clicked.connect(self.reset_proxy)
        self.pushButton_filldown.clicked.connect(self.filldown)
        self.tableView.verticalHeader().hide()
        self.update_model()

    def filldown(self):
        select = self.tableView.selectionModel()
        index = select.currentIndex()

        max_rows = self.sort_proxy_model.rowCount()
        data_orig = self.sort_proxy_model.data(index, Qt.DisplayRole)

        for r in range(index.row() + 1, max_rows):
            index_new = self.sort_proxy_model.index(r, index.column())
            data_new = self.sort_proxy_model.data(index_new, Qt.DisplayRole)
            if data_new == '':
                self.sort_proxy_model.setData(index_new, data_orig, Qt.EditRole)
            else:
                break

    def update_model(self):
        self.model = PandasModel(self.df, self.conf['fields'])
        self.sort_proxy_model = MultiSortFilterProxyModel()
        self.sort_proxy_model.setSourceModel(self.model)
        self.tableView.setModel(self.sort_proxy_model)
        self.set_col_widths()

    def reset_proxy(self):
        self.sort_proxy_model.sort(-1)
        self.tableView.horizontalHeader().setSortIndicator(-1, Qt.SortOrder.DescendingOrder)

    # populate settings

    def populate_labs(self):

        prev_lab = self.settings.value('lab_code') or None

        for l in self.conf['lab_code']:
            self.comboBox_lab.addItem(l)

        if prev_lab:
            self.comboBox_lab.setCurrentText(prev_lab)

        self.comboBox_lab.currentIndexChanged.connect(self.update_data_lab)

    def populate_criterion(self):
        checked_list = self.settings.value('criterion')

        for c in self.conf['criterion']:
            item = QStandardItem(c)
            item.setCheckable(True)
            if c in checked_list:
                item.setCheckState(Qt.Checked)
            self.criterion_model.appendRow(item)

        self.listView_criterion.setModel(self.criterion_model)
        self.listView_criterion.clicked.connect(self.set_criterion_delegate)

    def populate_instrument(self):
        checked_list = self.settings.value('instrument') or []
        for c in self.conf['instrument']:
            item = QStandardItem(c)
            item.setCheckable(True)
            if c in checked_list:
                item.setCheckState(Qt.Checked)
            self.instrument_model.appendRow(item)

        self.listView_instrument.setModel(self.instrument_model)
        self.listView_instrument.clicked.connect(self.set_instrument_delegate)

    def populate_platform(self):
        checked_list = self.settings.value('platform') or []
        for c in self.conf['platform']:
            item = QStandardItem(c)
            item.setCheckable(True)
            if c in checked_list:
                item.setCheckState(Qt.Checked)
            self.platform_model.appendRow(item)

        self.listView_platform.setModel(self.platform_model)
        self.listView_platform.clicked.connect(self.set_platform_delegate)

    def populate_library_method(self):
        checked_list = self.settings.value('library_method') or []
        print(checked_list)
        for c in self.conf['library_method']:
            item = QStandardItem(c)
            item.setCheckable(True)
            if c in checked_list:
                item.setCheckState(Qt.Checked)
            self.library_method_model.appendRow(item)

        self.listView_library_method.setModel(self.library_method_model)
        self.listView_library_method.clicked.connect(self.set_library_delegate)

    def populate_region(self):
        checked_list = self.settings.value('region_code') or []
        print(checked_list)
        for r in self.conf['region_code']:
            item = QStandardItem(r)
            item.setCheckable(True)
            if r in checked_list:
                item.setCheckState(Qt.Checked)
            self.region_model.appendRow(item)

        self.listView_region.setModel(self.region_model)
        self.listView_region.clicked.connect(self.set_region_delegate)

    def populate_column(self):
        for c in self.conf['fields']:
            item = QStandardItem(c)
            item.setCheckable(True)
            item.setFlags(~Qt.ItemIsDropEnabled)
            self.column_model.appendRow(item)

        self.listView_column.setModel(self.column_model)
        self.listView_column.setSelectionMode(QAbstractItemView.SingleSelection)
        self.listView_column.setDragEnabled(True)
        self.listView_column.viewport().setAcceptDrops(True)
        self.listView_column.setDragDropMode(QAbstractItemView.InternalMove)
        self.listView_column.setDropIndicatorShown(True)
        self.listView_column.setDragDropOverwriteMode(False)

    def populate_user(self):
        user = self.settings.value('user') or None
        if user:
            self.lineEdit_user.setText(user)

        self.lineEdit_user.textEdited.connect(self.update_user)

    def populate_server(self):
        server = self.settings.value("server") or None
        if server:
            self.lineEdit_server.setText(server)

        self.lineEdit_server.textEdited.connect(self.update_server)

    def populate_path(self):
        path = self.settings.value("path") or None
        if path:
            self.lineEdit_path.setText(path)

        self.lineEdit_path.textEdited.connect(self.update_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            files = []
            for url in event.mimeData().urls():
                files.append(str(url.toLocalFile()))

            self.parse_files(files)

        else:
            event.ignore()

    def df_insert(self, df, row):
        insert_loc = df.index.max()

        if pd.isna(insert_loc):
            df.loc[0] = row
        else:
            df.loc[insert_loc + 1] = row

    def parse_files(self, files):
        parsed_files = []
        for file in files:
            f = Path(file)
            if f.is_dir():
                for path in Path(f).rglob('*.fastq.gz'):
                    parsed_files.append(path)
            elif f.match('*.fastq.gz'):
                parsed_files.append(f)


        _data = {}
        for file in parsed_files:
            f = file.stem.split('.')[0]
            sample = f.split('_')[0]
            lane = f.split('_')[-1]

            if not sample in _data:
                _data[sample] = {}

            _data[sample]['lane'] = lane
            if '_R1_' in f:
                _data[sample]['fastq1'] = file
            elif '_R2_' in f:
                _data[sample]['fastq2'] = file

        data = []
        for sample in _data:
            row = dict()
            row['mark'] = 0
            row['internal_lab_id'] = sample
            row['lab_code'] = self.comboBox_lab.currentText()
            for key in _data[sample]:
                row[key] = _data[sample][key]

            data.append(row)

        self.add_data(data)

    def add_data(self, data):
        new_df = pd.DataFrame(data)
        self.df = self.df.append(new_df)
        self.df = self.df.fillna('')
        self.update_model()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            indexes = self.tableView.selectedIndexes()
            model = self.tableView.model()
            for i in indexes:
                if model.flags(i) & Qt.ItemIsEditable:
                    model.setData(i, "", Qt.EditRole)

        elif event.key() == Qt.Key_Copy:
            indexes = self.tableView.selectedIndexes()
            model = self.tableView.model()
            for i in indexes:
                data = model.data(i, Qt.DisplayRole)

        else:
            super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    apply_stylesheet(app, theme='dark_teal.xml')
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
