# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/wdgYearMonth.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_wdgYearMonth(object):
    def setupUi(self, wdgYearMonth):
        wdgYearMonth.setObjectName("wdgYearMonth")
        wdgYearMonth.resize(673, 38)
        self.verticalLayout = QtWidgets.QVBoxLayout(wdgYearMonth)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(wdgYearMonth)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.cmdPrevious = QtWidgets.QToolButton(wdgYearMonth)
        self.cmdPrevious.setObjectName("cmdPrevious")
        self.horizontalLayout.addWidget(self.cmdPrevious)
        self.cmbMonth = QtWidgets.QComboBox(wdgYearMonth)
        self.cmbMonth.setObjectName("cmbMonth")
        self.cmbMonth.addItem("")
        self.cmbMonth.addItem("")
        self.cmbMonth.addItem("")
        self.cmbMonth.addItem("")
        self.cmbMonth.addItem("")
        self.cmbMonth.addItem("")
        self.cmbMonth.addItem("")
        self.cmbMonth.addItem("")
        self.cmbMonth.addItem("")
        self.cmbMonth.addItem("")
        self.cmbMonth.addItem("")
        self.cmbMonth.addItem("")
        self.horizontalLayout.addWidget(self.cmbMonth)
        self.cmbYear = QtWidgets.QComboBox(wdgYearMonth)
        self.cmbYear.setObjectName("cmbYear")
        self.horizontalLayout.addWidget(self.cmbYear)
        self.cmdNext = QtWidgets.QToolButton(wdgYearMonth)
        self.cmdNext.setObjectName("cmdNext")
        self.horizontalLayout.addWidget(self.cmdNext)
        self.line = QtWidgets.QFrame(wdgYearMonth)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.cmdCurrent = QtWidgets.QPushButton(wdgYearMonth)
        self.cmdCurrent.setObjectName("cmdCurrent")
        self.horizontalLayout.addWidget(self.cmdCurrent)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(wdgYearMonth)
        QtCore.QMetaObject.connectSlotsByName(wdgYearMonth)

    def retranslateUi(self, wdgYearMonth):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("wdgYearMonth", "Select a month and a year"))
        self.cmdPrevious.setToolTip(_translate("wdgYearMonth", "Previous month"))
        self.cmdPrevious.setText(_translate("wdgYearMonth", "<"))
        self.cmbMonth.setToolTip(_translate("wdgYearMonth", "Select a month"))
        self.cmbMonth.setItemText(0, _translate("wdgYearMonth", "January"))
        self.cmbMonth.setItemText(1, _translate("wdgYearMonth", "February"))
        self.cmbMonth.setItemText(2, _translate("wdgYearMonth", "March"))
        self.cmbMonth.setItemText(3, _translate("wdgYearMonth", "April"))
        self.cmbMonth.setItemText(4, _translate("wdgYearMonth", "May"))
        self.cmbMonth.setItemText(5, _translate("wdgYearMonth", "June"))
        self.cmbMonth.setItemText(6, _translate("wdgYearMonth", "July"))
        self.cmbMonth.setItemText(7, _translate("wdgYearMonth", "August"))
        self.cmbMonth.setItemText(8, _translate("wdgYearMonth", "September"))
        self.cmbMonth.setItemText(9, _translate("wdgYearMonth", "October"))
        self.cmbMonth.setItemText(10, _translate("wdgYearMonth", "November"))
        self.cmbMonth.setItemText(11, _translate("wdgYearMonth", "December"))
        self.cmbYear.setToolTip(_translate("wdgYearMonth", "Select a year"))
        self.cmdNext.setToolTip(_translate("wdgYearMonth", "Next month"))
        self.cmdNext.setText(_translate("wdgYearMonth", ">"))
        self.cmdCurrent.setToolTip(_translate("wdgYearMonth", "Current month"))
        self.cmdCurrent.setText(_translate("wdgYearMonth", "Current month"))
