from PyQt5.QtWidgets import QDialog, QWidget, QLineEdit, QCheckBox, QDialogButtonBox
from caloriestracker.ui.Ui_frmProductsAdd import Ui_frmProductsAdd
from caloriestracker.ui.myqwidgets import qmessagebox
from caloriestracker.objects.product import ProductPersonal, Product
from datetime import datetime

class frmProductsAdd(QDialog, Ui_frmProductsAdd):
    def __init__(self, mem, product, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.product=product
        self.parent=parent

        self.qlepAmount.setLabel(self.tr("Amount"))
        self.qlepFat.setLabel(self.tr("Fat"))
        self.qlepProtein.setLabel(self.tr("Protein"))
        self.qlepCarbohydrate.setLabel(self.tr("Carbohydrates"))
        self.qlepCalories.setLabel(self.tr("Calories"))
        self.qlepSalt.setLabel(self.tr("Salt"))
        self.qlepCholesterol.setLabel(self.tr("Cholesterol"))
        self.qlepSodium.setLabel(self.tr("Sodium"))
        self.qlepPotassium.setLabel(self.tr("Potassium"))
        self.qlepFiber.setLabel(self.tr("Fiber"))
        self.qlepSugar.setLabel(self.tr("Sugar"))
        self.qlepSaturatedFat.setLabel(self.tr("Saturated fat"))
        
        self.qlepAmount.setSuffix(self.tr("g"))
        self.qlepFat.setSuffix(self.tr("g"))
        self.qlepProtein.setSuffix(self.tr("g"))
        self.qlepCarbohydrate.setSuffix(self.tr("g"))
        self.qlepCalories.setSuffix(self.tr("g"))
        self.qlepSalt.setSuffix(self.tr("g"))
        self.qlepCholesterol.setSuffix(self.tr("mg"))
        self.qlepSodium.setSuffix(self.tr("mg"))
        self.qlepPotassium.setSuffix(self.tr("mg"))
        self.qlepFiber.setSuffix(self.tr("g"))
        self.qlepSugar.setSuffix(self.tr("g"))
        self.qlepSaturatedFat.setSuffix(self.tr("g"))
        
        if self.product==None:
            self.__insert=True
            self.mem.data.companies.qcombobox(self.cmbCompanies)
            self.cmbCompanies.setCurrentIndex(-1)
            self.mem.data.foodtypes.qcombobox(self.cmbFoodtypes)
            self.cmbFoodtypes.setCurrentIndex(-1)
            self.lbl.setText(self.tr("Add a new personal product"))
            self.qlepAmount.setValue(100)
            self.cmbsAdditives.setManagers(self.mem.settings, "frmProductsAdd", "cmbsAdditives", self.mem.data.additives, None)
        else:
            self.__insert=False
            self.mem.data.companies.qcombobox(self.cmbCompanies, self.product.company)
            self.mem.data.foodtypes.qcombobox(self.cmbFoodtypes, self.product.foodtype)
            if self.product.company==None:
                self.cmbCompanies.setCurrentIndex(-1)
            if self.product.foodtype==None:
                self.cmbFoodtypes.setCurrentIndex(-1)
            self.txtName.setText(self.product.name)
            self.qlepAmount.setValue(self.product.amount)
            self.qlepFat.setValue(self.product.fat)
            self.qlepProtein.setValue(self.product.protein)
            self.qlepCarbohydrate.setValue(self.product.carbohydrate)
            self.qlepCalories.setValue(self.product.calories)
            self.qlepSalt.setValue(self.product.salt)
            self.qlepCholesterol.setValue(self.product.cholesterol)
            self.qlepSodium.setValue(self.product.sodium)
            self.qlepPotassium.setValue(self.product.potassium)
            self.qlepFiber.setValue(self.product.fiber)
            self.qlepSugar.setValue(self.product.sugars)
            self.qlepSaturatedFat.setValue(self.product.saturated_fat)            
            self.lbl.setText(self.tr("Edit a personal product"))
            self.cmbsAdditives.setManagers(self.mem.settings, "frmProductsAdd", "cmbsAdditives", self.mem.data.additives, self.product.additives)
        self.qlepAmount.setMandatory(True)
        self.qlepCalories.setMandatory(True)
        self.qlepCarbohydrate.setMandatory(True)
        self.qlepProtein.setMandatory(True)
        self.qlepFat.setMandatory(True)
        self.qlepCalories.txt.setFocus()
        
        
    def setReadOnly(self):
        self.lbl.setText(self.tr("Product information"))
        qmessagebox(
            self.tr("This is a system product so you can't edit it.") + "\n" +
            self.tr("Please, if it's something wrong with it, you can create an issue at") + "\n" + 
            "https://github.com/turulomio/caloriestracker/issues"+ "\n" +
            self.tr("I'll fix it as soon as posible. ;)")
        )
        for widget in self.findChildren(QWidget):
            if widget.__class__==QLineEdit:
                widget.setReadOnly(True)
            elif widget.__class__==QCheckBox:
                widget.setEnabled(False)
            widget.blockSignals(True)
        self.bb.button(QDialogButtonBox.Ok).setEnabled(False)
        self.bb.blockSignals(False)
        self.bb.button(QDialogButtonBox.Cancel).blockSignals(False)

    def on_bb_accepted(self):            
        if self.qlepAmount.value()<=0:
            qmessagebox(self.tr("Amount value must be greater than 0"), ":/caloriestracker/book.png")
            return
        
        cmb_index=self.cmbCompanies.findText(self.cmbCompanies.currentText())
        company=None if cmb_index==-1 else self.mem.data.companies.find_by_string_id(self.cmbCompanies.itemData(cmb_index))
        foodtype=None if self.cmbFoodtypes.currentIndex()==-1 else self.mem.data.foodtypes.find_by_id(self.cmbFoodtypes.itemData(self.cmbFoodtypes.currentIndex()))
        if foodtype==None:
            qmessagebox(self.tr("You neet to set a food type"),  ":/caloriestracker/book.png")
            return
        system_company=None if company==None else company.system_company
        if self.product==None:        
            if self.mem.isProductsMaintainerMode(): 
                productclass=Product
            else:
                productclass=ProductPersonal
            self.product=productclass(
            self.mem, 
            self.txtName.text(), 
            self.qlepAmount.value(), 
            self.qlepFat.value(), 
            self.qlepProtein.value(), 
            self.qlepCarbohydrate.value(), 
            company, 
            datetime.now(), 
            None, 
            None, 
            self.qlepCalories.value(), 
            self.qlepSalt.value(), 
            self.qlepCholesterol.value(), 
            self.qlepSodium.value(), 
            self.qlepPotassium.value(), 
            self.qlepFiber.value(), 
            self.qlepSugar.value(), 
            self.qlepSaturatedFat.value(), 
            system_company, 
            foodtype, 
            self.cmbsAdditives.selected(), 
            None)
        else:
            self.product.name=self.txtName.text()
            self.product.amount=self.qlepAmount.value()
            self.product.fat=self.qlepFat.value()
            self.product.protein=self.qlepProtein.value()
            self.product.carbohydrate=self.qlepCarbohydrate.value()
            self.product.company=company
            self.product.calories=self.qlepCalories.value()
            self.product.salt=self.qlepSalt.value()
            self.product.cholesterol=self.qlepCholesterol.value()
            self.product.sodium=self.qlepSodium.value()
            self.product.potassium=self.qlepPotassium.value()
            self.product.fiber=self.qlepFiber.value()
            self.product.sugars=self.qlepSugar.value()
            self.product.saturated_fat=self.qlepSaturatedFat.value()
            self.product.system_company=system_company
            self.product.foodtype=foodtype
            self.product.additives=self.cmbsAdditives.selected()
        self.product.save()
        if self.mem.isProductsMaintainerMode():
            if self.__insert==True:
                self.parent.products.append(self.product) #Manager of the parent widget
                self.mem.data.products.append(self.product) #Manager of the singleton
                self.mem.insertProducts.append(self.product)
            else:
                self.mem.updateProducts.append(self.product)
            self.mem.data.products.order_by_name()
        else:#Not maintainer mode
            if self.__insert==True:
                self.parent.products.append(self.product) #Manager of the parent widget
                self.mem.data.products.append(self.product) #Manager of the singleton
            self.mem.con.commit()
        self.accept()

    def on_bb_rejected(self):
        self.reject()  


