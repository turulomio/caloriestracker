## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README


from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QLineEdit, QWidget, QHBoxLayout, QLabel, QCheckBox, QSizePolicy
from decimal import Decimal
from stdnum import iban

class myQLineEdit(QLineEdit):
    doubleClicked=pyqtSignal()
    def __init__(self, parent):
        QWidget.__init__(self, parent)       
        self.textChanged.connect(self.on_textChanged)
        self.setMaxLength(30)

    def isValid(self):
        """Devuelve si el textedit es un float o un decimal valido"""
        if self.decimal()==None:
            return False
        return True

    def setBackgroundRed(self, red):
        if red==True:
            css = """QLineEdit { background-color: rgb(255, 182, 182); }"""
        else:
            css=""
        self.setStyleSheet(css)

    @pyqtSlot(str)
    def on_textChanged(self, text):
        pos=self.cursorPosition()
        text=text.replace(",", ".")
        text=text.replace("e", "0")#Avoids scientific numbers
        self.setText(text)
        if self.isValid():        
            self.setBackgroundRed(False)
        else:
            self.setBackgroundRed(True)
        self.setCursorPosition(pos)     
        
#    def keyReleaseEvent(self, event):
#        super(myQLineEdit, self).keyReleaseEvent(event)
#        if event.text() in ("0123456789.,"):
#            print("acepted")
#            event.accept()
#            return
#        print ("ignore")
#        print (event.text())
#        event.ignore()
        
    def decimal(self):
        """Devuelve el decimal o un None si hay error"""
        try:
            #Due to database precision (18,6) debe redondear a 10^12
            a=Decimal(self.text())
            if a<Decimal(1000000000000):
                return a
            else:
                return None
        except:
            return None

    def float(self):
        try:
            return float(self.text())
        except:
            return None
            
    def setText(self, num):
        """This funcion  overrides QLineEdit settext and lets enter numbers, int, float, decimals"""
        super(myQLineEdit, self).setText(str(num))
        

    def mouseDoubleClickEvent(self, event):
        print("MOUSEDOUBLECLICKEVENT")
        self.doubleClicked.emit()
        print("EMITEED")


class myQLineEditValidated(QLineEdit):
    validated=pyqtSignal()
    refused=pyqtSignal()
    def __init__(self, parent):
        QWidget.__init__(self, parent)       
        self.textChanged.connect(self.on_textChanged)

    def setBackgroundRed(self, red):
        if red==True:
            css = """QLineEdit { background-color: rgb(255, 182, 182); }"""
        else:
            css=""
        self.setStyleSheet(css)
        
    def isValid(self):
        raise NotImplementedError()
 
    @pyqtSlot(str)
    def on_textChanged(self, text):
        if self.isValid():        
            self.setBackgroundRed(False)
            self.validated.emit()
        else:
            self.setBackgroundRed(True)
            self.refused.emit()

## QLineEdit that changes to red color if text is not a valid bank account
class myQLineEditValidatingAccount(myQLineEditValidated):
    def __init__(self, parent):
        myQLineEditValidated.__init__(self, parent)
        
    def isValid(self):
        try:
            iban.validate(self.text())
            return True
        except:
            return False

## QLineEdit that changes to red color if text is not a valid credit card
class myQLineEditValidatingCreditCard(myQLineEditValidated):
    def __init__(self, parent):
        myQLineEditValidated.__init__(self, parent)
        
    def isValid(self):
        try:
            return self.checkCreditCardNumber(self.text())
        except:
            return False
            
    def checkCreditCardNumber(self, cc_number=''):
        sum_ = 0
        parity = len(cc_number) % 2
        for i, digit in enumerate([int(x) for x in cc_number]):
            if i % 2 == parity:
                digit *= 2
                if digit > 9:
                    digit -= 9
            sum_ += digit
        if sum_ % 10 == 0:
            return True
        return False


## Class to manage decimals, with None values showing a suffix
class myQLineEditPlus(QWidget):
    changed=pyqtSignal()
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.parent=parent
        self.lbl=QLabel(self)
        self.chk=QCheckBox(self)
        self.chk.setFocusPolicy(Qt.NoFocus)
        self.txt=QLineEdit(self)
        self.lblSuffix=QLabel(self)
        self.lay = QHBoxLayout(self)
        self.lay.addWidget(self.lbl)
        self.lay.addWidget(self.chk)
        self.lay.addWidget(self.txt)
        self.lay.addWidget(self.lblSuffix)
        self.setLayout(self.lay)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        self.lbl.setSizePolicy(sizePolicy)


        self.setSuffix("")
        self.setValue(None)
        self.setLabel(self.tr("Add a value"))

        self.chk.stateChanged.connect(self.on_chk_stateChanged)
        self.txt.textChanged.connect(self.on_textChanged)
        self.txt.setMaxLength(30)
        self.txt.setAlignment(Qt.AlignRight)


    ## Functión to get the suffix in a label next to qlineedit
    def getSuffix(self):
        return self.lblSuffix.text()

    ## Functión to set the suffix in a label next to qlineedit    
    def setSuffix(self, value):
        if value==None or value=="":
            self.lblSuffix.hide()
        else:
            self.lblSuffix.show()
            self.lblSuffix.setText(value)

    ## Functión to get the label next to qlineedit
    def getLabel(self):
        return self.lbl.text()

    ## Functión to set the label next to qlineedit    
    def setLabel(self, value):
        value="" if value==None else value
        if value=="":
            self.lbl.hide()
        else:
            self.lbl.show()
            self.lbl.setText(value)

    def value(self):
        if self.chk.isChecked()==False:
            return None
        if self.isNumber():
            return Decimal(self.txt.text())
        return None

    def setValue(self, v):
        self.txt.blockSignals(True)
        if v==None:
            self.chk.setCheckState(Qt.Unchecked)
            self.txt.setEnabled(False)
            self.txt.setText("")
        else:
            self.chk.setCheckState(Qt.Checked)
            self.txt.setEnabled(True)
            self.txt.setText(str(v))
        self.txt.blockSignals(False)
        self.changed.emit()

    def on_chk_stateChanged(self, state):
        if state==Qt.Unchecked:
            self.setValue(None)
        else:
            self.setValue("0")

    def isChecked(self):
        return self.chk.isChecked()

    def isValid(self):
        if self.isNumber() or self.chk.isChecked()==False:
            return True
        else:
            return False

    def isNumber(self):
        try:
            Decimal(self.txt.text())
            return True
        except:
            return False

    @pyqtSlot(str)
    def on_textChanged(self, text):
        pos=self.txt.cursorPosition()
        text=text.replace(",", ".")
        text=text.replace("e", "0")#Avoids scientific numbers
        self.setValue(text)
        if self.isChecked()==False:
            self.txt.setStyleSheet("QLineEdit { background-color: rgb(239, 239, 239); }")
        elif self.isNumber():
            self.txt.setStyleSheet("QLineEdit { background-color: rgb(255, 255, 255); }")
        else:
            self.txt.setStyleSheet("QLineEdit { background-color: rgb(255, 182, 182); }")
        self.txt.setCursorPosition(pos)


    def setMandatory(self, b):
        if b==True:
            self.chk.hide()
            self.chk.setCheckState(Qt.Checked)
            #self.txt.setText("0")
            #self.txt.setEnabled(True)
        else:
            self.chk.show()
