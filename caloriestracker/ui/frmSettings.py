from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmSettings import Ui_frmSettings
from caloriestracker.ui.wdgDatetime import wdgDatetime

class frmSettings(QDialog, Ui_frmSettings):
    def __init__(self, mem, parent = None, name = None, modal = False):
        QDialog.__init__(self, parent)
        if name:
            self.setObjectName(name)
        self.setModal(True)
        self.setupUi(self)
        self.mem=mem
        
        wdgDatetime.pytz_zones_qcombobox(self.cmbZones, self.mem.localzone)
        self.mem.frmAccess.languages.qcombobox(self.cmbLanguages,self.mem.frmAccess.languages.selected)

 
    @pyqtSlot()
    def on_buttonbox_accepted(self):
        self.mem.localzone=self.cmbZones.itemData(self.cmbZones.currentIndex())
        self.mem.settings.setValue("access/language", self.mem.frmAccess.languages.selected.id)
        self.mem.settings.setValue("mem/localzone", self.mem.localzone)
        self.mem.frmAccess.languages.cambiar(self.cmbLanguages.itemData(self.cmbLanguages.currentIndex()), "caloriestracker")       
        self.retranslateUi(self)
        self.mem.frmMain.retranslateUi(self)
        self.mem.settings.sync()
        self.accept() 

    @pyqtSlot()
    def on_buttonbox_rejected(self):
        self.reject()
        

    @pyqtSlot(str)      
    def on_cmbLanguages_currentIndexChanged(self, stri):
        self.mem.frmAccess.languages.selected=self.mem.frmAccess.languages.find_by_id(self.cmbLanguages.itemData(self.cmbLanguages.currentIndex()))
        self.mem.frmAccess.languages.cambiar(self.mem.frmAccess.languages.selected.id, "caloriestracker")
        self.retranslateUi(self)
