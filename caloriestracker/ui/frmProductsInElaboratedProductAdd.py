from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmProductsInElaboratedProductAdd import Ui_frmProductsInElaboratedProductAdd
from caloriestracker.libcaloriestracker import ProductInElaboratedProduct
from caloriestracker.ui.myqwidgets import qmessagebox

class frmProductsInElaboratedProductAdd(QDialog, Ui_frmProductsInElaboratedProductAdd):
    def __init__(self, mem, elaboratedproduct,  productinelaboratedproduct=None, parent=None, ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.elaboratedproduct=elaboratedproduct
        self.productinelaboratedproduct=productinelaboratedproduct
        if self.productinelaboratedproduct==None:
            self.lbl.setText(self.tr("Add a product in the elaborated meal"))
            self.mem.data.products.qcombobox(self.cmbProducts)
            self.cmbProducts.setCurrentIndex(-1)
            self.product=None
        else:
            self.lbl.setText(self.tr("Edit a product in the elaborated meal"))
            self.mem.data.products.qcombobox(self.cmbProducts, self.productinelaboratedproduct.product)
            self.spnAmount.setValue(self.productinelaboratedproduct.amount)
            self.product=self.productinelaboratedproduct.product

    def on_bb_accepted(self):
        if self.product==None:
            qmessagebox(self.tr("You must select a product from the popup list"))
            return
        if self.productinelaboratedproduct==None:
            self.productinelaboratedproduct=ProductInElaboratedProduct(  self.mem, 
                    self.product, 
                    self.product.system_product, 
                    self.spnAmount.value(), 
                    self.elaboratedproduct, 
                    None)   
            self.elaboratedproduct.products_in.append(self.productinelaboratedproduct)
        else:
            self.productinelaboratedproduct.product=self.product
            self.productinelaboratedproduct.amount=self.spnAmount.value()
            self.productinelaboratedproduct.system_product=self.product.system_product
        self.productinelaboratedproduct.save()
        self.mem.con.commit()
        self.accept()

    def on_bb_rejected(self):
        self.reject()

    @pyqtSlot(str)
    def on_cmbProducts_currentTextChanged(self, text):
        index=self.cmbProducts.findText(text)
        if index==-1:
            self.product=None
            self.cmbFormats.clear()
        else:
            self.product=self.mem.data.products.find_by_string_id(self.cmbProducts.itemData(index))
            self.product.needStatus(1)
            self.product.formats.qcombobox(self.cmbFormats, None, needtoselect=True)

            
    @pyqtSlot(int)
    def on_cmbFormats_currentIndexChanged(self, index):
        if self.product!=None:
            format=self.product.formats.find_by_string_id(self.cmbFormats.itemData(index))
            if format!=None:
                self.spnAmount.setValue(float(format.amount))
