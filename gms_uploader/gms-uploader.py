import sys
from io import StringIO
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
import resources
from modules.pandasmodel import PandasModel
from modules.delegates import ComboBoxDelegate, \
    DateAutoCorrectDelegate, AgeDelegate, IconCheckBoxDelegate
from modules.dialogs import MsgError, MsgAlert, ValidationDialog
from modules.sortfilterproxymodel import MultiSortFilterProxyModel
from modules.auxiliary_functions import get_pseudo_id_code_number, zfill_int, to_list, get_pd_row_index, \
    date_validate, age_validate, add_gridlayout_row
from modules.validate import validate
from modules.dialogs import Uploader
import pandas as pd
from datetime import datetime
from pathlib import Path
import yaml
import csv
from gms_uploader.ui.mw import Ui_MainWindow
import qdarktheme
#from qt_material import apply_stylesheet

__version__ = '0.1.1-beta.5'
__title__ = 'GMS-uploader'


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setup_complete = False
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.clipboard = QGuiApplication.clipboard()

        self.qsettings = QSettings("Genomic Medicine Sweden", "GMS-uploader")

        self.setWindowIcon(QIcon(':/img/GMS-logo.png'))
        self.setWindowTitle(__title__ + " " + __version__)

        self.set_tb_bkg()

        # add icons
        self.set_icons()

        default_config_path = Path('config', 'config.yaml')
        with default_config_path.open(encoding='utf8') as fp:
            self.conf = yaml.safe_load(fp)

        if not self.settings_validate():
            msg = MsgAlert("Incompatible saved settings: (re-)initializing...")
            msg.exec()

            self.qsettings.clear()
            self.settings_init()

        self.fx_config = None

        self.settings_setup()

        self.tableView_columns = list(self.conf['model_fields'].keys())

        self.df = pd.DataFrame(columns=self.tableView_columns)
        self.model = PandasModel(self.df, self.conf['model_fields'])
        self.mfilter_sort_proxy_model = MultiSortFilterProxyModel()

        self.filter_cols = self.get_filter_cols()

        # setup settings

        self.delegates = {}
        self.delegates['patient'] = {}
        self.delegates['lab'] = {}
        self.delegates['organism'] = {}

        self.set_signals()
        self.tableviews_setup()
        self.stackedWidget.setCurrentIndex(0)
        self.tabWidget_metadata.setCurrentIndex(0)
        self.set_hidden_columns()
        self.set_col_widths()

        self.set_delegates()

        # Status widgets change status to activated when there is data in the model. Default is disabled.

        self.status_widgets = [
            self.action_import_csv,
            self.action_upload_meta_seqs,
            self.pushButton_filtermarked,
            self.pushButton_invert,
            self.pushButton_drop,
            self.pushButton_clear,
            self.pushButton_filldown,
            self.pushButton_resetfilters,
            self.action_save_meta,
            self.action_import_fx,
            self.action_paste_fx,
            self.lineEdit_filter
        ]

        self.set_datastatus_empty(True)
        self.ui_init()
        self.setup_complete = True

    # setup and init-related functions

    def ui_init(self):
        self.tabWidget_metadata.setStyleSheet("QTabWidget::pane { border: 0; }")
        self.scrollArea.setStyleSheet("QScrollArea { border: 0; }")
        self.toolBar.setFixedWidth(50)
        self.toolBar.setMovable(False)
        self.tabWidget_metadata.setTabText(0, "patient metadata")
        self.tabWidget_metadata.setTabText(1, "organism metadata")
        self.tabWidget_metadata.setTabText(2, "lab metadata")
        self.lineEdit_filter.setPlaceholderText("freetext filter")

    def get_filter_cols(self):
        cols = list(self.df.columns)
        used_cols = self.conf['freetext_filter']['model_fields']
        return [self.df.columns.get_loc(c) for c in cols if c in used_cols]

    def set_tb_bkg(self):
        """
        Sets bg image to tableviews. Image shown before metadata is imported.
        :return: None
        """

        img = ':/img/GMS-logo.png'

        for tbv in [self.tableView_patient,
                    self.tableView_organism,
                    self.tableView_lab]:
            tbv.setStyleSheet(
                """
                background-repeat: no-repeat;
                background-position: center;
                background-image: url(%s);
                """
                % img
            )
            tbv.horizontalScrollBar().setStyleSheet(
                """
                background: white;
                """
            )

    def rem_tb_bkg(self):
        """
        Removes bg image from tableviews. Images removed when metadata is imported, otherwise
        they are visible through the tables.
        :return: None
        """
        for tbv in [self.tableView_patient, self.tableView_organism, self.tableView_lab]:
            tbv.setStyleSheet("background-image: none;")

    def set_signals(self):
        """
        Setup of signals for static widgets (pushbuttons, actionbuttons, lineedit for filter).
        :return:
        """
        self.action_show_prefs.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.action_show_meta.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.lineEdit_filter.textChanged.connect(self.set_free_filter)
        self.pushButton_filtermarked.setCheckable(True)
        self.pushButton_filtermarked.clicked.connect(self.set_mark_filter)
        self.pushButton_drop.clicked.connect(self.drop_rows)
        self.pushButton_clear.clicked.connect(self.clear_table)
        self.action_select_seq_files.triggered.connect(self.get_seq_files)
        self.action_upload_meta_seqs.triggered.connect(self.upload)
        self.action_save_meta.triggered.connect(self.save_metadata_file)
        self.action_open_meta.triggered.connect(self.open_metadata_file)
        self.pushButton_invert.clicked.connect(self.invert_marks)
        self.action_import_csv.triggered.connect(self.get_csv_file_combine)
        self.action_import_fx.triggered.connect(self.import_fx_file)

    def set_icons(self):

        self.action_open_meta.setIcon(QIcon(':/icons/AppIcons/folder-open-outline_mdi.svg'))
        self.action_save_meta.setIcon(QIcon(':/icons/AppIcons/content-save-outline_mdi.svg'))
        self.action_show_meta.setIcon(QIcon(':/icons/AppIcons/table_mdi.svg'))
        self.action_show_prefs.setIcon(QIcon(':/icons/AppIcons/cog-outline_mdi.svg'))
        self.action_upload_meta_seqs.setIcon(QIcon(':/icons/AppIcons/tray-arrow-up_mdi.svg'))
        self.action_select_seq_files.setIcon(QIcon(':/icons/AppIcons/folder-open-outline-dna_mdi.svg'))
        self.action_import_csv.setIcon(QIcon(':/icons/AppIcons/import-csv_own.svg'))
        self.action_import_fx.setIcon(QIcon(':/icons/AppIcons/content-import-fx_own.svg'))
        self.action_paste_fx.setIcon(QIcon(':/icons/AppIcons/content-paste-fx_own.svg'))
        self.pushButton_filldown.setIcon(QIcon(':/icons/AppIcons/arrow-down_mdi.svg'))
        self.pushButton_drop.setIcon(QIcon(':/icons/AppIcons/close_mdi.svg'))
        self.pushButton_clear.setIcon(QIcon(':/icons/AppIcons/delete-outline_mdi.svg'))
        self.pushButton_resetfilters.setIcon(QIcon(':/icons/AppIcons/filter-remove-outline_mdi.svg'))
        self.pushButton_filtermarked.setIcon(QIcon(':/icons/AppIcons/filter-outline_mdi.svg'))
        self.pushButton_invert.setIcon(QIcon(':/icons/AppIcons/invert_own.svg'))

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

    def settings_validate(self):
        """
        Compares qsetting keys with keys in config file to make sure there is no mismatch.
        :return: True if ok, False otherwise
        """
        all_keys = self.qsettings.allKeys()
        for key in all_keys:
            wtype, field = key.split('/')
            if wtype not in self.conf['settings_values']:
                return False
            if field not in self.conf['settings_values'][wtype]:
                return False

        for wtype in self.conf['settings_values']:
            for field in self.conf['settings_values'][wtype]:
                store_key = "/".join([wtype, field])
                if store_key not in all_keys:
                    return False

        return True

    def settings_init(self):
        """
        If there is a qsettings and config settings don't match, clear qsettings and reset to
        default values (from config).
        :return: None
        """
        self.qsettings.clear()

        for name in self.conf['settings_values']['hidden']:
            store_key = "/".join(['hidden', name])
            self.qsettings.setValue(store_key, self.conf['settings_values']['hidden'][name])

        for name in self.conf['settings_values']['entered_value']:
            store_key = "/".join(['entered_value', name])
            self.qsettings.setValue(store_key, self.conf['settings_values']['entered_value'][name])

        for name in self.conf['settings_values']['select_single']:
            store_key = "/".join(['select_single', name])
            for i, key in enumerate(self.conf['settings_values']['select_single'][name]):
                if self.conf['settings_values']['select_single'][name][key]:
                    self.qsettings.setValue(store_key, key)

        for name in self.conf['settings_values']['select_multi']:
            store_key = "/".join(['select_multi', name])
            checked_items = []
            for key, checked in self.conf['settings_values']['select_multi'][name].items():
                if checked:
                    checked_items.append(key)

            self.qsettings.setValue(store_key, checked_items)

        self.set_pseudo_id_start()

    def set_static_lineedits(self):
        """
        Sets values in static lineedits on the dataview pane.
        :return: None
        """
        self.lineEdit_submitter.setText(self.qsettings.value("entered_value/submitter"))
        self.lineEdit_credentials_path.setText(self.qsettings.value("entered_value/credentials_filepath"))
        self.lineEdit_lab.setText(self.qsettings.value("select_single/lab"))
        self.lineEdit_seq_technology.setText(self.qsettings.value("select_single/seq_technology"))
        self.lineEdit_host.setText(self.qsettings.value("select_single/host"))
        self.lineEdit_lib_method.setText(self.qsettings.value("select_single/library_method"))
        self.lineEdit_bucket.setText(self.qsettings.value("select_single/hcp_bucket"))
        self.lineEdit_pseudo_id.setText(self.qsettings.value("hidden/pseudo_id_start"))
        self.lineEdit_import_fx.setText(self.qsettings.value("select_single/import_fx"))

    def settings_setup(self):
        """
        Creates and sets up dymamic setting widgets based on the config file
        :return: None
        """

        for category in self.conf['settings_structure']:
            category_name = category['label']
            label = QLabel(category_name)
            label.setProperty("class", "bold")
            self.verticalLayout_forms.addWidget(label)

            if category['target_layout'] == "form":
                grid_layout = QGridLayout()
                grid_layout.setColumnMinimumWidth(0, 150)

                self.verticalLayout_forms.addLayout(grid_layout)

                for item in category['items']:
                    for field_type, fields in item.items():
                        if field_type == "entered_value":
                            for field in fields:
                                func = self.get_button_func(field)
                                if func:
                                    button_name = field + "button"
                                    button = QPushButton("...", objectName=button_name)
                                    button.clicked.connect(func)
                                    edit = QLineEdit(objectName=field)
                                    edit.textChanged.connect(self.settings_update)
                                    edit.setReadOnly(True)

                                    hbox = QHBoxLayout()
                                    hbox.addWidget(edit)
                                    hbox.addWidget(button)

                                    label = QLabel(field)
                                    label.setProperty("class", "padding-left")
                                    label.setMinimumWidth(40)

                                    store_key = "/".join([field_type, field])
                                    value = self.qsettings.value(store_key)
                                    edit.setText(value)

                                    add_gridlayout_row(grid_layout, label, hbox)

                                else:
                                    edit = QLineEdit(objectName=field, editingFinished=self.settings_update)
                                    store_key = "/".join([field_type, field])
                                    value = self.qsettings.value(store_key)
                                    edit.setText(value)

                                    label = QLabel(field)
                                    label.setProperty("class", "padding-left")
                                    label.setMinimumWidth(40)

                                    add_gridlayout_row(grid_layout, label, edit)

                        elif field_type == "select_single":
                            for field in fields:
                                combo = QComboBox(objectName=field)
                                combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                                items = []
                                if field in self.conf['add_empty_selection']:
                                    items = ['None']

                                items.extend(list(self.conf['settings_values']['select_single'][field].keys()))
                                combo.addItems(items)

                                store_key = "/".join(['select_single', field])
                                value = self.qsettings.value(store_key)
                                combo.setCurrentText(value)

                                label = QLabel(field)
                                label.setProperty("class", "padding-left")
                                label.setMinimumWidth(40)

                                combo.currentTextChanged.connect(self.settings_update)

                                add_gridlayout_row(grid_layout, label, combo)

                        elif field_type == "select_single_fx":
                            for field in fields:
                                combo = QComboBox(objectName=field)
                                combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                                if field in self.conf['add_empty_selection']:
                                    items = ['None']

                                base = Path(__file__).parent
                                fx_module_dirs = list(Path(base, 'fx').iterdir())

                                for d in fx_module_dirs:
                                    items.append(str(d.name))

                                combo.addItems(items)

                                store_key = "/".join(['select_single', field])
                                value = self.qsettings.value(store_key)
                                combo.setCurrentText(value)

                                label = QLabel(field)
                                label.setProperty("class", "padding-left")
                                label.setMinimumWidth(40)

                                combo.currentTextChanged.connect(self.settings_update)

                                add_gridlayout_row(grid_layout, label, combo)

            elif category['target_layout'] == "tabs":

                tabwidget_settings = QTabWidget(objectName='tabwidget_settings')
                tabwidget_settings.setMinimumHeight(420)
                tabwidget_settings.setStyleSheet("QTabWidget::pane { border: 0; }")
                tabwidget_settings.setMinimumHeight(550)
                self.verticalLayout_tabs.addWidget(tabwidget_settings)

                for item in category['items']:
                    for field_type, fields in item.items():
                        if field_type == "select_multi":
                            for field in fields:
                                store_key = "/".join([field_type, field])
                                store_checked = to_list(self.qsettings.value(store_key))

                                model = QStandardItemModel()
                                model.setColumnCount(2)
                                tableview = QTableView()
                                model = QStandardItemModel(objectName=field)
                                model.setColumnCount(2)

                                for key, checked in self.conf['settings_values'][field_type][field].items():
                                    item1 = QStandardItem("0")
                                    item2 = QStandardItem(key)

                                    if key in store_checked:
                                        item1.setText("1")

                                    model.appendRow([item1, item2])

                                tableview.setModel(model)
                                tableview.setItemDelegateForColumn(0, IconCheckBoxDelegate(None))
                                tableview.setColumnWidth(0, 15)
                                hheader = tableview.horizontalHeader()
                                hheader.setStretchLastSection(True)
                                hheader.hide()
                                tableview.verticalHeader().setDefaultSectionSize(20)
                                tableview.verticalHeader().hide()
                                tableview.setShowGrid(False)
                                model.itemChanged.connect(self.settings_multi_update)

                                tabwidget_settings.addTab(tableview, field)


        self.set_pseudo_id_start()
        self.set_static_lineedits()

    def settings_update(self):
        """
        Called when dynamic setting widgets are changed, updates qsettings values.
        :return: None
        """
        obj = self.sender()
        name = obj.objectName()

        if isinstance(obj, QLineEdit):
            store_key = "/".join(['entered_value', name])
            self.qsettings.setValue(store_key, obj.text())

        elif isinstance(obj, QComboBox):
            store_key = "/".join(['select_single', name])
            value = obj.currentText()
            self.qsettings.setValue(store_key, value)
            self.update_delegates()

        self.set_pseudo_id_start()
        self.set_static_lineedits()

    def settings_multi_update(self, index):
        model = index.model()
        name = model.objectName()

        checked_items = []
        for row in range(model.rowCount()):
            if str(model.data(model.index(row, 0)))== "1":
                checked_items.append(model.data(model.index(row, 1)))

        store_key = "/".join(['select_multi', name])
        self.qsettings.setValue(store_key, checked_items)
        self.update_delegates()

    def tableviews_setup(self):
        """
        Setup of data tableviews, connects to mfilter_sort_proxy_model, and the pandas model.
        :return: None
        """

        self.mfilter_sort_proxy_model.setSourceModel(self.model)

        self.tableView_patient.setModel(self.mfilter_sort_proxy_model)
        self.tableView_patient.setEditTriggers(QAbstractItemView.DoubleClicked
                                               | QAbstractItemView.SelectedClicked
                                               | QAbstractItemView.EditKeyPressed)
        self.tableView_patient.horizontalHeader().setStretchLastSection(True)
        self.tableView_patient.horizontalHeader().setSectionsMovable(True)
        self.tableView_patient.setSortingEnabled(True)

        self.tableView_organism.setModel(self.mfilter_sort_proxy_model)
        self.tableView_organism.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)
        self.tableView_organism.horizontalHeader().setStretchLastSection(True)
        self.tableView_organism.horizontalHeader().setSectionsMovable(True)
        self.tableView_organism.setSortingEnabled(True)

        self.tableView_lab.setModel(self.mfilter_sort_proxy_model)
        self.tableView_lab.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.SelectedClicked | QAbstractItemView.EditKeyPressed)
        self.tableView_lab.horizontalHeader().setStretchLastSection(True)
        self.tableView_lab.horizontalHeader().setSectionsMovable(True)
        self.tableView_lab.setSortingEnabled(True)

        self.pushButton_resetfilters.clicked.connect(self.reset_sort_filter)
        self.pushButton_filldown.clicked.connect(self.filldown)
        self.tableView_patient.verticalHeader().hide()
        self.tableView_lab.verticalHeader().hide()
        self.tableView_organism.verticalHeader().hide()
        self.update_model()

    def load_fx_settings(self):
        store_key = "/".join(['select_single', 'import_fx'])
        fx_name = self.qsettings.value(store_key)


        default_config_path = Path('config', 'config.yaml')
        with default_config_path.open(encoding='utf8') as fp:
            self.conf = yaml.safe_load(fp)

    # model and data-import related functions

    def update_model(self):
        self.model = PandasModel(self.df, self.conf['model_fields'])
        self.mfilter_sort_proxy_model = MultiSortFilterProxyModel()
        self.mfilter_sort_proxy_model.setSourceModel(self.model)
        self.tableView_patient.setModel(self.mfilter_sort_proxy_model)
        self.tableView_lab.setModel(self.mfilter_sort_proxy_model)
        self.tableView_organism.setModel(self.mfilter_sort_proxy_model)

        self.set_col_widths()

    def df_insert(self, df, row):
        insert_loc = df.index.max()

        if pd.isna(insert_loc):
            df.loc[0] = row
        else:
            df.loc[insert_loc + 1] = row

    def verify_files(self, files):
        """
        Ensures that all filespaths in a list exist and have correct suffixes, corresponding to
        raw sequence data files. Only correct files are returned. If a path is a dir, paths for files in that directory are listed,
        verified and returned.
        :param files: list of filepaths and/or dirpaths
        :return: list of verified filepaths
        """
        verified_files = []
        for file in files:
            f = Path(file)
            if f.is_dir():
                for type in self.conf['seq_files']:
                    ext = self.conf['seq_files'][type]['ext']
                    for fp in f.rglob(ext):
                        if Path(fp).exists():
                            verified_files.append(fp)

            else:
                for type in self.conf['seq_files']:
                    ext = self.conf['seq_files'][type]['ext']
                    if f.match(ext) and f.exists():
                        verified_files.append(f)

        return verified_files

    def extract_metadata_from_filenames(self, files):
        """
        Extract metadata from sequence data filenames
        :param files: list of filepaths
        :return: list of dicts with metadata from filenames
        """

        _data = {}
        for file in files:
            seq_path = file.parent
            filename = file.name
            filename_obj = Path(filename)

            sample = filename.split('_')[0]

            if sample not in _data:
                _data[sample] = {}
                _data[sample]['seq_path'] = str(seq_path)

            if filename_obj.match(self.conf['seq_files']['fastq_gz']['ext']):

                f = file.stem.split('.')[0]
                lane = f.split('_')[-1]

                _data[sample]['lane'] = lane

                if 'fastq' not in _data[sample]:
                    _data[sample]['fastq'] = []

                fastq_list = _data[sample]['fastq']
                fastq_list.append(filename)

            elif filename_obj.match(self.conf['seq_files']['fast5']['ext']):
                if 'fast5' not in _data[sample]:
                    _data[sample]['fast5'] = []

                fast5_list = _data[sample]['fast5']
                fast5_list.append(filename)

        filename_metadata = []
        for sample in _data:
            row = dict()
            row['mark'] = 0 # add mark column
            row['internal_lab_id'] = sample
            for key in _data[sample]:
                value = _data[sample][key]
                if isinstance(value, list):
                    sorted_files = sorted(value)
                    row[key] = sorted_files
                else:
                    row[key] = value

            filename_metadata.append(row)

        return filename_metadata

    def find_duplicates(self, df1, df2):
        """
        Checks if the same internal_lab_id are present in two dataframes
        :param df1: dataframe1
        :param df2: dataframe2
        :return: Bool
        """
        df3 = df1.append(df2)
        return df3['internal_lab_id'].duplicated().any()

    def add_files_metadata_to_model(self, data):
        """
        Creates new pandas df, from files and metadata, check for duplicates
        and merge with existing df dataset and create new model.
        :param data: list of dicts containing metadata and filenames
        :return: None
        """
        new_df = pd.DataFrame(data)

        if not new_df.empty:
            if not self.find_duplicates(self.df, new_df):
                self.df = self.df.append(new_df)
                self.df = self.df.fillna('')
                self.update_model()
                self.rem_tb_bkg()
                self.set_datastatus_empty(False)
            else:
                msg_box = QMessageBox()
                msg_box.setText("Duplicate SampleIDs present in imported data.")
                msg_box.exec()

    # set path functions

    def set_seq_path(self):
        """
        Sets sequence base path in dynamic lineedit widget from file-picker.
        :return: None
        """
        obj = self.sender()
        button_name = obj.objectName()
        name = button_name.strip("button")

        dialog = QFileDialog()

        default_path = str(Path.home())

        dirpath = dialog.getExistingDirectory(self,
                                              'Set an awesome seq root path',
                                              default_path,
                                              options=QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)

        if dirpath:
            edit = self.stackedWidgetPage2.findChild(QLineEdit, name, Qt.FindChildrenRecursively)
            edit.setText(dirpath)

    def set_csv_path(self):
        """
        Set base path to for filedialog for importing csv files.
        :return: None
        """
        obj = self.sender()
        button_name = obj.objectName()
        name = button_name.strip("button")

        dialog = QFileDialog()

        default_fn = str(Path.home())

        dirpath = dialog.getExistingDirectory(self,
                                              'Set an awesome csv root path',
                                              default_fn,
                                              options=QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)

        if dirpath:
            edit = self.stackedWidgetPage2.findChild(QLineEdit, name, Qt.FindChildrenRecursively)
            edit.setText(dirpath)

    def set_metadata_output_path(self):
        """
        Sets dir where metadata json files should be stored.
        :return: None
        """
        obj = self.sender()
        button_name = obj.objectName()
        name = button_name.strip("button")

        dialog = QFileDialog()

        default_fn = str(Path.home())

        dirpath = dialog.getExistingDirectory(self,
                                              'Set an awesome metadata output path',
                                              default_fn,
                                              options=QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)

        edit = self.stackedWidgetPage2.findChild(QLineEdit, name, Qt.FindChildrenRecursively)
        edit.setText(dirpath)

    def set_metadata_docs_path(self):
        """
        Sets base dir path where to save and open pickeled metadata dataframes.
        :return: None
        """
        obj = self.sender()
        button_name = obj.objectName()
        name = button_name.strip("button")

        dialog = QFileDialog()

        default_fn = str(Path.home())

        dirpath = dialog.getExistingDirectory(self,
                                              'Set an awesome metadata docs path',
                                              default_fn,
                                              options=QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)

        edit = self.stackedWidgetPage2.findChild(QLineEdit, name, Qt.FindChildrenRecursively)
        edit.setText(dirpath)

    def set_pseudo_id_filepath(self):
        """
        Set filepath to textfile where pseudo_ids should be stored
        :return: None
        """
        obj = self.sender()
        button_name = obj.objectName()
        name = button_name.strip("button")

        dialog = QFileDialog()

        default_fn = "gms-uploader_1_pseudoids.txt"

        pseudo_id_fp, _ = dialog.getSaveFileName(self,
                                                 'Set an awesome pseudo_id filepath',
                                                 default_fn,
                                                 "pseudo_ID files (*_pseudoids.txt)",
                                                 options=QFileDialog.DontUseNativeDialog |
                                                         QFileDialog.DontConfirmOverwrite)
        pif_obj = Path(pseudo_id_fp)
        if pif_obj.parent.exists():
            edit = self.stackedWidgetPage2.findChild(QLineEdit, name, Qt.FindChildrenRecursively)
            edit.setText(pseudo_id_fp)
            pif_obj.touch(exist_ok=True)

    def set_credentials_filepath(self):
        """
        Sets filepath to credentials json file, used for S3 upload to the HCP/NGP
        :return: None
        """
        obj = self.sender()
        button_name = obj.objectName()
        name = button_name.strip("button")

        dialog = QFileDialog()

        credentials_path, _ = dialog.getOpenFileName(self,
                                                     'Select an awesome credentials json file',
                                                     "",
                                                     "json files (*.json)",
                                                     options=QFileDialog.DontUseNativeDialog |
                                                             QFileDialog.DontConfirmOverwrite)

        f_obj = Path(credentials_path)
        if f_obj.parent.exists():
            edit = self.stackedWidgetPage2.findChild(QLineEdit, name, Qt.FindChildrenRecursively)
            edit.setText(credentials_path)

    # delegates

    def update_delegates(self):
        if self.setup_complete:
            self.set_delegates()

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

        store_key = "/".join(["select_multi", field])
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
        """
        sets checboxdelegate
        :param field: field name
        :return: Nothing
        """
        for view in self.conf['model_fields'][field]['view']:
            self.delegates[view][field] = IconCheckBoxDelegate(None)

            if view == 'patient':
                self.tableView_patient.setItemDelegateForColumn(self.tableView_columns.index(field),
                                                                self.delegates[view][field])
            elif view == 'lab':
                self.tableView_lab.setItemDelegateForColumn(self.tableView_columns.index(field),
                                                            self.delegates[view][field])
            elif view == 'organism':
                self.tableView_organism.setItemDelegateForColumn(self.tableView_columns.index(field),
                                                                 self.delegates[view][field])

    # Data-view, filter and related functions, utility functions

    def get_button_func(self, name):
        """
        gets correct slot function for button
        :param name: name of settings field
        :return: func or None if field has no associated button
        """
        func = None
        if name in self.conf['add_buttons']:
            if name == "pseudo_id_filepath":
                func = self.set_pseudo_id_filepath
            elif name == "seq_base_path":
                func = self.set_seq_path
            elif name == "csv_base_path":
                func = self.set_csv_path
            elif name == "metadata_output_path":
                func = self.set_metadata_output_path
            elif name == "metadata_docs_path":
                func = self.set_metadata_docs_path
            elif name == "credentials_filepath":
                func = self.set_credentials_filepath

        return func

    def accept_paste(self, value, colname):

        if not self.conf['model_fields'][colname]['edit'] or colname == 'mark':
            return False

        if isinstance(self.conf['paste_validators']['model_fields'][colname], bool):
            if self.conf['paste_validators']['model_fields'][colname] is True:
                return value
            else:
                return False

        if 'qsettings' in self.conf['paste_validators']['model_fields'][colname]:
            key = self.conf['paste_validators']['model_fields'][colname]['qsettings']
            accepted = self.qsettings.value(key)
            if isinstance(accepted, list):
                if value not in accepted:
                    return False
            if isinstance(accepted, str):
                if value != accepted:
                    return False

        if 'func' in self.conf['paste_validators']['model_fields'][colname]:
            func = self.conf['paste_validators']['model_fields'][colname]['func']
            if func == "date_validate":
                return date_validate(value)

            if func == "age_validate":
                return age_validate(value)

        return value

    def set_mark_filter(self):
        if self.pushButton_filtermarked.isChecked():
            self.mfilter_sort_proxy_model.setCheckedFilter()

        else:
            self.mfilter_sort_proxy_model.clearCheckedFilter()

    def set_free_filter(self):
        text = self.lineEdit_filter.text()
        search = QRegularExpression(text, QRegularExpression.CaseInsensitiveOption)
        self.mfilter_sort_proxy_model.setFilterByColumns(self.filter_cols, search)

    def drop_rows(self):
        self.model.dropMarkedRows()
        if self.df.empty:
            self.set_datastatus_empty(True)

    def filldown(self):
        visible_tableview = self.get_current_tableview()
        if visible_tableview:
            select = visible_tableview.selectionModel()
            index = select.currentIndex()

            max_rows = self.mfilter_sort_proxy_model.rowCount()
            data_orig = self.mfilter_sort_proxy_model.data(index, Qt.DisplayRole)

            for r in range(index.row() + 1, max_rows):
                index_new = self.mfilter_sort_proxy_model.index(r, index.column())
                data_new = self.mfilter_sort_proxy_model.data(index_new, Qt.DisplayRole)
                if data_new == '':
                    self.mfilter_sort_proxy_model.setData(index_new, data_orig, Qt.EditRole)
                else:
                    break

    def clear_table(self):
        self.df = pd.DataFrame(columns=self.tableView_columns)
        self.update_model()
        self.set_datastatus_empty(True)

    def reset_sort_filter(self):
        self.mfilter_sort_proxy_model.sort(-1)
        self.tableView_patient.horizontalHeader().setSortIndicator(-1, Qt.SortOrder.DescendingOrder)
        self.lineEdit_filter.setText('')
        self.pushButton_filtermarked.setChecked(False)
        self.set_mark_filter()

        for i in range(0, self.model.rowCount()):
            idx = self.model.index(i, 0)
            new_value = "0"
            self.model.setData(idx, new_value, Qt.EditRole)

    def get_current_tableview(self):
        for tbv in [self.tableView_patient, self.tableView_lab, self.tableView_organism]:
            if tbv.isVisible():
                return tbv

    def invert_marks(self):
        for i in range(0, self.model.rowCount()):
            idx = self.model.index(i, 0)
            value = self.model.data(idx, Qt.DisplayRole)

            if value == "0":
                new_value = "1"
            else:
                new_value = "0"

            self.model.setData(idx, new_value, Qt.EditRole)

    def set_datastatus_empty(self, value):
        for w in self.status_widgets:
            w.setDisabled(value)

    # pseudo_id-related functions

    def set_pseudo_id_start(self):
        file = self.qsettings.value("entered_value/pseudo_id_filepath")

        if file:
            file_obj = Path(file)

            self.qsettings.setValue('hidden/pseudo_id_start', "None")

            if file_obj.exists():
                pseudo_ids = file_obj.read_text().splitlines()

                prev_prefix, prev_number = get_pseudo_id_code_number(pseudo_ids)

                if prev_number < 0:
                    msg = MsgError("Something is wrong with the set pseudo_id file.")
                    msg.exec()
                else:
                    lab = self.qsettings.value('select_single/lab')

                    if lab:
                        curr_prefix = self.conf['tr']['lab_to_code'][lab]

                        if prev_prefix is not None:
                            if curr_prefix != prev_prefix:
                                msg = MsgError("Current and previous pseudo_id do not match.")
                                msg.exec()

                        elif curr_prefix == prev_prefix or prev_prefix is None:
                            curr_znumber_str = zfill_int(prev_number + 1)
                            pseudo_id_start = curr_prefix + "-" + curr_znumber_str
                            self.qsettings.setValue('hidden/pseudo_id_start', pseudo_id_start)
                            self.qsettings.setValue('hidden/pseudo_id_start_int', prev_number + 1)
                            self.qsettings.setValue('hidden/pseudo_id_start_prefix', curr_prefix)

    def create_pseudo_ids(self):
        pseudo_ids = []
        prefix = self.qsettings.value('hidden/pseudo_id_start_prefix')
        start = self.qsettings.value('hidden/pseudo_id_start_int')
        end = start + len(self.df)

        for number in range(start, end):
            pseudo_ids.append(prefix + "-" + zfill_int(number))

        return pseudo_ids

    # Import/export functions

    def upload(self):
        self.df['lab'] = self.qsettings.value('select_single/lab')
        self.df['host'] = self.qsettings.value('select_single/host')
        self.df['seq_technology'] = self.qsettings.value('select_single/seq_technology')

        df2 = self.df.fillna('')
        errors = validate(df2)

        if errors:
            vdialog = ValidationDialog(errors)
            vdialog.exec()
            return False

        sample_seqs = {}
        files_list = []
        for _, row in self.df.iterrows():
            _seqs = []
            if row['fastq']:
                _list = row["fastq"]
                for filename in _list:
                    files_list.append(Path(row["seq_path"], filename))
                    _seqs.append(Path(row["seq_path"], filename))

            if row['fast5']:
                _list = row["fast5"]
                for filename in _list:
                    files_list.append(Path(row["seq_path"], filename))
                    _seqs.append(Path(row["seq_path"], filename))

            sample_seqs[row['internal_lab_id']] = _seqs

        self.df['lab_code'] = self.df['lab'].apply(lambda x: self.conf['tr']['lab_to_code'][x])
        self.df['region_code'] = self.df['region'].apply(lambda x: self.conf['tr']['region_to_code'][x])
        self.df['pseudo_id'] = self.create_pseudo_ids()

        meta_fields = [field for field in self.conf['model_fields'] if self.conf['model_fields'][field]['to_meta']]
        df_submit = self.df[meta_fields]

        now = datetime.now()
        tag = now.strftime("%Y-%m-%dT%H.%M.%S")
        json_file = Path(self.qsettings.value('entered_value/metadata_output_path'), tag + "_meta.json")

        with open(json_file, 'w', encoding='utf-8') as file:
            df_submit.to_json(file, orient="records", force_ascii=False)

        # upload_params = [json_file,
        #                  sample_seqs,
        #                  tag,
        #                  self.qsettings['entered_value/credentials_path'],
        #                  self.qsettings['select_single/hcp_bucket']
        #                  ]

        c_path = self.qsettings.value('entered_value/credentials_filepath')
        bucket = self.qsettings.value('select_single/hcp_bucket')

        uploader = Uploader(c_path,
                            tag,
                            bucket,
                            json_file,
                            files_list)

        uploader.exec()

        #
        # if all(upload_params):
        #     thread = QThread()
        #     worker = UploadWorker(*upload_params)
        #     worker.moveToThread(thread)
        #
        #     thread.started.connect(self.worker.run)
        #     worker.finished.connect(self.thread.quit)
        #     worker.finished.connect(self.worker.deleteLater)
        #     thread.finished.connect(self.thread.deleteLater)
        #     worker.progress.connect(self.reportProgress)
        #

    def save_metadata_file(self):
        now = datetime.now()
        dt_str = now.strftime("%Y-%m-%dT%H.%M.%S")
        dialog = QFileDialog()

        p_str = self.qsettings.value('entered_value/metadata_docs_path')

        if p_str and Path(p_str).exists():
            default_path = p_str
        else:
            default_path = str(Path.home())

        default_path = Path(default_path, dt_str + "_metadata.pkl")

        filepath, _ = dialog.getSaveFileName(self,
                                             'Save an awesome metadata file',
                                             str(default_path),
                                             "metadata files (*.pkl)",
                                             options=QFileDialog.DontUseNativeDialog)
        if filepath:
            self.df.to_pickle(filepath)

    def open_metadata_file(self):

        p_str = self.qsettings.value('entered_value/metadata_docs_path')

        if p_str and Path(p_str).exists():
            default_path = p_str
        else:
            default_path = str(Path.home())

        dialog = QFileDialog()
        filepath, _ = dialog.getOpenFileName(self,
                                             'Open an awesome metadata file',
                                              default_path,
                                              "metadata files (*.pkl)",
                                              options=QFileDialog.DontUseNativeDialog)

        if filepath:
            self.df = pd.read_pickle(filepath)
            self.update_model()

        if not self.df.empty:
                self.rem_tb_bkg()
                self.set_datastatus_empty(False)

    def get_seq_files(self):

        p_str = self.qsettings.value('entered_value/seq_base_path')

        if p_str and Path(p_str).exists():
            default_path = p_str
        else:
            default_path = str(Path.home())

        dialog = QFileDialog()
        files, _ = dialog.getOpenFileNames(self,
                                           "Select sequence data files",
                                           default_path,
                                           "Sequence files (*.fast5 *.fastq.gz *.fastq *.fq.gz *.fq",
                                           options=QFileDialog.DontUseNativeDialog)

        verified_files = self.verify_files(files)
        file_metadata = self.extract_metadata_from_filenames(verified_files)
        self.add_files_metadata_to_model(file_metadata)

    def get_csv_file_combine(self):

        p_str = self.qsettings.value('entered_value/csv_base_path')

        if p_str and Path(p_str).exists():
            default_path = p_str
        else:
            default_path = str(Path.home())

        dialog = QFileDialog()
        filepath, _ = dialog.getOpenFileName(self,
                                             'Open an awesome metadata file',
                                              default_path,
                                              "metadata csv files (*.csv)",
                                              options=QFileDialog.DontUseNativeDialog)


        if filepath:

            colnames = list(self.df.columns)

            with open(filepath, encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    r = get_pd_row_index(self.df, row['internal_lab_id'], 'internal_lab_id')
                    for key, value in row.items():
                        if key in colnames:
                            self.df.at[r, key] = value

            self.update_model()

    def str_to_pd(self):
        clipboard = QGuiApplication.clipboard()
        mime_data = clipboard.mimeData()

        data_str = mime_data.text()

        str_obj = StringIO(data_str)
        df = pd.read_csv(str_obj, sep="\t")

        # for i, r in enumerate(rows):
        #     columns = r.split("\t")
        #     for j, value in enumerate(columns):
        #         colname = self.df.columns[i_col + j]
        #         valid_value = self.accept_paste(value, colname)
        #         if valid_value:
        #             model.setData(model.index(i_row + i, i_col + j), valid_value)
        #

    def import_fx_file(self):

        store_key = "/".join(['select_single', 'import_paste_fx'])
        fx_name = self.qsettings.value(store_key)

        print(fx_name)


        filetypes = None
        if fx_name == "analytix":
            filetypes = "metadata fx files (*.xls)"

        if not filetypes:
            return False

        p_str = self.qsettings.value('entered_value/csv_base_path')

        if p_str and Path(p_str).exists():
            default_path = p_str
        else:
            default_path = str(Path.home())

        dialog = QFileDialog()
        filepath, _ = dialog.getOpenFileName(self,
                                             'Open an awesome fx metadata file',
                                              default_path,
                                              filetypes,
                                              options=QFileDialog.DontUseNativeDialog)


        if filepath:
            data = pd.read_csv(filepath, delimiter=";")
            print(data)


            # colnames = list(self.df.columns)
            #
            # with open(filepath, encoding='utf-8-sig') as csvfile:
            #     reader = csv.DictReader(csvfile)
            #     for row in reader:
            #         r = get_pd_row_index(self.df, row['internal_lab_id'], 'internal_lab_id')
            #         for key, value in row.items():
            #             if key in colnames:
            #                 self.df.at[r, key] = value
            #
            # self.update_model()

    # Reimplemented functions

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

            verified_files = self.verify_files(files)
            file_metadata = self.extract_metadata_from_filenames(verified_files)
            self.add_files_metadata_to_model(file_metadata)

        else:
            event.ignore()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            visible_tableview = self.get_current_tableview()
            if visible_tableview:
                indexes = visible_tableview.selectedIndexes()
                visible_tableview.edit(indexes[0])

        elif event.key() == (Qt.Key_Control and Qt.Key_D):
            self.filldown()

        elif event.key() == Qt.Key_Delete:
            visible_tableview = self.get_current_tableview()
            if visible_tableview:
                indexes = visible_tableview.selectedIndexes()
                model = visible_tableview.model()
                for i in indexes:
                    if model.flags(i) & Qt.ItemIsEditable:
                        model.setData(i, "", Qt.EditRole)

        elif event.matches(QKeySequence.Copy):
            visible_tableview = self.get_current_tableview()
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
                        c = [model.data(i, Qt.DisplayRole)]
                        old_row = i.row()

                r.append("\t".join(c))
                copy_data = "\n".join(r)

                self.clipboard.setText(copy_data)

        elif event.matches(QKeySequence.Paste):

            clipboard = QGuiApplication.clipboard()
            mime_data = clipboard.mimeData()

            curr_view = self.get_current_tableview()

            model = curr_view.model()
            index = curr_view.selectionModel().currentIndex()
            i_row = index.row()
            i_col = index.column()

            rows = mime_data.text().split("\n")
            for i, r in enumerate(rows):
                columns = r.split("\t")
                for j, value in enumerate(columns):
                    colname = self.df.columns[i_col + j]
                    valid_value = self.accept_paste(value, colname)
                    if valid_value:
                        model.setData(model.index(i_row + i, i_col + j), valid_value)

        else:
            super().keyPressEvent(event)



def main():
    try:
        import pyi_splash
    except:
        pass

    app = QApplication(sys.argv)
    window = MainWindow()

    style_add = """
    QTableView { 
        gridline-color: lightgrey;
    }
    .bold { 
        font-weight: bold;
        font-size: 16px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: grey;
    }
    .padding-left { 
        padding-left: 10px;
    }

    """

    style = qdarktheme.load_stylesheet("light") + style_add
    app.setStyleSheet(style)

    try:
        pyi_splash.close()
    except:
        pass

    window.show()


    sys.exit(app.exec())


if __name__ == "__main__":
    main()