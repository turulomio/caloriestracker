from PyQt5.QtWidgets import QDialog
from caloriestracker.ui.Ui_frmAuxiliarTables import Ui_frmAuxiliarTables

class frmAuxiliarTables(QDialog, Ui_frmAuxiliarTables):
    def __init__(self, mem,  parent = None, name = None, modal = False):
        """
        Constructor
        
        @param parent The parent widget of this dialog. (QWidget)
        @param name The name of this dialog. (QString)
        @param modal Flag indicating a modal dialog. (boolean)
        """
        QDialog.__init__(self,  parent)
        if name:
            self.setObjectName(name)
        self.setModal(True)
        self.setupUi(self)
        self.mem=mem

        self.tblConcepts.settings(self.mem, "frmAuxiliarTables")
