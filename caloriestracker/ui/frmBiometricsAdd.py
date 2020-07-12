from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmBiometricsAdd import Ui_frmBiometricsAdd
from caloriestracker.ui.myqwidgets import qmessagebox
from caloriestracker.objects.biometrics import Biometrics
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
        elif self.mem.user.biometrics.last()==None:#No last_biometrics no data in database
            self.wdgDT.set(datetime.now(), self.mem.localzone)
            self.mem.data.activities.qcombobox(self.cmbActivity)
            self.mem.data.weightwishes.qcombobox(self.cmbWeightWish)
            self.lbl.setText(self.tr("Add a new biometrics information register"))        
        else:#Uses last data
            self.wdgDT.set(datetime.now(), self.mem.localzone)
            self.mem.data.activities.qcombobox(self.cmbActivity, self.mem.user.biometrics.last().activity)
            self.mem.data.weightwishes.qcombobox(self.cmbWeightWish, self.mem.user.biometrics.last().weightwish)
            self.spnHeight.setValue(self.mem.user.biometrics.last().height)
            self.spnWeight.setValue(self.mem.user.biometrics.last().weight)
            self.lbl.setText(self.tr("Add a new biometrics information register"))

    def on_bb_accepted(self):
        activity=self.mem.data.activities.find_by_id(self.cmbActivity.itemData(self.cmbActivity.currentIndex()))
        weightwish=self.mem.data.weightwishes.find_by_id(self.cmbWeightWish.itemData(self.cmbWeightWish.currentIndex()))
        
        if activity is None or weightwish is None:
            qmessagebox(self.tr("You must select an activity and a weight wish"))
            return

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
        self.biometric.save()
        self.mem.con.commit()
        self.mem.user.needStatus(1, downgrade_to=0)
        self.accept()

    def on_bb_rejected(self):
        self.reject()  


