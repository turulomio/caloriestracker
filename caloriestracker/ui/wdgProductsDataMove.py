from PyQt5.QtWidgets import QWidget, QTableWidgetItem,  QMessageBox
from caloriestracker.ui.Ui_wdgProductsDataMove import Ui_wdgProductsDataMove
from caloriestracker.libcaloriestrackerfunctions import qcenter, qright

class wdgProductsDataMove(QWidget, Ui_wdgProductsDataMove):
    def __init__(self, mem,  origin, destiny, parent = None, name = None, modal = False):
        QWidget.__init__(self,  parent)
        self.mem=mem
        self.origin=origin
        self.destiny=destiny
        self.setupUi(self)
        self.table.settings(self.mem, "wdgProductsDataMove") 
        self.origin.needStatus(3)
        self.destiny.needStatus(3)
        self.reload()
        
    def on_cmdInterchange_released(self):
        tmp=self.origin
        self.origin=self.destiny
        self.destiny=tmp
        self.reload()
    
    ## Sets tabble data
    def reload(self):
        self.table.applySettings()
        for i,  p in enumerate([self.origin, self.destiny]):
            self.table.setItem(i, 0, qcenter(p.id))
            self.table.item(i, 0).setIcon(p.stockmarket.country.qicon())
            self.table.setItem(i, 1, QTableWidgetItem(p.name))
            self.table.setItem(i, 2, QTableWidgetItem(p.isin))
            self.table.setItem(i, 3, qright(p.result.all.length()))
            self.table.setItem(i, 4, qright(p.dps.length()))
            self.table.setItem(i, 5, qright(self.mem.data.investments.InvestmentManager_with_investments_with_the_same_product(p).length()))
            opportunities=self.mem.con.cursor_one_field("select count(*) from opportunities where products_id=%s and executed is null and removed is null", (p.id, ))
            self.table.setItem(i, 6, qright(opportunities))
            self.table.setItem(i, 7, qright(p.splits.length()))
            self.table.setItem(i, 8, qright(p.estimations_dps.length()))
            self.table.setItem(i, 9, qright(p.estimations_eps.length()))

    def on_cmd_released(self):
        reply = QMessageBox.question(None, self.tr('Moving data between products'), self.tr("This action can't be undone.\nDo you want to continue?"), QMessageBox.Yes, QMessageBox.No)                  
        if reply==QMessageBox.Yes:
            self.mem.data.products.move_data_between_products(self.origin, self.destiny)
            self.origin.needStatus(3, downgrade_to=0)
            self.destiny.needStatus(3, downgrade_to=0)
            if self.chkInvestments.isChecked()==True:
                self.mem.data.investments.change_product_id(self.origin, self.destiny)
            self.mem.con.commit()
            self.reload()
            

