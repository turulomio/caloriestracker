# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/wdgUsers.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_wdgUsers(object):
    def setupUi(self, wdgUsers):
        wdgUsers.setObjectName("wdgUsers")
        wdgUsers.resize(1012, 669)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(wdgUsers)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl = QtWidgets.QLabel(wdgUsers)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl.setFont(font)
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.verticalLayout_3.addWidget(self.lbl)
        self.tblUsers = myQTableWidget(wdgUsers)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblUsers.sizePolicy().hasHeightForWidth())
        self.tblUsers.setSizePolicy(sizePolicy)
        self.tblUsers.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tblUsers.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tblUsers.setAlternatingRowColors(True)
        self.tblUsers.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tblUsers.setObjectName("tblUsers")
        self.tblUsers.setColumnCount(0)
        self.tblUsers.setRowCount(0)
        self.tblUsers.horizontalHeader().setStretchLastSection(False)
        self.tblUsers.verticalHeader().setVisible(False)
        self.verticalLayout_3.addWidget(self.tblUsers)
        self.lblFound = QtWidgets.QLabel(wdgUsers)
        self.lblFound.setObjectName("lblFound")
        self.verticalLayout_3.addWidget(self.lblFound)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.actionUserNew = QtWidgets.QAction(wdgUsers)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/caloriestracker/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUserNew.setIcon(icon)
        self.actionUserNew.setObjectName("actionUserNew")
        self.actionUserDelete = QtWidgets.QAction(wdgUsers)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/caloriestracker/list-remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUserDelete.setIcon(icon1)
        self.actionUserDelete.setObjectName("actionUserDelete")
        self.actionUserEdit = QtWidgets.QAction(wdgUsers)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/caloriestracker/document-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUserEdit.setIcon(icon2)
        self.actionUserEdit.setObjectName("actionUserEdit")

        self.retranslateUi(wdgUsers)
        QtCore.QMetaObject.connectSlotsByName(wdgUsers)

    def retranslateUi(self, wdgUsers):
        _translate = QtCore.QCoreApplication.translate
        self.lbl.setText(_translate("wdgUsers", "Users list"))
        self.lblFound.setText(_translate("wdgUsers", "Registers found"))
        self.actionUserNew.setText(_translate("wdgUsers", "New user"))
        self.actionUserNew.setToolTip(_translate("wdgUsers", "New user"))
        self.actionUserDelete.setText(_translate("wdgUsers", "Delete user"))
        self.actionUserDelete.setToolTip(_translate("wdgUsers", "Delete user"))
        self.actionUserEdit.setText(_translate("wdgUsers", "Edit user"))
        self.actionUserEdit.setToolTip(_translate("wdgUsers", "Edit user"))
from caloriestracker.ui.myqtablewidget import myQTableWidget
import caloriestracker.images.caloriestracker_rc
