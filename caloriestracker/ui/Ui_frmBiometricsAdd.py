# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/frmBiometricsAdd.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmBiometricsAdd(object):
    def setupUi(self, frmBiometricsAdd):
        frmBiometricsAdd.setObjectName("frmBiometricsAdd")
        frmBiometricsAdd.setWindowModality(QtCore.Qt.WindowModal)
        frmBiometricsAdd.resize(461, 464)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/caloriestracker/list-add-user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmBiometricsAdd.setWindowIcon(icon)
        frmBiometricsAdd.setModal(True)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(frmBiometricsAdd)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl = QtWidgets.QLabel(frmBiometricsAdd)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl.setFont(font)
        self.lbl.setStyleSheet("color: rgb(0, 128, 0);")
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.verticalLayout_3.addWidget(self.lbl)
        self.wdgDT = wdgDatetime(frmBiometricsAdd)
        self.wdgDT.setObjectName("wdgDT")
        self.verticalLayout_3.addWidget(self.wdgDT)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_6 = QtWidgets.QLabel(frmBiometricsAdd)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_5.addWidget(self.label_6)
        self.spnWeight = myQDoubleSpinBox(frmBiometricsAdd)
        self.spnWeight.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spnWeight.setMaximum(1000000.0)
        self.spnWeight.setObjectName("spnWeight")
        self.horizontalLayout_5.addWidget(self.spnWeight)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(frmBiometricsAdd)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.spnHeight = myQDoubleSpinBox(frmBiometricsAdd)
        self.spnHeight.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spnHeight.setMinimum(1.0)
        self.spnHeight.setMaximum(1000000.0)
        self.spnHeight.setProperty("value", 160.0)
        self.spnHeight.setObjectName("spnHeight")
        self.horizontalLayout.addWidget(self.spnHeight)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(frmBiometricsAdd)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.cmbActivity = QtWidgets.QComboBox(frmBiometricsAdd)
        self.cmbActivity.setEditable(False)
        self.cmbActivity.setObjectName("cmbActivity")
        self.horizontalLayout_3.addWidget(self.cmbActivity)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_16 = QtWidgets.QLabel(frmBiometricsAdd)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_17.addWidget(self.label_16)
        self.cmbWeightWish = QtWidgets.QComboBox(frmBiometricsAdd)
        self.cmbWeightWish.setEditable(False)
        self.cmbWeightWish.setObjectName("cmbWeightWish")
        self.horizontalLayout_17.addWidget(self.cmbWeightWish)
        self.verticalLayout_3.addLayout(self.horizontalLayout_17)
        self.bb = QtWidgets.QDialogButtonBox(frmBiometricsAdd)
        self.bb.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb.setObjectName("bb")
        self.verticalLayout_3.addWidget(self.bb)
        self.horizontalLayout_16.addLayout(self.verticalLayout_3)

        self.retranslateUi(frmBiometricsAdd)
        QtCore.QMetaObject.connectSlotsByName(frmBiometricsAdd)

    def retranslateUi(self, frmBiometricsAdd):
        _translate = QtCore.QCoreApplication.translate
        frmBiometricsAdd.setWindowTitle(_translate("frmBiometricsAdd", "Managing biometrics"))
        self.label_6.setText(_translate("frmBiometricsAdd", "Weight"))
        self.spnWeight.setSuffix(_translate("frmBiometricsAdd", " Kg"))
        self.label_3.setText(_translate("frmBiometricsAdd", "Height"))
        self.spnHeight.setSuffix(_translate("frmBiometricsAdd", " cm"))
        self.label_2.setText(_translate("frmBiometricsAdd", "Select your type of activity"))
        self.label_16.setText(_translate("frmBiometricsAdd", "Select your wish of weight"))
from caloriestracker.ui.myqdoublespinbox import myQDoubleSpinBox
from caloriestracker.ui.wdgDatetime import wdgDatetime
import caloriestracker.images.caloriestracker_rc
