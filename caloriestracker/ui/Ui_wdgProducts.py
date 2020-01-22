# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/wdgProducts.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_wdgProducts(object):
    def setupUi(self, wdgProducts):
        wdgProducts.setObjectName("wdgProducts")
        wdgProducts.resize(892, 654)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(wdgProducts)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl = QtWidgets.QLabel(wdgProducts)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl.setFont(font)
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.verticalLayout_3.addWidget(self.lbl)
        self.groupBox = QtWidgets.QGroupBox(wdgProducts)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.txt = QtWidgets.QLineEdit(self.groupBox)
        self.txt.setClearButtonEnabled(True)
        self.txt.setObjectName("txt")
        self.horizontalLayout.addWidget(self.txt)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(self.groupBox)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.cmd = QtWidgets.QToolButton(self.groupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/caloriestracker/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cmd.setIcon(icon)
        self.cmd.setObjectName("cmd")
        self.horizontalLayout_3.addWidget(self.cmd)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setEnabled(False)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.tblProducts = myQTableWidget(wdgProducts)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblProducts.sizePolicy().hasHeightForWidth())
        self.tblProducts.setSizePolicy(sizePolicy)
        self.tblProducts.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tblProducts.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblProducts.setAlternatingRowColors(True)
        self.tblProducts.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tblProducts.setObjectName("tblProducts")
        self.tblProducts.setColumnCount(0)
        self.tblProducts.setRowCount(0)
        self.tblProducts.horizontalHeader().setStretchLastSection(False)
        self.tblProducts.verticalHeader().setVisible(False)
        self.verticalLayout_3.addWidget(self.tblProducts)
        self.lblFound = QtWidgets.QLabel(wdgProducts)
        self.lblFound.setObjectName("lblFound")
        self.verticalLayout_3.addWidget(self.lblFound)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.actionProductNew = QtWidgets.QAction(wdgProducts)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/caloriestracker/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProductNew.setIcon(icon1)
        self.actionProductNew.setObjectName("actionProductNew")
        self.actionProductDelete = QtWidgets.QAction(wdgProducts)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/caloriestracker/list-remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProductDelete.setIcon(icon2)
        self.actionProductDelete.setObjectName("actionProductDelete")
        self.actionProductEdit = QtWidgets.QAction(wdgProducts)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/caloriestracker/document-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProductEdit.setIcon(icon3)
        self.actionProductEdit.setObjectName("actionProductEdit")
        self.actionFormats = QtWidgets.QAction(wdgProducts)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/caloriestracker/cube.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFormats.setIcon(icon4)
        self.actionFormats.setObjectName("actionFormats")

        self.retranslateUi(wdgProducts)
        QtCore.QMetaObject.connectSlotsByName(wdgProducts)
        wdgProducts.setTabOrder(self.txt, self.cmd)
        wdgProducts.setTabOrder(self.cmd, self.tblProducts)

    def retranslateUi(self, wdgProducts):
        _translate = QtCore.QCoreApplication.translate
        self.lbl.setText(_translate("wdgProducts", "Products list"))
        self.groupBox.setTitle(_translate("wdgProducts", "Select your search"))
        self.label.setText(_translate("wdgProducts", "Enter a string to search"))
        self.lblFound.setText(_translate("wdgProducts", "Registers found"))
        self.actionProductNew.setText(_translate("wdgProducts", "New product"))
        self.actionProductNew.setToolTip(_translate("wdgProducts", "New user product"))
        self.actionProductDelete.setText(_translate("wdgProducts", "Delete product"))
        self.actionProductDelete.setToolTip(_translate("wdgProducts", "Delete user product"))
        self.actionProductEdit.setText(_translate("wdgProducts", "Edit product"))
        self.actionProductEdit.setToolTip(_translate("wdgProducts", "Edit product"))
        self.actionFormats.setText(_translate("wdgProducts", "Show formats"))
        self.actionFormats.setToolTip(_translate("wdgProducts", "Show formats"))
from caloriestracker.ui.myqtablewidget import myQTableWidget
import caloriestracker.images.caloriestracker_rc
