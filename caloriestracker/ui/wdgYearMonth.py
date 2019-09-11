from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget
import datetime
from xulpymoney.ui.Ui_wdgYearMonth import Ui_wdgYearMonth
from xulpymoney.libxulpymoneyfunctions import function_name, qmessagebox

class wdgYearMonth(QWidget, Ui_wdgYearMonth):
    changed=pyqtSignal()
    def __init__(self,  parent = None, name = None):
        QWidget.__init__(self,  parent)
        self.setupUi(self)
        
        
    def initiate(self, firstyear,  lastyear, currentyear, currentmonth):
        """Debe ser la primera función después del constructor"""
        if firstyear==None:
            self.setEnabled(False)
            print (function_name(self), "Firstyear is None")
            return
        
        self.firstyear=firstyear
        self.lastyear=lastyear
        self.year=currentyear
        self.month=currentmonth
        for year in range(firstyear, lastyear+1):
            self.cmbYear.addItem(str(year), year)
        self.set(currentyear, currentmonth)
        
    def set(self,  year , month):
        self.year=year
        self.month=month
        self.cmbYear.setCurrentIndex(self.year-self.firstyear)
        self.cmbMonth.setCurrentIndex(self.month-1)

    @pyqtSlot(str)      
    def on_cmbYear_currentIndexChanged(self, text):
        self.year=int(text)
        self.changed.emit()
        
    @pyqtSlot(int)      
    def on_cmbMonth_currentIndexChanged(self, integ):
        self.month=integ+1
        self.changed.emit()
        
    def on_cmdNext_pressed(self):
        if self.month==12:
            if self.year==self.lastyear:
                qmessagebox(self.tr("I can't show the next month"))
                return
            self.month=1
            self.year=self.year+1
        else:
            self.month=self.month+1
        self.set(self.year, self.month)
        
    def on_cmdPrevious_pressed(self):
        if self.month==1:
            if self.firstyear==self.year:
                qmessagebox(self.tr("I can't show the previous month"))
                return
            self.month=12
            self.year=self.year-1
        else:
            self.month=self.month-1
        self.set(self.year, self.month)
        
    @pyqtSlot()      
    def on_cmdCurrent_pressed(self):
        self.set(datetime.date.today().year, datetime.date.today().month)
        
        

