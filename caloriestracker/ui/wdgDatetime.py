## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README


from PyQt5.QtCore import pyqtSignal,  pyqtSlot
from PyQt5.QtWidgets import QWidget, QCompleter
from datetime import datetime
from .Ui_wdgDatetime import Ui_wdgDatetime
from .. datetime_functions import dtaware
from logging import debug
from pytz import all_timezones, timezone



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
        self.localzone='UTC'#Used for now button
        self.cmbZone.blockSignals(True)
        self.pytz_zones_qcombobox(self.cmbZone, None)
        self.cmbZone.blockSignals(False)

    def setLocalzone(self, localzone):
        self.localzone=localzone

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
        self.set(datetime.now(), self.localzone)

    def setTitle(self, title):
        self.grp.setTitle(title)

    @staticmethod
    ## @param selected is a pytz name
    def pytz_zones_qcombobox(combo, selected):
        combo.completer().setCompletionMode(QCompleter.PopupCompletion)
        for tz in all_timezones:
            combo.addItem(tz, tz)
        if selected!=None:
            combo.setCurrentIndex(combo.findData(selected))

    ## @param dt can be a naive or aware. If aware it ignore it and set as naive with parmeter zone. If naive just put the zone to the dtnaive
    ## @param zone pytz name
    ## @param localzone pytz name
    def set(self, dt=None, zone=None):
        if dt==None or zone==None:
            self.on_cmdNow_released()
            return

        self.cmbZone.setCurrentIndex(self.cmbZone.findData(zone))

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
        if self.cmbZone.currentText() not in all_timezones:
            debug("Something wrong using self.localzone")
            zone=self.localzone
        else:
            zone=self.cmbZone.currentText()

        return dtaware(self.teDate.selectedDate().toPyDate(), time , zone)

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
        self.updateTooltip()
        self.changed.emit()

    def updateTooltip(self):
        self.setToolTip(self.tr("Selected datetime:\n{0}").format(self.datetime()))
