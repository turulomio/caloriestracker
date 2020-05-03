from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QMenu, QMessageBox
from caloriestracker.datetime_functions import dtaware_day_end_from_date
from caloriestracker.objects.meal import MealManager
from caloriestracker.objects.mealtotal import MealTotalManager_all
from caloriestracker.ui.Ui_wdgMeals import Ui_wdgMeals

class wdgMeals(QWidget, Ui_wdgMeals):
    def __init__(self, mem,  arrInt=[],  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.meals=MealManager(self.mem)
        self.tblMeals.setSettings(self.mem.settings, "wdgMeals", "tblMeals")
        self.tblMeals.table.customContextMenuRequested.connect(self.on_tblMeals_customContextMenuRequested)
        
        self.wdgPieMeals.setSettings(self.mem.settings, "wdgMeals", "wdgPieMeals")
        self.wdgPieFoodtypes.setSettings(self.mem.settings, "wdgMeals", "wdgPieFoodtypes")
        self.wdgTS.setSettings(self.mem.settings, "wdgMeals", "wdgTS")
        self.wdgPieFulfillment.setSettings(self.mem.settings, "wdgMeals", "wdgPieFulfillment")
        
        self.tab.setCurrentIndex(0)
        
        self.on_calendar_selectionChanged()

    def on_calendar_selectionChanged(self):
        mealtotals=MealTotalManager_all(self.mem, self.mem.user)
        mealtotals.load_biometrics()
        del self.meals
        self.meals=MealManager(self.mem, self.mem.con.mogrify("select * from meals where users_id=%s and datetime::date=%s order by datetime", (self.mem.user.id, self.calendar.selectedDate().toPyDate() )))
        self.meals.myqtablewidget(self.tblMeals)
        self.tblMeals.setOrderBy(0, False)
        self.lblFound.setText(self.tr("{} registers found").format(self.meals.length()))
        
        self.wdgPieMeals.clear()
        self.wdgPieMeals.pie.setTitle(self.tr("Daily user meals"))
        for key, value in self.meals.dictionary_grouping_by_fullName().items():
            self.wdgPieMeals.pie.appendData(key, value)
        self.wdgPieMeals.display()

        self.wdgPieFoodtypes.clear()
        self.wdgPieFoodtypes.pie.setTitle(self.tr("Daily user meals food types"))
        for key, value in self.meals.dictionary_grouping_by_foodtype().items():
            self.wdgPieFoodtypes.pie.appendData(key, value)
        self.wdgPieFoodtypes.display()
        
        self.wdgTS.clear()    #Temporal series
        self.wdgTS.ts.setTitle(self.tr("Daily user calories evolution"))
        s_evolution=self.wdgTS.ts.appendTemporalSeries(self.tr("Daily evolution"))
        for o in mealtotals:
            self.wdgTS.ts.appendTemporalSeriesData(s_evolution, dtaware_day_end_from_date(o.date,  self.mem.localzone),  o.calories)
            
        s_recommended=self.wdgTS.ts.appendTemporalSeries(self.tr("Recommended calories"))
        for o in self.mem.user.biometrics:
            self.wdgTS.ts.appendTemporalSeriesData(s_recommended, dtaware_day_end_from_date(o.datetime.date(), self.mem.localzone), o.bmr())
        self.wdgTS.display()
        
        self.wdgPieFulfillment.clear()
        self.wdgPieFulfillment.pie.setTitle(self.tr("Daily user calories fulfillment"))

        for key, value in mealtotals.dictionary_of_fulfillment().items():
            self.wdgPieFulfillment.pie.appendData(key, value)
        self.wdgPieFulfillment.display()
        
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
            self.tblMeals.selected.delete()
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
        w=frmMealsAdd(self.mem, self.tblMeals.selected, self)
        w.exec_()
        self.on_calendar_selectionChanged()
        
    @pyqtSlot() 
    def on_actionProductEdit_triggered(self):
        if self.tblMeals.selected.product.system_product==True:
            from caloriestracker.ui.frmProductsAdd import frmProductsAdd
            w=frmProductsAdd(self.mem, self.tblMeals.selected.product, self)
            w.setReadOnly()
            w.exec_()
        elif self.tblMeals.selected.product.system_product==False:
            if self.tblMeals.selected.product.elaboratedproducts_id==None:
                from caloriestracker.ui.frmProductsAdd import frmProductsAdd
                w=frmProductsAdd(self.mem, self.tblMeals.selected.product, self)
                w.exec_()
            else:#Elaborated product
                from caloriestracker.ui.frmProductsElaboratedAdd import frmProductsElaboratedAdd
                elaborated=self.mem.data.elaboratedproducts.find_by_id(self.tblMeals.selected.product.elaboratedproducts_id)
                w=frmProductsElaboratedAdd(self.mem, elaborated, self)
                w.exec_()
            self.on_calendar_selectionChanged()

    def on_tblMeals_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionMealNew)
        menu.addAction(self.actionMealDelete)
        menu.addAction(self.actionMealEdit)
        menu.addSeparator()
        menu.addAction(self.actionMealDeleteDay)
        menu.addSeparator()
        menu.addAction(self.actionProductEdit)
        menu.addSeparator()
        menu.addMenu(self.tblMeals.qmenu())
        
        if self.meals.length()>0:
            self.actionMealDeleteDay.setEnabled(True)
        else:
            self.actionMealDeleteDay.setEnabled(False)
        
        if self.tblMeals.selected==None:
            self.actionMealDelete.setEnabled(False)
            self.actionMealEdit.setEnabled(False)
            self.actionProductEdit.setEnabled(False)
        else:
            self.actionMealDelete.setEnabled(True)
            self.actionMealEdit.setEnabled(True)
            self.actionProductEdit.setEnabled(True)

        menu.exec_(self.tblMeals.table.mapToGlobal(pos))
