from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmCompaniesAdd import Ui_frmCompaniesAdd
from caloriestracker.libcaloriestracker import CompanyPersonal
from datetime import datetime

class frmCompaniesAdd(QDialog, Ui_frmCompaniesAdd):
    def __init__(self, mem, company=None, parent=None, ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.company=company
        
        if self.company==None:
            self.lbl.setText(self.tr("Add a new company"))
        else:
            self.lbl.setText(self.tr("Edit a company"))
            self.txtName.setText(self.company.name)

    def on_bb_accepted(self):
        if self.company==None:
            self.company=CompanyPersonal(self.mem, self.txtName.text(),  datetime.now(), None)
        else:
            self.company.name=self.txtName.text()
        self.company.save()
        self.mem.data.companies.append(self.company)
        self.mem.data.companies.order_by_name()
        self.mem.con.commit()
        self.accept()
    def on_bb_rejected(self):
        self.reject()  


