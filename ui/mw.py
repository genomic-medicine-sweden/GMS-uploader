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
        self.actionData = QAction(MainWindow)
        self.actionData.setObjectName(u"actionData")
        self.actionPreferences = QAction(MainWindow)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.action_open_meta = QAction(MainWindow)
        self.action_open_meta.setObjectName(u"action_open_meta")
        self.actionsave_meta = QAction(MainWindow)
        self.actionsave_meta.setObjectName(u"actionsave_meta")
        self.actionpreferences = QAction(MainWindow)
        self.actionpreferences.setObjectName(u"actionpreferences")
        self.actionmetadata = QAction(MainWindow)
        self.actionmetadata.setObjectName(u"actionmetadata")
        self.actionupload = QAction(MainWindow)
        self.actionupload.setObjectName(u"actionupload")
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
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_resetfilters = QPushButton(self.stackedWidgetPage1)
        self.pushButton_resetfilters.setObjectName(u"pushButton_resetfilters")

        self.gridLayout.addWidget(self.pushButton_resetfilters, 2, 5, 1, 1)

        self.pushButton_filldown = QPushButton(self.stackedWidgetPage1)
        self.pushButton_filldown.setObjectName(u"pushButton_filldown")

        self.gridLayout.addWidget(self.pushButton_filldown, 2, 1, 1, 1)

        self.pushButton_drop = QPushButton(self.stackedWidgetPage1)
        self.pushButton_drop.setObjectName(u"pushButton_drop")

        self.gridLayout.addWidget(self.pushButton_drop, 2, 6, 1, 1)

        self.pushButton_clear = QPushButton(self.stackedWidgetPage1)
        self.pushButton_clear.setObjectName(u"pushButton_clear")

        self.gridLayout.addWidget(self.pushButton_clear, 2, 7, 1, 1)

        self.lineEdit_filter = QLineEdit(self.stackedWidgetPage1)
        self.lineEdit_filter.setObjectName(u"lineEdit_filter")

        self.gridLayout.addWidget(self.lineEdit_filter, 2, 3, 1, 1)

        self.pushButton_filtermarked = QPushButton(self.stackedWidgetPage1)
        self.pushButton_filtermarked.setObjectName(u"pushButton_filtermarked")

        self.gridLayout.addWidget(self.pushButton_filtermarked, 2, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.tabWidget_metadata = QTabWidget(self.stackedWidgetPage1)
        self.tabWidget_metadata.setObjectName(u"tabWidget_metadata")
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.verticalLayout_4 = QVBoxLayout(self.tab_1)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.tableView_patient = QTableView(self.tab_1)
        self.tableView_patient.setObjectName(u"tableView_patient")

        self.verticalLayout_4.addWidget(self.tableView_patient)

        self.tabWidget_metadata.addTab(self.tab_1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_12 = QVBoxLayout(self.tab_2)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.tableView_organism = QTableView(self.tab_2)
        self.tableView_organism.setObjectName(u"tableView_organism")

        self.verticalLayout_12.addWidget(self.tableView_organism)

        self.tabWidget_metadata.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_11 = QVBoxLayout(self.tab_3)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
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
        self.formLayout_settings = QFormLayout()
        self.formLayout_settings.setObjectName(u"formLayout_settings")

        self.verticalLayout_3.addLayout(self.formLayout_settings)

        self.verticalLayout_settings = QVBoxLayout()
        self.verticalLayout_settings.setObjectName(u"verticalLayout_settings")

        self.verticalLayout_3.addLayout(self.verticalLayout_settings)

        self.stackedWidget.addWidget(self.stackedWidgetPage2)

        self.verticalLayout.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.action_open_meta)
        self.toolBar.addAction(self.actionsave_meta)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionmetadata)
        self.toolBar.addAction(self.actionpreferences)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionupload)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget_metadata.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionData.setText(QCoreApplication.translate("MainWindow", u"Data", None))
#if QT_CONFIG(tooltip)
        self.actionData.setToolTip(QCoreApplication.translate("MainWindow", u"Data", None))
#endif // QT_CONFIG(tooltip)
        self.actionPreferences.setText(QCoreApplication.translate("MainWindow", u"Inst\u00e4llningar", None))
#if QT_CONFIG(tooltip)
        self.actionPreferences.setToolTip(QCoreApplication.translate("MainWindow", u"Preferences", None))
#endif // QT_CONFIG(tooltip)
        self.action_open_meta.setText(QCoreApplication.translate("MainWindow", u"open_meta", None))
#if QT_CONFIG(tooltip)
        self.action_open_meta.setToolTip(QCoreApplication.translate("MainWindow", u"Open metadata file ", None))
#endif // QT_CONFIG(tooltip)
        self.actionsave_meta.setText(QCoreApplication.translate("MainWindow", u"save_meta", None))
#if QT_CONFIG(tooltip)
        self.actionsave_meta.setToolTip(QCoreApplication.translate("MainWindow", u"Save metadata file", None))
#endif // QT_CONFIG(tooltip)
        self.actionpreferences.setText(QCoreApplication.translate("MainWindow", u"preferences", None))
#if QT_CONFIG(tooltip)
        self.actionpreferences.setToolTip(QCoreApplication.translate("MainWindow", u"Preferences", None))
#endif // QT_CONFIG(tooltip)
        self.actionmetadata.setText(QCoreApplication.translate("MainWindow", u"metadata", None))
#if QT_CONFIG(tooltip)
        self.actionmetadata.setToolTip(QCoreApplication.translate("MainWindow", u"Metadata", None))
#endif // QT_CONFIG(tooltip)
        self.actionupload.setText(QCoreApplication.translate("MainWindow", u"upload", None))
#if QT_CONFIG(tooltip)
        self.actionupload.setToolTip(QCoreApplication.translate("MainWindow", u"Upload", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_resetfilters.setText(QCoreApplication.translate("MainWindow", u"Reset filters", None))
        self.pushButton_filldown.setText(QCoreApplication.translate("MainWindow", u"Filldown selected column", None))
        self.pushButton_drop.setText(QCoreApplication.translate("MainWindow", u"Drop marked rows", None))
        self.pushButton_clear.setText(QCoreApplication.translate("MainWindow", u"Clear table", None))
        self.pushButton_filtermarked.setText(QCoreApplication.translate("MainWindow", u"Filter marked rows", None))
        self.tabWidget_metadata.setTabText(self.tabWidget_metadata.indexOf(self.tab_1), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tabWidget_metadata.setTabText(self.tabWidget_metadata.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.tabWidget_metadata.setTabText(self.tabWidget_metadata.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Tab 3", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

