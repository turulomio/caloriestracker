from PyQt5.QtCore import QObject
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable

## https://www.aditivos-alimentarios.com/2016/01/E260.html

## Low No perjudicial o a muy altas dosis
## Medium A grandes dosis problemas o incluso cancerigeno.
## High problemas a dosis bajas y altas
class AdditiveRisk:
    def __init__(self, mem, id=None, name=None, risk=None):
        self.mem=mem
        self.id=id
        self.name=self.mem.trHS(name)
        
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

