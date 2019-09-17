from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmProductsElaboratedAdd import Ui_frmProductsElaboratedAdd
from caloriestracker.libcaloriestracker import ProductElaborated, ProductsInElaboratedProduct

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
            self.txtName.setText(self.elaborated.name)
            self.spnFinalAmount.setValue(self.elaborated.amount)
            self.lbl.setText(self.tr("Edit a personal and elaborated product"))
            self.productsin=ProductsInElaboratedProduct(self.mem, self.elaboratedproduct, "select * from products_in_elaboratedproducts")
            self.productsin.qtablewidgetitem(self.tblProductsIn)
            

    def on_bb_accepted(self):
        if self.elaboratedproduct==None:        
            self.product=ProductElaborated(self.mem)
            self.product.name=self.txtName.text(), 
            self.product.final_amount=0
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


