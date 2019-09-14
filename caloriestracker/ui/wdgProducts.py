from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QMenu, QMessageBox
from caloriestracker.ui.Ui_wdgProducts import Ui_wdgProducts
from caloriestracker.libcaloriestrackerfunctions import qmessagebox
from caloriestracker.libmanagers import ManagerSelectionMode
from logging import debug

class wdgProducts(QWidget, Ui_wdgProducts):
    def __init__(self, mem,  arrInt=[],  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.tblProducts.settings(self.mem, "wdgProducts")
        self.products=None

    @pyqtSlot() 
    def on_actionProductDelete_triggered(self):
        if self.products.selected[0].is_deletable()==False:
            qmessagebox(self.tr("This product can't be removed, because is marked as not remavable"))
            return
            
        if self.products.selected[0].is_system()==True:
            qmessagebox(self.tr("This product can't be removed, because is a system product"))
            return
            
        respuesta = QMessageBox.warning(self, self.tr("Xulpymoney"), self.tr("Deleting data from selected product ({0}). If you use manual update mode, data won't be recovered. Do you want to continue?".format(self.products.selected[0].id)), QMessageBox.Ok | QMessageBox.Cancel)
        if respuesta==QMessageBox.Ok:
            self.arrInt.remove(self.products.selected[0].id)
            self.mem.data.products.remove(self.products.selected[0])
            self.mem.con.commit()
            self.build_array_from_arrInt()            

    @pyqtSlot() 
    def on_actionProductNew_triggered(self):
        pass
#        w=frmProductReport(self.mem, None, self)
#        w.exec_()        
#        del self.arrInt
#        self.arrInt=[w.product.id, ]
#        self.build_array_from_arrInt()



    def on_txt_returnPressed(self):
        self.on_cmd_pressed()

    def on_cmd_pressed(self):
        #        if len(self.txt.text().upper())<=2:            
        #            qmessagebox(self.tr("Search too wide. You need more than 2 characters"))
        #            return
        del self.products
        self.products=self.mem.data.products.ProductAllManager_contains_string(self.txt.text())
        self.products.setSelectionMode(ManagerSelectionMode.Object)
        self.products.qtablewidget(self.tblProducts)
        self.lblFound.setText(self.tr("{} products found").format(self.products.length()))

    def on_tblProducts_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionProductNew)
        menu.addAction(self.actionProductDelete)
        menu.addAction(self.actionProductEdit)
        
        #Enabled disabled  
        if self.products.selected==None:
            self.actionProductDelete.setEnabled(False)
            self.actionProductEdit.setEnabled(False)
        else:
            self.actionProductDelete.setEnabled(True)
            self.actionProductEdit.setEnabled(True)
        menu.exec_(self.tblProducts.mapToGlobal(pos))

    def on_tblProducts_itemSelectionChanged(self):
        self.products.cleanSelection()
        for i in self.tblProducts.selectedItems():
            if i.column()==0:#only once per row
                self.products.selected=self.products.arr[i.row()]
        debug("Selected product: " + str(self.products.selected))

