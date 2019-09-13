## @namespace caloriestracker.libxulpymoneytypes
## @brief Package with all xulpymoney types.
from PyQt5.QtGui import QColor

## Class with used QColors in app
class eQColor:
    Red=QColor(255, 148, 148)
    Green=QColor(148, 255, 148)


## Types for dt strings. Used in dtaware2string function
class eDtStrings:
    ## Parsed for ui
    QTableWidgetItem=1
    
    ## 20190909 0909
    Filename=2
    
    ## 201909090909
    String=3
