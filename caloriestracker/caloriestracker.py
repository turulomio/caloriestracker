## @namespace caloriestracker.caloriestracker
## @brief Main caloriestracker script.

from PyQt5.QtWidgets import  QDialog, qApp
from caloriestracker.mem import MemCaloriestracker
from caloriestracker.ui.frmAccess import frmAccess
from sys import exit
import caloriestracker.images.caloriestracker_rc #Images of frmAccess were not loaded without this

def on_database_created(connectionqt):
    from caloriestracker.database_update import database_update
    from caloriestracker.version import __versiondatetime__
    from caloriestracker.ui.myqwidgets import qmessagebox
    database_update(connectionqt, "caloriestracker", __versiondatetime__, "Console")
    connectionqt.commit()
    qmessagebox(qApp.translate("Mem", "Calories Tracker have been correctly installed. Please login again"))
    exit(qApp.exec_())

def main():
    from PyQt5 import QtWebEngineWidgets # To avoid error must be imported before QCoreApplication
    dir(QtWebEngineWidgets)
    
    mem=MemCaloriestracker()
    mem.run()
    mem.frmAccess=frmAccess("caloriestracker", "frmAccess")
    mem.frmAccess.setResources(":/caloriestracker/caloriestracker.png", ":/caloriestracker/caloriestracker.png")
    mem.frmAccess.databaseCreated.connect(on_database_created)
    mem.frmAccess.setLabel(mem.tr("Please login to the Calories Tracker database"))
    mem.frmAccess.exec_()

    if mem.frmAccess.result()==QDialog.Accepted:
        mem.con=mem.frmAccess.con
        print(mem.con)
        mem.settings=mem.frmAccess.settings
        mem.setLocalzone()#Needs settings in mem
        if mem.args.products_maintainer==True:
            from caloriestracker.ui.frmMainProductsMaintainer import frmMainProductsMaintainer
            mem.setProductsMaintainerMode(True)
            mem.frmAccess.languages.cambiar("en", "caloriestracker")
            mem.frmMain = frmMainProductsMaintainer(mem)
        else:
            from caloriestracker.ui.frmMain import frmMain
            mem.frmMain=frmMain(mem)
        mem.frmMain.show()
        exit(mem.app.exec_())

if __name__=="__main__":
        main()
