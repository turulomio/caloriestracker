# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/frmProductsElaboratedAdd.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmProductsElaboratedAdd(object):
    def setupUi(self, frmProductsElaboratedAdd):
        frmProductsElaboratedAdd.setObjectName("frmProductsElaboratedAdd")
        frmProductsElaboratedAdd.setWindowModality(QtCore.Qt.WindowModal)
        frmProductsElaboratedAdd.resize(600, 577)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/caloriestracker/books.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmProductsElaboratedAdd.setWindowIcon(icon)
        frmProductsElaboratedAdd.setModal(True)
        self.horizontalLayout = QtWidgets.QHBoxLayout(frmProductsElaboratedAdd)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl = QtWidgets.QLabel(frmProductsElaboratedAdd)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl.setFont(font)
        self.lbl.setStyleSheet("color: rgb(0, 128, 0);")
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.verticalLayout_3.addWidget(self.lbl)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_15 = QtWidgets.QLabel(frmProductsElaboratedAdd)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_14.addWidget(self.label_15)
        self.txtName = QtWidgets.QLineEdit(frmProductsElaboratedAdd)
        self.txtName.setObjectName("txtName")
        self.horizontalLayout_14.addWidget(self.txtName)
        self.verticalLayout_3.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(frmProductsElaboratedAdd)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.cmbFoodtypes = QtWidgets.QComboBox(frmProductsElaboratedAdd)
        self.cmbFoodtypes.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.cmbFoodtypes.setObjectName("cmbFoodtypes")
        self.horizontalLayout_4.addWidget(self.cmbFoodtypes)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_16 = QtWidgets.QLabel(frmProductsElaboratedAdd)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_17.addWidget(self.label_16)
        self.spnFinalAmount = myQDoubleSpinBox(frmProductsElaboratedAdd)
        self.spnFinalAmount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spnFinalAmount.setDecimals(1)
        self.spnFinalAmount.setMinimum(1.0)
        self.spnFinalAmount.setMaximum(1000000.0)
        self.spnFinalAmount.setSingleStep(100.0)
        self.spnFinalAmount.setProperty("value", 1.0)
        self.spnFinalAmount.setObjectName("spnFinalAmount")
        self.horizontalLayout_17.addWidget(self.spnFinalAmount)
        self.verticalLayout_3.addLayout(self.horizontalLayout_17)
        self.tblProductsIn = myQTableWidget(frmProductsElaboratedAdd)
        self.tblProductsIn.setObjectName("tblProductsIn")
        self.verticalLayout_3.addWidget(self.tblProductsIn)
        self.bb = QtWidgets.QDialogButtonBox(frmProductsElaboratedAdd)
        self.bb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb.setObjectName("bb")
        self.verticalLayout_3.addWidget(self.bb)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.actionProductInNew = QtWidgets.QAction(frmProductsElaboratedAdd)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/caloriestracker/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProductInNew.setIcon(icon1)
        self.actionProductInNew.setObjectName("actionProductInNew")
        self.actionProductInDelete = QtWidgets.QAction(frmProductsElaboratedAdd)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/caloriestracker/list-remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProductInDelete.setIcon(icon2)
        self.actionProductInDelete.setObjectName("actionProductInDelete")
        self.actionProductInEdit = QtWidgets.QAction(frmProductsElaboratedAdd)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/caloriestracker/document-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProductInEdit.setIcon(icon3)
        self.actionProductInEdit.setObjectName("actionProductInEdit")
        self.actionProductEdit = QtWidgets.QAction(frmProductsElaboratedAdd)
        self.actionProductEdit.setIcon(icon)
        self.actionProductEdit.setObjectName("actionProductEdit")

        self.retranslateUi(frmProductsElaboratedAdd)
        QtCore.QMetaObject.connectSlotsByName(frmProductsElaboratedAdd)

    def retranslateUi(self, frmProductsElaboratedAdd):
        _translate = QtCore.QCoreApplication.translate
        frmProductsElaboratedAdd.setWindowTitle(_translate("frmProductsElaboratedAdd", "Managing elaborated products"))
        self.label_15.setText(_translate("frmProductsElaboratedAdd", "Name of the product"))
        self.label_3.setText(_translate("frmProductsElaboratedAdd", "Select food type"))
        self.label_16.setText(_translate("frmProductsElaboratedAdd", "Final amount"))
        self.spnFinalAmount.setSuffix(_translate("frmProductsElaboratedAdd", " g"))
        self.actionProductInNew.setText(_translate("frmProductsElaboratedAdd", "New product in elaboration"))
        self.actionProductInNew.setToolTip(_translate("frmProductsElaboratedAdd", "New product in elaboration"))
        self.actionProductInDelete.setText(_translate("frmProductsElaboratedAdd", "Delete product in elaboration"))
        self.actionProductInDelete.setToolTip(_translate("frmProductsElaboratedAdd", "Delete product in elaboration"))
        self.actionProductInEdit.setText(_translate("frmProductsElaboratedAdd", "Edit product in elaboration"))
        self.actionProductInEdit.setToolTip(_translate("frmProductsElaboratedAdd", "Edit product in elaboration"))
        self.actionProductEdit.setText(_translate("frmProductsElaboratedAdd", "Edit product"))
        self.actionProductEdit.setToolTip(_translate("frmProductsElaboratedAdd", "Edit product"))
from caloriestracker.ui.myqdoublespinbox import myQDoubleSpinBox
from caloriestracker.ui.myqtablewidget import myQTableWidget
import caloriestracker.images.caloriestracker_rc
