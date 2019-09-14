## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmAccess import Ui_frmAccess
from caloriestracker.connection_pg_qt import ConnectionQt
from caloriestracker.libcaloriestrackerfunctions import qmessagebox

class frmAccess(QDialog, Ui_frmAccess):
    def __init__(self, mem, parent = None, name = None, modal = False):
        """Returns accepted if conection is done, or rejected if there's an error"""""
        QDialog.__init__(self,  parent)
        self.mem=mem
        self.setModal(True)
        self.setupUi(self)
        self.parent=parent
        self.cmbLanguages.disconnect()
        self.mem.languages.qcombobox(self.cmbLanguages, self.mem.language)
        self.cmbLanguages.currentIndexChanged.connect(self.on_cmbLanguages_currentIndexChanged)
        self.setPixmap(QPixmap(":xulpymoney/coins.png"))
        self.setTitle(self.tr("Xulpymoney - Access"))
        self.con=ConnectionQt()#Pointer to connection


    def setPixmap(self, qpixmap):
        icon = QIcon()
        icon.addPixmap(qpixmap, QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)        
        
    def setTitle(self, text):
        self.setWindowTitle(text)
        
    def setLabel(self, text):
        self.lbl.setText(text)
        
    def showLanguage(self, boolean):
        if boolean==False:
            self.cmbLanguages.hide()
            self.lblLanguage.hide()
        
        
    def config_load(self):
        self.txtDB.setText(self.mem.settings.value("frmAccess/db", "xulpymoney" ))
        self.txtPort.setText(self.mem.settings.value("frmAccess/port", "5432"))
        self.txtUser.setText(self.mem.settings.value("frmAccess/user", "postgres" ))
        self.txtServer.setText(self.mem.settings.value("frmAccess/server", "127.0.0.1" ))
        self.txtPass.setFocus()
        
    def config_save(self):
        self.mem.settings.setValue("frmAccess/db", self.txtDB.text() )
        self.mem.settings.setValue("frmAccess/port",  self.txtPort.text())
        self.mem.settings.setValue("frmAccess/user" ,  self.txtUser.text())
        self.mem.settings.setValue("frmAccess/server", self.txtServer.text())   
        self.mem.settings.setValue("mem/language", self.cmbLanguages.itemData(self.cmbLanguages.currentIndex()))
        self.mem.language=self.mem.languages.find_by_id(self.cmbLanguages.itemData(self.cmbLanguages.currentIndex()))

    @pyqtSlot(int)      
    def on_cmbLanguages_currentIndexChanged(self, stri):
        self.mem.language=self.mem.languages.find_by_id(self.cmbLanguages.itemData(self.cmbLanguages.currentIndex()))
        self.mem.settings.setValue("mem/language", self.mem.language.id)
        self.mem.languages.cambiar(self.mem.language.id)
        self.retranslateUi(self)

    def make_connection(self):
        """Función que realiza la conexión devolviendo true o false con el éxito"""
        try:
            self.con.init__create(self.txtUser.text(), self.txtPass.text(), self.txtServer.text(), self.txtPort.text(), self.txtDB.text())
            self.con.connect()
            return self.con.is_active()
        except:
            print ("Error in function make_connection",  self.mem.con)
            return False
    
    @pyqtSlot() 
    def on_cmdYN_accepted(self):
        self.con.init__create(self.txtUser.text(), self.txtPass.text(), self.txtServer.text(), self.txtPort.text(), self.txtDB.text())
        self.con.connect()
        if self.con.is_active():
            self.config_save()
            self.accept()
        else:
            qmessagebox(self.tr("Error conecting to {} database in {} server").format(self.con.db, self.con.server))
            self.reject()

    @pyqtSlot() 
    def on_cmdYN_rejected(self):
        self.reject()



