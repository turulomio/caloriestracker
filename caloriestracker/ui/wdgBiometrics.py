from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QMenu, QMessageBox
from caloriestracker.libcaloriestracker import BiometricsManager
from caloriestracker.ui.Ui_wdgBiometrics import Ui_wdgBiometrics
from logging import debug
from datetime import date

class wdgBiometrics(QWidget, Ui_wdgBiometrics):
    def __init__(self, mem,  parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem
        self.biometrics=BiometricsManager(self.mem)
        self.tblBiometrics.settings(self.mem, "wdgBiometrics")    
        self.wdgYM.initiate(1900,  date.today().year, date.today().year, date.today().month)
        
    @pyqtSlot() 
    def on_wdgYM_changed(self):
        del self.biometrics
        sql=self.mem.con.mogrify("select * from biometrics where users_id=%s and date_part('year',datetime)=%s and date_part('month',datetime)=%s order by datetime", (self.mem.user.id, self.wdgYM.year, self.wdgYM.month ))
        self.biometrics=BiometricsManager(self.mem, sql, True)
        self.biometrics.qtablewidget(self.tblBiometrics)
        
    @pyqtSlot()
    def on_actionBiometricsNew_triggered(self):
        from caloriestracker.ui.frmBiometricsAdd import frmBiometricsAdd
        w=frmBiometricsAdd(self.mem, None, self)
        w.exec_()
        self.on_wdgYM_changed()

    @pyqtSlot()
    def on_actionBiometricsDelete_triggered(self):
        reply = QMessageBox.question(None, self.tr('Asking your confirmation'), self.tr("This action can't be undone.\nDo you want to delete this record?"), QMessageBox.Yes, QMessageBox.No)                  
        if reply==QMessageBox.Yes:
            self.biometrics.selected.delete()
            self.mem.con.commit()
            self.mem.user.load_last_biometrics()
        self.on_wdgYM_changed()

    @pyqtSlot()
    def on_actionBiometricsEdit_triggered(self):
        from caloriestracker.ui.frmBiometricsAdd import frmBiometricsAdd
        w=frmBiometricsAdd(self.mem, self.biometrics.selected, self)
        w.exec_()
        self.on_wdgYM_changed()

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
