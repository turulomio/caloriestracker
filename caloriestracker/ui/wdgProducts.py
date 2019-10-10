from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QMenu, QMessageBox
from caloriestracker.ui.Ui_wdgProducts import Ui_wdgProducts
from caloriestracker.libcaloriestracker import ProductAllManager, ProductElaborated
from caloriestracker.ui.myqwidgets import qmessagebox
from caloriestracker.libmanagers import ManagerSelectionMode
from logging import debug

class wdgProducts(QWidget, Ui_wdgProducts):
    def __init__(self, mem,  arrInt=[],  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.tblProducts.settings(self.mem, "wdgProducts")
        self.products=ProductAllManager(self.mem)

    @pyqtSlot() 
    def on_actionProductDelete_triggered(self):
        if self.products.selected.is_deletable()==False:
            qmessagebox(self.tr("This product can't be removed, because is marked as not remavable"))
            return
            
        if self.products.selected.elaboratedproducts_id!=None:#Elaborated:
            qmessagebox(self.tr("Not developed yet, for elaborated product"))
            return
            
        reply = QMessageBox.question(None, self.tr('Asking your confirmation'), self.tr("This action can't be undone.\nDo you want to delete this record?"), QMessageBox.Yes, QMessageBox.No)                  
        if reply==QMessageBox.Yes:
            self.products.selected.delete()
            self.mem.con.commit()
            self.mem.data.products.remove(self.products.selected)
            self.on_cmd_pressed()

    @pyqtSlot() 
    def on_actionProductNew_triggered(self):
        from caloriestracker.ui.frmProductsAdd import frmProductsAdd
        w=frmProductsAdd(self.mem, None, self)
        w.exec_()
        self.on_cmd_pressed()

    @pyqtSlot() 
    def on_actionProductEdit_triggered(self):
        if self.products.selected.system_product==True:
            qmessagebox(
                self.tr("This is a system product so you can't edit it.") + "\n" +
                self.tr("Please, if it's something wrong with it create an issue at") + "\n" + 
                "https://github.com/turulomio/caloriestracker/issues"+ "\n" +
                self.tr("I'll fix it as soon as posible. ;)")
            )
        elif self.products.selected.system_product==False:
            if self.products.selected.elaboratedproducts_id==None:
                from caloriestracker.ui.frmProductsAdd import frmProductsAdd
                w=frmProductsAdd(self.mem, self.products.selected, self)
                w.exec_()
                self.on_cmd_pressed()
            else:#Elaborated product
                from caloriestracker.ui.frmProductsElaboratedAdd import frmProductsElaboratedAdd
                elaborated=ProductElaborated(self.mem, self.products.selected.elaboratedproducts_id)
                w=frmProductsElaboratedAdd(self.mem, elaborated, self)
                w.exec_()
                self.on_cmd_pressed()

    @pyqtSlot() 
    def on_actionFormats_triggered(self):
        from caloriestracker.ui.frmFormats import frmFormats
        w=frmFormats(self.mem, self.products.selected, self)
        w.exec_()

    def on_txt_returnPressed(self):
        self.on_cmd_pressed()
        
    @pyqtSlot(str) 
    def on_txt_textChanged(self, text):
        self.on_cmd_pressed()

    def on_cmd_pressed(self):
        #        if len(self.txt.text().upper())<=2:            
        #            qmessagebox(self.tr("Search too wide. You need more than 2 characters"))
        #            return
        del self.products
        self.products=self.mem.data.products.ObjectManager_with_name_contains_string(self.txt.text(), False, *self.mem.data.products.args)
        self.products.setSelectionMode(ManagerSelectionMode.Object)
        self.products.qtablewidget(self.tblProducts)
        self.lblFound.setText(self.tr("{} products found").format(self.products.length()))

    def on_tblProducts_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionProductNew)
        menu.addAction(self.actionProductDelete)
        menu.addAction(self.actionProductEdit)
        menu.addSeparator()
        menu.addAction(self.actionFormats)
        
        #Enabled disabled  
        if self.products.selected==None:
            self.actionProductDelete.setEnabled(False)
            self.actionProductEdit.setEnabled(False)
            self.actionFormats.setEnabled(False)
        else:
            self.actionProductDelete.setEnabled(True)
            self.actionProductEdit.setEnabled(True)
            self.actionFormats.setEnabled(True)
        menu.exec_(self.tblProducts.mapToGlobal(pos))

    def on_tblProducts_itemSelectionChanged(self):
        self.products.cleanSelection()
        for i in self.tblProducts.selectedItems():
            if i.column()==0:#only once per row
                self.products.selected=self.products.arr[i.row()]
        debug("Selected product: " + str(self.products.selected))
      
