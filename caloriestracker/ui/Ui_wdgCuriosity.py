# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/wdgCuriosity.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_wdgCuriosity(object):
    def setupUi(self, wdgCuriosity):
        wdgCuriosity.setObjectName("wdgCuriosity")
        wdgCuriosity.resize(508, 84)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(wdgCuriosity)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lblPixmap = QtWidgets.QLabel(wdgCuriosity)
        self.lblPixmap.setMinimumSize(QtCore.QSize(32, 32))
        self.lblPixmap.setMaximumSize(QtCore.QSize(32, 32))
        self.lblPixmap.setText("")
        self.lblPixmap.setPixmap(QtGui.QPixmap(":/caloriestracker/curiosity.png"))
        self.lblPixmap.setScaledContents(True)
        self.lblPixmap.setObjectName("lblPixmap")
        self.horizontalLayout_3.addWidget(self.lblPixmap)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(wdgCuriosity)
        self.label_2.setMinimumSize(QtCore.QSize(10, 0))
        self.label_2.setMaximumSize(QtCore.QSize(10, 16777215))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lblTitle = QtWidgets.QLabel(wdgCuriosity)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.lblTitle.setFont(font)
        self.lblTitle.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.lblTitle.setWordWrap(True)
        self.lblTitle.setObjectName("lblTitle")
        self.horizontalLayout.addWidget(self.lblTitle)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(wdgCuriosity)
        self.label.setMinimumSize(QtCore.QSize(60, 0))
        self.label.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lbl = QtWidgets.QLabel(wdgCuriosity)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lbl.setFont(font)
        self.lbl.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.lbl.setWordWrap(True)
        self.lbl.setObjectName("lbl")
        self.horizontalLayout_2.addWidget(self.lbl)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)

        self.retranslateUi(wdgCuriosity)
        QtCore.QMetaObject.connectSlotsByName(wdgCuriosity)

    def retranslateUi(self, wdgCuriosity):
        pass
import caloriestracker.images.caloriestracker_rc
