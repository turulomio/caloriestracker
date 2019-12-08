# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/wdgMealsMost.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_wdgMealsMost(object):
    def setupUi(self, wdgMealsMost):
        wdgMealsMost.setObjectName("wdgMealsMost")
        wdgMealsMost.resize(1012, 669)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(wdgMealsMost)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl = QtWidgets.QLabel(wdgMealsMost)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl.setFont(font)
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.verticalLayout.addWidget(self.lbl)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label = QtWidgets.QLabel(wdgMealsMost)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.cmbPeriod = QtWidgets.QComboBox(wdgMealsMost)
        self.cmbPeriod.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.cmbPeriod.setObjectName("cmbPeriod")
        self.cmbPeriod.addItem("")
        self.cmbPeriod.addItem("")
        self.cmbPeriod.addItem("")
        self.cmbPeriod.addItem("")
        self.cmbPeriod.addItem("")
        self.horizontalLayout_3.addWidget(self.cmbPeriod)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tblMeals = myQTableWidget(wdgMealsMost)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblMeals.sizePolicy().hasHeightForWidth())
        self.tblMeals.setSizePolicy(sizePolicy)
        self.tblMeals.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tblMeals.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblMeals.setAlternatingRowColors(True)
        self.tblMeals.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tblMeals.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tblMeals.setObjectName("tblMeals")
        self.tblMeals.setColumnCount(0)
        self.tblMeals.setRowCount(0)
        self.tblMeals.horizontalHeader().setStretchLastSection(False)
        self.tblMeals.verticalHeader().setVisible(True)
        self.verticalLayout.addWidget(self.tblMeals)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(wdgMealsMost)
        self.cmbPeriod.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(wdgMealsMost)

    def retranslateUi(self, wdgMealsMost):
        _translate = QtCore.QCoreApplication.translate
        self.lbl.setText(_translate("wdgMealsMost", "Meals I eat the most"))
        self.label.setText(_translate("wdgMealsMost", "Select a period"))
        self.cmbPeriod.setItemText(0, _translate("wdgMealsMost", "Last week"))
        self.cmbPeriod.setItemText(1, _translate("wdgMealsMost", "Last month"))
        self.cmbPeriod.setItemText(2, _translate("wdgMealsMost", "Last year"))
        self.cmbPeriod.setItemText(3, _translate("wdgMealsMost", "Last three years"))
        self.cmbPeriod.setItemText(4, _translate("wdgMealsMost", "All registers"))
from caloriestracker.ui.myqtablewidget import myQTableWidget
import caloriestracker.images.caloriestracker_rc
