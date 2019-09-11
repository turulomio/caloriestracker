from PyQt5.QtWidgets import QWidget
from xulpymoney.ui.Ui_wdgCuriosity import Ui_wdgCuriosity

class wdgCuriosity(QWidget, Ui_wdgCuriosity):
    def __init__(self, mem,  parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem

    def setTitle(self, text):
        self.lblTitle.setText(text)
        
    def setText(self, text):
        self.lbl.setText(text)
