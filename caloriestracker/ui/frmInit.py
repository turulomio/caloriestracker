import logging
from PyQt5.QtCore import pyqtSlot, QLocale
from PyQt5.QtWidgets import QDialog, QMessageBox
from caloriestracker.admin_pg import AdminPG
from caloriestracker.database_update import database_update
from caloriestracker.ui.myqwidgets import qmessagebox
from caloriestracker.ui.Ui_frmInit import Ui_frmInit

class frmInit(QDialog, Ui_frmInit):
    def __init__(self, mem, parent = None, name = None, modal = False):
        QDialog.__init__(self,  parent)
        self.mem=mem
        locale=QLocale()
        id=locale.system().name()
        if len(id)!=2:
            id=id[:-len(id)+2]
        print("Locale {} detected".format(id))
        self.setupUi(self)
        self.mem.languages.qcombobox(self.cmbLanguage, self.mem.languages.find_by_id(id))
    
    @pyqtSlot(str)      
    def on_cmbLanguage_currentIndexChanged(self, stri):
        self.mem.language=self.mem.languages.find_by_id(self.cmbLanguage.itemData(self.cmbLanguage.currentIndex()))
        self.mem.languages.cambiar(self.mem.language.id, "caloriestracker")
        self.retranslateUi(self)
    
    @pyqtSlot()
    def on_cmdCreate_released(self):
        respuesta = QMessageBox.warning(self, self.windowTitle(), self.tr("Do you want to create {} database in {}?".format(self.txtDB.text(), self.cmbLanguage.currentText())), QMessageBox.Ok | QMessageBox.Cancel)
        if respuesta==QMessageBox.Ok:                
            admin=AdminPG(self.txtUser.text(), self.txtPass.text(), self.txtServer.text(),  self.txtPort.text())
            if admin.db_exists(self.txtDB.text())==True:
                qmessagebox("Database already exists", self.mem.app_resouce())
                return
            if admin.create_db(self.txtDB.text())==True: 
                newcon=admin.connect_to_database(self.txtDB.text())
                database_update(newcon, "caloriestracker")
                qmessagebox(self.tr("Database created. Please run Calories Tracker and login"), self.mem.app_resouce())        
                logging.info ("App correctly closed")
                self.close()
            else:
                logging.error("Something went wrong")

