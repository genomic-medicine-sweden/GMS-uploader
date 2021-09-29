# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mw.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.action_open_meta = QAction(MainWindow)
        self.action_open_meta.setObjectName(u"action_open_meta")
        self.action_save_meta = QAction(MainWindow)
        self.action_save_meta.setObjectName(u"action_save_meta")
        self.action_show_prefs = QAction(MainWindow)
        self.action_show_prefs.setObjectName(u"action_show_prefs")
        self.action_show_meta = QAction(MainWindow)
        self.action_show_meta.setObjectName(u"action_show_meta")
        self.action_upload_meta_seqs = QAction(MainWindow)
        self.action_upload_meta_seqs.setObjectName(u"action_upload_meta_seqs")
        self.action_select_seq_files = QAction(MainWindow)
        self.action_select_seq_files.setObjectName(u"action_select_seq_files")
        self.action_import_csv = QAction(MainWindow)
        self.action_import_csv.setObjectName(u"action_import_csv")
        self.action_import_paste_fx = QAction(MainWindow)
        self.action_import_paste_fx.setObjectName(u"action_import_paste_fx")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidgetPage1 = QWidget()
        self.stackedWidgetPage1.setObjectName(u"stackedWidgetPage1")
        self.verticalLayout_2 = QVBoxLayout(self.stackedWidgetPage1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_2 = QLabel(self.stackedWidgetPage1)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.lineEdit_submitter = QLineEdit(self.stackedWidgetPage1)
        self.lineEdit_submitter.setObjectName(u"lineEdit_submitter")
        self.lineEdit_submitter.setReadOnly(True)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.lineEdit_submitter)

        self.label_5 = QLabel(self.stackedWidgetPage1)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_5)

        self.lineEdit_lab = QLineEdit(self.stackedWidgetPage1)
        self.lineEdit_lab.setObjectName(u"lineEdit_lab")
        self.lineEdit_lab.setReadOnly(True)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.lineEdit_lab)

        self.label_7 = QLabel(self.stackedWidgetPage1)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.label_7)

        self.lineEdit_host = QLineEdit(self.stackedWidgetPage1)
        self.lineEdit_host.setObjectName(u"lineEdit_host")
        self.lineEdit_host.setReadOnly(True)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.lineEdit_host)

        self.label_8 = QLabel(self.stackedWidgetPage1)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_3.setWidget(3, QFormLayout.LabelRole, self.label_8)

        self.lineEdit_pseudo_id = QLineEdit(self.stackedWidgetPage1)
        self.lineEdit_pseudo_id.setObjectName(u"lineEdit_pseudo_id")
        self.lineEdit_pseudo_id.setReadOnly(True)

        self.formLayout_3.setWidget(3, QFormLayout.FieldRole, self.lineEdit_pseudo_id)


        self.horizontalLayout.addLayout(self.formLayout_3)

        self.line = QFrame(self.stackedWidgetPage1)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label = QLabel(self.stackedWidgetPage1)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEdit_credentials_path = QLineEdit(self.stackedWidgetPage1)
        self.lineEdit_credentials_path.setObjectName(u"lineEdit_credentials_path")
        self.lineEdit_credentials_path.setReadOnly(True)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.lineEdit_credentials_path)

        self.label_10 = QLabel(self.stackedWidgetPage1)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_10)

        self.lineEdit_bucket = QLineEdit(self.stackedWidgetPage1)
        self.lineEdit_bucket.setObjectName(u"lineEdit_bucket")
        self.lineEdit_bucket.setReadOnly(True)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.lineEdit_bucket)

        self.label_6 = QLabel(self.stackedWidgetPage1)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_6)

        self.lineEdit_seq_technology = QLineEdit(self.stackedWidgetPage1)
        self.lineEdit_seq_technology.setObjectName(u"lineEdit_seq_technology")
        self.lineEdit_seq_technology.setReadOnly(True)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.lineEdit_seq_technology)

        self.label_9 = QLabel(self.stackedWidgetPage1)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_9)

        self.lineEdit_lib_method = QLineEdit(self.stackedWidgetPage1)
        self.lineEdit_lib_method.setObjectName(u"lineEdit_lib_method")
        self.lineEdit_lib_method.setReadOnly(True)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.lineEdit_lib_method)


        self.horizontalLayout.addLayout(self.formLayout_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.line_3 = QFrame(self.stackedWidgetPage1)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_3, 2, 9, 1, 1)

        self.pushButton_clear = QPushButton(self.stackedWidgetPage1)
        self.pushButton_clear.setObjectName(u"pushButton_clear")

        self.gridLayout.addWidget(self.pushButton_clear, 2, 11, 1, 1)

        self.pushButton_invert = QPushButton(self.stackedWidgetPage1)
        self.pushButton_invert.setObjectName(u"pushButton_invert")

        self.gridLayout.addWidget(self.pushButton_invert, 2, 1, 1, 1)

        self.pushButton_resetfilters = QPushButton(self.stackedWidgetPage1)
        self.pushButton_resetfilters.setObjectName(u"pushButton_resetfilters")

        self.gridLayout.addWidget(self.pushButton_resetfilters, 2, 6, 1, 1)

        self.pushButton_filtermarked = QPushButton(self.stackedWidgetPage1)
        self.pushButton_filtermarked.setObjectName(u"pushButton_filtermarked")

        self.gridLayout.addWidget(self.pushButton_filtermarked, 2, 0, 1, 1)

        self.lineEdit_filter = QLineEdit(self.stackedWidgetPage1)
        self.lineEdit_filter.setObjectName(u"lineEdit_filter")

        self.gridLayout.addWidget(self.lineEdit_filter, 2, 5, 1, 1)

        self.pushButton_filldown = QPushButton(self.stackedWidgetPage1)
        self.pushButton_filldown.setObjectName(u"pushButton_filldown")

        self.gridLayout.addWidget(self.pushButton_filldown, 2, 8, 1, 1)

        self.pushButton_drop = QPushButton(self.stackedWidgetPage1)
        self.pushButton_drop.setObjectName(u"pushButton_drop")

        self.gridLayout.addWidget(self.pushButton_drop, 2, 10, 1, 1)

        self.line_2 = QFrame(self.stackedWidgetPage1)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line_2, 2, 7, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.tabWidget_metadata = QTabWidget(self.stackedWidgetPage1)
        self.tabWidget_metadata.setObjectName(u"tabWidget_metadata")
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.verticalLayout_4 = QVBoxLayout(self.tab_1)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tableView_patient = QTableView(self.tab_1)
        self.tableView_patient.setObjectName(u"tableView_patient")

        self.verticalLayout_4.addWidget(self.tableView_patient)

        self.tabWidget_metadata.addTab(self.tab_1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_12 = QVBoxLayout(self.tab_2)
        self.verticalLayout_12.setSpacing(6)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.tableView_organism = QTableView(self.tab_2)
        self.tableView_organism.setObjectName(u"tableView_organism")

        self.verticalLayout_12.addWidget(self.tableView_organism)

        self.tabWidget_metadata.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_11 = QVBoxLayout(self.tab_3)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.tableView_lab = QTableView(self.tab_3)
        self.tableView_lab.setObjectName(u"tableView_lab")

        self.verticalLayout_11.addWidget(self.tableView_lab)

        self.tabWidget_metadata.addTab(self.tab_3, "")

        self.verticalLayout_2.addWidget(self.tabWidget_metadata)

        self.stackedWidget.addWidget(self.stackedWidgetPage1)
        self.stackedWidgetPage2 = QWidget()
        self.stackedWidgetPage2.setObjectName(u"stackedWidgetPage2")
        self.verticalLayout_3 = QVBoxLayout(self.stackedWidgetPage2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scrollArea = QScrollArea(self.stackedWidgetPage2)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_settings = QWidget()
        self.scrollAreaWidgetContents_settings.setObjectName(u"scrollAreaWidgetContents_settings")
        self.scrollAreaWidgetContents_settings.setGeometry(QRect(0, 0, 671, 582))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents_settings)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.formLayout_settings = QFormLayout()
        self.formLayout_settings.setObjectName(u"formLayout_settings")
        self.formLayout_settings.setHorizontalSpacing(6)
        self.formLayout_settings.setVerticalSpacing(6)

        self.verticalLayout_5.addLayout(self.formLayout_settings)

        self.verticalLayout_tab_settings = QVBoxLayout()
        self.verticalLayout_tab_settings.setObjectName(u"verticalLayout_tab_settings")

        self.verticalLayout_5.addLayout(self.verticalLayout_tab_settings)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_settings)

        self.verticalLayout_3.addWidget(self.scrollArea)

        self.stackedWidget.addWidget(self.stackedWidgetPage2)

        self.verticalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.LeftToolBarArea, self.toolBar)

        self.toolBar.addAction(self.action_open_meta)
        self.toolBar.addAction(self.action_save_meta)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_select_seq_files)
        self.toolBar.addAction(self.action_import_csv)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_import_paste_fx)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_show_meta)
        self.toolBar.addAction(self.action_show_prefs)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_upload_meta_seqs)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget_metadata.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_open_meta.setText(QCoreApplication.translate("MainWindow", u"open_meta", None))
