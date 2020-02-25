from PyQt5.QtWidgets import QWidget, QMessageBox
from caloriestracker.ui.Ui_wdgProductsDataMove import Ui_wdgProductsDataMove

class wdgProductsDataMove(QWidget, Ui_wdgProductsDataMove):
    def __init__(self, mem,  origin, destiny, parent):
        QWidget.__init__(self,  parent)
        self.mem=mem
        self.parent=parent
        self.origin=origin
        self.destiny=destiny
        self.setupUi(self)
        self.wdg.settings(self.mem.settings, "wdgProductsDataMove", "wdg") 
        self.mem.data.products.ProductManager().qtablewidget(self.wdg)

    def on_bb_accepted(self):
        reply = QMessageBox.question(None, self.tr('Moving data between products'), self.tr("This action can't be undone.\nDo you want to continue?"), QMessageBox.Yes, QMessageBox.No)                  
        if reply==QMessageBox.Yes:
            self.mem.data.products.move_data_between_products(self.origin, self.destiny)
            self.origin.needStatus(3, downgrade_to=0)
            self.destiny.needStatus(3, downgrade_to=0)
            self.mem.con.commit()
            
        self.parent.accept()

    def on_bb_rejected(self):
        self.parent.reject()

