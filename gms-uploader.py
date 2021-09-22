import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from modules.pandasmodel import PandasModel
from modules.delegates import CompleterDelegate, ComboBoxDelegate, \
    DateAutoCorrectDelegate, CheckBoxDelegate, AgeDelegate
from modules.dialogs import MsgError, MsgAlert, ValidationDialog
from modules.sortfilterproxymodel import MultiSortFilterProxyModel, MarkedFilterProxyModel
from modules.auxiliary_functions import get_pseudo_id_code_number, zfill_int, to_list
from modules.validate import validate
from modules.upload import hcp_upload
import pandas as pd
from datetime import datetime
from pathlib import Path
import yaml
from ui.mw import Ui_MainWindow
import qdarktheme

__version__ = '0.1.1'
__title__ = 'GMS-uploader'


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.clipboard = QGuiApplication.clipboard()

        self.qsettings = QSettings("Genomic Medicine Sweden", "GMS-uploader")

        self.setWindowIcon(QIcon('icons/GMS-logo.png'))
        self.setWindowTitle(__title__ + " " + __version__)

        self.actionsave_meta.setDisabled(True)
        self.action_open_meta.setDisabled(True)

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
        # print(all_keys)

        for key in all_keys:
            wtype, field = key.split('/')

            if wtype not in self.conf['settings']:
                # print("wtype not in conf settings", wtype)
                return False
            if field not in self.conf['settings'][wtype]:
                # print("field not in conf settings", field)
                return False

        for wtype in self.conf['settings']:
            for field in self.conf['settings'][wtype]:
                store_key = "/".join([wtype, field])
                if store_key not in all_keys:
                    # print("store_key not in all_keys", store_key)
                    return False

        return True

    def settings_init(self):
        self.qsettings.clear()

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

        self.set_pseudo_id_start()

    def set_static_lineedits(self):
        self.lineEdit_Submitter.setText(self.qsettings.value("qlineedits/Submitter"))
        self.lineEdit_key_id.setText(self.qsettings.value("qlineedits/AWS_key_id"))
        self.lineEdit_endpoint.setText(self.qsettings.value("qlineedits/Endpoint"))
        self.lineEdit_secret_key.setText(self.qsettings.value("qlineedits/AWS_secret_key"))
        self.lineEdit_Lab.setText(self.qsettings.value("qcomboboxes/Lab"))
        self.lineEdit_Sequencing_technology.setText(self.qsettings.value("qcomboboxes/Sequencing_technology"))
        self.lineEdit_host.setText(self.qsettings.value("qcomboboxes/Host"))
        self.lineEdit_lib_method.setText(self.qsettings.value("qcomboboxes/Library_method"))
        self.lineEdit_bucket.setText(self.qsettings.value("qcomboboxes/HCP_buckets"))
        self.lineEdit_pseudo_id.setText(self.qsettings.value("no_widget/Pseudo_ID_start"))

    def set_pseudo_id_path(self):
        obj = self.sender()
        button_name = obj.objectName()
        name = button_name.strip("button")

        dialog = QFileDialog()

        default_fn = "gms-uploader_1_pseudoids.txt"

        pseudo_id_fp, _ = dialog.getSaveFileName(self,
                                                 'Set an awesome filepath to store pseudo IDs',
                                                 default_fn,
                                                 "Pseudo ID store files (*_pseudoids.txt)",
                                                 options=QFileDialog.DontUseNativeDialog |
                                                         QFileDialog.DontConfirmOverwrite)
        pif_obj = Path(pseudo_id_fp)
        if pif_obj.parent.exists():
            edit = self.stackedWidgetPage2.findChild(QLineEdit, name, Qt.FindChildrenRecursively)
            edit.setText(pseudo_id_fp)
            pif_obj.touch(exist_ok=True)

    def set_data_root_path(self):
        obj = self.sender()
        button_name = obj.objectName()
        name = button_name.strip("button")

        dialog = QFileDialog()

        default_fn = str(Path.home())

        dirpath = dialog.getExistingDirectory(self,
                                              'Select an awesome root data path',
                                              default_fn,
                                              options=QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)

        edit = self.stackedWidgetPage2.findChild(QLineEdit, name, Qt.FindChildrenRecursively)
        edit.setText(dirpath)

    def set_metadata_save_path(self):
        obj = self.sender()
        button_name = obj.objectName()
        name = button_name.strip("button")

        dialog = QFileDialog()

        default_fn = str(Path.home())

        dirpath = dialog.getExistingDirectory(self,
                                              'Select an awesome root data path',
                                              default_fn,
                                              options=QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)

        edit = self.stackedWidgetPage2.findChild(QLineEdit, name, Qt.FindChildrenRecursively)
        edit.setText(dirpath)

    def settings_setup(self):
        for name in self.conf['settings']['qlineedits']:
            if name in self.conf['add_buttons']:
                if name == "Pseudo_ID_filepath":
                    func = self.set_pseudo_id_path
                elif name == "Data_root_path":
                    func = self.set_data_root_path
                elif name == "Metadata_save_path":
                    func = self.set_metadata_save_path

                button_name = name + "button"
                button = QPushButton("...", objectName=button_name)
                button.clicked.connect(func)
                edit = QLineEdit(objectName=name)
                edit.textChanged.connect(self.settings_update)
                edit.setReadOnly(True)

                hbox = QHBoxLayout()
                hbox.addWidget(edit)
                hbox.addWidget(button)

                self.formLayout_settings.addRow(QLabel(name), hbox)

                store_key = "/".join(['qlineedits', name])
                value = self.qsettings.value(store_key)
                edit.setText(value)

            else:
                edit = QLineEdit(objectName=name, editingFinished=self.settings_update)
                if 'qlineedits' in self.conf['echomode_password']:
                    if name in self.conf['echomode_password']['qlineedits']:
                        edit.setEchoMode(QLineEdit.Password)
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
            items = to_list(self.qsettings.value(store_key))

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

        store_key = "/".join(['qcomboboxes', 'Lab'])

        self.set_pseudo_id_start()
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

        self.set_pseudo_id_start()
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
        datadir = self.qsettings.value('qlineedits/Data_root_path')
        dialog = QFileDialog()
        files, _ = dialog.getOpenFileNames(self,
                                        "Select sequence data files",
                                        datadir,
                                        "Sequence files (*.fast5 *.fastq.gz *.fastq *.fq.gz *.fq")

        self.parse_files(files)

    def set_icons(self):

        self.action_open_meta.setIcon(QIcon('fontawesome/file-import-solid.svg'))
        self.actionsave_meta.setIcon(QIcon('fontawesome/save-solid.svg'))
        self.actionmetadata.setIcon(QIcon('fontawesome/table-solid.svg'))
        self.actionpreferences.setIcon(QIcon('fontawesome/cogs-solid.svg'))
        self.actionupload.setIcon(QIcon('fontawesome/upload-solid.svg'))
        self.actionselect_seq_files.setIcon(QIcon('fontawesome/dna-solid.svg'))

        self.pushButton_filldown.setIcon(QIcon('fontawesome/arrow-down-solid.svg'))
        self.pushButton_filldown.setIconSize(QSize(18, 18))
        self.pushButton_drop.setIcon(QIcon('fontawesome/times-solid.svg'))
        self.pushButton_drop.setIconSize(QSize(18, 18))
        self.pushButton_clear.setIcon(QIcon('fontawesome/trash-solid.svg'))
        self.pushButton_clear.setIconSize(QSize(14, 14))
        self.pushButton_resetfilters.setIcon(QIcon('fontawesome/filter-reset-solid.svg'))
        self.pushButton_resetfilters.setIconSize(QSize(14, 14))
        self.pushButton_filtermarked.setIcon(QIcon('fontawesome/filter-solid.svg'))
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
        items.extend(to_list(self.qsettings.value(store_key)))

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
                _data[sample]['Seq_path'] = str(seqpath)

            if filename_obj.match(self.conf['seqfiles']['fastq_gz']['ext']):
                f = file.stem.split('.')[0]
                lane = f.split('_')[-1]

                _data[sample]['Lane'] = lane

                for field, pat in self.conf['seqfiles']['fastq_gz']['fields'].items():
                    if filename_obj.match(pat):
                        _data[sample][field] = str(filename)

            elif filename_obj.match(self.conf['seqfiles']['fast5']['ext']):
                for field, pat in self.conf['seqfiles']['fast5']['fields'].items():
                    if filename_obj.match(pat):
                        _data[sample][field] = str(filename)

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
        if event.key() == Qt.Key_Return:
            visible_tableview = self.get_visible_tableview()
            if visible_tableview:
                indexes = visible_tableview.selectedIndexes()
                visible_tableview.edit(indexes[0])

        elif event.key() == Qt.Key_Delete:
            visible_tableview = self.get_visible_tableview()
            if visible_tableview:
                indexes = visible_tableview.selectedIndexes()
                model = visible_tableview.model()
                for i in indexes:
                    if model.flags(i) & Qt.ItemIsEditable:
                        model.setData(i, "", Qt.EditRole)

        elif event.matches(QKeySequence.Copy):
            visible_tableview = self.get_visible_tableview()
            if visible_tableview:
                indexes = visible_tableview.selectedIndexes()
                model = visible_tableview.model()

                c = []
                r = []
                old_row = None

                for i in indexes:
                    if i.row() == old_row or old_row is None:
                        c.append(model.data(i, Qt.DisplayRole))
                        old_row = i.row()
                    else:
                        r.append("\t".join(c))
                        c = []
                        c.append(model.data(i, Qt.DisplayRole))
                        old_row = i.row()

                r.append("\t".join(c))

                copy_data = "\n".join(r)
                self.clipboard.setText(copy_data)

        elif event.matches(QKeySequence.Paste):

            clipboard = QGuiApplication.clipboard()
            mimeData = clipboard.mimeData()

            curr_view = self.get_visible_tableview()

            model = curr_view.model()
            index = curr_view.selectionModel().currentIndex()
            i_row = index.row()
            i_col = index.column()

            rows = mimeData.text().split("\n")
            for i, r in enumerate(rows):
                columns = r.split("\t")
                for j, value in enumerate(columns):
                    model.setData(model.index(i_row + i, i_col + j), value)

        else:
            super().keyPressEvent(event)

    def set_pseudo_id_start(self):
        file = self.qsettings.value("qlineedits/Pseudo_ID_filepath")
        file_obj = Path(file)

        self.qsettings.setValue('no_widget/Pseudo_ID_start', "None")

        if file_obj.exists():
            pseudo_ids = file_obj.read_text().splitlines()

            prev_prefix, prev_number = get_pseudo_id_code_number(pseudo_ids)

            if prev_number < 0:
                msg = MsgError("Something is wrong with the set pseudo_id file.")
                msg.exec()
            else:
                lab = self.qsettings.value('qcomboboxes/Lab')

                if lab:
                    curr_prefix = self.conf['tr']['Lab_to_code'][lab]

                    if prev_prefix is not None:
                        if curr_prefix != prev_prefix:
                            msg = MsgError("Current and previous Pseudo_ID do not match.")
                            msg.exec()

                    elif curr_prefix == prev_prefix or prev_prefix is None:
                        curr_znumber_str = zfill_int(prev_number + 1)
                        pseudo_id_start = curr_prefix + "-" + curr_znumber_str
                        self.qsettings.setValue('no_widget/Pseudo_ID_start', pseudo_id_start)
                        self.qsettings.setValue('no_widget/Pseudo_ID_start_int', prev_number + 1)
                        self.qsettings.setValue('no_widget/Pseudo_ID_start_prefix', curr_prefix)

    def create_pseudo_ids(self):
        pseudo_ids = []
        prefix = self.qsettings.value('no_widget/Pseudo_ID_start_prefix')
        start = self.qsettings.value('no_widget/Pseudo_ID_start_int')
        end = start + len(self.df)

        for number in range(start, end):
            pseudo_ids.append(prefix + "-" + zfill_int(number))

        return pseudo_ids

    def upload(self):
        self.df['Lab'] = self.qsettings.value('qcomboboxes/Lab')
        self.df['Host'] = self.qsettings.value('qcomboboxes/Host')
        self.df['Sequencing_technology'] = self.qsettings.value('qcomboboxes/Sequencing_technology')

        df2 = self.df.fillna('')
        errors = validate(df2)

        if errors:
            vdialog = ValidationDialog(errors)
            vdialog.exec()
            return False

        sample_seqs = {}
        for _, row in self.df.iterrows():
            _seqs = []
            if row['Fastq1']:
                _seqs.append(Path(row["Seq_path"], row["Fastq1"]))
            if row['Fastq2']:
                _seqs.append(Path(row["Seq_path"], row["Fastq2"]))
            if row['Fast5']:
                _seqs.append(Path(row["Seq_path"], row["Fast5"]))

            sample_seqs[row['Internal_lab_ID']] = _seqs


        self.df['Lab_code'] = self.df['Lab'].apply(lambda x: self.conf['tr']['Lab_to_code'][x])
        self.df['Region_code'] = self.df['Region'].apply(lambda x: self.conf['tr']['Region_to_code'][x])
        self.df['Pseudo_ID'] = self.create_pseudo_ids()

        meta_fields = [field for field in self.conf['model_fields'] if self.conf['model_fields'][field]['to_meta']]
        df_submit = self.df[meta_fields]

        now = datetime.now()
        dt_str = now.strftime("%Y-%m-%dT%H.%M.%S")
        json_file = Path(self.qsettings['qlineedits/Metadata_save_path'], dt_str + "_meta.json")

        with open(json_file, 'w', encoding='utf-8') as file:
            df_submit.to_json(file, orient="records", force_ascii=False)

        if json_file \
            and sample_seqs \
            and dt_str \
            and self.qsettings['qlineedits/Endpoint'] \
            and self.qsettings['qlineedits/AWS_key_id'] \
            and self.qsettings['qlineedits/AWS_secret_key'] \
            and self.qsettings['qcomboboxes/HCP_buckets'] \
            and self.qsettings['qlineedits/Pseudo_ID_filepath']:

            ret_ok = hcp_upload(json_file,
                            sample_seqs,
                            dt_str,
                            self.qsettings['qlineedits/Endpoint'],
                            self.qsettings['qlineedits/AWS_key_id'],
                            self.qsettings['qlineedits/AWS_secret_key'],
                            self.qsettings['qcomboboxes/HCP_buckets']
                            )

            if ret_ok:
                pseudo_id_file = Path(self.qsettings['qlineedits/Pseudo_ID_filepath'])

                with pseudo_id_file.open("a") as f:
                    for i, row in df_submit.iterrows():
                        f.write(row['Pseudo_ID'] + "\t" + dt_str)


def main():
    try:
        import pyi_splash
    except:
        pass

    app = QApplication(sys.argv)
    window = MainWindow()
    app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    window.show()

    try:
        pyi_splash.close()
    except:
        pass

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
