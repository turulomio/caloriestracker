from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDialog, QMenu
from caloriestracker.ui.Ui_frmProductsElaboratedAdd import Ui_frmProductsElaboratedAdd
from caloriestracker.ui.frmProductsInElaboratedProductAdd import frmProductsInElaboratedProductAdd
from caloriestracker.libcaloriestracker import ProductElaborated
from logging import debug

class frmProductsElaboratedAdd(QDialog, Ui_frmProductsElaboratedAdd):
    def __init__(self, mem, elaboratedproduct=None, parent=None, ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.resize(self.mem.settings.value("frmProductsElaboratedAdd/qdialog", QSize(800, 600)))
        self.elaboratedproduct=elaboratedproduct
        self.tblProductsIn.settings(self.mem, "frmProductsElaboratedAdd")
        if self.elaboratedproduct==None:
            self.lbl.setText(self.tr("Add a new personal and elaborated product"))
            self.spnFinalAmount.setEnabled(False)
            self.tblProductsIn.setEnabled(False)
        else:
            self.elaboratedproduct.needStatus(1)
            self.txtName.setText(self.elaboratedproduct.name)
            self.spnFinalAmount.setValue(self.elaboratedproduct.final_amount)
            self.lbl.setText(self.tr("Edit a personal and elaborated product"))
            self.elaboratedproduct.products_in.qtablewidget(self.tblProductsIn)
            
    @pyqtSlot() 
    def on_actionProductInDelete_triggered(self):
        self.elaboratedproduct.products_in.selected.delete()
        self.elaboratedproduct.products_in.remove(self.elaboratedproduct.products_in.selected)
        self.mem.con.commit()
        self.elaboratedproduct.products_in.qtablewidget(self.tblProductsIn)

    @pyqtSlot() 
    def on_actionProductInNew_triggered(self):
        w=frmProductsInElaboratedProductAdd(self.mem, self.elaboratedproduct,  None, self)
        w.exec_()
        self.elaboratedproduct.products_in.qtablewidget(self.tblProductsIn)

    @pyqtSlot() 
    def on_actionProductInEdit_triggered(self):
        w=frmProductsInElaboratedProductAdd(self.mem, self.elaboratedproduct, self.elaboratedproduct.products_in.selected, self)
        w.exec_()
        self.elaboratedproduct.products_in.qtablewidget(self.tblProductsIn)

    def on_tblProductsIn_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionProductInNew)
        menu.addAction(self.actionProductInDelete)
        menu.addAction(self.actionProductInEdit)
        
        #Enabled disabled  
        if self.elaboratedproduct.products_in.selected==None:
            self.actionProductInDelete.setEnabled(False)
            self.actionProductInEdit.setEnabled(False)
        else:
            self.actionProductInDelete.setEnabled(True)
            self.actionProductInEdit.setEnabled(True)
        menu.exec_(self.tblProductsIn.mapToGlobal(pos))

    def on_tblProductsIn_itemSelectionChanged(self):
        self.elaboratedproduct.products_in.cleanSelection()
        for i in self.tblProductsIn.selectedItems():
            if i.column()==0 and i.row()<self.elaboratedproduct.products_in.length():#only once per row
                self.elaboratedproduct.products_in.selected=self.elaboratedproduct.products_in.arr[i.row()]
        debug("Selected product in elaborated products: " + str(self.elaboratedproduct.products_in.selected))

    def on_bb_accepted(self):
        if self.elaboratedproduct==None:        
            self.elaboratedproduct=ProductElaborated(self.mem)
            self.elaboratedproduct.name=self.txtName.text()
            self.elaboratedproduct.final_amount=self.spnFinalAmount.value()
            self.mem.data.elaboratedproducts.append(self.elaboratedproduct)
            self.mem.data.elaboratedproducts.order_by_name()
        else:
            self.elaboratedproduct.name=self.txtName.text()
            self.elaboratedproduct.final_amount=self.spnFinalAmount.value()
        self.elaboratedproduct.save()
        self.mem.con.commit()
        self.mem.settings.setValue("frmProductsElaboratedAdd/qdialog", self.size())
        self.accept()

    def on_bb_rejected(self):
        self.mem.settings.setValue("frmProductsElaboratedAdd/qdialog", self.size())
        self.reject()

