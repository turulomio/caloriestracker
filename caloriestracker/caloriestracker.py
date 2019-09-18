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
    mem.frmAccess=frmAccess("caloriestracker","frmAccess")
    mem.frmAccess.setResources(":/caloriestracker/books.png", ":/caloriestracker/meals.svg")
    mem.frmAccess.setLabel(mem.tr("Please login to the Calories Tracker database"))
    mem.frmAccess.exec_()

    if mem.frmAccess.result()==QDialog.Accepted:
        mem.con=mem.frmAccess.con
        mem.settings=mem.frmAccess.settings
        mem.setLocalzone()#Needs settings in mem

        mem.frmMain = frmMain(mem)
        mem.frmMain.show()
        exit(mem.app.exec_())

if __name__=="__main__":
        main()
