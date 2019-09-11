from PyQt5.QtCore import pyqtSignal,  pyqtSlot
from PyQt5.QtWidgets import QWidget
import datetime
from xulpymoney.ui.Ui_wdgDatetime import Ui_wdgDatetime
from xulpymoney.libxulpymoneyfunctions import dtaware

class wdgDatetime(QWidget, Ui_wdgDatetime):
    """Usage:
    Use constructor wdgDatetime()
    Set if show seconds, microseconds, zone
    Use set function to set the zone
    """
    changed=pyqtSignal()
    def __init__(self,  parent = None, name = None):
        QWidget.__init__(self,  parent)
        self.setupUi(self)
        self.mem=None
        self.teMicroseconds.setSuffix(self.tr(" \u03bcs"))        
        self.showMicroseconds=True
        self.showSeconds=True
        self.showZone=True
        self.zone=None#Set in set()                                                                                                     
        
    def show_microseconds(self, show):
        self.showMicroseconds=show
        if show==True:
            self.teMicroseconds.show()
        else:
            self.teMicroseconds.hide()
    
    def show_seconds(self, show):
        """Hides seconds when show is True. The datetime funtion the hour with zero seconds.
        show_seconds(False) doestn't implies show_microseconds(False). You must added manually."""
        self.showSeconds=show
        if show==True:
            self.teTime.setDisplayFormat("HH:mm:ss")
        else:
            self.teTime.setDisplayFormat("HH:mm")
        
    def show_timezone(self, show):
        """Hiding this all zones will have localzone defined in self.mem.localzone"""
        self.showZone=show
        if show==True:
            self.cmbZone.show()
        else:
            self.cmbZone.hide()
            
    def on_cmdNow_released(self):
        self.set(self.mem, datetime.datetime.now(), self.mem.localzone)

    def setTitle(self, title):
        self.grp.setTitle(title)

    def setCombine(self, mem, date, time, zone):
        """Use datetime combine to pass date and time"""
        self.set(mem, datetime.datetime.combine(date, time), zone)


    def set(self,  mem, dt=None,  zone=None):
        """Can be called several times"""
        self.mem=mem
        if self.cmbZone.count()==0:#Load combo zone, before, problems with on_changed
            self.mem.zones.qcombobox(self.cmbZone)  
            
        if dt==None or zone==None:
            self.on_cmdNow_released()
            return
            
        if self.showZone==False:
            self.on_cmbZone_currentIndexChanged(self.mem.localzone.name)
        else:
            self.on_cmbZone_currentIndexChanged(zone.name)
        
        self.teDate.setSelectedDate(dt.date())
        
        if self.showSeconds==False:
            dt=dt.replace(second=0)
        self.teTime.setTime(dt.time())
        
        if self.showMicroseconds==False:
            dt=dt.replace(microsecond=0)
        self.teMicroseconds.setValue(dt.microsecond)
        
        self.updateTooltip()
        self.changed.emit()
        
        
    def date(self):
        return self.teDate.selectedDate().toPyDate()
        
    def datetime(self):
        #qt only miliseconds
        time=self.teTime.time().toPyTime()
        time=time.replace(microsecond=self.teMicroseconds.value())
        return dtaware(self.teDate.selectedDate().toPyDate(), time , self.zone.name)

    def on_teDate_selectionChanged(self):
        self.updateTooltip()
        self.changed.emit()
        
    def on_teTime_timeChanged(self, time):
        self.updateTooltip()
        self.changed.emit()
        
    @pyqtSlot(int)   
    def on_teMicroseconds_valueChanged(self):
        self.updateTooltip()
        self.changed.emit()
        
    @pyqtSlot(str)      
    def on_cmbZone_currentIndexChanged(self, stri):
        self.zone=self.mem.zones.find_by_name(stri)
        self.updateTooltip()
        self.changed.emit()
        
    def updateTooltip(self):
        self.setToolTip(self.tr("Selected datetime:\n{0}").format(self.datetime()))

        

