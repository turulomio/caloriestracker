## @namesapace caloriestracker.ui.frmMain
## @brief User interface main window.
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QMainWindow,  QWidget, QLabel, QComboBox
from caloriestracker.database_update import database_update
from caloriestracker.libcaloriestracker import ProductManager
from caloriestracker.ui.myqwidgets import qmessagebox
from caloriestracker.ui.Ui_frmMain import Ui_frmMain
from caloriestracker.ui.wdgCuriosities import wdgCuriosities
from caloriestracker.ui.frmSettings import frmSettings
from caloriestracker.version import __versiondate__
from os import environ

class frmMain(QMainWindow, Ui_frmMain):
    def __init__(self, mem, parent = 0,  flags = False):
        QMainWindow.__init__(self, None)
        self.setupUi(self)
        self.showMaximized()
        
        self.mem=mem
        self.mem.con.inactivity_timeout.connect(self.inactivity_timeout)
        
        database_update(self.mem.con, "caloriestracker")
        
        self.w=QWidget()       
        self.statusBar.addWidget(QLabel(self.mem.con.url_string()))

        self.mem.load_db_data() ##CARGA TODOS LOS DATOS Y LOS VINCULA       
  
        if self.mem.con.is_superuser():
            self.setWindowTitle(self.tr("Calories Tracker 2019-{0} \xa9 (Admin mode)").format(__versiondate__.year))#print ("Xulpymoney 2010-{0} © €".encode('unicode-escape'))
            self.setWindowIcon(self.mem.qicon_admin())
        else:
            self.setWindowTitle(self.tr("Calories Tracker 2019-{0} \xa9").format(__versiondate__.year))
            
        self.tbMain.addSeparator()
        self.lblUsers=QLabel()
        self.lblUsers.setText(self.tr("Select a user"))
        self.tbUsers.addWidget(self.lblUsers)
        self.cmbUsers=QComboBox()
        self.tbUsers.addWidget(self.cmbUsers)
        self.mem.data.users.qcombobox(self.cmbUsers, self.mem.user, icons=True)
        self.cmbUsers.currentIndexChanged.connect(self.on_cmbUsers_currentIndexChanged)
        
        b="Bread"
        print(self.mem.trHS(b))
        
    @pyqtSlot(int)
    def on_cmbUsers_currentIndexChanged(self, index):
        self.mem.user=self.mem.data.users.find_by_id(int(self.cmbUsers.itemData(self.cmbUsers.currentIndex())))
        print(self.mem.user, index)
        self.mem.settings.setValue("mem/currentuser", self.mem.user.id)
        self.on_actionBiometrics_triggered()
        qmessagebox("Changed user to {}".format(self.mem.user.name))        

    def inactivity_timeout(self):
        self.hide()
        qmessagebox(self.tr("Disconnecting due to {} minutes of inactivity.".format(self.mem.con.inactivity_timeout_minutes)))
        self.on_actionExit_triggered()


    @pyqtSlot()  
    def on_actionExit_triggered(self):
        self.mem.__del__()
        print ("App correctly closed")
        self.close()
        self.destroy()
        
    @pyqtSlot()
    def on_actionAbout_triggered(self):
        from caloriestracker.ui.frmAbout import frmAbout
        fr=frmAbout(self.mem)
        fr.exec_()

    @pyqtSlot()  
    def on_actionMemory_triggered(self):        
        self.mem.data.load()

    @pyqtSlot()  
    def on_actionHelp_triggered(self):
        def in_external():
            QDesktopServices.openUrl(QUrl(self.mem.url_wiki))

        try:
            user=environ['USER']
        except:
            user=None

        try: ## Remove when qwebwenginewidgets work again
            from caloriestracker.ui.frmHelp import frmHelp

            if user!=None and user=="root":
                in_external()
            else:
                w=frmHelp(self.mem, self)
                w.show()
        except:
            in_external()

    @pyqtSlot()  
    def on_actionSettings_triggered(self):
        w=frmSettings(self.mem, self)
        w.exec_()
        self.retranslateUi(self)

    @pyqtSlot()  
    def on_actionMeals_triggered(self):
        from caloriestracker.ui.wdgMeals import wdgMeals
        self.w.close()
        self.w=wdgMeals(self.mem,  self)
        self.layout.addWidget(self.w)
        self.w.show()

    @pyqtSlot()  
    def on_actionUsers_triggered(self):
        from caloriestracker.ui.wdgUsers import wdgUsers
        self.w.close()
        self.w=wdgUsers(self.mem,  self)
        self.layout.addWidget(self.w)
        self.w.show()

    @pyqtSlot()  
    def on_actionCuriosities_triggered(self):
        self.w.close()
        self.w=wdgCuriosities(self.mem,  self)
        self.layout.addWidget(self.w)
        self.w.show()

    @pyqtSlot()  
    def on_actionBiometrics_triggered(self):
        from caloriestracker.ui.wdgBiometrics import wdgBiometrics
        self.w.close()
        self.w=wdgBiometrics(self.mem,  self)
        self.layout.addWidget(self.w)
        self.w.show()

    @pyqtSlot()  
    def on_actionBiometricsAdd_triggered(self):
        from caloriestracker.ui.frmBiometricsAdd import frmBiometricsAdd
        w=frmBiometricsAdd(self.mem, None,  self)
        w.exec_()

    @pyqtSlot()  
    def on_actionCompanies_triggered(self):
        from caloriestracker.ui.wdgCompanies import wdgCompanies
        self.w.close()
        self.w=wdgCompanies(self.mem,  self)
        self.layout.addWidget(self.w)
        self.w.show()
        self.w.txt.setFocus()

    @pyqtSlot()  
    def on_actionCompaniesAdd_triggered(self):
        from caloriestracker.ui.frmCompaniesAdd import frmCompaniesAdd
        w=frmCompaniesAdd(self.mem,  None, self)
        w.exec_()
    
    @pyqtSlot()  
    def on_actionElaboratedProducts_triggered(self):
        from caloriestracker.ui.wdgProductsElaborated import wdgProductsElaborated
        self.w.close()
        self.w=wdgProductsElaborated(self.mem,  self)
        self.layout.addWidget(self.w)
        self.w.show()
        self.w.txt.setFocus()

    @pyqtSlot()  
    def on_actionElaboratedProductAdd_triggered(self):
        from caloriestracker.ui.frmProductsElaboratedAdd import frmProductsElaboratedAdd
        w=frmProductsElaboratedAdd(self.mem, None, self)
        w.exec_()
        elaborated=w.elaboratedproduct
        w=frmProductsElaboratedAdd(self.mem, elaborated, self)
        w.exec_()
        
    @pyqtSlot()  
    def on_actionProductsUpdate_triggered(self):
        p=ProductManager(self.mem)
        p.update_from_internet()
        self.actionProductsUpdate.setText(self.tr("Update products from Internet"))
        self.actionProductsUpdate.setIcon(QIcon(":/caloriestracker/cloud_download.png"))

    @pyqtSlot()  
    def on_actionProducts_triggered(self):
        self.w.close()
        from caloriestracker.ui.wdgProducts import wdgProducts
        self.w=wdgProducts(self.mem, self)
        self.layout.addWidget(self.w)
        self.w.show()
        self.w.txt.setFocus()
        
