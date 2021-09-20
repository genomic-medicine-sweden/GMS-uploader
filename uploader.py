import sys
import os
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from modules.pandasmodel import PandasModel
from modules.delegates import CompleterDelegate, ComboBoxDelegate, \
    DateAutoCorrectDelegate, CheckBoxDelegate, AgeDelegate
from modules.dialogs import MsgError, MsgAlert
from modules.sortfilterproxymodel import MultiSortFilterProxyModel, MarkedFilterProxyModel
import pandas as pd
from pathlib import Path
import yaml
from ui.mw import Ui_MainWindow
import qdarktheme

__version__ = '0.1.0'
__title__ = 'uploader'


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)

        self.qsettings = QSettings("Genomic Medicine Sweden", "GMS-uploader")

        self.setWindowIcon(QIcon('icons/GMS-logo.png'))
        self.setWindowTitle("GMS-uploader " + __version__)

        # add icons
        self.set_icons()

        default_config_path = Path('config', 'config.yaml')
        with default_config_path.open(encoding='utf8') as fp:
            self.conf = yaml.safe_load(fp)

        if not self.validate_settings():
            msg = MsgAlert("Incompatible saved settings: (re-)initializing...")
            msg.exec()

            self.qsettings.clear()
            self.settings_init()

        self.settings_setup()

        self.tableView_columns = list(self.conf['model_fields'].keys())

        self.df = pd.DataFrame(columns=self.tableView_columns)
        self.model = PandasModel(self.df, self.conf['model_fields'])
        self.multifilter_sort_proxy_model = MultiSortFilterProxyModel()

        self.tabWidget_metadata.setTabText(0, "Patient metadata")
        self.tabWidget_metadata.setTabText(1, "Organism metadata")
        self.tabWidget_metadata.setTabText(2, "Lab metadata")

        self.lineEdit_filter.setPlaceholderText("Freetext filter")

        # setup settings

        self.delegates = {}
        self.delegates['patient'] = {}
        self.delegates['lab'] = {}
        self.delegates['organism'] = {}

        self.set_signals()
        self.tableView_setup()
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget_metadata.setCurrentIndex(0)
        self.set_hidden_columns()
        self.set_col_widths()

        self.set_delegates()

    def validate_settings(self):
        all_keys = self.qsettings.allKeys()

        for key in all_keys:
            wtype, field = key.split('/')

            if wtype not in self.conf['settings']:
                return False
            if field not in self.conf['settings'][wtype]:
                return False

        for wtype in self.conf['settings']:
            for field in self.conf['settings'][wtype]:
                store_key = "/".join([wtype, field])
                if store_key not in all_keys:
                    return False

        return True

    def settings_init(self):
        self.qsettings.clear()

        for name in self.conf['settings']['qlineedits_buttons']:
            store_key = "/".join(['qlineedits_buttons', name])
            self.qsettings.setValue(store_key, self.conf['settings']['qlineedits_buttons'][name])

        for name in self.conf['settings']['qlineedits']:
            store_key = "/".join(['qlineedits', name])
            self.qsettings.setValue(store_key, self.conf['settings']['qlineedits'][name])

        for name in self.conf['settings']['qcomboboxes']:
            store_key = "/".join(['qcomboboxes', name])
            for i, key in enumerate(self.conf['settings']['qcomboboxes'][name]):
                if self.conf['settings']['qcomboboxes'][name][key]:
                    self.qsettings.setValue(store_key, key)

        for name in self.conf['settings']['qlistwidgets']:
            store_key = "/".join(['qlistwidgets', name])
            checked_items = []
            for key, checked in self.conf['settings']['qlistwidgets'][name].items():
                if checked:
                    checked_items.append(key)

            self.qsettings.setValue(store_key, checked_items)

    def set_static_lineedits(self):
        self.lineEdit_Submitter.setText(self.qsettings.value("qlineedits/Submitter"))
        self.lineEdit_key_id.setText(self.qsettings.value("qlineedits/AWS_key_id"))
        self.lineEdit_endpoint.setText(self.qsettings.value("qlineedits/Endpoint"))
        self.lineEdit_secret_key.setText(self.qsettings.value("qlineedits/AWS_secret_key"))
        self.lineEdit_Lab_code.setText(self.qsettings.value("qcomboboxes/Lab_code"))
        self.lineEdit_Sequencing_technology.setText(self.qsettings.value("qcomboboxes/Sequencing_technology"))
        self.lineEdit_host.setText(self.qsettings.value("qcomboboxes/Host"))
        self.lineEdit_lib_method.setText(self.qsettings.value("qcomboboxes/Library_method"))
        self.lineEdit_bucket.setText(self.qsettings.value("qcomboboxes/HCP_buckets"))

    def set_pseudo_id_path(self):
        obj = self.sender()
        button_name = obj.objectName()
        name = button_name.strip("button")

        dialog = QFileDialog()

        default_fn = "gms-uploader_1_pseudoids.txt"

        pseudo_id_fp, filter = dialog.getSaveFileName(self,
                                                      'Set an awesome filepath to store pseudo IDs',
                                                      default_fn,
                                                      "Pseudo ID store files (*_pseudoids.txt)",
                                                      options=QFileDialog.DontUseNativeDialog)
        print(pseudo_id_fp)
        edit = self.stackedWidgetPage2.findChild(QLineEdit, name, Qt.FindChildrenRecursively)
        edit.setText(pseudo_id_fp)

    def settings_setup(self):
        for name in self.conf['settings']['qlineedits_buttons']:
            button_name = name + "button"
            button = QPushButton("...", objectName=button_name, clicked=self.set_pseudo_id_path)
            edit = QLineEdit(objectName=name, editingFinished=self.settings_update)


            hbox = QHBoxLayout()
            hbox.addWidget(edit)
            hbox.addWidget(button)

            self.formLayout_settings.addRow(QLabel(name), hbox)

            store_key = "/".join(['qlineedits', name])
            value = self.qsettings.value(store_key)
            edit.setText(value)

        for name in self.conf['settings']['qlineedits']:
            edit = QLineEdit(objectName=name, editingFinished=self.settings_update)
            store_key = "/".join(['qlineedits', name])
            value = self.qsettings.value(store_key)
            edit.setText(value)
            self.formLayout_settings.addRow(QLabel(name), edit)

        for name in self.conf['settings']['qcomboboxes']:
            combo = QComboBox(objectName=name)
            combo.addItems(list(self.conf['settings']['qcomboboxes'][name].keys()))

            store_key = "/".join(['qcomboboxes', name])
            value = self.qsettings.value(store_key)
            combo.setCurrentText(value)
            self.formLayout_settings.addRow(QLabel(name), combo)
            combo.currentTextChanged.connect(self.settings_update)

        tabwidget_settings = QTabWidget(objectName='tabwidget_settings')
        self.verticalLayout_settings.addWidget(tabwidget_settings)

        for name in self.conf['settings']['qlistwidgets']:
            listwidget = QListWidget(objectName=name)
            listwidget.itemChanged.connect(self.settings_update)
            tabwidget_settings.addTab(listwidget, name)
            checked_items = []

            store_key = "/".join(['qlistwidgets', name])
            items = self.to_list(self.qsettings.value(store_key))

            for key, checked in self.conf['settings']['qlistwidgets'][name].items():
                item = QListWidgetItem()
                item.setText(key)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                if key in items:
                    item.setCheckState(Qt.Checked)
                    checked_items.append(key)
                else:
                    item.setCheckState(Qt.Unchecked)

                listwidget.addItem(item)

            self.set_static_lineedits()

    def settings_update(self):
        obj = self.sender()
        name = obj.objectName()

        if isinstance(obj, QLineEdit):
            store_key = "/".join(['qlineedits', name])
            self.qsettings.setValue(store_key, obj.text())

        elif isinstance(obj, QComboBox):
            store_key = "/".join(['qcomboboxes', name])
            value = obj.currentText()
            self.qsettings.setValue(store_key, value)

        elif isinstance(obj, QListWidget):
            store_key = "/".join(['qlistwidgets', name])

            checked_items = []
            for x in range(obj.count()):
                key = obj.item(x).text()
                if obj.item(x).checkState() == Qt.Checked:
                    checked_items.append(key)

            self.qsettings.setValue(store_key, checked_items)

        self.set_static_lineedits()

    def set_signals(self):
        self.actionpreferences.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.actionmetadata.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.lineEdit_filter.textChanged.connect(self.set_free_filter)
        self.pushButton_filtermarked.setCheckable(True)
        self.pushButton_filtermarked.clicked.connect(self.set_mark_filter)
        self.pushButton_drop.clicked.connect(self.drop_rows)
        self.pushButton_clear.clicked.connect(self.clear_table)
        self.actionselect_seq_files.triggered.connect(self.get_files_folders)
        self.actionupload.triggered.connect(self.upload)

    def get_files_folders(self):
        dialog = QFileDialog()
        files, _ = dialog.getOpenFileNames(self,
                                        "Select sequence data files",
                                        "",
                                        "Sequence files (*.fast5 *.fastq.gz *.fastq *.fq.gz *.fq")

        self.parse_files(files)

    def set_icons(self):

        self.action_open_meta.setIcon(QIcon('fontawsome/file-import-solid.svg'))
        self.actionsave_meta.setIcon(QIcon('fontawsome/save-solid.svg'))
        self.actionmetadata.setIcon(QIcon('fontawsome/table-solid.svg'))
        self.actionpreferences.setIcon(QIcon('fontawsome/cogs-solid.svg'))
        self.actionupload.setIcon(QIcon('fontawsome/upload-solid.svg'))
        self.actionselect_seq_files.setIcon(QIcon('fontawsome/dna-solid.svg'))

        self.pushButton_filldown.setIcon(QIcon('fontawsome/arrow-down-solid.svg'))
        self.pushButton_filldown.setIconSize(QSize(18, 18))
        self.pushButton_drop.setIcon(QIcon('fontawsome/times-solid.svg'))
        self.pushButton_drop.setIconSize(QSize(18, 18))
        self.pushButton_clear.setIcon(QIcon('fontawsome/trash-solid.svg'))
        self.pushButton_clear.setIconSize(QSize(14, 14))
        self.pushButton_resetfilters.setIcon(QIcon('fontawsome/filter-reset-solid.svg'))
        self.pushButton_resetfilters.setIconSize(QSize(14, 14))
        self.pushButton_filtermarked.setIcon(QIcon('fontawsome/filter-solid.svg'))
        self.pushButton_filtermarked.setIconSize(QSize(14, 14))

    def drop_rows(self):
        self.model.dropMarkedRows()
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

    def set_mark_filter(self):
        print("set filter")
        print(self.pushButton_filtermarked.isChecked())
        if self.pushButton_filtermarked.isChecked():
            self.multifilter_sort_proxy_model.setCheckedFilter()

        else:
            self.multifilter_sort_proxy_model.clearCheckedFilter()

    def set_free_filter(self):
        text = self.lineEdit_filter.text()
        search = QRegularExpression(text, QRegularExpression.CaseInsensitiveOption)
        self.multifilter_sort_proxy_model.setFilterByColumns([1, 2, 3], search)

    def set_delegates(self):
        for field in self.conf['model_fields']:
            if 'checkbox' in self.conf['model_fields'][field]['delegates']:
                self.set_checkbox_delegate(field)

            elif 'combobox' in self.conf['model_fields'][field]['delegates']:
                self.set_combobox_delegate(field)

            elif 'date' in self.conf['model_fields'][field]['delegates']:
                self.set_date_delegate(field)

            elif 'age' in self.conf['model_fields'][field]['delegates']:
                self.set_age_delegate(field)

    def set_combobox_delegate(self, field):

        store_key = "/".join(["qlistwidgets", field])
        items = ['']
        items.extend(self.to_list(self.qsettings.value(store_key)))

        for view in self.conf['model_fields'][field]['view']:
            self.delegates[view][field] = ComboBoxDelegate(items)

            if view == 'patient':
                self.tableView_patient.setItemDelegateForColumn(self.tableView_columns.index(field),
                                                                self.delegates[view][field])
            elif view == 'lab':
                self.tableView_lab.setItemDelegateForColumn(self.tableView_columns.index(field),
                                                            self.delegates[view][field])
            elif view == 'organism':
                self.tableView_organism.setItemDelegateForColumn(self.tableView_columns.index(field),
                                                                 self.delegates[view][field])

    def set_date_delegate(self, field):
        for view in self.conf['model_fields'][field]['view']:
            self.delegates[view][field] = DateAutoCorrectDelegate()
            if view == 'patient':
                self.tableView_patient.setItemDelegateForColumn(self.tableView_columns.index(field),
                                                                self.delegates[view][field])
            elif view == 'lab':
                self.tableView_lab.setItemDelegateForColumn(self.tableView_columns.index(field),
                                                            self.delegates[view][field])
            elif view == 'organism':
                self.tableView_organism.setItemDelegateForColumn(self.tableView_columns.index(field),
                                                                 self.delegates[view][field])

    def set_age_delegate(self, field):
        for view in self.conf['model_fields'][field]['view']:
            self.delegates[view][field] = AgeDelegate()

            if view == 'patient':
                self.tableView_patient.setItemDelegateForColumn(self.tableView_columns.index(field),
                                                                self.delegates[view][field])
            elif view == 'lab':
                self.tableView_lab.setItemDelegateForColumn(self.tableView_columns.index(field),
                                                            self.delegates[view][field])
            elif view == 'organism':
                self.tableView_organism.setItemDelegateForColumn(self.tableView_columns.index(field),
                                                                 self.delegates[view][field])

    def set_checkbox_delegate(self, field):
        for view in self.conf['model_fields'][field]['view']:
            self.delegates[view][field] = CheckBoxDelegate(None)

            if view == 'patient':
                self.tableView_patient.setItemDelegateForColumn(self.tableView_columns.index(field),
                                                                self.delegates[view][field])
            elif view == 'lab':
                self.tableView_lab.setItemDelegateForColumn(self.tableView_columns.index(field),
                                                            self.delegates[view][field])
            elif view == 'organism':
                self.tableView_organism.setItemDelegateForColumn(self.tableView_columns.index(field),
                                                                 self.delegates[view][field])

    def to_list(self, obj):
        if type(obj) is list:
            return obj
        else:
            return []

    def tableView_setup(self):

        self.multifilter_sort_proxy_model.setSourceModel(self.model)

        self.tableView_patient.setModel(self.multifilter_sort_proxy_model)
        self.tableView_patient.setEditTriggers(QAbstractItemView.DoubleClicked
                                               | QAbstractItemView.SelectedClicked
                                               | QAbstractItemView.EditKeyPressed)
        self.tableView_patient.horizontalHeader().setStretchLastSection(True)
        self.tableView_patient.horizontalHeader().setSectionsMovable(True)
        self.tableView_patient.setSortingEnabled(True)

        self.tableView_organism.setModel(self.multifilter_sort_proxy_model)
        self.tableView_organism.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)
        self.tableView_organism.horizontalHeader().setStretchLastSection(True)
        self.tableView_organism.horizontalHeader().setSectionsMovable(True)
        self.tableView_organism.setSortingEnabled(True)

        self.tableView_lab.setModel(self.multifilter_sort_proxy_model)
        self.tableView_lab.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)
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
        visible_tableview = self.get_visible_tableview()
        print(visible_tableview)
        if visible_tableview:
            select = visible_tableview.selectionModel()
            index = select.currentIndex()

            max_rows = self.multifilter_sort_proxy_model.rowCount()
            data_orig = self.multifilter_sort_proxy_model.data(index, Qt.DisplayRole)

            for r in range(index.row() + 1, max_rows):
                index_new = self.multifilter_sort_proxy_model.index(r, index.column())
                data_new = self.multifilter_sort_proxy_model.data(index_new, Qt.DisplayRole)
                if data_new == '':
                    self.multifilter_sort_proxy_model.setData(index_new, data_orig, Qt.EditRole)
                else:
                    break

    def clear_table(self):
        self.df = pd.DataFrame(columns=self.tableView_columns)
        self.update_model()

    def update_model(self):
        self.model = PandasModel(self.df, self.conf['model_fields'])
        self.multifilter_sort_proxy_model = MultiSortFilterProxyModel()
        self.multifilter_sort_proxy_model.setSourceModel(self.model)
        self.tableView_patient.setModel(self.multifilter_sort_proxy_model)
        self.tableView_lab.setModel(self.multifilter_sort_proxy_model)
        self.tableView_organism.setModel(self.multifilter_sort_proxy_model)

        self.set_col_widths()

    def reset_proxy(self):
        self.multifilter_sort_proxy_model.sort(-1)
        self.tableView_patient.horizontalHeader().setSortIndicator(-1, Qt.SortOrder.DescendingOrder)
        self.lineEdit_filter.setText('')
        self.pushButton_filtermarked.setChecked(False)
        self.set_mark_filter()

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
                for type in self.conf['seqfiles']:
                    ext = self.conf['seqfiles'][type]['ext']
                    for fp in f.rglob(ext):
                        parsed_files.append(fp)

            else:
                for type in self.conf['seqfiles']:
                    ext = self.conf['seqfiles'][type]['ext']
                    if f.match(ext):
                        parsed_files.append(f)


        _data = {}
        for file in parsed_files:
            seqpath = file.parent
            filename = file.name
            filename_obj = Path(filename)

            sample = filename.split('_')[0]

            if not sample in _data:
                _data[sample] = {}
                _data[sample]['Seq_path'] = seqpath

            if filename_obj.match(self.conf['seqfiles']['fastq_gz']['ext']):
                f = file.stem.split('.')[0]
                lane = f.split('_')[-1]

                _data[sample]['Lane'] = lane

                for field, pat in self.conf['seqfiles']['fastq_gz']['fields'].items():
                    print(pat, field)
                    if filename_obj.match(pat):
                        _data[sample][field] = filename

            elif filename_obj.match(self.conf['seqfiles']['fast5']['ext']):
                for field, pat in self.conf['seqfiles']['fast5']['fields'].items():
                    if filename_obj.match(pat):
                        _data[sample][field] = filename

        data = []
        for sample in _data:
            row = dict()
            row['Mark'] = 0
            row['Internal_lab_ID'] = sample
            for key in _data[sample]:
                row[key] = _data[sample][key]

            data.append(row)

        self.add_data(data)

    def find_duplicates(self, df1, df2):
        df3 = df1.append(df2)

        duplicates = df3['Internal_lab_ID'].duplicated().any()

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

    def get_visible_tableview(self):
        for tbv in [self.tableView_patient, self.tableView_lab, self.tableView_organism]:
            if tbv.isVisible():
                return tbv

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            visible_tableview = self.get_visible_tableview()
            if visible_tableview:
                indexes = visible_tableview.selectedIndexes()
                model = visible_tableview.model()
                for i in indexes:
                    if model.flags(i) & Qt.ItemIsEditable:
                        model.setData(i, "", Qt.EditRole)

        elif event.key() == Qt.Key_Copy:
            visible_tableview = self.get_visible_tableview()
            if visible_tableview:
                indexes = visible_tableview.selectedIndexes()
                model = visible_tableview.model()
                for i in indexes:
                    data = model.data(i, Qt.DisplayRole)

        if event.key() == Qt.Key_Return:
            visible_tableview = self.get_visible_tableview()
            print(visible_tableview)
            if visible_tableview:
                indexes = visible_tableview.selectedIndexes()
                visible_tableview.edit(indexes[0])
        else:
            super().keyPressEvent(event)

    def upload(self):
        meta_fields = [field for field in self.conf['model_fields'] if self.conf['model_fields'][field]['to_meta']]
        df_submit = self.df[meta_fields]

        seqfiles = {}
        for index, row in self.df.iterrows():
            _tmp = []

            if row['Fastq1']:
                _tmp.append(Path(row['Seq_path'], row['Fastq1']))
            if row['Fastq2']:
                _tmp.append(Path(row['Seq_path'], row['Fastq2']))
            if row['Fast5']:
                _tmp.append(Path(row['Seq_path'], row['Fast5']))

            seqfiles[row['Internal_lab_ID']] = _tmp

        print(df_submit)
        for idx in seqfiles:
            print(seqfiles[idx])


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