#if QT_CONFIG(tooltip)
        self.action_open_meta.setToolTip(QCoreApplication.translate("MainWindow", u"open metadata file ", None))
#endif // QT_CONFIG(tooltip)
        self.action_save_meta.setText(QCoreApplication.translate("MainWindow", u"save_meta", None))
#if QT_CONFIG(tooltip)
        self.action_save_meta.setToolTip(QCoreApplication.translate("MainWindow", u"save metadata file", None))
#endif // QT_CONFIG(tooltip)
        self.action_show_prefs.setText(QCoreApplication.translate("MainWindow", u"show_preferences", None))
#if QT_CONFIG(tooltip)
        self.action_show_prefs.setToolTip(QCoreApplication.translate("MainWindow", u"show preferences", None))
#endif // QT_CONFIG(tooltip)
        self.action_show_meta.setText(QCoreApplication.translate("MainWindow", u"show_metadata", None))
#if QT_CONFIG(tooltip)
        self.action_show_meta.setToolTip(QCoreApplication.translate("MainWindow", u"show metadata", None))
#endif // QT_CONFIG(tooltip)
        self.action_upload_meta_seqs.setText(QCoreApplication.translate("MainWindow", u"upload_meta", None))
#if QT_CONFIG(tooltip)
        self.action_upload_meta_seqs.setToolTip(QCoreApplication.translate("MainWindow", u"upload", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.action_upload_meta_seqs.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+U", None))
#endif // QT_CONFIG(shortcut)
        self.action_select_seq_files.setText(QCoreApplication.translate("MainWindow", u"select_seq_files", None))
#if QT_CONFIG(tooltip)
        self.action_select_seq_files.setToolTip(QCoreApplication.translate("MainWindow", u"select seq files", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.action_select_seq_files.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.action_import_csv.setText(QCoreApplication.translate("MainWindow", u"import_csv", None))
#if QT_CONFIG(tooltip)
        self.action_import_csv.setToolTip(QCoreApplication.translate("MainWindow", u"import metadata from csv", None))
#endif // QT_CONFIG(tooltip)
        self.action_import_paste_fx.setText(QCoreApplication.translate("MainWindow", u"import_paste_fx", None))
#if QT_CONFIG(tooltip)
        self.action_import_paste_fx.setToolTip(QCoreApplication.translate("MainWindow", u"import data via parsing clipboard data", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"submitter:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"lab:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"host:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"pseudo_id_start:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"credentials_path:", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"bucket:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"seq_technology:", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"library_method:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_clear.setToolTip(QCoreApplication.translate("MainWindow", u"clear table", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
#if QT_CONFIG(tooltip)
        self.pushButton_invert.setToolTip(QCoreApplication.translate("MainWindow", u"invert marks", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_invert.setText(QCoreApplication.translate("MainWindow", u"Invert", None))
#if QT_CONFIG(tooltip)
        self.pushButton_resetfilters.setToolTip(QCoreApplication.translate("MainWindow", u"reset sort, remove filters and marks", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_resetfilters.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
#if QT_CONFIG(tooltip)
        self.pushButton_filtermarked.setToolTip(QCoreApplication.translate("MainWindow", u"filter to view marked rows only", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_filtermarked.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
#if QT_CONFIG(tooltip)
        self.lineEdit_filter.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>freetext filter</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.pushButton_filldown.setToolTip(QCoreApplication.translate("MainWindow", u"filldown from selected cell\n"
"shortcut: ctrl+f", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_filldown.setText(QCoreApplication.translate("MainWindow", u"Filldown", None))
#if QT_CONFIG(tooltip)
        self.pushButton_drop.setToolTip(QCoreApplication.translate("MainWindow", u"delete marked rows", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_drop.setText(QCoreApplication.translate("MainWindow", u"Delete ", None))
        self.tabWidget_metadata.setTabText(self.tabWidget_metadata.indexOf(self.tab_1), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidget_metadata.setTabText(self.tabWidget_metadata.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.tabWidget_metadata.setTabText(self.tabWidget_metadata.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Tab 3", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

