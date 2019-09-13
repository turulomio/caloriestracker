from PyQt5.QtWidgets import QWidget, QSpacerItem, QSizePolicy
from caloriestracker.ui.Ui_wdgCuriosities import Ui_wdgCuriosities
from caloriestracker.ui.wdgCuriosity import wdgCuriosity

class wdgCuriosities(QWidget, Ui_wdgCuriosities):
    def __init__(self, mem,  parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem


        c=wdgCuriosity(self.mem)
        c.setTitle(self.tr("Curiosity 1"))
        c.setText("Text 1")
        self.layout.addWidget(c)
        c=wdgCuriosity(self.mem)
        c.setTitle(self.tr("Curiosity 2"))
        c.setText("Text 2")
        self.layout.addWidget(c)

        self.layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding))
