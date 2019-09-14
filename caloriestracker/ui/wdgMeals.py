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
        self.tblMeals.settings(self.mem, "wdgMeals")
        self.on_calendar_selectionChanged()
        
    def on_calendar_selectionChanged(self):
        del self.meals
        self.meals=MealManager(self.mem, self.mem.con.mogrify("select * from meals where users_id=%s and datetime::date=%s order by datetime", (self.mem.user.id, self.calendar.selectedDate().toPyDate() )))
        self.meals.qtablewidget(self.tblMeals)
        
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
    def on_actionMealEdit_triggered(self):
        from caloriestracker.ui.frmMealsAdd import frmMealsAdd
        w=frmMealsAdd(self.mem, self.meals.selected, self)
        w.exec_()
        self.on_calendar_selectionChanged()

    def on_tblMeals_itemSelectionChanged(self):
        self.meals.cleanSelection()
        for i in self.tblMeals.selectedItems():
            if i.column()==0 and i.row()<self.meals.length():#only once per row
                self.meals.selected=self.meals.arr[i.row()]
        debug("Selected meal: {}".format(self.meals.selected))

    def on_tblMeals_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionMealNew)
        menu.addAction(self.actionMealDelete)
        menu.addAction(self.actionMealEdit)
        menu.addSeparator()
        
        if self.meals.selected==None:
            self.actionMealDelete.setEnabled(False)
            self.actionMealEdit.setEnabled(False)
        else:
            self.actionMealDelete.setEnabled(True)
            self.actionMealEdit.setEnabled(True)

        menu.exec_(self.tblMeals.mapToGlobal(pos))
