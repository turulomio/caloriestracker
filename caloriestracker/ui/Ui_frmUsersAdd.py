# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/frmUsersAdd.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmUsersAdd(object):
    def setupUi(self, frmUsersAdd):
        frmUsersAdd.setObjectName("frmUsersAdd")
        frmUsersAdd.setWindowModality(QtCore.Qt.WindowModal)
        frmUsersAdd.resize(417, 161)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/caloriestracker/list-add-user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmUsersAdd.setWindowIcon(icon)
        frmUsersAdd.setModal(True)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(frmUsersAdd)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl = QtWidgets.QLabel(frmUsersAdd)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl.setFont(font)
        self.lbl.setStyleSheet("color: rgb(0, 128, 0);")
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.verticalLayout_3.addWidget(self.lbl)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(frmUsersAdd)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.txtName = QtWidgets.QLineEdit(frmUsersAdd)
        self.txtName.setObjectName("txtName")
        self.horizontalLayout_5.addWidget(self.txtName)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.bb = QtWidgets.QDialogButtonBox(frmUsersAdd)
        self.bb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb.setObjectName("bb")
        self.verticalLayout_3.addWidget(self.bb)
        self.horizontalLayout_16.addLayout(self.verticalLayout_3)

        self.retranslateUi(frmUsersAdd)
        QtCore.QMetaObject.connectSlotsByName(frmUsersAdd)

    def retranslateUi(self, frmUsersAdd):
        _translate = QtCore.QCoreApplication.translate
        frmUsersAdd.setWindowTitle(_translate("frmUsersAdd", "Managing companies"))
        self.label_6.setText(_translate("frmUsersAdd", "Name of the company"))
import caloriestracker.images.caloriestracker_rc
