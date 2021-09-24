# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'uploader_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.1.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(496, 364)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label)

        self.lineEdit_tag = QLineEdit(Dialog)
        self.lineEdit_tag.setObjectName(u"lineEdit_tag")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_tag)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.lineEdit_endpoint = QLineEdit(Dialog)
        self.lineEdit_endpoint.setObjectName(u"lineEdit_endpoint")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_endpoint)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.lineEdit_bucket = QLineEdit(Dialog)
        self.lineEdit_bucket.setObjectName(u"lineEdit_bucket")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_bucket)


        self.verticalLayout.addLayout(self.formLayout)

        self.tableWidget = QTableWidget(Dialog)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout.addWidget(self.tableWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_start = QPushButton(Dialog)
        self.pushButton_start.setObjectName(u"pushButton_start")

        self.horizontalLayout.addWidget(self.pushButton_start)

        self.pushButton_terminate = QPushButton(Dialog)
        self.pushButton_terminate.setObjectName(u"pushButton_terminate")

        self.horizontalLayout.addWidget(self.pushButton_terminate)

        self.pushButton_close = QPushButton(Dialog)
        self.pushButton_close.setObjectName(u"pushButton_close")

        self.horizontalLayout.addWidget(self.pushButton_close)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"tag:", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"endpoint", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"bucket:", None))
        self.pushButton_start.setText(QCoreApplication.translate("Dialog", u"Start upload", None))
        self.pushButton_terminate.setText(QCoreApplication.translate("Dialog", u"Terminate", None))
        self.pushButton_close.setText(QCoreApplication.translate("Dialog", u"Close", None))
    # retranslateUi

