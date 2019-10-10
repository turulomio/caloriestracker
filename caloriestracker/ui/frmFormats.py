from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDialog, QMenu
from caloriestracker.ui.Ui_frmFormats import Ui_frmFormats
from caloriestracker.ui.myqwidgets import qmessagebox
from logging import debug

class frmFormats(QDialog, Ui_frmFormats):
    def __init__(self, mem, product, parent=None, ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.product=product
        self.tblFormats.settings(self.mem, "tblFormats")
        self.resize(self.mem.settings.value("frmFormats/qdialog", QSize(800, 600)))
        self.lbl.setText(self.tr("Formats of {}").format(self.product.fullName()))
        self.product.needStatus(1)
        self.product.formats.qtablewidget(self.tblFormats)

    @pyqtSlot() 
    def on_actionFormatDelete_triggered(self):
        if self.product.system_product==False:
            self.product.formats.selected.delete()
            self.product.formats.remove(self.product.formats.selected)
            self.mem.con.commit()
            self.product.formats.qtablewidget(self.tblFormats)
        else:
            qmessagebox(
                self.tr("This format is of a system product so you can't edit it.") + "\n" +
                self.tr("Please, if it's something wrong with it create an issue at") + "\n" + 
                "https://github.com/turulomio/caloriestracker/issues"+ "\n" +
                self.tr("I'll fix it as soon as posible. ;)"),  self.mem.app_resource())

    @pyqtSlot() 
    def on_actionFormatNew_triggered(self):
        if self.product.system_product==False:
            from caloriestracker.ui.frmFormatsAdd import frmFormatsAdd
            w=frmFormatsAdd(self.mem, self.product, None , self)
            w.exec_()
            self.product.formats.qtablewidget(self.tblFormats)
        else:
            qmessagebox(
                self.tr("This format is of a system product so you can't edit it.") + "\n" +
                self.tr("Please, if it's something wrong with it create an issue at") + "\n" + 
                "https://github.com/turulomio/caloriestracker/issues"+ "\n" +
                self.tr("I'll fix it as soon as posible. ;)"),  self.mem.app_resource())

    @pyqtSlot() 
    def on_actionFormatEdit_triggered(self):
        if self.product.system_product==False:
            from caloriestracker.ui.frmFormatsAdd import frmFormatsAdd
            w=frmFormatsAdd(self.mem, self.product, self.product.formats.selected, self)
            w.exec_()
            self.product.formats.qtablewidget(self.tblFormats)
        else:
            qmessagebox(
                self.tr("This format is of a system product so you can't edit it.") + "\n" +
                self.tr("Please, if it's something wrong with it create an issue at") + "\n" + 
                "https://github.com/turulomio/caloriestracker/issues"+ "\n" +
                self.tr("I'll fix it as soon as posible. ;)"),  self.mem.app_resource())


    def on_tblFormats_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionFormatNew)
        menu.addAction(self.actionFormatDelete)
        menu.addAction(self.actionFormatEdit)
        
        #Enabled disabled  
        if self.product.formats.selected==None:
            self.actionFormatDelete.setEnabled(False)
            self.actionFormatEdit.setEnabled(False)
        else:
            self.actionFormatDelete.setEnabled(True)
            self.actionFormatEdit.setEnabled(True)
        menu.exec_(self.tblFormats.mapToGlobal(pos))

    def on_tblFormats_itemSelectionChanged(self):
        self.product.formats.cleanSelection()
        for i in self.tblFormats.selectedItems():
            if i.column()==0 and i.row()<self.product.formats.length():#only once per row
                self.product.formats.selected=self.product.formats.arr[i.row()]
        debug("Selected format: " + str(self.product.formats.selected))

    def on_bb_accepted(self):
        self.mem.settings.setValue("frmFormats/qdialog", self.size())
        self.accept()

    def on_bb_rejected(self):
        self.mem.settings.setValue("frmFormats/qdialog", self.size())
        self.reject()  
