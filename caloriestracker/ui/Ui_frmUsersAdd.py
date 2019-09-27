# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/frmUsersAdd.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmUsersAdd(object):
    def setupUi(self, frmUsersAdd):
        frmUsersAdd.setObjectName("frmUsersAdd")
        frmUsersAdd.setWindowModality(QtCore.Qt.WindowModal)
        frmUsersAdd.resize(471, 336)
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.txtName = QtWidgets.QLineEdit(frmUsersAdd)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtName.sizePolicy().hasHeightForWidth())
        self.txtName.setSizePolicy(sizePolicy)
        self.txtName.setObjectName("txtName")
        self.horizontalLayout_5.addWidget(self.txtName)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_7 = QtWidgets.QLabel(frmUsersAdd)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)
        self.dtBirthday = QtWidgets.QDateEdit(frmUsersAdd)
        self.dtBirthday.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.dtBirthday.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.dtBirthday.setCalendarPopup(True)
        self.dtBirthday.setObjectName("dtBirthday")
        self.horizontalLayout_6.addWidget(self.dtBirthday)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.chkMale = QtWidgets.QCheckBox(frmUsersAdd)
        self.chkMale.setChecked(True)
        self.chkMale.setObjectName("chkMale")
        self.verticalLayout_3.addWidget(self.chkMale)
        self.bb = QtWidgets.QDialogButtonBox(frmUsersAdd)
        self.bb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb.setObjectName("bb")
        self.verticalLayout_3.addWidget(self.bb)
        self.horizontalLayout_16.addLayout(self.verticalLayout_3)

        self.retranslateUi(frmUsersAdd)
        QtCore.QMetaObject.connectSlotsByName(frmUsersAdd)

    def retranslateUi(self, frmUsersAdd):
        _translate = QtCore.QCoreApplication.translate
        frmUsersAdd.setWindowTitle(_translate("frmUsersAdd", "Managing users"))
        self.label_6.setText(_translate("frmUsersAdd", "Name"))
        self.label_7.setText(_translate("frmUsersAdd", "Select your birthday"))
        self.dtBirthday.setDisplayFormat(_translate("frmUsersAdd", "yyyy-MM-dd"))
        self.chkMale.setText(_translate("frmUsersAdd", "Check if you\'re a male"))
import caloriestracker.images.caloriestracker_rc
