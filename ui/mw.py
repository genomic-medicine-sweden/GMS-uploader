# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mw.ui'
##
## Created by: Qt User Interface Compiler version 6.1.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionData = QAction(MainWindow)
        self.actionData.setObjectName(u"actionData")
        self.actionPreferences = QAction(MainWindow)
        self.actionPreferences.setObjectName(u"actionPreferences")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget_data = QWidget()
        self.tabWidget_data.setObjectName(u"tabWidget_data")
        self.verticalLayout_2 = QVBoxLayout(self.tabWidget_data)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lineEdit_data_user = QLineEdit(self.tabWidget_data)
        self.lineEdit_data_user.setObjectName(u"lineEdit_data_user")

        self.gridLayout_2.addWidget(self.lineEdit_data_user, 0, 3, 1, 1)

        self.label_5 = QLabel(self.tabWidget_data)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 0, 2, 1, 1)

        self.lineEdit_data_lab = QLineEdit(self.tabWidget_data)
        self.lineEdit_data_lab.setObjectName(u"lineEdit_data_lab")

        self.gridLayout_2.addWidget(self.lineEdit_data_lab, 0, 1, 1, 1)

        self.label_4 = QLabel(self.tabWidget_data)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(34, 0))

        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_delrow = QPushButton(self.tabWidget_data)
        self.pushButton_delrow.setObjectName(u"pushButton_delrow")

        self.gridLayout.addWidget(self.pushButton_delrow, 2, 4, 1, 1)

        self.pushButton_resetsort = QPushButton(self.tabWidget_data)
        self.pushButton_resetsort.setObjectName(u"pushButton_resetsort")

        self.gridLayout.addWidget(self.pushButton_resetsort, 2, 6, 1, 1)

        self.lineEdit_filter = QLineEdit(self.tabWidget_data)
        self.lineEdit_filter.setObjectName(u"lineEdit_filter")

        self.gridLayout.addWidget(self.lineEdit_filter, 2, 2, 1, 1)

        self.label_6 = QLabel(self.tabWidget_data)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(34, 0))

        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)

        self.pushButton_filldown = QPushButton(self.tabWidget_data)
        self.pushButton_filldown.setObjectName(u"pushButton_filldown")

        self.gridLayout.addWidget(self.pushButton_filldown, 2, 5, 1, 1)

        self.pushButton_fastp = QPushButton(self.tabWidget_data)
        self.pushButton_fastp.setObjectName(u"pushButton_fastp")

        self.gridLayout.addWidget(self.pushButton_fastp, 2, 3, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.tableView = QTableView(self.tabWidget_data)
        self.tableView.setObjectName(u"tableView")

        self.verticalLayout_2.addWidget(self.tableView)

        self.tabWidget.addTab(self.tabWidget_data, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_4 = QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton = QPushButton(self.tab)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout_4.addWidget(self.pushButton)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.plainTextEdit = QPlainTextEdit(self.tab)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.plainTextEdit)

        self.label_8 = QLabel(self.tab)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_8)

        self.plainTextEdit_2 = QPlainTextEdit(self.tab)
        self.plainTextEdit_2.setObjectName(u"plainTextEdit_2")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.plainTextEdit_2)

        self.label_9 = QLabel(self.tab)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_9)


        self.verticalLayout_4.addLayout(self.formLayout)

        self.tabWidget.addTab(self.tab, "")
        self.tabWidget_settings = QWidget()
        self.tabWidget_settings.setObjectName(u"tabWidget_settings")
        self.verticalLayout_3 = QVBoxLayout(self.tabWidget_settings)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label = QLabel(self.tabWidget_settings)
        self.label.setObjectName(u"label")

        self.gridLayout_3.addWidget(self.label, 0, 1, 1, 1)

        self.label_2 = QLabel(self.tabWidget_settings)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 0, 3, 1, 1)

        self.lineEdit_user = QLineEdit(self.tabWidget_settings)
        self.lineEdit_user.setObjectName(u"lineEdit_user")

        self.gridLayout_3.addWidget(self.lineEdit_user, 0, 4, 1, 1)

        self.comboBox_lab = QComboBox(self.tabWidget_settings)
        self.comboBox_lab.setObjectName(u"comboBox_lab")

        self.gridLayout_3.addWidget(self.comboBox_lab, 0, 2, 1, 1)

        self.label_3 = QLabel(self.tabWidget_settings)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 1, 1, 1, 1)

        self.lineEdit_server = QLineEdit(self.tabWidget_settings)
        self.lineEdit_server.setObjectName(u"lineEdit_server")

        self.gridLayout_3.addWidget(self.lineEdit_server, 1, 2, 1, 1)

        self.label_7 = QLabel(self.tabWidget_settings)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_3.addWidget(self.label_7, 1, 3, 1, 1)

        self.lineEdit_path = QLineEdit(self.tabWidget_settings)
        self.lineEdit_path.setObjectName(u"lineEdit_path")

        self.gridLayout_3.addWidget(self.lineEdit_path, 1, 4, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_3)

        self.tabWidget_2 = QTabWidget(self.tabWidget_settings)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.regions = QWidget()
        self.regions.setObjectName(u"regions")
        self.verticalLayout_6 = QVBoxLayout(self.regions)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.listView_region = QListView(self.regions)
        self.listView_region.setObjectName(u"listView_region")

        self.verticalLayout_6.addWidget(self.listView_region)

        self.tabWidget_2.addTab(self.regions, "")
        self.criterion = QWidget()
        self.criterion.setObjectName(u"criterion")
        self.verticalLayout_10 = QVBoxLayout(self.criterion)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.listView_criterion = QListView(self.criterion)
        self.listView_criterion.setObjectName(u"listView_criterion")

        self.verticalLayout_10.addWidget(self.listView_criterion)

        self.tabWidget_2.addTab(self.criterion, "")
        self.instrument = QWidget()
        self.instrument.setObjectName(u"instrument")
        self.verticalLayout_8 = QVBoxLayout(self.instrument)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.listView_instrument = QListView(self.instrument)
        self.listView_instrument.setObjectName(u"listView_instrument")

        self.verticalLayout_8.addWidget(self.listView_instrument)

        self.tabWidget_2.addTab(self.instrument, "")
        self.platform = QWidget()
        self.platform.setObjectName(u"platform")
        self.verticalLayout_9 = QVBoxLayout(self.platform)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.listView_platform = QListView(self.platform)
        self.listView_platform.setObjectName(u"listView_platform")

        self.verticalLayout_9.addWidget(self.listView_platform)

        self.tabWidget_2.addTab(self.platform, "")
        self.library_method = QWidget()
        self.library_method.setObjectName(u"library_method")
        self.verticalLayout_5 = QVBoxLayout(self.library_method)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.listView_library_method = QListView(self.library_method)
        self.listView_library_method.setObjectName(u"listView_library_method")

        self.verticalLayout_5.addWidget(self.listView_library_method)

        self.tabWidget_2.addTab(self.library_method, "")
        self.column = QWidget()
        self.column.setObjectName(u"column")
        self.verticalLayout_7 = QVBoxLayout(self.column)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.listView_column = QListView(self.column)
        self.listView_column.setObjectName(u"listView_column")

        self.verticalLayout_7.addWidget(self.listView_column)

        self.tabWidget_2.addTab(self.column, "")

        self.verticalLayout_3.addWidget(self.tabWidget_2)

        self.tabWidget.addTab(self.tabWidget_settings, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)


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
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"USER", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"LAB", None))
        self.pushButton_delrow.setText(QCoreApplication.translate("MainWindow", u"drop selected rows", None))
        self.pushButton_resetsort.setText(QCoreApplication.translate("MainWindow", u"reset", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"FILTER", None))
        self.pushButton_filldown.setText(QCoreApplication.translate("MainWindow", u"fill down", None))
        self.pushButton_fastp.setText(QCoreApplication.translate("MainWindow", u"run fastp", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidget_data), QCoreApplication.translate("MainWindow", u"Data", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"QC", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"console", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"metadata", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Upload", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"LAB", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"USER", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"SERVER", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"PATH", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.regions), QCoreApplication.translate("MainWindow", u"regions", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.criterion), QCoreApplication.translate("MainWindow", u"criteria", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.instrument), QCoreApplication.translate("MainWindow", u"instruments", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.platform), QCoreApplication.translate("MainWindow", u"platforms", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.library_method), QCoreApplication.translate("MainWindow", u"library_methods", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.column), QCoreApplication.translate("MainWindow", u"columns", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidget_settings), QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

