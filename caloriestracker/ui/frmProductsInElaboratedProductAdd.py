from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmProductsInElaboratedProductAdd import Ui_frmProductsInElaboratedProductAdd
from caloriestracker.libcaloriestracker import ProductInElaboratedProduct

class frmProductsInElaboratedProductAdd(QDialog, Ui_frmProductsInElaboratedProductAdd):
    def __init__(self, mem, elaboratedproduct,  productinelaboratedproduct=None, parent=None, ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.elaboratedproduct=elaboratedproduct
        self.productinelaboratedproduct=productinelaboratedproduct
        if self.productinelaboratedproduct==None:
            self.mem.data.products.qcombobox(self.cmbProducts)
            self.cmbProducts.setCurrentIndex(-1)
        else:
            self.mem.data.products.qcombobox(self.cmbProducts, self.productinelaboratedproduct.product)
            self.spnAmount.setValue(self.productinelaboratedproduct.amount)

    def on_bb_accepted(self):
        product=self.mem.data.products.find_by_string_id(self.cmbProducts.itemData(self.cmbProducts.currentIndex()))
        if self.productinelaboratedproduct==None:
            self.productinelaboratedproduct=ProductInElaboratedProduct(  self.mem, 
                    product, 
                    product.system_product, 
                    self.spnAmount.value(), 
                    self.elaboratedproduct, 
                    None)
        else:
            self.productinelaboratedproduct.product=product
            self.productinelaboratedproduct.amount=self.spnAmount.value()
            self.productinelaboratedproduct.system_product=product.system_product
        self.elaboratedproduct.products_in.append(self.productinelaboratedproduct)
        self.productinelaboratedproduct.save()
        self.mem.con.commit()
        self.accept()

    def on_bb_rejected(self):
        self.reject()  
        self.reject()  


    @pyqtSlot(int)
    def on_cmbProducts_currentIndexChanged(self, index):
        product=self.mem.data.products.find_by_string_id(self.cmbProducts.itemData(self.cmbProducts.currentIndex()))
        if product!=None:
            product.needStatus(1)
            product.formats.qcombobox(self.cmbFormats, needtoselect=True)
            
    @pyqtSlot(int)
    def on_cmbFormats_currentIndexChanged(self, index):
        product=self.mem.data.products.find_by_string_id(self.cmbProducts.itemData(self.cmbProducts.currentIndex()))
        format=product.formats.find_by_id(self.cmbFormats.itemData(self.cmbFormats.currentIndex()))
        if format!=None:
            self.spnAmount.setValue(format.amount)
