# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/wdgMeals.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_wdgMeals(object):
    def setupUi(self, wdgMeals):
        wdgMeals.setObjectName("wdgMeals")
        wdgMeals.resize(1012, 669)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(wdgMeals)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl = QtWidgets.QLabel(wdgMeals)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl.setFont(font)
        self.lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl.setObjectName("lbl")
        self.verticalLayout.addWidget(self.lbl)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.calendar = QtWidgets.QCalendarWidget(wdgMeals)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendar.sizePolicy().hasHeightForWidth())
        self.calendar.setSizePolicy(sizePolicy)
        self.calendar.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendar.setObjectName("calendar")
        self.horizontalLayout.addWidget(self.calendar)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tblMeals = mqtwObjects(wdgMeals)
        self.tblMeals.setObjectName("tblMeals")
        self.verticalLayout.addWidget(self.tblMeals)
        self.lblFound = QtWidgets.QLabel(wdgMeals)
        self.lblFound.setObjectName("lblFound")
        self.verticalLayout.addWidget(self.lblFound)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.actionMealNew = QtWidgets.QAction(wdgMeals)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/caloriestracker/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMealNew.setIcon(icon)
        self.actionMealNew.setObjectName("actionMealNew")
        self.actionMealDelete = QtWidgets.QAction(wdgMeals)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/caloriestracker/list-remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMealDelete.setIcon(icon1)
        self.actionMealDelete.setObjectName("actionMealDelete")
        self.actionMealEdit = QtWidgets.QAction(wdgMeals)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/caloriestracker/document-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMealEdit.setIcon(icon2)
        self.actionMealEdit.setObjectName("actionMealEdit")
        self.actionProductEdit = QtWidgets.QAction(wdgMeals)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/caloriestracker/books.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProductEdit.setIcon(icon3)
        self.actionProductEdit.setObjectName("actionProductEdit")
        self.actionMealDeleteDay = QtWidgets.QAction(wdgMeals)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/caloriestracker/button_cancel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMealDeleteDay.setIcon(icon4)
        self.actionMealDeleteDay.setObjectName("actionMealDeleteDay")

        self.retranslateUi(wdgMeals)
        QtCore.QMetaObject.connectSlotsByName(wdgMeals)

    def retranslateUi(self, wdgMeals):
        _translate = QtCore.QCoreApplication.translate
        self.lbl.setText(_translate("wdgMeals", "Your meals"))
        self.lblFound.setText(_translate("wdgMeals", "Registers found"))
        self.actionMealNew.setText(_translate("wdgMeals", "New meal"))
        self.actionMealNew.setToolTip(_translate("wdgMeals", "New meal"))
        self.actionMealDelete.setText(_translate("wdgMeals", "Delete meal"))
        self.actionMealDelete.setToolTip(_translate("wdgMeals", "Delete meal"))
        self.actionMealEdit.setText(_translate("wdgMeals", "Edit meal"))
        self.actionMealEdit.setToolTip(_translate("wdgMeals", "Edit meal"))
        self.actionProductEdit.setText(_translate("wdgMeals", "Edit product"))
        self.actionProductEdit.setToolTip(_translate("wdgMeals", "Edit product"))
        self.actionMealDeleteDay.setText(_translate("wdgMeals", "Delete selected date meals"))
        self.actionMealDeleteDay.setToolTip(_translate("wdgMeals", "Delete selected date meals"))
from caloriestracker.ui.myqtablewidget import mqtwObjects
import caloriestracker.images.caloriestracker_rc
