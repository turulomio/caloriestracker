from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDialog, QMenu
from caloriestracker.objects.productelaborated import ProductElaborated
from caloriestracker.ui.Ui_frmProductsElaboratedAdd import Ui_frmProductsElaboratedAdd
from caloriestracker.ui.frmProductsInElaboratedProductAdd import frmProductsInElaboratedProductAdd
from caloriestracker.ui.myqwidgets import qmessagebox
from datetime import datetime
from logging import debug

class frmProductsElaboratedAdd(QDialog, Ui_frmProductsElaboratedAdd):
    def __init__(self, mem, elaboratedproduct=None, parent=None, ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.resize(self.mem.settings.value("frmProductsElaboratedAdd/qdialog", QSize(800, 600)))
        self.elaboratedproduct=elaboratedproduct
        self.tblProductsIn.setSettings(self.mem.settings, "frmProductsElaboratedAdd","tblProductsIn")
        self.tblProductsIn.table.customContextMenuRequested.connect(self.on_tblProductsIn_customContextMenuRequested)
        self.tblProductsIn.table.itemSelectionChanged.connect(self.on_tblProductsIn_itemSelectionChanged)
        if self.elaboratedproduct==None:
            self.lbl.setText(self.tr("Add a new personal and elaborated product"))
            self.spnFinalAmount.setEnabled(False)
            self.tblProductsIn.setEnabled(False)
            self.mem.data.foodtypes.qcombobox(self.cmbFoodtypes)
            self.cmbFoodtypes.setCurrentIndex(-1)
        else:
            self.mem.data.foodtypes.qcombobox(self.cmbFoodtypes, self.elaboratedproduct.foodtype)
            if self.elaboratedproduct.foodtype==None:
                self.cmbFoodtypes.setCurrentIndex(-1)
            self.elaboratedproduct.needStatus(1)
            self.txtName.setText(self.elaboratedproduct.name)
            self.chkObsolete.setChecked(self.elaboratedproduct.obsolete)
            self.spnFinalAmount.setValue(self.elaboratedproduct.final_amount)
            self.lbl.setText(self.tr("Edit a personal and elaborated product"))
            self.elaboratedproduct.products_in.qtablewidget(self.tblProductsIn)
            
    @pyqtSlot() 
    def on_actionProductInDelete_triggered(self):
        self.elaboratedproduct.products_in.selected.delete()
        self.elaboratedproduct.products_in.remove(self.elaboratedproduct.products_in.selected)
        self.elaboratedproduct.save()
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
        
    @pyqtSlot(float)
    def on_spnFinalAmount_valueChanged(self, value):
        print("Changed")
        self.elaboratedproduct.final_amount=self.spnFinalAmount.value()
        self.elaboratedproduct.save()
        self.mem.con.commit()
        self.elaboratedproduct.products_in.qtablewidget(self.tblProductsIn)
        
    @pyqtSlot() 
    def on_actionProductEdit_triggered(self):
        if self.elaboratedproduct.products_in.selected.product.system_product==True:
            qmessagebox(
                self.tr("This is a system product so you can't edit it.") + "\n" +
                self.tr("Please, if it's something wrong with it create an issue at") + "\n" + 
                "https://github.com/turulomio/caloriestracker/issues"+ "\n" +
                self.tr("I'll fix it as soon as posible. ;)")
            )
        elif self.elaboratedproduct.products_in.selected.product.system_product==False:
            if self.elaboratedproduct.products_in.selected.product.elaboratedproducts_id==None:
                from caloriestracker.ui.frmProductsAdd import frmProductsAdd
                w=frmProductsAdd(self.mem, self.elaboratedproduct.products_in.selected.product, self)
                w.exec_()
            else:#Elaborated product
                from caloriestracker.ui.frmProductsElaboratedAdd import frmProductsElaboratedAdd
                elaborated=self.mem.data.elaboratedproducts.find_by_id(self.elaboratedproduct.products_in.selected.product.elaboratedproducts_id)
                w=frmProductsElaboratedAdd(self.mem, elaborated, self)
                w.exec_()
            self.elaboratedproduct.products_in.qtablewidget(self.tblProductsIn)

    def on_tblProductsIn_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionProductInNew)
        menu.addAction(self.actionProductInDelete)
        menu.addAction(self.actionProductInEdit)
        menu.addSeparator()
        menu.addAction(self.actionProductEdit)
        
        #Enabled disabled  
        if self.elaboratedproduct.products_in.selected==None:
            self.actionProductInDelete.setEnabled(False)
            self.actionProductInEdit.setEnabled(False)
            self.actionProductEdit.setEnabled(False)
        else:
            self.actionProductInDelete.setEnabled(True)
            self.actionProductInEdit.setEnabled(True)
            self.actionProductEdit.setEnabled(True)
        menu.exec_(self.tblProductsIn.table.mapToGlobal(pos))

    def on_tblProductsIn_itemSelectionChanged(self):
        self.elaboratedproduct.products_in.cleanSelection()
        for i in self.tblProductsIn.table.selectedItems():
            if i.column()==0 and i.row()<self.elaboratedproduct.products_in.length():#only once per row
                self.elaboratedproduct.products_in.selected=self.elaboratedproduct.products_in.arr[i.row()]
        debug("Selected product in elaborated products: " + str(self.elaboratedproduct.products_in.selected))

    def on_bb_accepted(self):
        foodtype=None if self.cmbFoodtypes.currentIndex()==-1 else self.mem.data.foodtypes.find_by_id(self.cmbFoodtypes.itemData(self.cmbFoodtypes.currentIndex()))
        if foodtype==None:
            qmessagebox(self.tr("You neet to set a food type"),  ":/caloriestracker/book.png")
            return
 
        if self.elaboratedproduct==None:        
            self.elaboratedproduct=ProductElaborated(self.mem)
            self.elaboratedproduct.name=self.txtName.text()
            self.elaboratedproduct.foodtype=foodtype
            self.elaboratedproduct.obsolete=self.chkObsolete.isChecked()
            self.elaboratedproduct.final_amount=self.spnFinalAmount.value()
            self.mem.data.elaboratedproducts.append(self.elaboratedproduct)
            self.mem.data.elaboratedproducts.order_by_name()
        else:
            self.elaboratedproduct.name=self.txtName.text()
            self.elaboratedproduct.obsolete=self.chkObsolete.isChecked()
            self.elaboratedproduct.foodtype=foodtype
            self.elaboratedproduct.final_amount=self.spnFinalAmount.value()
        self.elaboratedproduct.last=datetime.now()
        self.elaboratedproduct.save()
        self.mem.con.commit()
        self.mem.settings.setValue("frmProductsElaboratedAdd/qdialog", self.size())
        self.accept()

    def on_bb_rejected(self):
        self.mem.settings.setValue("frmProductsElaboratedAdd/qdialog", self.size())
        self.reject()

