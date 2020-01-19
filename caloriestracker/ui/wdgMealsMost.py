from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from caloriestracker.ui.Ui_wdgMealsMost import Ui_wdgMealsMost
from caloriestracker.ui.myqtablewidget import qleft, qnumber
from datetime import date,  timedelta

class wdgMealsMost(QWidget, Ui_wdgMealsMost):
    def __init__(self, mem,  arrInt=[],  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.tblMeals.settings(self.mem, "wdgMealsMost")
        self.cmbPeriod.setCurrentIndex(int(self.mem.settings.value("wdgMealsMost/cmbPeriod_index", "0")))

    @pyqtSlot(int)
    def on_cmbPeriod_currentIndexChanged(self, index):
        if index==0:
            datefrom= date.today()-timedelta(days=7)
        elif index==1:
            datefrom= date.today()-timedelta(days=30)
        elif index==2:
            datefrom= date.today()-timedelta(days=365)
        elif index==3:
            datefrom= date.today()-timedelta(days=365*3)
        elif index==4:
            datefrom= date(1900, 1, 1)
        self.mem.settings.setValue("wdgMealsMost/cmbPeriod_index", self.cmbPeriod.currentIndex())
        
        rows=self.mem.con.cursor_rows("""
            select 
                sum(meals.amount), 
                allproducts.id, 
                allproducts.system_product 
            from 
                meals, 
                allproducts 
            where 
                meals.datetime::date>%s and
                meals.products_id=allproducts.id and 
                meals.system_product=allproducts.system_product 
            group by 
                allproducts.id, 
                allproducts.system_product 
            order by 
                sum desc""", (datefrom, ))        
        
        self.tblMeals.setColumnCount(2)
        self.tblMeals.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Product")))
        self.tblMeals.setHorizontalHeaderItem(1, QTableWidgetItem(self.tr("Amount")))
   
        self.tblMeals.applySettings()
        self.tblMeals.clearContents()
        self.tblMeals.setRowCount(len(rows))
        for i, row in enumerate(rows):
            product=self.mem.data.products.find_by_id_system(row['id'], row['system_product'])
            self.tblMeals.setItem(i, 0, qleft(product.fullName()))
            self.tblMeals.setItem(i, 1, qnumber(row['sum']))
