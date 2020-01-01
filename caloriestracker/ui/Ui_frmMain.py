# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caloriestracker/ui/frmMain.ui'
#
# Created by: PyQt5 UI code generator 5.14.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frmMain(object):
    def setupUi(self, frmMain):
        frmMain.setObjectName("frmMain")
        frmMain.resize(811, 625)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frmMain.sizePolicy().hasHeightForWidth())
        frmMain.setSizePolicy(sizePolicy)
        frmMain.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/caloriestracker/caloriestracker.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmMain.setWindowIcon(icon)
        self.central = QtWidgets.QWidget(frmMain)
        self.central.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.central.sizePolicy().hasHeightForWidth())
        self.central.setSizePolicy(sizePolicy)
        self.central.setObjectName("central")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.central)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setObjectName("layout")
        self.horizontalLayout.addLayout(self.layout)
        frmMain.setCentralWidget(self.central)
        self.menuBar = QtWidgets.QMenuBar(frmMain)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 811, 34))
        self.menuBar.setObjectName("menuBar")
        self.menuAyuda = QtWidgets.QMenu(self.menuBar)
        self.menuAyuda.setObjectName("menuAyuda")
        self.menuXulpymoney = QtWidgets.QMenu(self.menuBar)
        self.menuXulpymoney.setObjectName("menuXulpymoney")
        self.menuProducts = QtWidgets.QMenu(self.menuBar)
        self.menuProducts.setObjectName("menuProducts")
        self.menuMealss = QtWidgets.QMenu(self.menuBar)
        self.menuMealss.setObjectName("menuMealss")
        self.menuCompanies = QtWidgets.QMenu(self.menuBar)
        self.menuCompanies.setObjectName("menuCompanies")
        self.menuUsers = QtWidgets.QMenu(self.menuBar)
        self.menuUsers.setObjectName("menuUsers")
        frmMain.setMenuBar(self.menuBar)
        self.tbMain = QtWidgets.QToolBar(frmMain)
        self.tbMain.setIconSize(QtCore.QSize(26, 26))
        self.tbMain.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.tbMain.setObjectName("tbMain")
        frmMain.addToolBar(QtCore.Qt.TopToolBarArea, self.tbMain)
        self.statusBar = QtWidgets.QStatusBar(frmMain)
        self.statusBar.setObjectName("statusBar")
        frmMain.setStatusBar(self.statusBar)
        self.tbUsers = QtWidgets.QToolBar(frmMain)
        self.tbUsers.setObjectName("tbUsers")
        frmMain.addToolBar(QtCore.Qt.TopToolBarArea, self.tbUsers)
        self.actionExit = QtWidgets.QAction(frmMain)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/caloriestracker/exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon1)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(frmMain)
        self.actionAbout.setIcon(icon)
        self.actionAbout.setObjectName("actionAbout")
        self.actionMemory = QtWidgets.QAction(frmMain)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/caloriestracker/transfer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMemory.setIcon(icon2)
        self.actionMemory.setObjectName("actionMemory")
        self.actionSettings = QtWidgets.QAction(frmMain)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/caloriestracker/configure.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon3)
        self.actionSettings.setObjectName("actionSettings")
        self.actionHelp = QtWidgets.QAction(frmMain)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/caloriestracker/benchmark.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHelp.setIcon(icon4)
        self.actionHelp.setObjectName("actionHelp")
        self.actionProducts = QtWidgets.QAction(frmMain)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/caloriestracker/books.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProducts.setIcon(icon5)
        self.actionProducts.setObjectName("actionProducts")
        self.actionElaboratedProducts = QtWidgets.QAction(frmMain)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/caloriestracker/keko.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionElaboratedProducts.setIcon(icon6)
        self.actionElaboratedProducts.setObjectName("actionElaboratedProducts")
        self.actionCuriosities = QtWidgets.QAction(frmMain)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/caloriestracker/curiosity.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCuriosities.setIcon(icon7)
        self.actionCuriosities.setObjectName("actionCuriosities")
        self.actionMeals = QtWidgets.QAction(frmMain)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/caloriestracker/meals.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMeals.setIcon(icon8)
        self.actionMeals.setObjectName("actionMeals")
        self.actionBiometricsAdd = QtWidgets.QAction(frmMain)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/caloriestracker/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBiometricsAdd.setIcon(icon9)
        self.actionBiometricsAdd.setObjectName("actionBiometricsAdd")
        self.actionBiometrics = QtWidgets.QAction(frmMain)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/caloriestracker/biometrics.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBiometrics.setIcon(icon10)
        self.actionBiometrics.setObjectName("actionBiometrics")
        self.actionElaboratedProductAdd = QtWidgets.QAction(frmMain)
        self.actionElaboratedProductAdd.setIcon(icon6)
        self.actionElaboratedProductAdd.setObjectName("actionElaboratedProductAdd")
        self.actionCompaniesAdd = QtWidgets.QAction(frmMain)
        self.actionCompaniesAdd.setIcon(icon9)
        self.actionCompaniesAdd.setObjectName("actionCompaniesAdd")
        self.actionCompanies = QtWidgets.QAction(frmMain)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/caloriestracker/companies.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCompanies.setIcon(icon11)
        self.actionCompanies.setObjectName("actionCompanies")
        self.actionUsers = QtWidgets.QAction(frmMain)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/caloriestracker/list-add-user.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionUsers.setIcon(icon12)
        self.actionUsers.setObjectName("actionUsers")
        self.actionReportIssue = QtWidgets.QAction(frmMain)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/caloriestracker/alarm_clock.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionReportIssue.setIcon(icon13)
        self.actionReportIssue.setObjectName("actionReportIssue")
        self.actionMealsMost = QtWidgets.QAction(frmMain)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/caloriestracker/crown.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMealsMost.setIcon(icon14)
        self.actionMealsMost.setObjectName("actionMealsMost")
        self.menuAyuda.addAction(self.actionAbout)
        self.menuAyuda.addSeparator()
        self.menuAyuda.addAction(self.actionCuriosities)
        self.menuAyuda.addSeparator()
        self.menuAyuda.addAction(self.actionReportIssue)
        self.menuAyuda.addSeparator()
        self.menuAyuda.addAction(self.actionHelp)
        self.menuXulpymoney.addSeparator()
        self.menuXulpymoney.addAction(self.actionMemory)
        self.menuXulpymoney.addSeparator()
        self.menuXulpymoney.addAction(self.actionSettings)
        self.menuXulpymoney.addSeparator()
        self.menuXulpymoney.addAction(self.actionExit)
        self.menuProducts.addSeparator()
        self.menuProducts.addAction(self.actionProducts)
        self.menuProducts.addSeparator()
        self.menuProducts.addAction(self.actionElaboratedProductAdd)
        self.menuProducts.addAction(self.actionElaboratedProducts)
        self.menuMealss.addAction(self.actionMeals)
        self.menuMealss.addSeparator()
        self.menuMealss.addAction(self.actionMealsMost)
        self.menuCompanies.addAction(self.actionCompanies)
        self.menuCompanies.addSeparator()
        self.menuCompanies.addAction(self.actionCompaniesAdd)
        self.menuUsers.addAction(self.actionUsers)
        self.menuUsers.addSeparator()
        self.menuUsers.addAction(self.actionBiometricsAdd)
        self.menuUsers.addAction(self.actionBiometrics)
        self.menuBar.addAction(self.menuXulpymoney.menuAction())
        self.menuBar.addAction(self.menuUsers.menuAction())
        self.menuBar.addAction(self.menuCompanies.menuAction())
        self.menuBar.addAction(self.menuProducts.menuAction())
        self.menuBar.addAction(self.menuMealss.menuAction())
        self.menuBar.addAction(self.menuAyuda.menuAction())
        self.tbMain.addAction(self.actionMeals)
        self.tbMain.addAction(self.actionBiometrics)
        self.tbMain.addAction(self.actionElaboratedProducts)
        self.tbMain.addAction(self.actionCompanies)
        self.tbMain.addAction(self.actionProducts)
        self.tbMain.addSeparator()
        self.tbMain.addAction(self.actionMealsMost)
        self.tbMain.addSeparator()
        self.tbMain.addAction(self.actionSettings)
        self.tbMain.addAction(self.actionCuriosities)
        self.tbMain.addAction(self.actionExit)

        self.retranslateUi(frmMain)
        QtCore.QMetaObject.connectSlotsByName(frmMain)

    def retranslateUi(self, frmMain):
        _translate = QtCore.QCoreApplication.translate
        self.menuAyuda.setTitle(_translate("frmMain", "&Help"))
        self.menuXulpymoney.setTitle(_translate("frmMain", "C&alories tracker"))
        self.menuProducts.setTitle(_translate("frmMain", "&Products"))
        self.menuMealss.setTitle(_translate("frmMain", "&Meals"))
        self.menuCompanies.setTitle(_translate("frmMain", "&Companies"))
        self.menuUsers.setTitle(_translate("frmMain", "&Users"))
        self.tbMain.setWindowTitle(_translate("frmMain", "Main toolbar"))
        self.tbUsers.setWindowTitle(_translate("frmMain", "Users toolbar"))
        self.actionExit.setText(_translate("frmMain", "E&xit"))
        self.actionExit.setToolTip(_translate("frmMain", "Exit"))
        self.actionExit.setShortcut(_translate("frmMain", "Alt+Esc"))
        self.actionAbout.setText(_translate("frmMain", "&About"))
        self.actionAbout.setToolTip(_translate("frmMain", "About"))
        self.actionAbout.setShortcut(_translate("frmMain", "F2"))
        self.actionMemory.setText(_translate("frmMain", "&Update memory"))
        self.actionMemory.setToolTip(_translate("frmMain", "Update memory"))
        self.actionSettings.setText(_translate("frmMain", "&Settings"))
        self.actionSettings.setToolTip(_translate("frmMain", "Settings"))
        self.actionHelp.setText(_translate("frmMain", "&Help"))
        self.actionHelp.setToolTip(_translate("frmMain", "Help"))
        self.actionHelp.setShortcut(_translate("frmMain", "F1"))
        self.actionProducts.setText(_translate("frmMain", "Products list"))
        self.actionProducts.setToolTip(_translate("frmMain", "Products list"))
        self.actionProducts.setShortcut(_translate("frmMain", "Ctrl+B"))
        self.actionElaboratedProducts.setText(_translate("frmMain", "Elaborated products list"))
        self.actionElaboratedProducts.setToolTip(_translate("frmMain", "Elaborated products list"))
        self.actionCuriosities.setText(_translate("frmMain", "&Curiosities"))
        self.actionCuriosities.setToolTip(_translate("frmMain", "Curiosities"))
        self.actionMeals.setText(_translate("frmMain", "Meals"))
        self.actionMeals.setToolTip(_translate("frmMain", "Meals"))
        self.actionBiometricsAdd.setText(_translate("frmMain", "Add biometrics"))
        self.actionBiometricsAdd.setToolTip(_translate("frmMain", "Add biometrics"))
        self.actionBiometrics.setText(_translate("frmMain", "Biometric information"))
        self.actionBiometrics.setToolTip(_translate("frmMain", "Biometric information"))
        self.actionElaboratedProductAdd.setText(_translate("frmMain", "Add an elaborated product"))
        self.actionElaboratedProductAdd.setToolTip(_translate("frmMain", "Add an elaborated product"))
        self.actionCompaniesAdd.setText(_translate("frmMain", "Add a company"))
        self.actionCompaniesAdd.setToolTip(_translate("frmMain", "Add a company"))
        self.actionCompanies.setText(_translate("frmMain", "Companies list"))
        self.actionCompanies.setToolTip(_translate("frmMain", "Companies list"))
        self.actionUsers.setText(_translate("frmMain", "Users list"))
        self.actionUsers.setToolTip(_translate("frmMain", "Users list"))
        self.actionReportIssue.setText(_translate("frmMain", "Report an issue"))
        self.actionReportIssue.setToolTip(_translate("frmMain", "Report an issue"))
        self.actionMealsMost.setText(_translate("frmMain", "Meals I eat the most"))
        self.actionMealsMost.setToolTip(_translate("frmMain", "Meals I eat the most"))
import caloriestracker.images.caloriestracker_rc
