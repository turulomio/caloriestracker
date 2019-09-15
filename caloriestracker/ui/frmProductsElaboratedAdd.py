from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmProductsElaboratedAdd import Ui_frmProductsElaboratedAdd
from caloriestracker.libcaloriestracker import ProductPersonal

class frmProductsElaboratedAdd(QDialog, Ui_frmProductsElaboratedAdd):
    def __init__(self, mem, elaboratedproduct=None, parent=None, ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.elaboratedproduct=elaboratedproduct
        if self.elaboratedproduct==None:
            self.lbl.setText(self.tr("Add a new personal and elaborated product"))
        else:
            self.txtName.setText(self.elaborated.name)
            self.spnFinalAmount.setValue(self.elaborated.amount)
            self.lbl.setText(self.tr("Edit a personal and elaborated product"))

    def on_bb_accepted(self):
        if self.product==None:        
            self.product=ProductPersonal(
            self.mem, 
            self.txtName.text(), 
            None)
            self.mem.data.products.append(self.product)
            self.mem.data.products.order_by_name()
        else:
            self.product.name=self.txtName.text()
            self.product.amount=self.spnAmount.value()

        self.product.save()
        self.mem.con.commit()
        self.accept()

    def on_bb_rejected(self):
        self.reject()  


