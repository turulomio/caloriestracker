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
        self.meals.clean()
        self.meals.init__from_db(self.mem.con.mogrify("select * from meals where datetime::date=%s", (self.calendar.selectedDate().toPyDate(), )))
        self.meals.qtablewidget(self.tblMeals)
