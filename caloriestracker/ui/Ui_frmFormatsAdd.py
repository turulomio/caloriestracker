# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/frmFormatsAdd.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmFormatsAdd(object):
    def setupUi(self, frmFormatsAdd):
        frmFormatsAdd.setObjectName("frmFormatsAdd")
        frmFormatsAdd.setWindowModality(QtCore.Qt.WindowModal)
        frmFormatsAdd.resize(731, 181)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/caloriestracker/books.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmFormatsAdd.setWindowIcon(icon)
        frmFormatsAdd.setModal(True)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(frmFormatsAdd)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl = QtWidgets.QLabel(frmFormatsAdd)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl.setFont(font)
        self.lbl.setStyleSheet("color: rgb(0, 128, 0);")
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.verticalLayout_3.addWidget(self.lbl)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_4 = QtWidgets.QLabel(frmFormatsAdd)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.txtName = QtWidgets.QLineEdit(frmFormatsAdd)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtName.sizePolicy().hasHeightForWidth())
        self.txtName.setSizePolicy(sizePolicy)
        self.txtName.setObjectName("txtName")
        self.horizontalLayout_2.addWidget(self.txtName)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(frmFormatsAdd)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.spnAmount = myQDoubleSpinBox(frmFormatsAdd)
        self.spnAmount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spnAmount.setProperty("showGroupSeparator", True)
        self.spnAmount.setMinimum(1.0)
        self.spnAmount.setMaximum(1000000.0)
        self.spnAmount.setProperty("value", 100.0)
        self.spnAmount.setObjectName("spnAmount")
        self.horizontalLayout.addWidget(self.spnAmount)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.bb = QtWidgets.QDialogButtonBox(frmFormatsAdd)
        self.bb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb.setObjectName("bb")
        self.verticalLayout_3.addWidget(self.bb)
        self.horizontalLayout_16.addLayout(self.verticalLayout_3)

        self.retranslateUi(frmFormatsAdd)
        QtCore.QMetaObject.connectSlotsByName(frmFormatsAdd)

    def retranslateUi(self, frmFormatsAdd):
        _translate = QtCore.QCoreApplication.translate
        frmFormatsAdd.setWindowTitle(_translate("frmFormatsAdd", "Managing formats in products"))
        self.label_4.setText(_translate("frmFormatsAdd", "Name of the format"))
        self.label_3.setText(_translate("frmFormatsAdd", "Amount"))
        self.spnAmount.setSuffix(_translate("frmFormatsAdd", " g"))
from caloriestracker.ui.myqdoublespinbox import myQDoubleSpinBox
import caloriestracker.images.caloriestracker_rc
