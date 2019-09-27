# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/frmMealsAdd.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmMealsAdd(object):
    def setupUi(self, frmMealsAdd):
        frmMealsAdd.setObjectName("frmMealsAdd")
        frmMealsAdd.setWindowModality(QtCore.Qt.WindowModal)
        frmMealsAdd.resize(538, 373)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/caloriestracker/meals.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmMealsAdd.setWindowIcon(icon)
        frmMealsAdd.setModal(True)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(frmMealsAdd)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl = QtWidgets.QLabel(frmMealsAdd)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl.setFont(font)
        self.lbl.setStyleSheet("color: rgb(0, 128, 0);")
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.verticalLayout.addWidget(self.lbl)
        self.wdgDT = wdgDatetime(frmMealsAdd)
        self.wdgDT.setObjectName("wdgDT")
        self.verticalLayout.addWidget(self.wdgDT)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(frmMealsAdd)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.cmbProducts = QtWidgets.QComboBox(frmMealsAdd)
        self.cmbProducts.setEditable(True)
        self.cmbProducts.setObjectName("cmbProducts")
        self.horizontalLayout_3.addWidget(self.cmbProducts)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(frmMealsAdd)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.cmbFormats = QtWidgets.QComboBox(frmMealsAdd)
        self.cmbFormats.setEditable(False)
        self.cmbFormats.setObjectName("cmbFormats")
        self.horizontalLayout_4.addWidget(self.cmbFormats)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(frmMealsAdd)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.spnAmount = myQDoubleSpinBox(frmMealsAdd)
        self.spnAmount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spnAmount.setMaximum(1000000.0)
        self.spnAmount.setProperty("value", 100.0)
        self.spnAmount.setObjectName("spnAmount")
        self.horizontalLayout.addWidget(self.spnAmount)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.bb = QtWidgets.QDialogButtonBox(frmMealsAdd)
        self.bb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb.setObjectName("bb")
        self.verticalLayout.addWidget(self.bb)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(frmMealsAdd)
        QtCore.QMetaObject.connectSlotsByName(frmMealsAdd)
        frmMealsAdd.setTabOrder(self.cmbProducts, self.spnAmount)

    def retranslateUi(self, frmMealsAdd):
        _translate = QtCore.QCoreApplication.translate
        frmMealsAdd.setWindowTitle(_translate("frmMealsAdd", "Managing meals"))
        self.label_2.setText(_translate("frmMealsAdd", "Select a product"))
        self.label_4.setText(_translate("frmMealsAdd", "Select a format"))
        self.label_3.setText(_translate("frmMealsAdd", "Add an amount"))
        self.spnAmount.setSuffix(_translate("frmMealsAdd", " g"))
from caloriestracker.ui.myqdoublespinbox import myQDoubleSpinBox
from caloriestracker.ui.wdgDatetime import wdgDatetime
import caloriestracker.images.caloriestracker_rc
