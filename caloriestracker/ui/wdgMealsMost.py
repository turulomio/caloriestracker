from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from caloriestracker.ui.Ui_wdgMealsMost import Ui_wdgMealsMost
from datetime import date,  timedelta

class wdgMealsMost(QWidget, Ui_wdgMealsMost):
    def __init__(self, mem,  arrInt=[],  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.tblMeals.settings(self.mem.settings, "wdgMealsMost", "tblMeals")
        self.tblMeals.table.customContextMenuRequested.connect(self.on_tblMeals_customContextMenuRequested)
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
        
        data=[]
        for i, row in enumerate(rows):
            product=self.mem.data.products.find_by_id_system(row['id'], row['system_product'])
            data.append([
                product.fullName(), 
                row['sum'], 
            ])
        self.tblMeals.setData(
            [self.tr("Product"), self.tr("Amount")], 
            None, 
            data
        )   

    def on_tblMeals_customContextMenuRequested(self,  pos):
        self.tblMeals.qmenu().exec_(self.tblMeals.mapToGlobal(pos))
