from PyQt5.QtCore import pyqtSlot, QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QMenu, QMessageBox, QLabel, QDialog, QVBoxLayout
from caloriestracker.libcaloriestracker import CompanyAllManager
from caloriestracker.ui.myqtablewidget import myQTableWidget
from caloriestracker.ui.myqwidgets import qmessagebox
from caloriestracker.libmanagers import ManagerSelectionMode
from caloriestracker.ui.Ui_wdgCompanies import Ui_wdgCompanies
from logging import debug

class wdgCompanies(QWidget, Ui_wdgCompanies):
    def __init__(self, mem,  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.tblCompanies.settings(self.mem, "wdgCompanies")
        self.companies=CompanyAllManager(self.mem)

    @pyqtSlot() 
    def on_actionCompanyDelete_triggered(self):
        if self.companies.selected.is_deletable()==False:
            qmessagebox(self.tr("This product can't be removed, because is marked as not remavable"))
            return
            
        reply = QMessageBox.question(None, self.tr('Asking your confirmation'), self.tr("This action can't be undone.\nDo you want to delete this record?"), QMessageBox.Yes, QMessageBox.No)                  
        if reply==QMessageBox.Yes:
            self.companies.selected.delete()
            self.mem.con.commit()
            self.mem.data.companies.remove(self.companies.selected)
            self.on_cmd_pressed()

    @pyqtSlot() 
    def on_actionCompanyNew_triggered(self):
        from caloriestracker.ui.frmCompaniesAdd import frmCompaniesAdd
        w=frmCompaniesAdd(self.mem, None, self)
        w.exec_()
        self.on_cmd_pressed()

    @pyqtSlot() 
    def on_actionCompanyEdit_triggered(self):
        if self.companies.selected.system_company==True:
            qmessagebox(
                self.tr("This is a system company so you can't edit it.") + "\n" +
                self.tr("Please, if it's something wrong with it create an issue at") + "\n" + 
                "https://github.com/turulomio/caloriestracker/issues"+ "\n" +
                self.tr("I'll fix it as soon as posible. ;)")
            )
        elif self.companies.selected.system_company==False:
            from caloriestracker.ui.frmCompaniesAdd import frmCompaniesAdd
            w=frmCompaniesAdd(self.mem, self.companies.selected, self)
            w.exec_()
            self.on_cmd_pressed()

    @pyqtSlot() 
    def on_actionCompanyProducts_triggered(self):
        d=QDialog(self)
        d.resize(self.mem.settings.value("wdgCompanies/frmCompanyProducts", QSize(800, 600)))
        title=self.tr("Products of {}").format(self.companies.selected.name)
        d.setWindowTitle(title)
        lay = QVBoxLayout(d)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        lbl=QLabel(d)
        lbl.setText(title)
        lbl.setFont(font)
        lbl.setAlignment(Qt.AlignCenter)
        lay.addWidget(lbl)
        companyproducts=self.mem.data.products.ProductAllManager_of_same_company(self.companies.selected)
        table=myQTableWidget(d)
        table.setObjectName("tblCompanyProducts")
        table.settings(self.mem, "wdgCompanies")
        companyproducts.qtablewidget(table)
        lay.addWidget(table)
        d.exec_()
        self.mem.settings.setValue("wdgCompanies/frmCompanyProducts", d.size())

    def on_txt_returnPressed(self):
        self.on_cmd_pressed()        

    @pyqtSlot(str) 
    def on_txt_textChanged(self, text):
        self.on_cmd_pressed()

    def on_cmd_pressed(self):
        #        if len(self.txt.text().upper())<=2:            
        #            qmessagebox(self.tr("Search too wide. You need more than 2 characters"))
        #            return
        del self.companies
        self.companies=self.mem.data.companies.ObjectManager_with_name_contains_string(self.txt.text(), False, *self.mem.data.products.args)
        self.companies.setSelectionMode(ManagerSelectionMode.Object)
        self.companies.qtablewidget(self.tblCompanies)
        self.lblFound.setText(self.tr("{} products found").format(self.companies.length()))

    def on_tblCompanies_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionCompanyNew)
        menu.addAction(self.actionCompanyDelete)
        menu.addAction(self.actionCompanyEdit)
        menu.addSeparator()
        menu.addAction(self.actionCompanyProducts)
        
        #Enabled disabled  
        if self.companies.selected==None:
            self.actionCompanyDelete.setEnabled(False)
            self.actionCompanyEdit.setEnabled(False)
            self.actionCompanyProducts.setEnabled(False)
        else:
            self.actionCompanyDelete.setEnabled(True)
            self.actionCompanyEdit.setEnabled(True)
            self.actionCompanyProducts.setEnabled(True)
        menu.exec_(self.tblCompanies.mapToGlobal(pos))

    def on_tblCompanies_itemSelectionChanged(self):
        self.companies.cleanSelection()
        for i in self.tblCompanies.selectedItems():
            if i.column()==0:#only once per row
                self.companies.selected=self.companies.arr[i.row()]
        debug("Selected product: " + str(self.companies.selected))
      
