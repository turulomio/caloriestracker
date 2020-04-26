from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDialog, QMenu
from caloriestracker.ui.Ui_frmFormats import Ui_frmFormats
from caloriestracker.ui.myqwidgets import qmessagebox

class frmFormats(QDialog, Ui_frmFormats):
    def __init__(self, mem, product, parent=None, ):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.product=product
        self.tblFormats.setSettings(self.mem.settings, "frmFormats", "tblFormats")
        self.tblFormats.table.customContextMenuRequested.connect(self.on_tblFormats_customContextMenuRequested)
        self.resize(self.mem.settings.value("frmFormats/qdialog", QSize(800, 600)))
        self.lbl.setText(self.tr("Formats of {}").format(self.product.fullName()))
        self.product.needStatus(1)
        self.product.formats.qtablewidget(self.tblFormats)

    @pyqtSlot() 
    def on_actionFormatDelete_triggered(self):
        if self.product.system_product==False:
            self.tblFormats.selected.delete()
            self.product.formats.remove(self.tblFormats.selected)
            self.mem.con.commit()
            self.product.formats.qtablewidget(self.tblFormats)
        else:
            qmessagebox(
                self.tr("This format is of a system product so you can't edit it.") + "\n" +
                self.tr("Please, if it's something wrong with it create an issue at") + "\n" + 
                "https://github.com/turulomio/caloriestracker/issues"+ "\n" +
                self.tr("I'll fix it as soon as posible. ;)"))

    @pyqtSlot() 
    def on_actionFormatNew_triggered(self):
        if self.product.system_product==False or self.mem.isProductsMaintainerMode()==True:
            from caloriestracker.ui.frmFormatsAdd import frmFormatsAdd
            w=frmFormatsAdd(self.mem, self.product, None , self)
            w.exec_()
            self.product.formats.qtablewidget(self.tblFormats)
        else:
            qmessagebox(
                self.tr("This format is of a system product so you can't edit it.") + "\n" +
                self.tr("Please, if it's something wrong with it create an issue at") + "\n" + 
                "https://github.com/turulomio/caloriestracker/issues"+ "\n" +
                self.tr("I'll fix it as soon as posible. ;)"))

    @pyqtSlot() 
    def on_actionFormatEdit_triggered(self):
        if self.product.system_product==False or self.mem.isProductsMaintainerMode()==True:
            from caloriestracker.ui.frmFormatsAdd import frmFormatsAdd
            w=frmFormatsAdd(self.mem, self.product, self.tblFormats.selected, self)
            w.exec_()
            self.product.formats.qtablewidget(self.tblFormats)
        else:
            qmessagebox(
                self.tr("This format is of a system product so you can't edit it.") + "\n" +
                self.tr("Please, if it's something wrong with it create an issue at") + "\n" + 
                "https://github.com/turulomio/caloriestracker/issues"+ "\n" +
                self.tr("I'll fix it as soon as posible. ;)"))


    def on_tblFormats_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionFormatNew)
        menu.addAction(self.actionFormatDelete)
        menu.addAction(self.actionFormatEdit)
        
        #Enabled disabled  
        if self.tblFormats.selected==None:
            self.actionFormatDelete.setEnabled(False)
            self.actionFormatEdit.setEnabled(False)
        else:
            self.actionFormatDelete.setEnabled(True)
            self.actionFormatEdit.setEnabled(True)
        menu.exec_(self.tblFormats.table.mapToGlobal(pos))

    def on_bb_accepted(self):
        self.mem.settings.setValue("frmFormats/qdialog", self.size())
        self.accept()

    def on_bb_rejected(self):
        self.mem.settings.setValue("frmFormats/qdialog", self.size())
        self.reject()  
