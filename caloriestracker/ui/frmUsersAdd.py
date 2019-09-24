from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmUsersAdd import Ui_frmUsersAdd
from caloriestracker.libcaloriestracker import User
from datetime import datetime, date

class frmUsersAdd(QDialog, Ui_frmUsersAdd):
    def __init__(self, mem, user=None, parent=None, ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.user=user
        self.resize(self.mem.settings.value("frmUsersAdd/qdialog", QSize(800, 600)))
        
        if self.user==None:
            self.lbl.setText(self.tr("Add a new user"))
            self.dtBirthday.setDate(date.today())
            
        else:
            self.lbl.setText(self.tr("Edit a user"))
            self.txtName.setText(self.user.name)
            self.dtBirthday.setDate(self.user.birthday)
            self.chkMale.setChecked(self.user.male)

    def on_bb_accepted(self):
        if self.user==None:
            self.user=User(self.mem, self.txtName.text(), self.chkMale.isChecked(), self.dtBirthday.date().toPyDate(), datetime.now(), None, None)
            self.mem.data.users.append(self.user)
        else:
            self.user.name=self.txtName.text()
            self.user.male=self.chkMale.isChecked()
            self.user.birthday=self.dtBirthday.date().toPyDate()
        self.user.save()
        self.mem.con.commit()
        self.mem.data.users.order_by_name()
        self.mem.settings.setValue("frmUsersAdd/qdialog", self.size())
        self.accept()

    def on_bb_rejected(self):
        self.mem.settings.setValue("frmUsersAdd/qdialog", self.size())
        self.reject()  


