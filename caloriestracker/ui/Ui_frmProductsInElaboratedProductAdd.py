# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/frmProductsInElaboratedProductAdd.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmProductsInElaboratedProductAdd(object):
    def setupUi(self, frmProductsInElaboratedProductAdd):
        frmProductsInElaboratedProductAdd.setObjectName("frmProductsInElaboratedProductAdd")
        frmProductsInElaboratedProductAdd.setWindowModality(QtCore.Qt.WindowModal)
        frmProductsInElaboratedProductAdd.resize(581, 223)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/caloriestracker/books.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmProductsInElaboratedProductAdd.setWindowIcon(icon)
        frmProductsInElaboratedProductAdd.setModal(True)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(frmProductsInElaboratedProductAdd)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl = QtWidgets.QLabel(frmProductsInElaboratedProductAdd)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl.setFont(font)
        self.lbl.setStyleSheet("color: rgb(0, 128, 0);")
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.verticalLayout_3.addWidget(self.lbl)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(frmProductsInElaboratedProductAdd)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.cmbProducts = QtWidgets.QComboBox(frmProductsInElaboratedProductAdd)
        self.cmbProducts.setEditable(True)
        self.cmbProducts.setObjectName("cmbProducts")
        self.horizontalLayout_3.addWidget(self.cmbProducts)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(frmProductsInElaboratedProductAdd)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.cmbFormats = QtWidgets.QComboBox(frmProductsInElaboratedProductAdd)
        self.cmbFormats.setEditable(False)
        self.cmbFormats.setObjectName("cmbFormats")
        self.horizontalLayout_4.addWidget(self.cmbFormats)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(frmProductsInElaboratedProductAdd)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.spnAmount = myQDoubleSpinBox(frmProductsInElaboratedProductAdd)
        self.spnAmount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spnAmount.setProperty("showGroupSeparator", True)
        self.spnAmount.setMinimum(1.0)
        self.spnAmount.setMaximum(1000000.0)
        self.spnAmount.setProperty("value", 100.0)
        self.spnAmount.setObjectName("spnAmount")
        self.horizontalLayout.addWidget(self.spnAmount)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.bb = QtWidgets.QDialogButtonBox(frmProductsInElaboratedProductAdd)
        self.bb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb.setObjectName("bb")
        self.verticalLayout_3.addWidget(self.bb)
        self.horizontalLayout_16.addLayout(self.verticalLayout_3)

        self.retranslateUi(frmProductsInElaboratedProductAdd)
        QtCore.QMetaObject.connectSlotsByName(frmProductsInElaboratedProductAdd)

    def retranslateUi(self, frmProductsInElaboratedProductAdd):
        _translate = QtCore.QCoreApplication.translate
        frmProductsInElaboratedProductAdd.setWindowTitle(_translate("frmProductsInElaboratedProductAdd", "Managing products in an elaborated product"))
        self.label_2.setText(_translate("frmProductsInElaboratedProductAdd", "Select a product"))
        self.label_4.setText(_translate("frmProductsInElaboratedProductAdd", "Select a format"))
        self.label_3.setText(_translate("frmProductsInElaboratedProductAdd", "Amount"))
        self.spnAmount.setSuffix(_translate("frmProductsInElaboratedProductAdd", " g"))
from caloriestracker.ui.myqdoublespinbox import myQDoubleSpinBox
import caloriestracker.images.caloriestracker_rc
