from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmMealsAdd import Ui_frmMealsAdd
from caloriestracker.libcaloriestracker import Meal
from caloriestracker.ui.myqwidgets import qmessagebox
from datetime import datetime, date, timedelta

class frmMealsAdd(QDialog, Ui_frmMealsAdd):
    def __init__(self, mem, meal=None, parent=None ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.meal=meal
        self.parent=parent
        self.wdgDT.show_microseconds(False)
        self.wdgDT.setLocalzone(self.mem.localzone)
        
        if self.meal==None:
            self.lbl.setText(self.tr("Add a new meal"))
            self.mem.data.products.qcombobox(self.cmbProducts)
            self.cmbProducts.setCurrentIndex(-1)
            parent_calendar_date=self.parent.calendar.selectedDate().toPyDate()
            if parent_calendar_date==date.today():#Set parents calendar date if it's different to today
                self.wdgDT.set(datetime.now(), self.mem.localzone)
            else:
                last=self.parent.meals.last().datetime+timedelta(minutes=1) if self.parent.meals.length()>0 else datetime.combine(parent_calendar_date, datetime.now().time())
                self.wdgDT.set(datetime(parent_calendar_date.year, parent_calendar_date.month, parent_calendar_date.day, last.hour, last.minute, last.second), self.mem.localzone)
            self.product=None
        else:
            self.lbl.setText(self.tr("Edit a meal"))
            self.mem.data.products.qcombobox(self.cmbProducts, self.meal.product)
            self.wdgDT.set(self.meal.datetime, self.mem.localzone)
            self.spnAmount.setValue(self.meal.amount)
            self.product=self.meal.product

        for i in range(1, 25):
            self.cmbMult.addItem("x{}".format(i), i)


    @pyqtSlot(str)
    def on_cmbProducts_currentTextChanged(self, text):
        index=self.cmbProducts.findText(text)
        if index==-1:
            self.product=None
            self.cmbFormats.clear()
        else:
            self.product=self.mem.data.products.find_by_string_id(self.cmbProducts.itemData(index))
            self.product.needStatus(1)
            self.product.formats.qcombobox(self.cmbFormats, selected=None, needtoselect=True)
        self.cmbMult.setCurrentIndex(0)
            
    @pyqtSlot(int)
    def on_cmbFormats_currentIndexChanged(self, index):
        if self.product!=None:
            format=self.product.formats.find_by_string_id(self.cmbFormats.itemData(index))
            if format!=None:
                self.spnAmount.setValue(float(format.amount)*self.cmbMult.itemData(self.cmbMult.currentIndex()))
            
    @pyqtSlot(int)
    def on_cmbMult_currentIndexChanged(self, index):
        self.on_cmbFormats_currentIndexChanged(self.cmbFormats.currentIndex())

    def on_bb_accepted(self):
        if self.product==None:
            qmessagebox(self.tr("You must select a product from the popup list"))
            return
        if self.meal==None:
            self.meal=Meal(self.mem, self.wdgDT.datetime(), self.product, self.spnAmount.value(), self.mem.user, self.product.system_product, None)
        else:
            self.meal.datetime=self.wdgDT.datetime()
            self.meal.product=self.product
            self.meal.amount=self.spnAmount.value()
            self.meal.system_product=self.product.system_product
        self.meal.save()
        self.mem.con.commit()
        self.accept()

    def on_bb_rejected(self):
        self.reject()
