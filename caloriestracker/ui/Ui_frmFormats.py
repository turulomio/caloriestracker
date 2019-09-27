# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/frmFormats.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmFormats(object):
    def setupUi(self, frmFormats):
        frmFormats.setObjectName("frmFormats")
        frmFormats.setWindowModality(QtCore.Qt.WindowModal)
        frmFormats.resize(658, 362)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/caloriestracker/books.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmFormats.setWindowIcon(icon)
        frmFormats.setModal(True)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(frmFormats)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl = QtWidgets.QLabel(frmFormats)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl.setFont(font)
        self.lbl.setStyleSheet("color: rgb(0, 128, 0);")
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.verticalLayout_3.addWidget(self.lbl)
        self.tblFormats = myQTableWidget(frmFormats)
        self.tblFormats.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tblFormats.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblFormats.setAlternatingRowColors(True)
        self.tblFormats.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tblFormats.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tblFormats.setObjectName("tblFormats")
        self.tblFormats.setColumnCount(0)
        self.tblFormats.setRowCount(0)
        self.verticalLayout_3.addWidget(self.tblFormats)
        self.bb = QtWidgets.QDialogButtonBox(frmFormats)
        self.bb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb.setObjectName("bb")
        self.verticalLayout_3.addWidget(self.bb)
        self.horizontalLayout_16.addLayout(self.verticalLayout_3)
        self.actionFormatNew = QtWidgets.QAction(frmFormats)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/caloriestracker/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFormatNew.setIcon(icon1)
        self.actionFormatNew.setObjectName("actionFormatNew")
        self.actionFormatDelete = QtWidgets.QAction(frmFormats)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/caloriestracker/list-remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFormatDelete.setIcon(icon2)
        self.actionFormatDelete.setObjectName("actionFormatDelete")
        self.actionFormatEdit = QtWidgets.QAction(frmFormats)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/caloriestracker/document-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFormatEdit.setIcon(icon3)
        self.actionFormatEdit.setObjectName("actionFormatEdit")

        self.retranslateUi(frmFormats)
        QtCore.QMetaObject.connectSlotsByName(frmFormats)

    def retranslateUi(self, frmFormats):
        _translate = QtCore.QCoreApplication.translate
        frmFormats.setWindowTitle(_translate("frmFormats", "Managing product formats"))
        self.actionFormatNew.setText(_translate("frmFormats", "New product format"))
        self.actionFormatNew.setToolTip(_translate("frmFormats", "New product format"))
        self.actionFormatDelete.setText(_translate("frmFormats", "Delete product format"))
        self.actionFormatDelete.setToolTip(_translate("frmFormats", "Delete product format"))
        self.actionFormatEdit.setText(_translate("frmFormats", "Edit product format"))
        self.actionFormatEdit.setToolTip(_translate("frmFormats", "Edit product format"))
from caloriestracker.ui.myqtablewidget import myQTableWidget
import caloriestracker.images.caloriestracker_rc
