# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/wdgYear.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_wdgYear(object):
    def setupUi(self, wdgYear):
        wdgYear.setObjectName("wdgYear")
        wdgYear.resize(448, 52)
        self.verticalLayout = QtWidgets.QVBoxLayout(wdgYear)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(wdgYear)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.cmdPrevious = QtWidgets.QToolButton(wdgYear)
        self.cmdPrevious.setObjectName("cmdPrevious")
        self.horizontalLayout.addWidget(self.cmdPrevious)
        self.cmbYear = QtWidgets.QComboBox(wdgYear)
        self.cmbYear.setObjectName("cmbYear")
        self.horizontalLayout.addWidget(self.cmbYear)
        self.cmdNext = QtWidgets.QToolButton(wdgYear)
        self.cmdNext.setObjectName("cmdNext")
        self.horizontalLayout.addWidget(self.cmdNext)
        self.line = QtWidgets.QFrame(wdgYear)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.cmdCurrent = QtWidgets.QPushButton(wdgYear)
        self.cmdCurrent.setObjectName("cmdCurrent")
        self.horizontalLayout.addWidget(self.cmdCurrent)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(wdgYear)
        QtCore.QMetaObject.connectSlotsByName(wdgYear)

    def retranslateUi(self, wdgYear):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("wdgYear", "Select a year"))
        self.cmdPrevious.setToolTip(_translate("wdgYear", "Previous year"))
        self.cmdPrevious.setText(_translate("wdgYear", "<"))
        self.cmbYear.setToolTip(_translate("wdgYear", "Select a year"))
        self.cmdNext.setToolTip(_translate("wdgYear", "Next year"))
        self.cmdNext.setText(_translate("wdgYear", ">"))
        self.cmdCurrent.setToolTip(_translate("wdgYear", "Current year"))
        self.cmdCurrent.setText(_translate("wdgYear", "Current Year"))
