from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmMealsAdd import Ui_frmMealsAdd
from caloriestracker.libcaloriestracker import Meal
from datetime import datetime

class frmMealsAdd(QDialog, Ui_frmMealsAdd):
    def __init__(self, mem, meal=None, parent=None, ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.meal=meal
        self.wdgDT.show_microseconds(False)
        self.wdgDT.setLocalzone(self.mem.localzone)
        if self.meal==None:
            self.mem.data.products.qcombobox(self.cmbProducts)
            self.cmbProducts.setCurrentIndex(-1)
            self.wdgDT.set(datetime.now(), self.mem.localzone)
        else:
            self.mem.data.products.qcombobox(self.cmbProducts, self.meal.product)
            self.wdgDT.set(self.meal.datetime, self.mem.localzone)
            self.spnAmount.setValue(self.meal.amount)

    def on_bb_accepted(self):
        product=self.mem.data.products.find_by_string_id(self.cmbProducts.itemData(self.cmbProducts.currentIndex()))
        if self.meal==None:
            self.meal=Meal(self.mem, self.wdgDT.datetime(), product, self.spnAmount.value(), self.mem.user, product.system_product, None)
        else:
            self.meal.datetime=self.wdgDT.datetime()
            self.meal.product=product
            self.meal.amount=self.spnAmount.value()
            self.meal.system_product=product.system_product
        self.meal.save()
        self.mem.con.commit()
        self.accept()

    def on_bb_rejected(self):
        self.reject()
