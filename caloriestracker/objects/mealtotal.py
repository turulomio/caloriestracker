from PyQt5.QtCore import QObject
from caloriestracker.libmanagers import ObjectManager_Selectable


class MealTotal:
    def __init__(self, mem, date=None, calories=None):
        self.mem=mem
        self.date=date
        self.calories=calories
        
    def load_biometrics(self):
        self.biometrics=self.mem.user.biometrics.find_by_date(self.date)
        
    ## @ True if meals in arr have a daily bmr fullfillment. None if no data
    def daily_fulfillment(self):
        if self.biometrics is None:
            return None
        if self.calories>self.biometrics.bmr():
            return False
        else:
            return True
        
        
## Class to manage products
class MealTotalManager(QObject, ObjectManager_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_Selectable.__init__(self)
        
    def load_biometrics(self):
        for o in self:
            o.load_biometrics()
        
    ## Used to fill fullfillment chart
    def dictionary_of_fulfillment(self):        
        d={self.tr("Yes"):0,  self.tr("No"):0, self.tr("Without data"):0}
        for o in self:
            if o.biometrics is None:
                d[self.tr("Without data")]=d[self.tr("Without data")]+1
            elif o.biometrics.bmr()>o.calories:
                d[self.tr("Yes")]=d[self.tr("Yes")]+1
            elif o.biometrics.bmr()<=o.calories:
                d[self.tr("No")]=d[self.tr("No")]+1
        return d



def MealTotal_from_row(mem, row):
    r=MealTotal(mem)
    r.date=row['date']
    r.calories=row['calories']
    return r

def MealTotalManager_from_db(mem, sql):
    r=MealTotalManager(mem)
    for row in mem.con.cursor_rows(sql):
        r.append(MealTotal_from_row(mem, row))
    return r
        
    
def MealTotalManager_all(mem, user):
    sql="""
    select 
    datetime::date as date, 
    sum(meals.amount*allproducts.calories/allproducts.amount) as calories 
    from 
    meals, 
    allproducts 
    where 
    meals.products_id=allproducts.id and 
    meals.system_product=allproducts.system_product and 
    users_id={}
    group by 
    datetime::date 
    order by 
    datetime::date
    """.format(user.id)
    return MealTotalManager_from_db(mem, sql)
