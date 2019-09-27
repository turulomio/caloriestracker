# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/wdgCuriosities.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_wdgCuriosities(object):
    def setupUi(self, wdgCuriosities):
        wdgCuriosities.setObjectName("wdgCuriosities")
        wdgCuriosities.resize(400, 299)
        self.layout_2 = QtWidgets.QHBoxLayout(wdgCuriosities)
        self.layout_2.setObjectName("layout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblApp = QtWidgets.QLabel(wdgCuriosities)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lblApp.setFont(font)
        self.lblApp.setScaledContents(False)
        self.lblApp.setAlignment(QtCore.Qt.AlignCenter)
        self.lblApp.setIndent(-1)
        self.lblApp.setObjectName("lblApp")
        self.verticalLayout.addWidget(self.lblApp)
        self.scrollArea = QtWidgets.QScrollArea(wdgCuriosities)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 382, 237))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setObjectName("layout")
        self.horizontalLayout_3.addLayout(self.layout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.layout_2.addLayout(self.verticalLayout)

        self.retranslateUi(wdgCuriosities)
        QtCore.QMetaObject.connectSlotsByName(wdgCuriosities)

    def retranslateUi(self, wdgCuriosities):
        _translate = QtCore.QCoreApplication.translate
        self.lblApp.setText(_translate("wdgCuriosities", "Calories Tracker curiosities"))
import caloriestracker.images.caloriestracker_rc
