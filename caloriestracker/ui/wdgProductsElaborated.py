from PyQt5.QtCore import pyqtSlot, QSize
from PyQt5.QtWidgets import QWidget, QMenu, QMessageBox
from caloriestracker.ui.Ui_wdgProductsElaborated import Ui_wdgProductsElaborated
from caloriestracker.libcaloriestracker import ProductElaboratedManager
from caloriestracker.ui.frmProductsElaboratedAdd import frmProductsElaboratedAdd
from caloriestracker.ui.myqwidgets import qmessagebox
from caloriestracker.libmanagers import ManagerSelectionMode
from logging import debug

class wdgProductsElaborated(QWidget, Ui_wdgProductsElaborated):
    def __init__(self, mem,  arrInt=[],  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.resize(self.mem.settings.value("wdgProductsElaborated/qdialog", QSize(800, 600)))
        self.tblProductsElaborated.settings(self.mem, "wdgProductsElaborated")
        self.elaboratedproducts=ProductElaboratedManager(self.mem)
        self.on_cmd_pressed()

    @pyqtSlot() 
    def on_actionProductDelete_triggered(self):
        if self.elaboratedproducts.selected.is_deletable()==False:
            qmessagebox(self.tr("This elaborated product can't be removed, because is marked as not remavable"))
            return

        reply = QMessageBox.question(None, self.tr('Asking your confirmation'), self.tr("This action can't be undone.\nDo you want to delete this record?"), QMessageBox.Yes, QMessageBox.No)                  
        if reply==QMessageBox.Yes:
            self.elaboratedproducts.selected.delete()
            self.mem.con.commit()
            self.mem.data.elaboratedproducts.remove(self.elaboratedproducts.selected)
            self.on_cmd_pressed()

    @pyqtSlot() 
    def on_actionProductNew_triggered(self):
        w=frmProductsElaboratedAdd(self.mem, None, self)
        w.exec_()
        self.on_cmd_pressed()

    @pyqtSlot() 
    def on_actionProductEdit_triggered(self):
        w=frmProductsElaboratedAdd(self.mem, self.elaboratedproducts.selected, self)
        w.exec_()
        self.on_cmd_pressed()
        
    @pyqtSlot(str) 
    def on_txt_textChanged(self, text):
        self.on_cmd_pressed()

    def on_txt_returnPressed(self):
        self.on_cmd_pressed()

    def on_cmd_pressed(self):
        del self.elaboratedproducts
        self.elaboratedproducts=self.mem.data.elaboratedproducts.ObjectManager_with_name_contains_string(self.txt.text(), False, *self.mem.data.products.args)
        self.elaboratedproducts.setSelectionMode(ManagerSelectionMode.Object)
        self.elaboratedproducts.qtablewidget(self.tblProductsElaborated)
        self.lblFound.setText(self.tr("{} products found").format(self.elaboratedproducts.length()))

    def on_tblProductsElaborated_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionProductNew)
        menu.addAction(self.actionProductDelete)
        menu.addAction(self.actionProductEdit)
        
        #Enabled disabled  
        if self.elaboratedproducts.selected==None:
            self.actionProductDelete.setEnabled(False)
            self.actionProductEdit.setEnabled(False)
        else:
            self.actionProductDelete.setEnabled(True)
            self.actionProductEdit.setEnabled(True)
        menu.exec_(self.tblProductsElaborated.mapToGlobal(pos))

    def on_tblProductsElaborated_itemSelectionChanged(self):
        self.elaboratedproducts.cleanSelection()
        for i in self.tblProductsElaborated.selectedItems():
            if i.column()==0:#only once per row
                self.elaboratedproducts.selected=self.elaboratedproducts.arr[i.row()]
        debug("Selected elaboratedproducts: " + str(self.elaboratedproducts.selected))
      
    def on_bb_accepted(self):
        self.mem.settings.setValue("wdgProductsElaborated/qdialog", self.size())
        self.accept()
        
    def on_bb_rejected(self):
        self.mem.settings.setValue("wdgProductsElaborated/qdialog", self.size())
