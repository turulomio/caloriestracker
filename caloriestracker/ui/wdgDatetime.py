## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README


from PyQt5.QtCore import pyqtSignal,  pyqtSlot,  Qt
from PyQt5.QtWidgets import QWidget, QCompleter, QToolButton, QLineEdit, QHBoxLayout, QVBoxLayout, QApplication, QLabel
from datetime import datetime
from .Ui_wdgDatetime import Ui_wdgDatetime
from .. datetime_functions import dtaware
from .myqdialog import MyModalQDialog
from logging import debug
from pytz import all_timezones

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
        self.cmdNow.setFocus()
        self.chkNone.hide()
        self.lineNone.hide()

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
            
    ## Sets if chkNone is showed
    ## @param show Boolean
    def show_none(self, show):
        if show is True:
            self.chkNone.show()
            self.lineNone.show()
        else:
            self.chkNone.hide()
            self.lineNone.hide()

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
    ## @param combo QComboBox
    ## @param selected is a pytz name
    def pytz_zones_qcombobox(combo, selected):
        combo.completer().setCompletionMode(QCompleter.PopupCompletion)
        for tz in all_timezones:
            combo.addItem(tz, tz)
        if selected!=None:
            combo.setCurrentIndex(combo.findData(selected))

    ## @param dt can be a naive or aware. If aware it ignore it and set as naive with parmeter zone. If naive just put the zone to the dtnaive
    ## @param zone pytz name
    def set(self, dt=None, zone=None):
        if self.chkNone.isHidden():# chkNone hidden will set now
            if dt is None or zone is None:
                self.on_cmdNow_released()
                return
        else:# chkNone visible witll set check to None
            if dt is None or zone is None:
                self.chkNone.setCheckState(Qt.Checked)
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
        if self.chkNone.isChecked():
            return None
        else:
            return self.teDate.selectedDate().toPyDate()

    ## Returns a dtaware datetime or None if something is wrong
    def datetime(self):
        if self.chkNone.isChecked():
            return None
        #qt only miliseconds
        time=self.teTime.time().toPyTime()
        time=time.replace(microsecond=self.teMicroseconds.value())
        if self.cmbZone.currentText() not in all_timezones:
            debug("Something wrong using self.localzone")
            zone=self.localzone
        else:
            zone=self.cmbZone.currentText()

        try:
            return dtaware(self.teDate.selectedDate().toPyDate(), time , zone)
        except:
            return None
            
    def on_chkNone_stateChanged(self, state):
            self.teDate.setEnabled(not self.chkNone.isChecked())
            self.teMicroseconds.setEnabled(not self.chkNone.isChecked())
            self.teTime.setEnabled(not self.chkNone.isChecked())
            self.cmbZone.setEnabled(not self.chkNone.isChecked())
            self.cmdNow.setEnabled(not self.chkNone.isChecked())
            self.updateTooltip()
            self.changed.emit()
        
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

    @pyqtSlot()
    def on_teDate_keyPressEvent(self, event):
        print("NO FUNCIONA PORQUE NO ES UNA SEÑAL NI HAY EN QCALENDAR")
        if event.key() not in [Qt.Key_0, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5, Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9]:
            event.reject()
        else:
            event.accept()

    @pyqtSlot(str)      
    def on_cmbZone_currentIndexChanged(self, stri):
        self.updateTooltip()
        self.changed.emit()

    def updateTooltip(self):
        self.setToolTip(self.tr("Selected datetime:\n{0}").format(self.datetime()))

class wdgDatetimeOneLine(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._lbl=QLabel(self)
        self.setLabel(self.tr("Select date and time"))
        self._dt=wdgDatetime(self)
        self._button=QToolButton(self)
        self._txt=QLineEdit(self)
        self._txt.setReadOnly(True)
        self._button.released.connect(self.on_button_released)
        lay=QHBoxLayout(self)
        lay.addWidget(self._lbl)
        lay.addWidget(self._txt)
        lay.addWidget(self._button)
        
        
        self._dialog=MyModalQDialog(self)
        self._dialog.setWindowTitle(self.tr("Select date and time"))
        self._dialog.setWidgets(self._dt)
        
    def setLabel(self, s):
        self._lbl.setText(s)

    def setSettings(self, settings, settingsSection="wdgDatetime",  settingsObject="qdialog"):
        self._settings=settings
        self._settingsSection=settingsSection
        self._settingsObject=settingsObject
        self.setObjectName(self._settingsObject)
        self._dialog.setSettings(self._settings, self._settingsSection, self._settingsObject+"_qdialog")

    def wdgDatetime(self):
        return self._dt
        
    def button(self):
        return self._button
        
    def on_button_released(self):
        self._dialog.exec_()
        self._txt.setText(str(self._dt.datetime()))


if __name__ == '__main__':
    from sys import exit
    from PyQt5.QtCore import QSettings
    app = QApplication([])

    main=QWidget()
    
    w = wdgDatetime()
    w.show_none(True)
    w.set()
   
    oneline = wdgDatetimeOneLine()
    oneline.setSettings(QSettings())
    oneline.wdgDatetime().show_none(True)
    oneline.wdgDatetime().set()

    #Widget
    lay=QVBoxLayout(main)
    lay.addWidget(w)
    lay.addWidget(oneline)
    main.resize(300, 550)
    main.move(300, 300)
    main.setWindowTitle('wdgDatetime example')
    main.show()
    exit(app.exec_())
