## @namespace caloriestracker.caloriestracker
## @brief Main caloriestracker script.

import sys
import argparse
import logging
import signal
from colorama import init, Style, Fore

from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QApplication,  QDialog
from caloriestracker.libcaloriestracker import MemCaloriestracker
from caloriestracker.version import  __versiondate__
from caloriestracker.libcaloriestrackerfunctions import addDebugSystem, addCommonToArgParse
from caloriestracker.ui.frmAccess import frmAccess
from caloriestracker.ui.frmMain import frmMain

def signal_handler(signal, frame):
        logging.critical(Style.BRIGHT+Fore.RED+app.translate("Core","You pressed 'Ctrl+C', exiting..."))
        sys.exit(1)

######################

def main():
    from PyQt5 import QtWebEngineWidgets # To avoid error must be imported before QCoreApplication
    dir(QtWebEngineWidgets)
    init(autoreset=True)

    global app
    app = QApplication(sys.argv)
    app.setOrganizationName("caloriestracker")
    app.setOrganizationDomain("caloriestracker")
    app.setApplicationName("caloriestracker")

    signal.signal(signal.SIGINT, signal_handler)

    parser=argparse.ArgumentParser(
            prog='caloriestracker', 
            description=app.translate("Core",'Personal accounting system'),  
            epilog=app.translate("Core","If you like this app, please give me a star in GitHub (https://github.com/turulomio/caloriestracker).")+"\n" +
                app.translate("Core","Developed by Mariano Mu\xf1oz 2015-{} \xa9".format(__versiondate__.year)),
            formatter_class=argparse.RawTextHelpFormatter
        )
    addCommonToArgParse(parser)
    args=parser.parse_args()        

    addDebugSystem(args)

    mem=MemCaloriestracker()
    mem.setQTranslator(QTranslator(app))
    mem.languages.cambiar(mem.language.id)

    access=frmAccess(mem)
    access.setLabel(QApplication.translate("Core","Please login to the caloriestracker database"))
    access.config_load()
    access.exec_()

    if access.result()==QDialog.Accepted:
        mem.con=access.con

        mem.frmMain = frmMain(mem)
        mem.frmMain.show()
        sys.exit(app.exec_())

if __name__=="__main__":
        main()
