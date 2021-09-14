import sys
import os
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from modules.pandasmodel import PandasModel
from modules.delegates import CompleterDelegate, ComboBoxDelegate, DateAutoCorrectDelegate, CheckBoxDelegate
from modules.dialogs import MsgError, MsgAlert
from modules.sortfilterproxymodel import MultiSortFilterProxyModel
import pandas as pd
from pathlib import Path
import yaml
from ui.mw import Ui_MainWindow


__version__ = '0.0.7'
__title__ = 'uploader'


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)

        self.setWindowIcon(QIcon('icons/arrow-up.png'))
        self.setWindowTitle("GMS-uploader")

        # declarations
        self.current_settings = {}
        self.current_settings['qlineedits'] = {}
        self.current_settings['qcomboboxes'] = {}
        self.current_settings['qlistwidgets'] = {}


        # add icons
        self.add_icons()

        # load settings
        appdata = os.getenv('APPDATA')
        self.personalized_config_path = Path(appdata, 'GMS-uploader', 'config.yaml')

        # if not personalized_config_path.exists():
        # self.config_setup(self.personalized_config_path)

        with self.personalized_config_path.open(encoding='utf8') as fp:
            self.conf = yaml.safe_load(fp)

        self.tableView_columns = list(self.conf['model_fields'].keys())

        self.df = pd.DataFrame(columns=self.tableView_columns)
        self.model = PandasModel(self.df, self.conf['model_fields'])
        self.sort_proxy_model = MultiSortFilterProxyModel()

        self.tabWidget_metadata.setTabText(0, "Patient metadata")
        self.tabWidget_metadata.setTabText(1, "Organism metadata")
        self.tabWidget_metadata.setTabText(2, "Lab metadata")

        # setup settings
        self.settings_dict = {}
        self.settings_setup(self.conf)
        self.set_signals()
        self.tableView_setup()
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget_metadata.setCurrentIndex(0)
        self.set_hidden_columns()
        self.set_col_widths()



        # self.set_delegates()
        # self.set_datatab_values()
        # self.set_signals()

    def settings_setup(self, config):
        for name in config['settings']['qlineedits']:
            edit = QLineEdit(objectName=name, editingFinished=self.settings_update)
            edit.setText(self.config['settings']['qlineedits'][name])
            self.formLayout_settings.addRow(QLabel(name), edit)
            self.current_settings['qlineedits'][name] = self.config['settings']['qlineedits'][name]

        for name in config['settings']['qcomboboxes']:
            combo = QComboBox(objectName=name)
            combo.currentTextChanged.connect(self.settings_update)
            combo.addItems(list(config['settings']['qcomboboxes'][name].keys()))

            for i, key in enumerate(config['settings']['qcomboboxes'][name]):
                if config['settings']['qcomboboxes'][name][key]:
                    combo.setCurrentIndex(i)
                    self.current_settings['qlineedits'][name] = combo.currentText()

            self.formLayout_settings.addRow(QLabel(name), combo)

        if len(config['settings']['qlistwidgets']) > 0:
            tabwidget_settings = QTabWidget(objectName='tabwidget_settings')
            self.verticalLayout_settings.addWidget(tabwidget_settings)

            for name in config['settings']['qlistwidgets']:
                listwidget = QListWidget(objectName=name)
                listwidget.itemChanged.connect(self.settings_update)
                tabwidget_settings.addTab(listwidget, name)
                checked_items = []
                for key, checked in config['settings']['qlistwidgets'][name].items():
                    item = QListWidgetItem()
                    item.setText(key)
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    if checked:
                        item.setCheckState(Qt.Checked)
                        checked_items.append(key)
                    else:
                        item.setCheckState(Qt.Unchecked)

                    listwidget.addItem(item)
                    self.current_settings['qlistwidgets'][name] = checked_items

    def save_config(self):
        with self.personalized_config_path.open('w', encoding='utf8') as fp:
            yaml.safe_dump(self.conf, fp, encoding='utf-8', allow_unicode=True, sort_keys=False)

    def settings_update(self):
        obj = self.sender()
        name = obj.objectName()

        if isinstance(obj, QLineEdit):
            self.conf['settings']['qlineedits'][name] = obj.text()
            self.current_settings['qlineedits'][name] = obj.text()

        if isinstance(obj, QComboBox):
            current = obj.currentText()
            self.current_settings['qcomboboxes'][name] = current
            for key in self.conf['settings']['qcomboboxes'][name]:
                if key == current:
                    self.conf['settings']['qcomboboxes'][name][key] = True

                else:
                    self.conf['settings']['qcomboboxes'][name][key] = False

        if isinstance(obj, QListWidget):
            checked_items = []
            for x in range(obj.count()):
                key = obj.item(x).text()
                if obj.item(x).checkState() == Qt.Checked:
                    self.conf['settings']['qlistwidgets'][name][key] = True
                    checked_items.append(key)
                else:
                    self.conf['settings']['qlistwidgets'][name][key] = False

            self.current_settings['qlistwidgets'][name] = checked_items


        self.save_config()

    def config_setup(self, p_config):
        msg = MsgAlert("Personalized config does not exist or is invalid.\nImporting from template")
        msg.exec()

        from shutil import copyfile
        d_config = Path(os.getcwd(), 'config', 'config.yaml')

        if not p_config.parent.exists():
            p_config.parent.mkdir(parents=True)

        copyfile(d_config, p_config)

    def set_signals(self):
        self.actionpreferences.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.actionmetadata.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(0))

    def add_icons(self):
        self.action_open_meta.setIcon(QIcon('fontawsome/file-import-solid-white.svg'))
        self.actionsave_meta.setIcon(QIcon('fontawsome/save-solid-white.svg'))
        self.actionmetadata.setIcon(QIcon('fontawsome/table-solid-white.svg'))
        self.actionpreferences.setIcon(QIcon('fontawsome/cogs-solid-white.svg'))
        self.actionupload.setIcon(QIcon('fontawsome/upload-solid-white.svg'))

        self.pushButton_filldown.setIcon(QIcon('fontawsome/arrow-down-solid-white.svg'))
        self.pushButton_drop.setIcon(QIcon('fontawsome/times-solid-white.svg'))
        self.pushButton_clear.setIcon(QIcon('fontawsome/trash-solid-white.svg'))
        self.pushButton_filtermarked.setIcon(QIcon('fontawsome/filter-solid-white.svg'))
        self.pushButton_resetfilters.setIcon(QIcon('fontawsome/filter-reset-solid-white.svg'))

    def drop_rows(self):
        proxy_model = self.tableView_patient.model()
        selection = self.tableView_patient.selectionModel()
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

    def set_col_widths(self):
        for i, name in enumerate(self.conf['model_fields']):
            self.tableView_patient.setColumnWidth(i, self.conf['model_fields'][name]['col_width'])
            self.tableView_organism.setColumnWidth(i, self.conf['model_fields'][name]['col_width'])
            self.tableView_lab.setColumnWidth(i, self.conf['model_fields'][name]['col_width'])

    def set_hidden_columns(self):
        for i, name in enumerate(self.conf['model_fields']):
            if 'patient' not in self.conf['model_fields'][name]['view']:
                self.tableView_patient.setColumnHidden(i, True)
            if 'organism' not in self.conf['model_fields'][name]['view']:
                self.tableView_organism.setColumnHidden(i, True)
            if 'lab' not in self.conf['model_fields'][name]['view']:
                self.tableView_lab.setColumnHidden(i, True)

    def set_datatab_values(self):
        self.update_data_lab()
        self.update_data_user()

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
        self.settings.setValue('Lab_code', txt)

    def update_data_user(self):
        txt = self.lineEdit_user.text() or None

        if txt:
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
        self.checkbox_delegate_patient = CheckBoxDelegate(None)
        self.checkbox_delegate_sequence = CheckBoxDelegate(None)

        self.tableView_sample_info.setItemDelegateForColumn(self.tableView_columns.index('Mark'),
                                                            self.checkbox_delegate_patient)

        self.tableView_seq_info.setItemDelegateForColumn(self.tableView_columns.index('mark'),
                                                            self.checkbox_delegate_sequence)

    def set_criterion_delegate(self):
        checked_list = self.checked_to_list(self.criterion_model)
        self.criterion_delegate = ComboBoxDelegate(checked_list)
        self.tableView_sample_info.setItemDelegateForColumn(self.tableView_columns.index('Selection_criterion'), self.criterion_delegate)
        self.update_settings(checked_list, 'Selection_criterion')

    def set_region_delegate(self):
        checked_list = self.checked_to_list(self.region_model)
        self.region_delegate = ComboBoxDelegate(checked_list)
        self.tableView_sample_info.setItemDelegateForColumn(self.tableView_columns.index('Region_code'), self.region_delegate)
        self.update_settings(checked_list, 'Region_code')

    def set_date_delegate(self):
        self.date_delegate = DateAutoCorrectDelegate()
        self.tableView_sample_info.setItemDelegateForColumn(self.tableView_columns.index('date'), self.date_delegate)

    def set_instrument_delegate(self):
        checked_list = self.checked_to_list(self.instrument_model)
        self.instrument_delegate = ComboBoxDelegate(checked_list)
        self.tableView_sample_info.setItemDelegateForColumn(self.tableView_columns.index('instrument'), self.instrument_delegate)
        self.update_settings(checked_list, 'instrument')

    def set_platform_delegate(self):
        checked_list = self.checked_to_list(self.platform_model)
        self.platform_delegate = ComboBoxDelegate(checked_list)
        self.tableView_sample_info.setItemDelegateForColumn(self.tableView_columns.index('platform'), self.platform_delegate)
        self.update_settings(checked_list, 'platform')

    def set_library_delegate(self):
        checked_list = self.checked_to_list(self.library_method_model)
        self.library_delegate = ComboBoxDelegate(checked_list)
        self.tableView_sample_info.setItemDelegateForColumn(self.tableView_columns.index('library_method'), self.library_delegate)
        self.update_settings(checked_list, 'library_method')

    def tableView_setup(self):
        self.sort_proxy_model.setSourceModel(self.model)
        self.tableView_patient.setModel(self.sort_proxy_model)
        self.tableView_patient.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.tableView_patient.horizontalHeader().setStretchLastSection(True)
        self.tableView_patient.horizontalHeader().setSectionsMovable(True)
        self.tableView_patient.setSortingEnabled(True)

        self.tableView_organism.setModel(self.sort_proxy_model)
        self.tableView_organism.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.tableView_organism.horizontalHeader().setStretchLastSection(True)
        self.tableView_organism.horizontalHeader().setSectionsMovable(True)
        self.tableView_organism.setSortingEnabled(True)

        self.tableView_lab.setModel(self.sort_proxy_model)
        self.tableView_lab.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.tableView_lab.horizontalHeader().setStretchLastSection(True)
        self.tableView_lab.horizontalHeader().setSectionsMovable(True)
        self.tableView_lab.setSortingEnabled(True)

        self.pushButton_resetfilters.clicked.connect(self.reset_proxy)
        self.pushButton_filldown.clicked.connect(self.filldown)
        self.tableView_patient.verticalHeader().hide()
        self.tableView_lab.verticalHeader().hide()
        self.tableView_organism.verticalHeader().hide()
        self.update_model()

    def filldown(self):
        select = self.tableView_patient.selectionModel()
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
        print(self.conf['model_fields'])
        self.model = PandasModel(self.df, self.conf['model_fields'])
        self.sort_proxy_model = MultiSortFilterProxyModel()
        self.sort_proxy_model.setSourceModel(self.model)
        self.tableView_patient.setModel(self.sort_proxy_model)
        self.tableView_lab.setModel(self.sort_proxy_model)
        self.tableView_organism.setModel(self.sort_proxy_model)

        self.set_col_widths()

    def reset_proxy(self):
        self.sort_proxy_model.sort(-1)
        self.tableView_sample_info.horizontalHeader().setSortIndicator(-1, Qt.SortOrder.DescendingOrder)

    # populate settings

    def populate_labs(self):

        prev_lab = self.settings.value('Lab_code') or None

        for l in self.conf['Lab_code']:
            self.comboBox_lab.addItem(l)

        if prev_lab:
            self.comboBox_lab.setCurrentText(prev_lab)

        self.comboBox_lab.currentIndexChanged.connect(self.update_data_lab)

    def populate_criterion(self):
        checked_list = self.settings.value('Selection_criterion')

        print(checked_list)

        for c in self.conf['Selection_criterion']:
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
        checked_list = self.settings.value('Region_code') or []
        print(checked_list)
        for r in self.conf['Region_code']:
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

            _data[sample]['Lane'] = lane
            if '_R1_' in f:
                _data[sample]['Fastq1'] = file
            elif '_R2_' in f:
                _data[sample]['Fastq2'] = file

        data = []
        current_lab_list = [k for k, v in self.conf['settings']['qcomboboxes']['Lab_code'].items() if v]
        print(current_lab_list)

        for sample in _data:
            row = dict()
            row['Mark'] = 0
            row['Internal_lab_ID'] = sample
            row['Lab_code'] = current_lab_list[0]
            for key in _data[sample]:
                row[key] = _data[sample][key]

            data.append(row)

        self.add_data(data)

    def find_duplicates(self, df1, df2):
        df3 = df1.append(df2)

        duplicates = df3['Internal_lab_ID'].duplicated().any()

        print(duplicates)



    def add_data(self, data):
        new_df = pd.DataFrame(data)

        if not self.find_duplicates(self.df, new_df):
            self.df = self.df.append(new_df)
            self.df = self.df.fillna('')
            self.update_model()
        else:
            msgBox = QMessageBox()
            msgBox.setText("Duplicate SampleIDs present in imported data.")
            msgBox.exec()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            indexes = self.tableView_sample_info.selectedIndexes()
            model = self.tableView_sample_info.model()
            for i in indexes:
                if model.flags(i) & Qt.ItemIsEditable:
                    model.setData(i, "", Qt.EditRole)

        elif event.key() == Qt.Key_Copy:
            indexes = self.tableView_sample_info.selectedIndexes()
            model = self.tableView_sample_info.model()
            for i in indexes:
                data = model.data(i, Qt.DisplayRole)

        else:
            super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
