from PyQt5.QtWidgets import QWidget, QMessageBox
from caloriestracker.ui.Ui_wdgProductsDataMove import Ui_wdgProductsDataMove
from caloriestracker.objects.product import move_product_personal_to_system
from caloriestracker.ui.myqwidgets import qmessagebox

class wdgProductsDataMove(QWidget, Ui_wdgProductsDataMove):
    def __init__(self, mem,  origin, parent):
        QWidget.__init__(self,  parent)
        self.mem=mem
        self.parent=parent
        self.origin=origin
        self.setupUi(self)
        self.wdg.setSettings(self.mem.settings, "wdgProductsDataMove", "wdg") 
        self.mem.data.products.ProductManager().qtablewidget(self.wdg)

    def on_bb_accepted(self):
        if self.origin is not None and self.wdg.selected is not None:
            r=self.tr("Moving data from personal product '{}' to system product '{}'").format(self.origin, self.wdg.selected)
            reply = QMessageBox.question(None, self.tr('Moving data between products'), r+"\n"+ self.tr("This action can't be undone.\nDo you want to continue?"), QMessageBox.Yes, QMessageBox.No)                  
            if reply==QMessageBox.Yes:
                move_product_personal_to_system(self.mem, self.origin,  self.wdg.selected)
                self.parent.accept()
        else:
            qmessagebox(self.tr("You must select a system product"))

    def on_bb_rejected(self):
        self.parent.reject()

