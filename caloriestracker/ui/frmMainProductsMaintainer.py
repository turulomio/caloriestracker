## @namesapace caloriestracker.ui.frmMainProductsMaintainer
## @brief User interface main window.
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QMainWindow,  QWidget, QLabel, QMessageBox
from caloriestracker.database_update import database_update
from caloriestracker.datetime_functions import dtnaive2string
from caloriestracker.objects.product import ProductManager
from caloriestracker.objects.company import CompanySystemManager
from caloriestracker.objects.format import FormatSystemManagerHeterogeneus
from caloriestracker.ui.Ui_frmMainProductsMaintainer import Ui_frmMainProductsMaintainer
from caloriestracker.ui.wdgCuriosities import wdgCuriosities
from caloriestracker.ui.frmSettings import frmSettings
from caloriestracker.version import __versiondatetime__
from datetime import datetime
from os import environ, system

class frmMainProductsMaintainer(QMainWindow, Ui_frmMainProductsMaintainer):
    def __init__(self, mem, parent = 0,  flags = False):
        QMainWindow.__init__(self, None)
        self.setupUi(self)
        self.showMaximized()
        
        self.mem=mem
        self.mem.insertProducts=ProductManager(self.mem)
        self.mem.updateProducts=ProductManager(self.mem)
        self.mem.insertCompanies=CompanySystemManager(self.mem)
        self.mem.updateCompanies=CompanySystemManager(self.mem)
        self.mem.insertFormats=FormatSystemManagerHeterogeneus(self.mem)
        self.mem.updateFormats=FormatSystemManagerHeterogeneus(self.mem)
        
        database_update(self.mem.con, "caloriestracker", __versiondatetime__, "Qt")
        
        self.w=QWidget()       
        self.statusBar.addWidget(QLabel(self.mem.con.url_string()))

        self.mem.load_db_data() ##CARGA TODOS LOS DATOS Y LOS VINCULA       
  
        self.setWindowTitle(self.tr("Calories Tracker 2019-{0} \xa9 (Products maintainer mode)").format(__versiondatetime__.year))#print ("Xulpymoney 2010-{0} © €".encode('unicode-escape'))
        self.setWindowIcon(QIcon(":/caloriestracker/books.png"))

    @pyqtSlot()  
    def on_actionExit_triggered(self):        
        reply = QMessageBox.question(
                    None, 
                    self.tr('Developer mode'), 
                    self.tr("""You are in developer mode.
Changes will not be saved in database, but they will added to a SQL format file, for futures updates.
Do you want to generate it?"""), 
                    QMessageBox.Yes, 
                    QMessageBox.No
                )
        if reply==QMessageBox.Yes:
            filename="{}.sql".format(dtnaive2string(datetime.now(), "%Y%m%d%H%M"))
            f=open(filename, "w")
            f.write("-- Companies inserts\n")
            for o in self.mem.insertCompanies.arr:
                f.write(o.sql_insert() + "\n")
            f.write("\n-- Companies updates\n")
            for o in self.mem.updateCompanies.arr:
                f.write(o.sql_update() + "\n")
            f.write("\n-- Products inserts\n")
            for o in self.mem.insertProducts.arr:
                f.write(o.sql_insert("products", returning_id=False) + "\n")
            f.write("\n-- Products updates\n")
            for o in self.mem.updateProducts.arr:
                f.write(o.sql_update("products") + "\n")
            f.write("\n-- Formats inserts\n")
            for o in self.mem.insertFormats.arr:
                f.write(o.sql_insert("formats", returning_id=False) + "\n")
            f.write("\n-- Formats updates\n")
            for o in self.mem.updateFormats.arr:
                f.write(o.sql_update("formats") + "\n")
            f.close()
        print ("App correctly closed")
        system("cat {}".format(filename))
#        self.close()
#        self.destroy()
        exit(0)
        
    @pyqtSlot()
    def on_actionAbout_triggered(self):
        from caloriestracker.ui.frmAbout import frmAbout
        fr=frmAbout(self.mem)
        fr.exec_()

    @pyqtSlot()  
    def on_actionReportIssue_triggered(self):        
            QDesktopServices.openUrl(QUrl("https://github.com/turulomio/caloriestracker/issues/new"))

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
    def closeEvent(self, event):
        event.accept()
        self.on_actionExit_triggered()


    @pyqtSlot()  
    def on_actionSettings_triggered(self):
        w=frmSettings(self.mem, self)
        w.exec_()
        self.retranslateUi(self)

    @pyqtSlot()  
    def on_actionCuriosities_triggered(self):
        self.w.close()
        self.w=wdgCuriosities(self.mem,  self)
        self.layout.addWidget(self.w)
        self.w.show()


    @pyqtSlot()  
    def on_actionCompanies_triggered(self):
        from caloriestracker.ui.wdgCompanies import wdgCompanies
        self.w.close()
        self.w=wdgCompanies(self.mem, True,  self)
        self.layout.addWidget(self.w)
        self.w.show()
        self.w.txt.setFocus()

    @pyqtSlot()  
    def on_actionCompaniesAdd_triggered(self):
        from caloriestracker.ui.frmCompaniesAdd import frmCompaniesAdd
        w=frmCompaniesAdd(self.mem,  None, self)
        w.exec_()

    @pyqtSlot()  
    def on_actionProducts_triggered(self):
        self.w.close()
        from caloriestracker.ui.wdgProducts import wdgProducts
        self.w=wdgProducts(self.mem, True, self)
        self.layout.addWidget(self.w)
        self.w.show()
        self.w.txt.setFocus()
