from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmSettings import Ui_frmSettings

class frmSettings(QDialog, Ui_frmSettings):
    def __init__(self, mem, parent = None, name = None, modal = False):
        QDialog.__init__(self, parent)
        if name:
            self.setObjectName(name)
        self.setModal(True)
        self.setupUi(self)
        self.mem=mem
        self.mem.languages.qcombobox(self.cmbLanguages,self.mem.language)
 
    @pyqtSlot()
    def on_buttonbox_accepted(self):
        self.mem.localcurrency=self.mem.currencies.find_by_id(self.cmbCurrencies.itemData(self.cmbCurrencies.currentIndex()))
        self.mem.localzone=self.mem.zones.find_by_id(self.cmbZones.itemData(self.cmbZones.currentIndex()))
        self.mem.settings.setValue("mem/language", self.mem.languages.selected.id)
        self.mem.settings.setValue("mem/localzone", self.mem.localzone)
        self.mem.languages.cambiar(self.cmbLanguages.itemData(self.cmbLanguages.currentIndex()))       
        self.retranslateUi(self)
        self.accept() 

    @pyqtSlot()
    def on_buttonbox_rejected(self):
        self.reject()
        

    @pyqtSlot(str)      
    def on_cmbLanguages_currentIndexChanged(self, stri):
        self.mem.languages.selected=self.mem.languages.find_by_id(self.cmbLanguages.itemData(self.cmbLanguages.currentIndex()))
        self.mem.languages.cambiar(self.mem.languages.selected.id)
        self.retranslateUi(self)
