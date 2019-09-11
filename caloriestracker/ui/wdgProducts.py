from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QMenu, QMessageBox
from xulpymoney.ui.Ui_wdgProducts import Ui_wdgProducts
from xulpymoney.ui.frmProductReport import frmProductReport
from xulpymoney.libmanagers import ManagerSelectionMode
from xulpymoney.libxulpymoney import QuoteAllIntradayManager
from xulpymoney.libxulpymoneyfunctions import qmessagebox
from xulpymoney.ui.frmQuotesIBM import frmQuotesIBM
from xulpymoney.ui.wdgProductsDataMove import wdgProductsDataMove
from xulpymoney.ui.frmEstimationsAdd import frmEstimationsAdd
from xulpymoney.ui.wdgProductHistoricalChart import wdgProductHistoricalBuyChart
import logging

class wdgProducts(QWidget, Ui_wdgProducts):
    def __init__(self, mem,  arrInt=[],  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.tblInvestments.settings(self.mem, "wdgProducts")
        self.mem.stockmarkets.qcombobox(self.cmbStockExchange)
        self.arrInt=arrInt#Lista de ids of products showed and used to show
        self.build_array_from_arrInt()

    def build_array_from_arrInt(self):        
        self.products=self.mem.data.products.ProductManager_with_id_in_list(self.arrInt)
        self.products.setSelectionMode(ManagerSelectionMode.List)
        self.products.needStatus(needstatus=1, progress=True)
        self.products.order_by_upper_name()
        self.lblFound.setText(self.tr("Found {0} records".format(self.products.length())))
        self.products.myqtablewidget(self.tblInvestments)

    @pyqtSlot()
    def on_actionFavorites_triggered(self):      
        if self.products.selected[0].id in self.mem.favorites:
            self.mem.favorites.remove(self.products.selected[0].id)
        else:
            self.mem.favorites.append(self.products.selected[0].id)
        logging.debug("Favoritos: {}".format(self.mem.favorites))
        self.mem.save_MemSettingsDB()
        
        del self.arrInt
        self.arrInt=[]
        for f in self.mem.favorites:
            self.arrInt.append(f)
        self.build_array_from_arrInt()
        

    @pyqtSlot()  
    def on_actionIbex35_triggered(self):
        del self.arrInt
        self.arrInt=[]
        for p in self.mem.data.products.arr:
            if p.agrupations.dbstring.find("|IBEX|")!=-1 and p.obsolete==False:
                self.arrInt.append(p.id)
        self.build_array_from_arrInt()

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
        w=frmProductReport(self.mem, None, self)
        w.exec_()        
        del self.arrInt
        self.arrInt=[w.product.id, ]
        self.build_array_from_arrInt()

    @pyqtSlot() 
    def on_actionPurchaseGraphic_triggered(self):
        self.products.selected[0].needStatus(2)
        d=QDialog(self)     
        d.showMaximized()
        d.setWindowTitle(self.tr("Purchase graph"))
        lay = QVBoxLayout(d)
        
        wc=wdgProductHistoricalBuyChart()
        wc.setProduct(self.products.selected[0], None)
        wc.setPrice(self.products.selected[0].result.basic.last.quote)
        wc.generate()
        wc.display()
        lay.addWidget(wc)
        d.exec_()
        
    @pyqtSlot() 
    def on_actionProductReport_triggered(self):
        w=frmProductReport(self.mem, self.products.selected[0], None,  self)
        w.exec_()        
        self.build_array_from_arrInt()
        
    @pyqtSlot() 
    def on_actionSortTPCDiario_triggered(self):
        if self.products.order_by_daily_tpc():
            self.products.myqtablewidget(self.tblInvestments)        
        else:
            qmessagebox(self.tr("I couldn't order data due to they have null values"))

    @pyqtSlot()
    def on_actionSortTPCAnual_triggered(self):
        if self.products.order_by_annual_tpc():
            self.products.myqtablewidget(self.tblInvestments)        
        else:
            qmessagebox(self.tr("I couldn't order data due to they have null values"))

    @pyqtSlot()
    def on_actionSortHour_triggered(self):
        self.products.order_by_datetime()
        self.products.myqtablewidget(self.tblInvestments)        

    @pyqtSlot()
    def on_actionSortName_triggered(self):
        self.products.order_by_upper_name()
        self.products.myqtablewidget(self.tblInvestments)        

    @pyqtSlot()
    def on_actionSortDividend_triggered(self):
        if self.products.order_by_dividend():
            self.products.myqtablewidget(self.tblInvestments)        
        else:
            qmessagebox(self.tr("I couldn't order data due to they have null values"))     
        
    def on_txt_returnPressed(self):
        self.on_cmd_pressed()

    def on_tblInvestments_cellDoubleClicked(self, row, column):
        self.on_actionProductReport_triggered()

    def on_cmd_pressed(self):
        if len(self.txt.text().upper())<=2:            
            qmessagebox(self.tr("Search too wide. You need more than 2 characters"))
            return

        # To filter by stockmarket
        sm=None
        if self.chkStockExchange.checkState()==Qt.Checked:
            sm=self.mem.stockmarkets.find_by_id(self.cmbStockExchange.itemData(self.cmbStockExchange.currentIndex()))     

        del self.arrInt
        self.arrInt=[]
        #Temporal ProductManager
        pros=self.mem.data.products.ProductManager_contains_string(self.txt.text())
        for p in pros.arr:
            #Filter sm
            if sm!=None and sm.id!=p.stockmarket.id:
                continue
            else:
                self.arrInt.append(p.id)

        self.build_array_from_arrInt()

    def on_tblInvestments_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionProductReport)
        menu.addAction(self.actionPurchaseGraphic)
        menu.addSeparator()
        menu.addAction(self.actionProductNew)
        menu.addAction(self.actionProductDelete)
        menu.addSeparator()
        menu.addAction(self.actionQuoteNew)
        menu.addAction(self.actionProductPriceLastRemove)
        menu.addAction(self.actionEstimationDPSNew)
        menu.addSeparator()
        menu.addAction(self.actionMergeCodes)
        menu.addAction(self.actionFavorites)
        if len(self.products.selected)==1:
            if self.products.selected[0].id in self.mem.favorites:
                self.actionFavorites.setText(self.tr("Remove from favorites"))
            else:
                self.actionFavorites.setText(self.tr("Add to favorites"))
        menu.addSeparator()
        menu.addAction(self.actionPurge)

        if len (self.products.selected)==1:
            if self.products.selected[0].id==79329:
                menu.addSeparator()
                menu.addAction(self.actionIbex35)
        menu.addSeparator()
        ordenar=QMenu(self.tr("Order by"))
        menu.addMenu(ordenar)
        ordenar.addAction(self.actionSortName)
        ordenar.addAction(self.actionSortHour)
        ordenar.addAction(self.actionSortTPCDiario)
        ordenar.addAction(self.actionSortTPCAnual)
        ordenar.addAction(self.actionSortDividend)
        
        #Enabled disabled  
        if len(self.products.selected)==1:
            self.actionMergeCodes.setEnabled(False)
            self.actionProductDelete.setEnabled(True)
            self.actionFavorites.setEnabled(True)
            self.actionProductReport.setEnabled(True)
            self.actionPurchaseGraphic.setEnabled(True)
            self.actionIbex35.setEnabled(True)
            self.actionQuoteNew.setEnabled(True)
            self.actionEstimationDPSNew.setEnabled(True)
            self.actionPurge.setEnabled(True)
            self.actionProductPriceLastRemove.setEnabled(True)
        elif len(self.products.selected)==2:
            self.actionMergeCodes.setEnabled(True)
        else:
            self.actionMergeCodes.setEnabled(False)
            self.actionProductDelete.setEnabled(False)
            self.actionFavorites.setEnabled(False)
            self.actionProductReport.setEnabled(False)
            self.actionPurchaseGraphic.setEnabled(False)
            self.actionIbex35.setEnabled(False)
            self.actionQuoteNew.setEnabled(False)
            self.actionEstimationDPSNew.setEnabled(False)
            self.actionPurge.setEnabled(False)
            self.actionProductPriceLastRemove.setEnabled(False)
        menu.exec_(self.tblInvestments.mapToGlobal(pos))

    @pyqtSlot() 
    def on_actionMergeCodes_triggered(self):
        #Only two checked in custom contest
        d=QDialog(self)
        d.setWindowTitle(self.tr("Merging codes"))
        w=wdgProductsDataMove(self.mem, self.products.selected[0], self.products.selected[1])
        lay = QVBoxLayout(d)
        lay.addWidget(w)
        d.resize(w.size())
        d.exec_()
        self.build_array_from_arrInt()
    
    def on_tblInvestments_itemSelectionChanged(self):
        self.products.cleanSelection()
        for i in self.tblInvestments.selectedItems():
            if i.column()==0:#only once per row
                self.products.selected.append(self.products.arr[i.row()])
        logging.debug(self.products.selected)

    @pyqtSlot()  
    def on_actionPurge_triggered(self):
        all=QuoteAllIntradayManager(self.mem)
        all.load_from_db(self.products.selected[0])
        numpurged=all.purge(progress=True)
        if numpurged!=None:#Canceled
            self.mem.con.commit()
            qmessagebox(self.tr("{0} quotes have been purged from {1}".format(numpurged, self.products.selected[0].name)))
        else:
            self.mem.con.rollback()

    @pyqtSlot()  
    def on_actionQuoteNew_triggered(self):
        w=frmQuotesIBM(self.mem,  self.products.selected[0])
        w.exec_()
        self.build_array_from_arrInt()

    @pyqtSlot() 
    def on_actionProductPriceLastRemove_triggered(self):
        self.products.selected[0].result.basic.last.delete()
        self.mem.con.commit()
        self.products.selected[0].needStatus(1, downgrade_to=0)
        self.build_array_from_arrInt()

    @pyqtSlot()  
    def on_actionEstimationDPSNew_triggered(self):
        d=frmEstimationsAdd(self.mem, self.products.selected[0], "dps")
        d.exec_()
        if d.result()==QDialog.Accepted:
            self.products.selected[0].needStatus(1, downgrade_to=0)
            self.build_array_from_arrInt()
