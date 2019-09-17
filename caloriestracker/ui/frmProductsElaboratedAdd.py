from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmProductsElaboratedAdd import Ui_frmProductsElaboratedAdd
from caloriestracker.libcaloriestracker import ProductElaborated

class frmProductsElaboratedAdd(QDialog, Ui_frmProductsElaboratedAdd):
    def __init__(self, mem, elaboratedproduct=None, parent=None, ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.elaboratedproduct=elaboratedproduct
        self.tblProductsIn.settings(self.mem, "frmProductsElaboratedAdd")
        if self.elaboratedproduct==None:
            self.lbl.setText(self.tr("Add a new personal and elaborated product"))
            self.spnFinalAmount.setEnabled(False)
            self.tblProductsIn.setEnabled(False)
        else:
            self.elaboratedproduct.load_products_in()
            self.txtName.setText(self.elaboratedproduct.name)
            self.spnFinalAmount.setValue(self.elaboratedproduct.final_amount)
            self.lbl.setText(self.tr("Edit a personal and elaborated product"))
            self.elaboratedproduct.products_in.qtablewidget(self.tblProductsIn)

    def on_bb_accepted(self):
        if self.elaboratedproduct==None:        
            self.elaboratedproduct=ProductElaborated(self.mem)
            self.elaboratedproduct.name=self.txtName.text(), 
            self.elaboratedproduct.final_amount=0
            self.mem.data.elaboratedproducts.append(self.elaboratedproduct)
            self.mem.data.elaboratedproducts.order_by_name()
        else:
            self.elaboratedproduct.name=self.txtName.text()
            self.elaboratedproduct.amount=self.spnAmount.value()

        self.elaboratedproduct.save()
        self.mem.con.commit()
        self.accept()

    def on_bb_rejected(self):
        self.reject()  


