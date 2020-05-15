from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QProgressDialog, QApplication
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable
from caloriestracker.objects.biometrics import BiometricsManager, BiometricsManager_all_from_db
from datetime import date, timedelta
from logging import debug

class User:
    def __init__(self, mem, name=None, male=None, birthday=None, starts=None, ends=None, id=None):
        self.mem=mem
        self.name=name
        self.male=male
        self.birthday=birthday
        self.starts=starts
        self.ends=ends
        self.id=id
        ## Variable with the current product status
        ## 0 No data
        ## 1 Loaded all biometrics
        self.status=0
        
    ## @param statusneeded  Integer with the status needed 
    ## @param downgrade_to Integer with the status to downgrade before checking needed status. If None it does nothing
    def needStatus(self, statusneeded, downgrade_to=None):
        if downgrade_to!=None:
            self.status=downgrade_to
        
        if self.status==statusneeded:
            return
        #0
        if self.status==0 and statusneeded==1: #MAIN
            self.biometrics=BiometricsManager_all_from_db(self.mem, self)
            self.status=1

    
    def __repr__(self):
        if self.mem.debuglevel=="DEBUG":
            return "User: {}. #{}".format(self.name,self.id)
        else:
            return "{}".format(self.name)
    
    ##Must be loaded later becaouse usermanager searches in users and is not yet loaded
    def load_biometrics(self):
        if self.id==None:
            self.biometrics=BiometricsManager(self.mem)
        else:
            self.biometrics=BiometricsManager_all_from_db(self.mem, self.id)
           
    def is_deletable(self):
        biometrics=self.mem.con.cursor_one_field("select count(*) from biometrics where users_id=%s", (self.id, ))
        meals=self.mem.con.cursor_one_field("select count(*) from meals where users_id=%s", (self.id, ))
        debug(f"User has {biometrics} biometric data and {meals} meals")
        if biometrics+meals>0 or self.id==1:
            return False
        return True
        
    def delete(self):
        if self.is_deletable()==True:
            self.mem.con.execute("delete from users where id=%s", (self.id, ))
        else:
            debug("I couldn't delete the user because it has dependent data")

    def save(self):
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("insert into users (name, male, birthday, starts, ends) values ( %s, %s, %s, %s, %s) returning id",  
                    (self.name, self.male, self.birthday, self.starts, self.ends))
        else:
            self.mem.con.execute("update users set name=%s, male=%s, birthday=%s, starts=%s, ends=%s where id=%s", 
                    (self.name, self.male, self.birthday, self.starts, self.ends, self.id))

    def age(self):
        return (date.today() - self.birthday) // timedelta(days=365.2425)

    def qicon(self):
        if self.male==True:
            return QIcon(":/caloriestracker/keko.png")
        else:
            return QIcon(":/caloriestracker/keka.png")
            
## Class to manage users
## UserManager(mem)
## UserManager(mem,sql,progress)
class UserManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=mem

    def qtablewidget(self, wdg):                
        data=[]
        for i, o in enumerate(self.arr):
            data.append([
                o.name,
                o.male,
                o.birthday, 
                o.starts, 
                o, 
            ])
        wdg.setDataWithObjects(
            [self.tr("Name"), self.tr("Male"), self.tr("Birthday"), self.tr("Starts")], 
            None, 
            data, 
            zonename=self.mem.localzone
        )

def User_from_row(mem, row):
    r=User(mem)
    r.name=row['name']
    r.male=row['male']
    r.birthday=row['birthday']
    r.starts=row['starts']
    r.ends=row['ends']
    r.id=row['id']
    return r
    
    
def UserManager_from_db(mem, sql,  progress):
    r=UserManager(mem)
    rows=mem.con.cursor_rows(sql)
    if progress==True:
        pd= QProgressDialog(r.tr("Loading {0} users from database").format(len(rows)),None, 0,len(rows))
        pd.setWindowIcon(QIcon(":/caloriestracker/coins.png"))
        pd.setModal(True)
        pd.setWindowTitle(r.tr("Loading users..."))
        pd.forceShow()
    for i, rowms in enumerate(rows):
        if progress==True:
            pd.setValue(i)
            pd.update()
            QApplication.processEvents()
        r.append(User_from_row(mem, rowms))
    return r
