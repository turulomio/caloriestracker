from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable
from caloriestracker.libcaloriestrackertypes import eAdditiveRisk

## https://www.aditivos-alimentarios.com/2016/01/E260.html

## Low No perjudicial o a muy altas dosis
## Medium A grandes dosis problemas o incluso cancerigeno.
## High problemas a dosis bajas y altas
class AdditiveRisk:
    def __init__(self, mem, id=None, name=None, risk=None):
        self.mem=mem
        self.id=id
        self.name=self.mem.trHS(name)
        
    def __str__(self):
        return self.name
        
    def qicon(self):
        if self.id==eAdditiveRisk.Low:
            return QIcon(":/caloriestracker/circle_green.png")
        elif self.id==eAdditiveRisk.Medium:
            return QIcon(":/caloriestracker/circle_yellow.png")
        elif self.id==eAdditiveRisk.NoRisk:
            return QIcon(":/caloriestracker/circle_white.png")
        elif self.id==eAdditiveRisk.NotEvaluated:
            return QIcon(":/caloriestracker/circle_gray.png")
        else:
            return QIcon(":/caloriestracker/circle_red.png")

class AdditiveRiskManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=mem
        
def AdditiveRisk_from_row(mem, row):
    return AdditiveRisk(mem, row['id'], row['name'])
        
def AdditiveRiskManager_from_sql(mem, sql, sql_args=[]):
    r=AdditiveRiskManager(mem)
    rows=mem.con.cursor_rows(sql, sql_args)
    for row in rows:
        r.append(AdditiveRisk_from_row(mem, row))
    return r
    
def AdditiveRiskManager_all(mem):
    return AdditiveRiskManager_from_sql(mem, "select * from additiverisks order by name")

