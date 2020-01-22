from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSpinBox
from logging import error


## Class used to distribute an amount. It's not used to set 3 values
## Amount is set with self.setValue(a) it distribute a equitative
## Amount is set with three values The sum of them will be the amount to distribute
class wdgDistributeIntegerBetween3(QWidget):
    valuesChanged=pyqtSignal()
    def __init__(self, parent=None):
        QWidget.__init__(self)
        self.parent=parent

        self.lblA=QLabel(self)
        self.lblB=QLabel(self)
        self.lblC=QLabel(self)
        self._setup_qspinboxes()

        self.lay = QHBoxLayout(self)
        self.lay.addWidget(self.lblA)
        self.lay.addWidget(self.spnA)
        self.lay.addWidget(self.lblB)
        self.lay.addWidget(self.spnB)
        self.lay.addWidget(self.lblC)
        self.lay.addWidget(self.spnC)
        self.setLayout(self.lay)

        for spn in [self.spnA, self.spnB, self.spnC]:
            spn.setAlignment(Qt.AlignRight)
        for lbl in [self.lblA, self.lblB, self.lblC]:
            lbl.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            
        self.spnA.valueChanged.connect(self._on_a_valueChanged)
        self.spnB.valueChanged.connect(self._on_b_valueChanged)
        self.spnC.valueChanged.connect(self._on_c_valueChanged)

    ## Blocks all spins signals
    def _block_all_signals(self, boolean):
        self.spnA.blockSignals(boolean)
        self.spnB.blockSignals(boolean)
        self.spnC.blockSignals(boolean)
            
    def _on_a_valueChanged(self, value):
        self._block_all_signals(True)
        diff=self._lasta-value
        if value<self._lasta:
            self.spnB.setValue(self.spnB.value()+diff)
        else:
            self.spnB.setValue(self.spnB.value()+diff)
        self._lasta=value
        self._lastb=self.spnB.value()
        self._block_all_signals(False)    
        
        self.valuesChanged.emit()
    
    def _on_b_valueChanged(self, value):
        self._block_all_signals(True)
        diff=self._lastb-value
        if value<self._lastb:
            self.spnC.setValue(self.spnC.value()+diff)
        else:
            self.spnC.setValue(self.spnC.value()+diff)
        self._lastb=value
        self._lastc=self.spnC.value()
        self._block_all_signals(False)
        self.valuesChanged.emit()

    def _on_c_valueChanged(self, value):
        self._block_all_signals(True)
        diff=self._lastc-value
        if value<self._lastc:
            self.spnA.setValue(self.spnA.value()+diff)
        else:
            self.spnA.setValue(self.spnA.value()+diff)
        self._lastc=value
        self._lasta=self.spnA.value()
        self._block_all_signals(False)
        self.valuesChanged.emit()
       
    ## Sets labels beside spinboxes
    def setLabels(self,a,b,c):
        self.lblA.setText(a)
        self.lblB.setText(b)
        self.lblC.setText(c)

    def _setup_qspinboxes(self):
        self.spnA=QSpinBox(self)
        self.spnB=QSpinBox(self)
        self.spnC=QSpinBox(self)

    ## if b or c are None it makes an equitative distribution
    ## This is used on init, so it doesn't emit signals
    ## Amount is set with self.setValue(a) it distribute a equitative
    ## Amount is set with three values The sum of them will be the amount to distribute
    def setValues(self, a, b=None, c=None):
        self._block_all_signals(True)
        if a==None:
            error("a can't be None")
        if b==None or c==None:
            a_3=int(a/3)
            self.spnA.setValue(a_3)
            self.spnB.setValue(a_3)
            self.spnC.setValue(a-2*a_3)
        else:
            self.spnA.setValue(a)
            self.spnB.setValue(b)
            self.spnC.setValue(c)
        self._lasta=self.spnA.value()
        self._lastb=self.spnB.value()
        self._lastc=self.spnC.value()
        self._block_all_signals(False)
        self.spnA.setMaximum(self._lasta+self._lastb+self._lastc)
        self.spnB.setMaximum(self._lasta+self._lastb+self._lastc)
        self.spnC.setMaximum(self._lasta+self._lastb+self._lastc)
        
    ## @return List with the three values
    def values(self):
        return [self.spnA.value(), self.spnB.value(), self.spnC.value()]

    ## Sets the suffix of the spinboxes
    def setSuffix(self, suffix):
        self.spnA.setSuffix(suffix)
        self.spnB.setSuffix(suffix)
        self.spnC.setSuffix(suffix)

if __name__ == '__main__':
    from sys import exit
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])

    w = wdgDistributeIntegerBetween3()
    w.move(300, 300)
    w.setSuffix(" %")
    w.setValues(100)
    w.setLabels("Carbohydrate","Fat","Protein")
    w.setWindowTitle('wdgDistributeAmount example')
    w.show()

    exit(app.exec_())
