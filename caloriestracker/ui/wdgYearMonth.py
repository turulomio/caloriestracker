## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget 
from datetime import date
from logging import debug
from .Ui_wdgYearMonth import Ui_wdgYearMonth
from .myqwidgets import qmessagebox

class wdgYearMonth(QWidget, Ui_wdgYearMonth):
    changed=pyqtSignal()
    def __init__(self,  parent = None, name = None):
        QWidget.__init__(self,  parent)


    ## Mandatory. It doesn't emit changed signal when called
    ## @param firstyear
    ## @param lastyear
    ## @param currentyear
    ## @param currentmonth
    ## @param emit Boolean. False by default. If False it doesn't emit anything after initiate

    def initiate(self, firstyear,  lastyear, currentyear, currentmonth, firstmonth=1, lastmonth=12,  emit=False):
        self.setupUi(self)
        self.firstyear=firstyear
        self.firstmonth=firstmonth
        self.lastyear=lastyear
        self.lastmonth=lastmonth
        self.year=currentyear
        self.month=currentmonth
        self.cmbYear.blockSignals(True)
        for year in range(firstyear, lastyear+1):
            self.cmbYear.addItem(str(year), year)
        self.cmbYear.blockSignals(False)
        self.set(currentyear, currentmonth, emit)
        
    def set(self,  year , month, emit=True):
        self.year=year
        self.month=month
        self.cmbYear.blockSignals(True)
        self.cmbYear.setCurrentIndex(self.year-self.firstyear)
        self.cmbYear.blockSignals(False)
        self.cmbMonth.blockSignals(True)
        self.cmbMonth.setCurrentIndex(self.month-1)
        self.cmbMonth.blockSignals(False)
        
        #Previous and next button
        if self.year==self.firstyear and self.month==self.firstmonth:
            self.cmdPrevious.setEnabled(False)
        else:
            self.cmdPrevious.setEnabled(True)
        if self.year==self.lastyear and self.month==self.lastmonth:
            self.cmdNext.setEnabled(False)
        else:
            self.cmdNext.setEnabled(True)
        
        if emit is True:
            self.changed.emit()
            debug("wdgYearMonth was changed to year: {}, month: {}".format(year, month))

    @pyqtSlot(str)      
    def on_cmbYear_currentIndexChanged(self, text):
        self.set(int(text), self.month, emit=True)
        
    @pyqtSlot(int)      
    def on_cmbMonth_currentIndexChanged(self, integ):
        self.set(self.year, integ+1, emit=True)
        
    def on_cmdNext_released(self):
        if self.month==12:
            if self.year==self.lastyear:
                qmessagebox(self.tr("I can't show the next month"))
                return
            self.month=1
            self.year=self.year+1
        else:
            self.month=self.month+1
        self.set(self.year, self.month, emit=True)
        
    def on_cmdPrevious_released(self):
        if self.month==1:
            if self.firstyear==self.year:
                qmessagebox(self.tr("I can't show the previous month"))
                return
            self.month=12
            self.year=self.year-1
        else:
            self.month=self.month-1
        self.set(self.year, self.month, emit=True)
        
    @pyqtSlot()      
    def on_cmdCurrent_released(self):
        self.set(date.today().year, date.today().month, emit=True)

def example():
    from sys import exit
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])

    w = wdgYearMonth()
    w.move(300, 300)
    w.initiate(2000, 2020, 2020, 11, emit=False)
    w.setWindowTitle('wdgYearMonth example')
    w.show()

    exit(app.exec_())
