# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_demo.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1105, 662)
        self.widget_display = QtWidgets.QWidget(Form)
        self.widget_display.setGeometry(QtCore.QRect(720, 0, 380, 660))
        self.widget_display.setObjectName("widget_display")
        self.widget_edit = QtWidgets.QWidget(Form)
        self.widget_edit.setGeometry(QtCore.QRect(0, 0, 721, 661))
        self.widget_edit.setObjectName("widget_edit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


