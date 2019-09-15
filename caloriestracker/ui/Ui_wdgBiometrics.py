# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/wdgBiometrics.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_wdgBiometrics(object):
    def setupUi(self, wdgBiometrics):
        wdgBiometrics.setObjectName("wdgBiometrics")
        wdgBiometrics.resize(1012, 669)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(wdgBiometrics)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl = QtWidgets.QLabel(wdgBiometrics)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl.setFont(font)
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.verticalLayout_3.addWidget(self.lbl)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.wdgYM = wdgYearMonth(wdgBiometrics)
        self.wdgYM.setObjectName("wdgYM")
        self.horizontalLayout.addWidget(self.wdgYM)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tblBiometrics = myQTableWidget(wdgBiometrics)
        self.tblBiometrics.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tblBiometrics.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblBiometrics.setAlternatingRowColors(True)
        self.tblBiometrics.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tblBiometrics.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tblBiometrics.setObjectName("tblBiometrics")
        self.tblBiometrics.setColumnCount(0)
        self.tblBiometrics.setRowCount(0)
        self.tblBiometrics.horizontalHeader().setStretchLastSection(False)
        self.tblBiometrics.verticalHeader().setVisible(False)
        self.horizontalLayout_2.addWidget(self.tblBiometrics)
        self.layChart = QtWidgets.QVBoxLayout()
        self.layChart.setObjectName("layChart")
        self.horizontalLayout_2.addLayout(self.layChart)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.lblFound = QtWidgets.QLabel(wdgBiometrics)
        self.lblFound.setObjectName("lblFound")
        self.verticalLayout_3.addWidget(self.lblFound)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.actionBiometricsNew = QtWidgets.QAction(wdgBiometrics)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/caloriestracker/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBiometricsNew.setIcon(icon)
        self.actionBiometricsNew.setObjectName("actionBiometricsNew")
        self.actionBiometricsDelete = QtWidgets.QAction(wdgBiometrics)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/caloriestracker/list-remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBiometricsDelete.setIcon(icon1)
        self.actionBiometricsDelete.setObjectName("actionBiometricsDelete")
        self.actionBiometricsEdit = QtWidgets.QAction(wdgBiometrics)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/caloriestracker/document-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBiometricsEdit.setIcon(icon2)
        self.actionBiometricsEdit.setObjectName("actionBiometricsEdit")

        self.retranslateUi(wdgBiometrics)
        QtCore.QMetaObject.connectSlotsByName(wdgBiometrics)

    def retranslateUi(self, wdgBiometrics):
        _translate = QtCore.QCoreApplication.translate
        self.lbl.setText(_translate("wdgBiometrics", "Your biometric information"))
        self.lblFound.setText(_translate("wdgBiometrics", "Registers found"))
        self.actionBiometricsNew.setText(_translate("wdgBiometrics", "New biometric information"))
        self.actionBiometricsNew.setToolTip(_translate("wdgBiometrics", "New biometric information"))
        self.actionBiometricsDelete.setText(_translate("wdgBiometrics", "Delete biometric information"))
        self.actionBiometricsDelete.setToolTip(_translate("wdgBiometrics", "Delete biometric information"))
        self.actionBiometricsEdit.setText(_translate("wdgBiometrics", "Edit biometric information"))
        self.actionBiometricsEdit.setToolTip(_translate("wdgBiometrics", "Edit biometric information"))
from caloriestracker.ui.myqtablewidget import myQTableWidget
from caloriestracker.ui.wdgYearMonth import wdgYearMonth
import caloriestracker.images.caloriestracker_rc
