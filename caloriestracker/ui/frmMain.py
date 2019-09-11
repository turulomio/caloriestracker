## @namesapace caloriestracker.ui.frmMain
## @brief User interface main window.

from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QMainWindow,  QWidget, QLabel
import os
import logging
from caloriestracker.ui.Ui_frmMain import Ui_frmMain
from caloriestracker.libcaloriestracker import ProductManager
from caloriestracker.libcaloriestrackerfunctions import qmessagebox, string2datetime, is_there_internet
from caloriestracker.version import __versiondate__
from caloriestracker.ui.wdgCuriosities import wdgCuriosities
from caloriestracker.ui.frmAuxiliarTables import frmAuxiliarTables
from caloriestracker.ui.frmSettings import frmSettings
from datetime import timezone


class frmMain(QMainWindow, Ui_frmMain):
    def __init__(self, mem, parent = 0,  flags = False):
        QMainWindow.__init__(self, None)
        self.setupUi(self)
        self.showMaximized()
        
        self.mem=mem
        self.mem.con.inactivity_timeout.connect(self.inactivity_timeout)        
        self.sqlvacio="select * from products where id=-999999"
        
        self.w=QWidget()       
        self.statusBar.addWidget(QLabel(self.mem.con.url_string()))

        self.mem.load_db_data() ##CARGA TODOS LOS DATOS Y LOS VINCULA       
  
        if self.mem.con.is_superuser():
            self.setWindowTitle(self.tr("Calories Tracker 2019-{0} \xa9 (Admin mode)").format(__versiondate__.year))#print ("Xulpymoney 2010-{0} © €".encode('unicode-escape'))
            self.setWindowIcon(self.mem.qicon_admin())
        else:
            self.setWindowTitle(self.tr("Calories Tracker 2019-{0} \xa9").format(__versiondate__.year))
            self.actionDocumentsPurge.setEnabled(False)
        

        #self.__checks_version_of_products_xlsx()

    ## Checks if products.xlsx version in Internet is older than db products.xlsx version in database
    def __checks_version_of_products_xlsx(self):
        dbversion=string2datetime(self.mem.settingsdb.value("Version of products.xlsx", "190001010000"), type=6)
        dbversion=dbversion.replace(tzinfo=timezone.utc)
        internetversion=self.mem.data.products.dtaware_internet_products_xlsx()
        if internetversion!=None and dbversion<internetversion:
            logging.info(self.tr("Products list outdated, please upgrade it"))
            self.actionProductsUpdate.setText(self.tr("Update products from Internet (NEEDED)"))
            self.actionProductsUpdate.setIcon(QIcon(":/caloriestracker/cloud_download_needed.png"))
        if is_there_internet()==False:
            self.actionProductsUpdate.setEnabled(False)


    def actionsEnabled(self, bool):
        self.menuBar.setEnabled(bool)
        self.toolBar.setEnabled(bool)
        

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
            user=os.environ['USER']
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
    def on_actionAuxiliarTables_triggered(self):
        w=frmAuxiliarTables(self.mem, self)
        w.exec_()
        
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
    def on_actionCuriosities_triggered(self):
        self.w.close()
        self.w=wdgCuriosities(self.mem,  self)
        self.layout.addWidget(self.w)
        self.w.show()
    
    @pyqtSlot()  
    def on_actionProductsUser_triggered(self):
        self.w.close()
        arrInt=[]
        for p in self.mem.data.products.arr:
            if p.id<0:
                arrInt.append(p.id)
        self.layout.addWidget(self.w)
        self.w.show()
        
    @pyqtSlot()  
    def on_actionProductsUpdate_triggered(self):
        p=ProductManager(self.mem)
        p.update_from_internet()
        self.actionProductsUpdate.setText(self.tr("Update products from Internet"))
        self.actionProductsUpdate.setIcon(QIcon(":/caloriestracker/cloud_download.png"))


    @pyqtSlot()  
    def on_actionTablasAuxiliares_triggered(self):
        w=frmAuxiliarTables(self.mem, self)
        w.tblTipos_reload()
        w.exec_()

    @pyqtSlot()  
    def on_actionSearch_triggered(self):
        self.w.close()
        self.layout.addWidget(self.w)
        self.w.show()
        
