from PyQt5.QtWidgets import QWidget
from caloriestracker.libcaloriestracker import MealManager
from caloriestracker.ui.Ui_wdgMeals import Ui_wdgMeals

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
