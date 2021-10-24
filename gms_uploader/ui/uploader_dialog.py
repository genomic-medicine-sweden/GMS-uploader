# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'uploader_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(681, 534)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.lineEdit_target = QLineEdit(Dialog)
        self.lineEdit_target.setObjectName(u"lineEdit_target")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_target)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.lineEdit_tag = QLineEdit(Dialog)
        self.lineEdit_tag.setObjectName(u"lineEdit_tag")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_tag)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.lineEdit_protocol = QLineEdit(Dialog)
        self.lineEdit_protocol.setObjectName(u"lineEdit_protocol")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_protocol)


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

        self.pushButton_stop = QPushButton(Dialog)
        self.pushButton_stop.setObjectName(u"pushButton_stop")

        self.horizontalLayout.addWidget(self.pushButton_stop)

        self.pushButton_delete_upload = QPushButton(Dialog)
        self.pushButton_delete_upload.setObjectName(u"pushButton_delete_upload")

        self.horizontalLayout.addWidget(self.pushButton_delete_upload)

        self.pushButton_close = QPushButton(Dialog)
        self.pushButton_close.setObjectName(u"pushButton_close")

        self.horizontalLayout.addWidget(self.pushButton_close)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"target:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"tag:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"protocol:", None))
        self.pushButton_start.setText(QCoreApplication.translate("Dialog", u"Start/resume", None))
        self.pushButton_stop.setText(QCoreApplication.translate("Dialog", u"Stop", None))
        self.pushButton_delete_upload.setText(QCoreApplication.translate("Dialog", u"Delete upload", None))
        self.pushButton_close.setText(QCoreApplication.translate("Dialog", u"Close", None))
    # retranslateUi

