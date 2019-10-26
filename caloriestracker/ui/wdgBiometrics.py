from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMenu, QMessageBox
from caloriestracker.libcaloriestracker import BiometricsManager
from caloriestracker.datetime_functions import dtaware_day_start_from_date
from caloriestracker.ui.Ui_wdgBiometrics import Ui_wdgBiometrics
from caloriestracker.ui.myqcharts import VCTemporalSeries
from caloriestracker.libmanagers import DVManager
from logging import debug
from datetime import date, timedelta

class wdgBiometrics(QWidget, Ui_wdgBiometrics):
    def __init__(self, mem,  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.biometrics=BiometricsManager(self.mem)
        self.tblBiometrics.settings(self.mem, "wdgBiometrics")    
        self.viewChartHeight=None
        self.viewChartWeight=None
        self.datefrom= date(1900, 1, 1)
        self.wdgYM.label.hide()
        self.wdgYM.blockSignals(True)
        self.wdgYM.initiate(1900,  date.today().year, date.today().year, date.today().month)
        self.wdgYM.blockSignals(False)
        self.on_rad20days_toggled(True)
        
    @pyqtSlot() 
    def on_wdgYM_changed(self):
        self.update()
        
        
    def update(self):
        del self.biometrics
        if self.rad20days.isChecked()==False:
            sql=self.mem.con.mogrify("select * from biometrics where users_id=%s and date_part('year',datetime)=%s and date_part('month',datetime)=%s order by datetime", (self.mem.user.id, self.wdgYM.year, self.wdgYM.month ))
        else:
            sql=self.mem.con.mogrify("""
WITH t AS (
    select * from biometrics where users_id=%s order by datetime desc limit 20
)
SELECT * FROM t ORDER BY datetime ASC""", (self.mem.user.id, ))
            
        self.biometrics=BiometricsManager(self.mem, sql, True)
        self.biometrics.qtablewidget(self.tblBiometrics)
        if self.viewChartHeight!=None:
            self.layHeight.removeWidget(self.viewChartHeight)
            self.viewChartHeight.close()
            self.layWeight.removeWidget(self.viewChartWeight)
            self.viewChartWeight.close()
        if self.biometrics.length()>0:
            self.viewChartHeight=VCHeight()
            self.viewChartHeight.setData(self.mem, self.datefrom)
            self.viewChartHeight.generate()
            self.layHeight.addWidget(self.viewChartHeight)
            
            self.viewChartWeight=VCWeight()
            self.viewChartWeight.setData(self.mem, self.datefrom)
            self.viewChartWeight.generate()
            self.layWeight.addWidget(self.viewChartWeight)

        

    @pyqtSlot(int)
    def on_cmbChart_currentIndexChanged(self, index):
        if index==0:
            self.datefrom= date(1900, 1, 1)
        elif index==1:
            self.datefrom= date.today()-timedelta(days=365)
        elif index==2:
            self.datefrom= date.today()-timedelta(days=365*3)
        self.update()
        
        
    @pyqtSlot()
    def on_actionBiometricsNew_triggered(self):
        from caloriestracker.ui.frmBiometricsAdd import frmBiometricsAdd
        w=frmBiometricsAdd(self.mem, None, self)
        w.exec_()
        self.update()

    @pyqtSlot()
    def on_actionBiometricsDelete_triggered(self):
        reply = QMessageBox.question(None, self.tr('Asking your confirmation'), self.tr("This action can't be undone.\nDo you want to delete this record?"), QMessageBox.Yes, QMessageBox.No)                  
        if reply==QMessageBox.Yes:
            self.biometrics.selected.delete()
            self.mem.con.commit()
            self.mem.user.load_last_biometrics()
        self.update()

    @pyqtSlot()
    def on_actionBiometricsEdit_triggered(self):
        from caloriestracker.ui.frmBiometricsAdd import frmBiometricsAdd
        w=frmBiometricsAdd(self.mem, self.biometrics.selected, self)
        w.exec_()
        self.update()

    def on_tblBiometrics_itemSelectionChanged(self):
        self.biometrics.cleanSelection()
        for i in self.tblBiometrics.selectedItems():
            if i.column()==0 and i.row()<self.biometrics.length():#only once per row
                self.biometrics.selected=self.biometrics.arr[i.row()]
        debug("Selected meal: {}".format(self.biometrics.selected))

    def on_tblBiometrics_customContextMenuRequested(self,  pos):
        menu=QMenu()
        menu.addAction(self.actionBiometricsNew)
        menu.addAction(self.actionBiometricsDelete)
        menu.addAction(self.actionBiometricsEdit)
        menu.addSeparator()
        
        if self.biometrics.selected==None:
            self.actionBiometricsDelete.setEnabled(False)
            self.actionBiometricsEdit.setEnabled(False)
        else:
            self.actionBiometricsDelete.setEnabled(True)
            self.actionBiometricsEdit.setEnabled(True)

        menu.exec_(self.tblBiometrics.mapToGlobal(pos))
        
    def on_rad20days_toggled(self, checked):
        self.wdgYM.setEnabled(not self.rad20days.isChecked())
        self.update()


##View chart of an biometrics
class VCWeight(VCTemporalSeries):
    def __init__(self):
        VCTemporalSeries.__init__(self)
        self.setTitle(self.tr("Weight evolution chart"))
        
    def setData(self, mem, date_from):
        self.mem=mem
        sql=self.mem.con.mogrify("""
            select 
                avg(weight), 
                datetime::date 
            from 
                biometrics 
            where 
                users_id=%s and 
                datetime::date>%s 
            group by datetime::date
            order by datetime::date
            """, (self.mem.user.id, date_from))
        self.weight=DVManager()
        self.sma_period=15
        for row in self.mem.con.cursor_rows(sql):
            self.weight.appendDV(dtaware_day_start_from_date(row['datetime'], self.mem.localzone),  row['avg'])
        self.sma_data=self.weight.sma(self.sma_period)

    ## Just draw the chart with selected options. To update it just close this object and create another one
    def generate(self):
        #Progress dialog 
        self.setProgressDialogEnabled(True)
        self.setProgressDialogAttributes(
                None, 
                self.tr("Loading {} biometrics").format(self.weight.length()), 
                QIcon(":caloriestracker/books.png"), 
                0, 
                self.weight.length()
        )
        weight=self.appendTemporalSeries(self.tr("Weight evolution"), None)
        sma=self.appendTemporalSeries(self.tr("Simple movil average {}").format(self.sma_period), None)
        for i in range(self.weight.length()):
            #Shows progress dialog
            self.setProgressDialogNumber(i+1)
            #Weight
            self.appendTemporalSeriesData(weight, self.weight.arr[i].datetime, self.weight.arr[i].value)
            #sma
            if i>=self.sma_period:
                self.appendTemporalSeriesData(sma, self.sma_data.arr[i-self.sma_period].datetime, self.sma_data.arr[i-self.sma_period].value)
        self.display()


##View chart of an biometrics
class VCHeight(VCTemporalSeries):
    def __init__(self):
        VCTemporalSeries.__init__(self)
        self.setTitle(self.tr("Height evolution chart"))
        
    def setData(self, mem, date_from):
        self.mem=mem
        sql=self.mem.con.mogrify("""
            select 
                max(height), 
                datetime::date 
            from 
                biometrics 
            where 
                users_id=%s and 
                datetime::date>%s 
            group by datetime::date
            order by datetime::date
            """, (self.mem.user.id, date_from))
        self.height=DVManager()
        for row in self.mem.con.cursor_rows(sql):
            self.height.appendDV(dtaware_day_start_from_date(row['datetime'], self.mem.localzone),  row['max'])

    ## Just draw the chart with selected options. To update it just close this object and create another one
    def generate(self):
        #Progress dialog 
        self.setProgressDialogEnabled(True)
        self.setProgressDialogAttributes(
                None, 
                self.tr("Loading {} biometrics").format(self.height.length()), 
                QIcon(":caloriestracker/books.png"), 
                0, 
                self.height.length()
        )
        height=self.appendTemporalSeries(self.tr("Height evolution"), None)
        for i in range(self.height.length()):
            #Shows progress dialog
            self.setProgressDialogNumber(i+1)
            #height
            self.appendTemporalSeriesData(height, self.height.arr[i].datetime, self.height.arr[i].value)
        self.display()
