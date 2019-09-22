from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmUsersAdd import Ui_frmUsersAdd
from caloriestracker.libcaloriestracker import CompanyPersonal
from datetime import datetime

class frmUsersAdd(QDialog, Ui_frmUsersAdd):
    def __init__(self, mem, user=None, parent=None, ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.user=user
        
        if self.user==None:
            self.lbl.setText(self.tr("Add a new user"))
        else:
            self.lbl.setText(self.tr("Edit a user"))
            self.txtName.setText(self.user.name)

    def on_bb_accepted(self):
        if self.user==None:
            self.user=CompanyPersonal(self.mem, self.txtName.text(),  datetime.now(), None, None)
        else:
            self.user.name=self.txtName.text()
        self.user.save()
        self.mem.data.companies.append(self.user)
        self.mem.data.companies.order_by_name()
        self.mem.con.commit()
        self.accept()
    def on_bb_rejected(self):
        self.reject()  


