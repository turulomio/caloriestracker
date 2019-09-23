from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmProductsAdd import Ui_frmProductsAdd
from caloriestracker.libcaloriestracker import ProductPersonal
from datetime import datetime

class frmProductsAdd(QDialog, Ui_frmProductsAdd):
    def __init__(self, mem, product=None, parent=None, ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.product=product
        if self.product==None:
            self.mem.data.companies.qcombobox(self.cmbCompanies)
            self.cmbCompanies.setCurrentIndex(-1)
            self.lbl.setText(self.tr("Add a new personal product"))
        else:
            self.mem.data.companies.qcombobox(self.cmbCompanies, self.product.company)
            if self.product.company==None:
                self.cmbCompanies.setCurrentIndex(-1)
            self.txtName.setText(self.product.name)
            self.spnAmount.setValue(self.product.amount)
            self.spnFat.setValue(self.product.fat)
            self.spnProtein.setValue(self.product.protein)
            self.spnCarbohydrate.setValue(self.product.carbohydrate)
            self.spnCalories.setValue(self.product.calories)
            self.spnSalt.setValue(self.product.salt)
            self.spnCholesterol.setValue(self.product.cholesterol)
            self.spnSodium.setValue(self.product.sodium)
            self.spnPotassium.setValue(self.product.potassium)
            self.spnFiber.setValue(self.product.fiber)
            self.spnSugar.setValue(self.product.sugars)
            self.spnSaturatedFat.setValue(self.product.saturated_fat)            
            self.lbl.setText(self.tr("Edit a personal product"))

    def on_bb_accepted(self):
        cmb_index=self.cmbCompanies.findText(self.cmbCompanies.currentText())
        company=None if cmb_index==-1 else self.mem.data.companies.find_by_string_id(self.cmbCompanies.itemData(cmb_index))
        system_company=None if company==None else company.system_company
        if self.product==None:        
            self.product=ProductPersonal(
            self.mem, 
            self.txtName.text(), 
            self.spnAmount.value(), 
            self.spnFat.value(), 
            self.spnProtein.value(), 
            self.spnCarbohydrate.value(), 
            company, 
            datetime.now(), 
            None, 
            None, 
            self.spnCalories.value(), 
            self.spnSalt.value(), 
            self.spnCholesterol.value(), 
            self.spnSodium.value(), 
            self.spnPotassium.value(), 
            self.spnFiber.value(), 
            self.spnSugar.value(), 
            self.spnSaturatedFat.value(), 
            system_company, 
            None)
            self.mem.data.products.append(self.product)
            self.mem.data.products.order_by_name()
        else:
            self.product.name=self.txtName.text()
            self.product.amount=self.spnAmount.value()
            self.product.fat=self.spnFat.value()
            self.product.protein=self.spnProtein.value()
            self.product.carbohydrate=self.spnCarbohydrate.value()
            self.product.company=company
            self.product.calories=self.spnCalories.value()
            self.product.salt=self.spnSalt.value()
            self.product.cholesterol=self.spnCholesterol.value()
            self.product.sodium=self.spnSodium.value()
            self.product.potassium=self.spnPotassium.value()
            self.product.fiber=self.spnFiber.value()
            self.product.sugars=self.spnSugar.value()
            self.product.saturated_fat=self.spnSaturatedFat.value()
            self.product.system_company=system_company
        self.product.save()
        self.mem.con.commit()
        self.accept()

    def on_bb_rejected(self):
        self.reject()  


