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

from PyQt5.QtCore import pyqtSlot, QSettings, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QMessageBox
from logging import debug
from os import environ
from .Ui_frmAccess import Ui_frmAccess
from .myqwidgets import qmessagebox, qinputbox_string
from .. connection_pg_qt import ConnectionQt
from .. admin_pg import AdminPG
from .. translationlanguages import TranslationLanguageManager

##After execute it you can link to a singleton for example
##mem.settings=access.settings
##mem.con=access.con

## @param module From this string we get the module translation path and de root 
## @param settings_root string for example "frmAccess" or "frmSync"
## @param settings QSettings of the app. If it's None it creates a Qsettings object, and you can get it with self.settings
class frmAccess(QDialog, Ui_frmAccess):
    databaseCreated=pyqtSignal(ConnectionQt)
    def __init__(self, module, settingsSection, settings=None, parent = None):
        QDialog.__init__(self,  parent)
        if settings==None:
            self.settings=QSettings()
        else:
            self.settings=settings
        self.settingsSection=settingsSection
        self.module=module

        self.setModal(True)
        self.setupUi(self)
        self.setResources()
        self.resize(self.settings.value(self.settingsSection +"/qdialog_size", QSize(200, 60)))
        self.parent=parent

        self.languages=TranslationLanguageManager()
        self.languages.load_all()
        self.languages.selected=self.languages.find_by_id(self.settings.value(self.settingsSection+"/language", "en"))
        self.languages.qcombobox(self.cmbLanguages, self.languages.selected)

        self.con=ConnectionQt()#Pointer to connection
        
        self.setTitle(self.tr("Log in PostreSQL database"))
        
        self.cmbProfiles_update()
        current_profile=self.settings.value(self.settingsSection+"/current_profile", "")
        if current_profile=="":
            self.txtDB.setText(self.settings.value(self.settingsSection +"/db", "" ))
            self.txtPort.setText(self.settings.value(self.settingsSection +"/port", "5432"))
            self.txtUser.setText(self.settings.value(self.settingsSection +"/user", "postgres" ))
            self.txtServer.setText(self.settings.value(self.settingsSection +"/server", "127.0.0.1" ))
        else:
            self.cmbProfiles.setCurrentText(current_profile)
        
    ## Reimplements QDialog.exec_ method to make an autologin if PGPASSWORD environment variable is detected.
    def exec_(self):
        try:
            self.password=environ['PGPASSWORD']
            debug("Password automatically set from environment variable")
            self.txtPass.setText(self.password)
            self.cmdYN.accepted.emit()
        except:
            self.txtPass.setFocus()
            QDialog.exec_(self)
        self.settings.setValue(self.settingsSection + "/qdialog_size", self.size())
        self.settings.sync()

    def setResources(   self, 
                                        pixmap=":/reusingcode/frmaccess_pixmap.png", 
                                        icon=":/reusingcode/frmaccess_icon.png",
                                        database_new=":/reusingcode/database_new.png", 
                                        profile_new=":/reusingcode/profile_new.png",
                                        profile_update=":/reusingcode/profile_update.png", 
                                        profile_delete=":/reusingcode/button_cancel.png"
                                    ):
        self.lblPixmap.setPixmap(QPixmap(pixmap))
        self.setWindowIcon(QIcon(icon))
        self.cmdDatabaseNew.setIcon(QIcon(database_new))
        self.cmdProfileNew.setIcon(QIcon(profile_new))
        self.cmdProfileUpdate.setIcon(QIcon(profile_update))
        self.cmdProfileDelete.setIcon(QIcon(profile_delete))

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
        self.settings.setValue(self.settingsSection+"/language", self.languages.selected.id)
        self.languages.cambiar(self.languages.selected.id, self.module)
        self.retranslateUi(self)
        
        
    @pyqtSlot(str)
    def on_cmbProfiles_currentTextChanged(self, stri):
        self.txtDB.setText(self.settings.value(self.settingsSection +"_profile_" + self.cmbProfiles.currentText() + "/db", "xulpymoney"))
        self.txtPort.setText(self.settings.value(self.settingsSection +"_profile_" + self.cmbProfiles.currentText() + "/port", "5432"))
        self.txtUser.setText(self.settings.value(self.settingsSection +"_profile_" + self.cmbProfiles.currentText() + "/user", "postgres"))
        self.txtServer.setText(self.settings.value(self.settingsSection +"_profile_" + self.cmbProfiles.currentText() + "/server", "127.0.0.1"))


    def __save_current_profile(self):
        if self.cmbProfiles.currentText()=="":
            self.settings.setValue(self.settingsSection + "/db", self.txtDB.text() )
            self.settings.setValue(self.settingsSection +"/port",  self.txtPort.text())
            self.settings.setValue(self.settingsSection +"/user" ,  self.txtUser.text())
            self.settings.setValue(self.settingsSection +"/server", self.txtServer.text())   
            self.settings.setValue(self.settingsSection +"/language", self.cmbLanguages.itemData(self.cmbLanguages.currentIndex()))
            self.settings.setValue(self.settingsSection + "/current_profile", "")
        else:
            self.settings.setValue(self.settingsSection +"_profile_" + self.cmbProfiles.currentText() + "/db", self.txtDB.text() )
            self.settings.setValue(self.settingsSection +"_profile_" + self.cmbProfiles.currentText() +"/port",  self.txtPort.text())
            self.settings.setValue(self.settingsSection +"_profile_" + self.cmbProfiles.currentText() +"/user" ,  self.txtUser.text())
            self.settings.setValue(self.settingsSection +"_profile_" + self.cmbProfiles.currentText() +"/server", self.txtServer.text())   
            self.settings.setValue(self.settingsSection +"_profile_" + self.cmbProfiles.currentText() +"/language", self.cmbLanguages.itemData(self.cmbLanguages.currentIndex()))
            self.settings.setValue(self.settingsSection + "/current_profile", self.cmbProfiles.currentText())
        self.settings.sync()

    @pyqtSlot() 
    def on_cmdYN_accepted(self):
        self.__save_current_profile()
        self.con.init__create(self.txtUser.text(), self.txtPass.text(), self.txtServer.text(), self.txtPort.text(), self.txtDB.text())
        self.con.connect()
        if self.con.is_active():
            self.accept()
        else:
            qmessagebox(self.tr("Error conecting to {} database in {} server").format(self.con.db, self.con.server))

    @pyqtSlot() 
    def on_cmdYN_rejected(self):
        self.reject()
        
        
    def on_cmdProfileNew_released(self):
        name=qinputbox_string(self.tr("Profile name"))
        self.cmbProfiles.addItem(name)
        self.settings.setValue(self.settingsSection +"/db", self.txtDB.text() )
        
    def on_cmdProfileUpdate_released(self):
        before=self.cmbProfiles.currentText()
        after=qinputbox_string(self.tr("Profile name"))
        self.cmbProfiles.setItemText( self.cmbProfiles.currentIndex(),  after)
        self.settings.remove(self.settingsSection+"_profile_" + before)
        self.__save_current_profile()

    def on_cmdProfileDelete_released(self):
        self.settings.remove(self.settingsSection+"_profile_" + self.cmbProfiles.currentText())
        self.settings.setValue(self.settingsSection + "/current_profile", "")
        self.cmbProfiles_update()        
        
    ## @return List of string with profile names
    def __list_of_profiles(self):  
        r=[]
        for group in self.settings.childGroups():
            if group.startswith(self.settingsSection+"_profile_"):
                r.append(group.replace(self.settingsSection+"_profile_", ""))
        print(r)
        return r

    def cmbProfiles_update(self, selected=None):
        profiles=self.__list_of_profiles()
        self.cmbProfiles.blockSignals(True)
        self.cmbProfiles.clear()
        for profile in profiles:
            self.cmbProfiles.addItem(profile)

        #Force without signals to be in -1. There were problems when 0 is selected, becouse it didn't emit anything
        self.cmbProfiles.setCurrentIndex(-1)
        if selected is None:
            self.cmbProfiles.blockSignals(False)
        else:
            self.cmbProfiles.blockSignals(False)
            self.cmbProfiles.setCurrentIndex(self.cmbProfiles.findData(selected.id))

    def on_cmdDatabaseNew_released(self):
        respuesta = QMessageBox.warning(self, self.windowTitle(), self.tr("Do you want to create {} database in {}?".format(self.txtDB.text(), self.cmbLanguages.currentText())), QMessageBox.Ok | QMessageBox.Cancel)
        if respuesta==QMessageBox.Ok:
            admin_pg=AdminPG(self.txtUser.text(), self.txtPass.text(),  self.txtServer.text(),  self.txtPort.text())
                           
            if admin_pg.db_exists(self.txtDB.text())==True:
                qmessagebox(self.tr("Xulpymoney database already exists"))
                return 

            if admin_pg.create_db(self.txtDB.text())==False:
                qmessagebox(self.newdb.error)
            else:
                self.__save_current_profile()
                self.con=admin_pg.connect_to_database(self.txtDB.text(),connectionqt=True)
                if self.con.is_active():
                    self.databaseCreated.emit(self.con)
                    self.accept()
                else:
                    qmessagebox(self.tr("Error conecting to {} database in {} server, after creating database").format(self.con.db, self.con.server))


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    print("This script uses xulpymoney resources for the example")
    from importlib import import_module #To avoid putting xulpymoney dependenci
    import_module("xulpymoney.images.xulpymoney_rc")
    app = QApplication([])
    w=frmAccess("xulpymoney", "frmAccessExample")
    w.setLabel("Probe conection")
    w.exec_()
