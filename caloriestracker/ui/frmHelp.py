from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QSize
from xulpymoney.ui.Ui_frmHelp import Ui_frmHelp

## Shows a Help dialog
class frmHelp(QDialog, Ui_frmHelp):
    def __init__(self,mem, parent = None, name = None, modal = False):
        QDialog.__init__(self, parent)
        self.mem=mem
        self.setupUi(self)
        self.resize(self.mem.settings.value("frmHelp/qdialog", QSize(800, 600)))

    ## Manage close event to save dialog size
    def closeEvent(self, event):
        self.mem.settings.setValue("frmHelp/qdialog", self.size())
        self.mem.settings.sync()
