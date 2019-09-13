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

    access=frmAccess(mem)
    access.setLabel(mem.tr("Please login to the caloriestracker database"))
    access.config_load()
    access.exec_()

    if access.result()==QDialog.Accepted:
        mem.con=access.con

        mem.frmMain = frmMain(mem)
        mem.frmMain.show()
        exit(mem.app.exec_())

if __name__=="__main__":
        main()
