from PyQt5.QtCore import pyqtSlot, QSize
from PyQt5.QtWidgets import QWidget, QMenu, QMessageBox, QDialog, QVBoxLayout
from caloriestracker.ui.Ui_wdgProducts import Ui_wdgProducts
from caloriestracker.objects.product import ProductAllManager, ProductManager
from caloriestracker.ui.myqwidgets import qmessagebox
from caloriestracker.libmanagers import ManagerSelectionMode

class wdgProducts(QWidget, Ui_wdgProducts):
    ## @param only_system_products Boolean. True only system products. False all products
    def __init__(self, mem,  only_system_products=False, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.tblProducts.setSettings(self.mem.settings, "wdgProducts", "tblProducts")
        self.tblProducts.table.customContextMenuRequested.connect(self.on_tblProducts_customContextMenuRequested)
        if only_system_products==True:
            self.products=ProductManager(self.mem)
            self.products.load_from_db("select * from products order by name")
        else:
            self.products=ProductAllManager(self.mem)
        self.products.qtablewidget(self.tblProducts)

    @pyqtSlot() 
    def on_actionProductDelete_triggered(self):
        if self.tblProducts.selected.is_deletable()==False:
            qmessagebox(self.tr("This product can't be removed, because is marked as not remavable"))
            return
            
        if self.tblProducts.selected.elaboratedproducts_id!=None:#Elaborated:
            qmessagebox(self.tr("Not developed yet, for elaborated product"))
            return
            
        reply = QMessageBox.question(None, self.tr('Asking your confirmation'), self.tr("This action can't be undone.\nDo you want to delete this record?"), QMessageBox.Yes, QMessageBox.No)                  
        if reply==QMessageBox.Yes:
            self.tblProducts.selected.delete()
            self.mem.con.commit()
            self.mem.data.products.remove(self.tblProducts.selected)
            self.on_cmd_pressed()

    ## Merges a personal product into a system one
    @pyqtSlot()
    def on_actionProductPersonalMerge_triggered(self):
        from caloriestracker.ui.wdgProductsDataMove import wdgProductsDataMove
        d=QDialog(self)
        d.resize(self.mem.settings.value("wdgProducts/frmProductPersonalMerge_size", QSize(800, 600)))
        d.setWindowTitle(self.tr("Merge personal product into a system one"))
        lay = QVBoxLayout(d)
        wdg=wdgProductsDataMove(self.mem, self.tblProducts.selected, None, d)
        lay.addWidget(wdg)
        d.exec_()
        self.mem.settings.setValue("wdgProducts/frmProductPersonalMerge_size", d.size())

    @pyqtSlot() 
    def on_actionProductNew_triggered(self):
        from caloriestracker.ui.frmProductsAdd import frmProductsAdd
        w=frmProductsAdd(self.mem, None, self)
        w.exec_()
        self.on_cmd_pressed()

    @pyqtSlot() 
    def on_actionProductEdit_triggered(self):
        if self.tblProducts.selected.system_product==True:
            from caloriestracker.ui.frmProductsAdd import frmProductsAdd
            w=frmProductsAdd(self.mem, self.tblProducts.selected, self)
            if self.mem.isProductsMaintainerMode()==False:
                w.setReadOnly()
            w.exec_()
        elif self.tblProducts.selected.system_product==False:
            if self.tblProducts.selected.elaboratedproducts_id==None:
                from caloriestracker.ui.frmProductsAdd import frmProductsAdd
                w=frmProductsAdd(self.mem, self.tblProducts.selected, self)
                w.exec_()
                self.on_cmd_pressed()
            else:#Elaborated product
                from caloriestracker.ui.frmProductsElaboratedAdd import frmProductsElaboratedAdd
                elaborated=self.mem.data.elaboratedproducts.find_by_id(self.tblProducts.selected.elaboratedproducts_id)
                w=frmProductsElaboratedAdd(self.mem, elaborated, self)
                w.exec_()
        self.on_cmd_pressed()

    @pyqtSlot() 
    def on_actionFormats_triggered(self):
        from caloriestracker.ui.frmFormats import frmFormats
        w=frmFormats(self.mem, self.tblProducts.selected, self)
        w.exec_()

    def on_txt_returnPressed(self):
        self.on_cmd_pressed()
        
    @pyqtSlot(str) 
    def on_txt_textChanged(self, text):
        self.on_cmd_pressed()

    def on_cmd_pressed(self):
        del self.products
        self.products=self.mem.data.products.ObjectManager_which_name_contains(self.txt.text(), False)
        self.products.setSelectionMode(ManagerSelectionMode.Object)
        self.products.qtablewidget(self.tblProducts)
        self.tblProducts.setOrderBy(0, False)
        self.lblFound.setText(self.tr("{} products found").format(self.products.length()))

    def on_tblProducts_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionProductNew)
        menu.addAction(self.actionProductDelete)
        menu.addAction(self.actionProductEdit)
        menu.addSeparator()
        menu.addAction(self.actionProductPersonalMerge)
        menu.addSeparator()
        menu.addAction(self.actionFormats)
        
        #Enabled disabled  
        if self.tblProducts.selected==None:
            self.actionProductDelete.setEnabled(False)
            self.actionProductEdit.setEnabled(False)
            self.actionFormats.setEnabled(False)
            self.actionProductPersonalMerge.setEnabled(False)
        else:
            self.actionProductDelete.setEnabled(True)
            self.actionProductEdit.setEnabled(True)
            self.actionFormats.setEnabled(True)
            self.actionProductPersonalMerge.setEnabled(True)
        menu.addMenu(self.tblProducts.qmenu())
        menu.exec_(self.tblProducts.table.mapToGlobal(pos))
      
