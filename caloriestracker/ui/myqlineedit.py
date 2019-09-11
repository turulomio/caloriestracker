from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLineEdit, QWidget
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
