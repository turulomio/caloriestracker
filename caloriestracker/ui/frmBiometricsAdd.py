from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmBiometricsAdd import Ui_frmBiometricsAdd
from caloriestracker.libcaloriestracker import Biometrics
from datetime import datetime

class frmBiometricsAdd(QDialog, Ui_frmBiometricsAdd):
    def __init__(self, mem, biometric=None, parent=None, ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.biometric=biometric
        self.wdgDT.show_microseconds(False)
        self.wdgDT.setLocalzone(self.mem.localzone)
        
        if self.biometric!=None:
            self.mem.data.activities.qcombobox(self.cmbActivity, self.biometric.activity)
            self.mem.data.weightwishes.qcombobox(self.cmbWeightWish, self.biometric.weightwish)
            self.wdgDT.set(self.biometric.datetime, self.mem.localzone)
            self.spnHeight.setValue(self.biometric.height)
            self.spnWeight.setValue(self.biometric.weight)
            self.lbl.setText(self.tr("Edit a biometrics information register"))
        elif self.mem.user.last_biometrics.datetime==None:#No last_biometrics no data in database
            self.wdgDT.set(datetime.now(), self.mem.localzone)
            self.mem.data.activities.qcombobox(self.cmbActivity)
            self.mem.data.weightwishes.qcombobox(self.cmbWeightWish)
            self.lbl.setText(self.tr("Add a new biometrics information register"))        
        else:#Uses last data
            self.wdgDT.set(datetime.now(), self.mem.localzone)
            self.mem.data.activities.qcombobox(self.cmbActivity, self.mem.user.last_biometrics.activity)
            self.mem.data.weightwishes.qcombobox(self.cmbWeightWish, self.mem.user.last_biometrics.weightwish)
            self.spnHeight.setValue(self.mem.user.last_biometrics.height)
            self.spnWeight.setValue(self.mem.user.last_biometrics.weight)
            self.lbl.setText(self.tr("Add a new biometrics information register"))

    def on_bb_accepted(self):
        activity=self.mem.data.activities.find_by_id(self.cmbActivity.itemData(self.cmbActivity.currentIndex()))
        weightwish=self.mem.data.weightwishes.find_by_id(self.cmbWeightWish.itemData(self.cmbWeightWish.currentIndex()))

        if self.biometric==None:        
            self.biometric=Biometrics(
                self.mem, 
                self.wdgDT.datetime(), 
                self.spnHeight.value(), 
                self.spnWeight.value(), 
                self.mem.user, 
                activity, 
                weightwish,
                None)
        else:
            self.biometric.datetime=self.wdgDT.datetime()
            self.biometric.height=self.spnHeight.value()
            self.biometric.weight=self.spnWeight.value()
            self.biometric.activity=activity
            self.biometric.weightwish=weightwish
        if self.biometric.datetime>self.mem.user.last_biometrics.datetime:
            self.mem.user.last_biometrics=self.biometric
        self.biometric.save()
        self.mem.con.commit()
        self.accept()

    def on_bb_rejected(self):
        self.reject()  


