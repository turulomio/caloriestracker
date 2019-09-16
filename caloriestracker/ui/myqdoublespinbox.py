from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDoubleSpinBox

from decimal import Decimal
class myQDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent):
        QDoubleSpinBox.__init__(self, parent)
#        self.valueChanged.connect(self.on_valueChanged)
        
    def value(self):
        return Decimal(QDoubleSpinBox.value(self))
        
#    def focusOutEvent(event)
#        pos=self.cursorPosition()
#        text=str(text).replace(".", ",")
#        self.setValue(text)
#        if self.isValid():        
#            self.setBackgroundRed(False)
#        else:
#            self.setBackgroundRed(True)
#        self.setCursorPosition(pos)     
        
                    
#    def setBackgroundRed(self, red):
#        if red==True:
#            css = """QLineEdit { background-color: rgb(255, 182, 182); }"""
#        else:
#            css=""
#        self.setStyleSheet(css)
