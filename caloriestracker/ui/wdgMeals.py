from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QMenu, QMessageBox
from caloriestracker.libcaloriestracker import MealManager
from caloriestracker.ui.Ui_wdgMeals import Ui_wdgMeals
from logging import debug

class wdgMeals(QWidget, Ui_wdgMeals):
    def __init__(self, mem,  arrInt=[],  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.meals=MealManager(self.mem)
        self.tblMeals.settings(self.mem.settings, "wdgMeals", "tblMeals")
        self.tblMeals.table.customContextMenuRequested.connect(self.on_tblMeals_customContextMenuRequested)
        self.tblMeals.table.itemSelectionChanged.connect(self.on_tblMeals_itemSelectionChanged)
        self.on_calendar_selectionChanged()
        
    def on_calendar_selectionChanged(self):
        del self.meals
        self.meals=MealManager(self.mem, self.mem.con.mogrify("select * from meals where users_id=%s and datetime::date=%s order by datetime", (self.mem.user.id, self.calendar.selectedDate().toPyDate() )))
        self.meals.myqtablewidget(self.tblMeals)
        self.lblFound.setText(self.tr("{} registers found").format(self.meals.length()))
        
    @pyqtSlot()
    def on_actionMealNew_triggered(self):
        from caloriestracker.ui.frmMealsAdd import frmMealsAdd
        w=frmMealsAdd(self.mem, None, self)
        w.exec_()
        self.on_calendar_selectionChanged()

    @pyqtSlot()
    def on_actionMealDelete_triggered(self):
        reply = QMessageBox.question(None, self.tr('Asking your confirmation'), self.tr("This action can't be undone.\nDo you want to delete this record?"), QMessageBox.Yes, QMessageBox.No)                  
        if reply==QMessageBox.Yes:
            self.meals.selected.delete()
            self.mem.con.commit()
            self.on_calendar_selectionChanged()
            
    @pyqtSlot()
    def on_actionMealDeleteDay_triggered(self):
        reply = QMessageBox.question(None, self.tr('Asking your confirmation'), self.tr("This action can't be undone.\nDo you want to delete all meals from selected day?"), QMessageBox.Yes, QMessageBox.No)                  
        if reply==QMessageBox.Yes:
            for meal in self.meals.arr:
                meal.delete()
            self.mem.con.commit()
            self.on_calendar_selectionChanged()

    @pyqtSlot()
    def on_actionMealEdit_triggered(self):
        from caloriestracker.ui.frmMealsAdd import frmMealsAdd
        w=frmMealsAdd(self.mem, self.meals.selected, self)
        w.exec_()
        self.on_calendar_selectionChanged()
        
    @pyqtSlot() 
    def on_actionProductEdit_triggered(self):
        if self.meals.selected.product.system_product==True:
            from caloriestracker.ui.frmProductsAdd import frmProductsAdd
            w=frmProductsAdd(self.mem, self.meals.selected.product, self)
            w.setReadOnly()
            w.exec_()
        elif self.meals.selected.product.system_product==False:
            if self.meals.selected.product.elaboratedproducts_id==None:
                from caloriestracker.ui.frmProductsAdd import frmProductsAdd
                w=frmProductsAdd(self.mem, self.meals.selected.product, self)
                w.exec_()
            else:#Elaborated product
                from caloriestracker.ui.frmProductsElaboratedAdd import frmProductsElaboratedAdd
                elaborated=self.mem.data.elaboratedproducts.find_by_id(self.meals.selected.product.elaboratedproducts_id)
                w=frmProductsElaboratedAdd(self.mem, elaborated, self)
                w.exec_()
            self.on_calendar_selectionChanged()

    def on_tblMeals_itemSelectionChanged(self):
        self.meals.cleanSelection()
        for i in self.tblMeals.table.selectedItems():
            if i.column()==0 and i.row()<self.meals.length():#only once per row
                self.meals.selected=self.meals.arr[i.row()]
        debug("Selected meal: {}".format(self.meals.selected))

    def on_tblMeals_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionMealNew)
        menu.addAction(self.actionMealDelete)
        menu.addAction(self.actionMealEdit)
        menu.addSeparator()
        menu.addAction(self.actionMealDeleteDay)
        menu.addSeparator()
        menu.addAction(self.actionProductEdit)
        
        if self.meals.length()>0:
            self.actionMealDeleteDay.setEnabled(True)
        else:
            self.actionMealDeleteDay.setEnabled(False)
        
        if self.meals.selected==None:
            self.actionMealDelete.setEnabled(False)
            self.actionMealEdit.setEnabled(False)
            self.actionProductEdit.setEnabled(False)
        else:
            self.actionMealDelete.setEnabled(True)
            self.actionMealEdit.setEnabled(True)
            self.actionProductEdit.setEnabled(True)

        menu.exec_(self.tblMeals.table.mapToGlobal(pos))
