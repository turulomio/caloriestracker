# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/frmHelp.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmHelp(object):
    def setupUi(self, frmHelp):
        frmHelp.setObjectName("frmHelp")
        frmHelp.resize(1078, 851)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/xulpymoney/books.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmHelp.setWindowIcon(icon)
        frmHelp.setSizeGripEnabled(True)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(frmHelp)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblApp = QtWidgets.QLabel(frmHelp)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lblApp.setFont(font)
        self.lblApp.setAlignment(QtCore.Qt.AlignCenter)
        self.lblApp.setObjectName("lblApp")
        self.verticalLayout.addWidget(self.lblApp)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.lblPixmap = QtWidgets.QLabel(frmHelp)
        self.lblPixmap.setMaximumSize(QtCore.QSize(68, 68))
        self.lblPixmap.setPixmap(QtGui.QPixmap(":/xulpymoney/books.png"))
        self.lblPixmap.setScaledContents(True)
        self.lblPixmap.setAlignment(QtCore.Qt.AlignCenter)
        self.lblPixmap.setObjectName("lblPixmap")
        self.horizontalLayout.addWidget(self.lblPixmap)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.webEngineView = QtWebEngineWidgets.QWebEngineView(frmHelp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.webEngineView.sizePolicy().hasHeightForWidth())
        self.webEngineView.setSizePolicy(sizePolicy)
        self.webEngineView.setUrl(QtCore.QUrl("https://github.com/turulomio/xulpymoney/wiki"))
        self.webEngineView.setObjectName("webEngineView")
        self.verticalLayout.addWidget(self.webEngineView)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(frmHelp)
        QtCore.QMetaObject.connectSlotsByName(frmHelp)

    def retranslateUi(self, frmHelp):
        _translate = QtCore.QCoreApplication.translate
        frmHelp.setWindowTitle(_translate("frmHelp", "Xulpymoney help"))
        self.lblApp.setText(_translate("frmHelp", "Xulpymoney Help"))
from PyQt5 import QtWebEngineWidgets
import caloriestracker.images.caloriestracker_rc
import xulpymoney_rc
