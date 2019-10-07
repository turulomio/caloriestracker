## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

## This file must be in a directory ui in the package
## In the parent  directory we need
## package_resources
## connection_pg
## translationlanguages

## access=frmAccess("frmAccess")
## access.setResources(":/calores.png","calores.png"
## access.exec_()

from PyQt5.QtCore import pyqtSlot, QSettings
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QMessageBox
from .Ui_frmAccess import Ui_frmAccess
from .. connection_pg_qt import ConnectionQt
from .. translationlanguages import TranslationLanguageManager

##After execute it you can link to a singleton for example
##mem.settings=access.settings
##mem.con=access.con

## @param module From this string we get the module translation path and de root 
## @param settings_root string for example "frmAccess" or "frmSync"
## @param settings QSettings of the app. If it's None it creates a Qsettings object, and you can get it with self.settings
class frmAccess(QDialog, Ui_frmAccess):
    def __init__(self, module, settings_root, settings=None, parent = None):
        QDialog.__init__(self,  parent)
        if settings==None:
            self.settings=QSettings()
        else:
            self.settings=settings
        self.settingsroot=settings_root
        self.module=module

        self.setModal(True)
        self.setupUi(self)
        self.parent=parent

#        self.cmbLanguages.disconnect()
        self.languages=TranslationLanguageManager()
        self.languages.load_all()
        self.languages.selected=self.languages.find_by_id(self.settings.value(self.settingsroot+"/language", "en"))
        self.languages.qcombobox(self.cmbLanguages, self.languages.selected)
#        self.cmbLanguages.currentIndexChanged.connect(self.on_cmbLanguages_currentIndexChanged)

        self.setTitle(self.tr("Log in PostreSQL database"))
        self.txtDB.setText(self.settings.value(self.settingsroot +"/db", "" ))
        self.txtPort.setText(self.settings.value(self.settingsroot +"/port", "5432"))
        self.txtUser.setText(self.settings.value(self.settingsroot +"/user", "postgres" ))
        self.txtServer.setText(self.settings.value(self.settingsroot +"/server", "127.0.0.1" ))
        self.txtPass.setFocus()

        self.con=ConnectionQt()#Pointer to connection

    def setResources(self, pixmap, icon):
        self.icon= QIcon(icon)
        self.pixmap=QPixmap(pixmap)
        self.lblPixmap.setPixmap(self.pixmap)
        self.setWindowIcon(self.icon)        

    def setTitle(self, text):
        self.setWindowTitle(text)

    def setLabel(self, text):
        self.lbl.setText(text)

    def setLanguagesVisible(self, boolean):
        if boolean==False:
            self.lblLanguage.hide()
            self.cmbLanguages.hide()

    @pyqtSlot(int)
    def on_cmbLanguages_currentIndexChanged(self, stri):
        self.languages.selected=self.languages.find_by_id(self.cmbLanguages.itemData(self.cmbLanguages.currentIndex()))
        self.settings.setValue(self.settingsroot+"/language", self.languages.selected.id)
        self.languages.cambiar(self.languages.selected.id, self.module)
        self.retranslateUi(self)

    @pyqtSlot() 
    def on_cmdYN_accepted(self):
        self.settings.setValue(self.settingsroot +"/db", self.txtDB.text() )
        self.settings.setValue(self.settingsroot +"/port",  self.txtPort.text())
        self.settings.setValue(self.settingsroot +"/user" ,  self.txtUser.text())
        self.settings.setValue(self.settingsroot +"/server", self.txtServer.text())   
        self.settings.setValue(self.settingsroot+"/language", self.cmbLanguages.itemData(self.cmbLanguages.currentIndex()))
        self.con.init__create(self.txtUser.text(), self.txtPass.text(), self.txtServer.text(), self.txtPort.text(), self.txtDB.text())
        self.con.connect()
        if self.con.is_active():
            self.accept()
        else:
            self.qmessagebox(self.tr("Error conecting to {} database in {} server").format(self.con.db, self.con.server))
            return

    @pyqtSlot() 
    def on_cmdYN_rejected(self):
        self.reject()

    def qmessagebox(self,  text):
        m=QMessageBox()
        m.setWindowIcon(self.icon)
        m.setIcon(QMessageBox.Information)
        m.setText(text)
        m.exec_()
