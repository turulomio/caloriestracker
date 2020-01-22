# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/wdgProductsDataMove.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_wdgProductsDataMove(object):
    def setupUi(self, wdgProductsDataMove):
        wdgProductsDataMove.setObjectName("wdgProductsDataMove")
        wdgProductsDataMove.setWindowModality(QtCore.Qt.WindowModal)
        wdgProductsDataMove.resize(1108, 358)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(wdgProductsDataMove)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl = QtWidgets.QLabel(wdgProductsDataMove)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl.setFont(font)
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.verticalLayout.addWidget(self.lbl)
        self.label = QtWidgets.QLabel(wdgProductsDataMove)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.table = myQTableWidget(wdgProductsDataMove)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setObjectName("table")
        self.table.setColumnCount(10)
        self.table.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(255, 192, 192))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        self.table.setItem(1, 0, item)
        self.horizontalLayout.addWidget(self.table)
        self.cmdInterchange = QtWidgets.QToolButton(wdgProductsDataMove)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/xulpymoney/transfer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmdInterchange.setIcon(icon)
        self.cmdInterchange.setObjectName("cmdInterchange")
        self.horizontalLayout.addWidget(self.cmdInterchange)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.chkInvestments = QtWidgets.QCheckBox(wdgProductsDataMove)
        self.chkInvestments.setObjectName("chkInvestments")
        self.verticalLayout.addWidget(self.chkInvestments)
        self.cmd = QtWidgets.QPushButton(wdgProductsDataMove)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/xulpymoney/merge.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmd.setIcon(icon1)
        self.cmd.setObjectName("cmd")
        self.verticalLayout.addWidget(self.cmd)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(wdgProductsDataMove)
        QtCore.QMetaObject.connectSlotsByName(wdgProductsDataMove)

    def retranslateUi(self, wdgProductsDataMove):
        _translate = QtCore.QCoreApplication.translate
        self.lbl.setText(_translate("wdgProductsDataMove", "Move data between products"))
        self.label.setText(_translate("wdgProductsDataMove", "All product data will be moved from origin product to destiny one. If there are invesments created with origin product, they will be referenced to destiny product.\n"
"If origin is a user product, you can delete afterwards, because it won\'t have any data"))
        item = self.table.verticalHeaderItem(0)
        item.setText(_translate("wdgProductsDataMove", "Origin"))
        item = self.table.verticalHeaderItem(1)
        item.setText(_translate("wdgProductsDataMove", "Destiny"))
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("wdgProductsDataMove", "Id"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("wdgProductsDataMove", "Name"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("wdgProductsDataMove", "ISIN"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("wdgProductsDataMove", "Quotes"))
        item = self.table.horizontalHeaderItem(4)
        item.setText(_translate("wdgProductsDataMove", "DPS"))
        item = self.table.horizontalHeaderItem(5)
        item.setText(_translate("wdgProductsDataMove", "Investments"))
        item = self.table.horizontalHeaderItem(6)
        item.setText(_translate("wdgProductsDataMove", "Oportunities"))
        item = self.table.horizontalHeaderItem(7)
        item.setText(_translate("wdgProductsDataMove", "Splits"))
        item = self.table.horizontalHeaderItem(8)
        item.setText(_translate("wdgProductsDataMove", "DPS estimations"))
        item = self.table.horizontalHeaderItem(9)
        item.setText(_translate("wdgProductsDataMove", "EPS Estimations"))
        __sortingEnabled = self.table.isSortingEnabled()
        self.table.setSortingEnabled(False)
        self.table.setSortingEnabled(__sortingEnabled)
        self.cmdInterchange.setText(_translate("wdgProductsDataMove", "..."))
        self.chkInvestments.setText(_translate("wdgProductsDataMove", "Change personal investments with origin product to destiny product"))
        self.cmd.setText(_translate("wdgProductsDataMove", "Move data"))
from caloriestracker.ui.myqtablewidget import myQTableWidget
import caloriestracker.images.caloriestracker_rc
