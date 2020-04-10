from PyQt5.QtCore import QObject
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable
class FoodType:
    def __init__(self, mem, id=None, name=None):
        self.mem=mem
        self.id=id
        self.name=self.mem.trHS(name)
        
class FoodTypeManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=mem
        
def FoodType_from_row(mem, row):
    return FoodType(mem, row['id'], row['name'])
        
def FoodTypeManager_from_sql(mem, sql, sql_args=[]):
    r=FoodTypeManager(mem)
    rows=mem.con.cursor_rows(sql, sql_args)
    for row in rows:
        r.append(FoodType_from_row(mem, row))
    r.order_by_name()
    return r
    
def FoodTypeManager_all(mem):
    return FoodTypeManager_from_sql(mem, "select * from foodtypes")
