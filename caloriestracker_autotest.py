from PyQt5.QtWidgets import  QDialog
from caloriestracker.ui.frmAccess import frmAccess
from caloriestracker.mem import MemCaloriestracker
import caloriestracker.images.caloriestracker_rc #Images of frmAccess were not loaded without this

from os import system, environ

from PyQt5 import QtWebEngineWidgets # To avoid error must be imported before QCoreApplication
dir(QtWebEngineWidgets)
print ("This script needs PGPASSWORD to be set")

password=environ['PGPASSWORD']

system("dropdb -U postgres -h 127.0.0.1 caloriestracker_autotest")

print("Emulating caloriestracker_init main function")

mem=MemCaloriestracker()
mem.run()
mem.frmAccess=frmAccess("caloriestracker", "frmAccess")
mem.frmAccess.setResources(":/caloriestracker/caloriestracker.png", ":/caloriestracker/caloriestracker.png")
mem.frmAccess.setLabel(mem.tr("Please login to the Calories Tracker database"))
mem.frmAccess.txtDB.setText("caloriestracker_autotest")
mem.frmAccess.txtPass.setText(password)
mem.frmAccess.on_cmdDatabaseNew_released()

print("You must select yes and ok to message")

print ("Emulating caloriestracker main function")

del mem
mem=MemCaloriestracker()
mem.run()
mem.frmAccess=frmAccess("caloriestracker", "frmAccess")
mem.frmAccess.setResources(":/caloriestracker/caloriestracker.png", ":/caloriestracker/caloriestracker.png")
mem.frmAccess.setLabel(mem.tr("Please login to the Calories Tracker database"))
mem.frmAccess.txtDB.setText("caloriestracker_autotest")
mem.frmAccess.txtPass.setText(password)
mem.frmAccess.on_cmdYN_accepted()


if mem.frmAccess.result()==QDialog.Accepted:
    mem.con=mem.frmAccess.con
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
