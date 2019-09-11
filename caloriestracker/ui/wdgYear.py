from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget
import datetime
from xulpymoney.ui.Ui_wdgYear import Ui_wdgYear
from xulpymoney.libxulpymoneyfunctions import function_name, qmessagebox

class wdgYear(QWidget, Ui_wdgYear):
    changed=pyqtSignal()
    def __init__(self,  parent = None, name = None):
        QWidget.__init__(self,  parent)
        self.setupUi(self)
        
        
    def initiate(self, firstyear,  lastyear, currentyear):
        """Debe ser la primera función después del constructor"""
        if firstyear==None:
            self.setEnabled(False)
            print (function_name(self), "Firstyear is None")
            return
        
        self.firstyear=firstyear
        self.lastyear=lastyear
        for year in range(firstyear, lastyear+1):
            self.cmbYear.addItem(str(year), year)
            
        if currentyear<firstyear:#If I set a currentyear that doesn't exist
            self.set(firstyear)
        else:
            self.set(currentyear)
        
    def set(self,  year):
        self.year=year
        self.cmbYear.setCurrentIndex(self.year-self.firstyear)
        if self.year==self.lastyear:
            self.cmdNext.setEnabled(False)
        else:
            self.cmdNext.setEnabled(True)

        if self.year==self.firstyear:
            self.cmdPrevious.setEnabled(False)
        else:
            self.cmdPrevious.setEnabled(True)
    @pyqtSlot(str)      
    def on_cmbYear_currentIndexChanged(self, text):
        self.year=int(text)
        self.changed.emit()
        
       
    def on_cmdNext_pressed(self):
        if self.year==self.lastyear:
            qmessagebox(self.tr("I can't show the next year"))
            return
        self.year=self.year+1
        self.set(self.year)
        
    def on_cmdPrevious_pressed(self):
        if self.firstyear==self.year:
            qmessagebox(self.tr("I can't show the previous year"))
            return
        self.year=self.year-1
        self.set(self.year)
        
    @pyqtSlot()      
    def on_cmdCurrent_pressed(self):
        self.set(datetime.date.today().year)
        
        

