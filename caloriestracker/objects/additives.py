from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable

class Additive:
    def __init__(self, mem, id=None, name=None, description=None, risk=None):
        self.mem=mem
        self.id=id
        self.name=self.mem.trHS(name)#E121
        self.description=self.mem.trHS(description)#Acido ...
        self.risk=risk
        
    def __str__(self):
        return "{}: {}".format(self.name, self.description)
        
    def qicon(self):
        if self.risk==None:
            return QIcon(":/caloriestracker/empty.svg")
        return self.risk.qicon()
        
        
class AdditiveManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=mem
        
def Additive_from_row(mem, row):
    return Additive(mem, row['id'], row['name'], row['description'], mem.data.additiverisks.find_by_id(row['additiverisks_id']))
        
def AdditiveManager_from_sql(mem, sql, sql_args=[]):
    r=AdditiveManager(mem)
    rows=mem.con.cursor_rows(sql, sql_args)
    for row in rows:
        r.append(Additive_from_row(mem, row))
    return r
    
def AdditiveManager_all(mem):
    return AdditiveManager_from_sql(mem, "select * from additives order by name")

def AdditiveManager_from_integer_list__mem(mem, arr):
    r=AdditiveManager(mem)
    if arr is not None:
        for n in arr:
            r.append(mem.data.additives.find_by_id(n))
    return r
    
