## @namespace caloriestracker.caloriestracker
## @brief Main caloriestracker script.

from PyQt5.QtWidgets import  QDialog
from caloriestracker.mem import MemCaloriestracker
from caloriestracker.ui.frmAccess import frmAccess
from caloriestracker.ui.frmMain import frmMain
from sys import exit

def main():
    from PyQt5 import QtWebEngineWidgets # To avoid error must be imported before QCoreApplication
    dir(QtWebEngineWidgets)
    
    mem=MemCaloriestracker()
    mem.run()
    mem.access=frmAccess("frmAccess")
    mem.access.setResources(":/caloriestracker/books.png", ":/caloriestracker/meals.svg")
    mem.access.setLabel(mem.tr("Please login to the Calories Tracker database"))
    mem.access.exec_()
    

    if mem.access.result()==QDialog.Accepted:
        mem.con=mem.access.con
        mem.settings=mem.access.settings
        mem.setLocalzone()#Needs settings in mem

        mem.frmMain = frmMain(mem)
        mem.frmMain.show()
        exit(mem.app.exec_())

if __name__=="__main__":
        main()
