from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QVBoxLayout

class MyQDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=None)
        
    ## @param widgets is a list of widgets to allow add several widgets
    def settings_and_exec_(self, mem, settings_key, widgets,  title):
        self.settings_key=settings_key
        self.mem=mem
        self.resize(self.mem.settings.value(self.settings_key, QSize(800, 600)))
        self.setWindowTitle(title)
        lay = QVBoxLayout(self)
        for wdg in widgets:
            lay.addWidget(wdg)
        self.exec_()
        self.mem.settings.setValue(self.settings_key, self.size())
