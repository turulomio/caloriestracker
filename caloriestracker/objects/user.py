
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QProgressDialog, QApplication
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable
from caloriestracker.objects.biometrics import BiometricsManager, Biometrics
from datetime import date, timedelta
from logging import debug

class User:
    ##User(mem)
    ##User(mem,rows) #Uses products_id and users_id in row
    ##User(mem, name, male, birthday, starts, ends, id):
    def __init__(self, *args):        
        def init__create( name, male, birthday, starts, ends, id):
            self.name=name
            self.male=male
            self.birthday=birthday
            self.starts=starts
            self.ends=ends
            self.id=id
        # #########################################
        self.mem=args[0]
        if len(args)==1:#User(mem)
            init__create(*[None]*6)
        elif len(args)==2:#User(mem,rows)
            init__create(args[1]['name'], args[1]['male'], args[1]['birthday'], args[1]['starts'],  args[1]['ends'], args[1]['id'])
        elif len(args)==7:#User(mem, name, male, birthday, starts, ends, id):
            init__create(*args[1:])
    
    def __repr__(self):
        if self.mem.debuglevel=="DEBUG":
            return "User: {}. #{}".format(self.name,self.id)
        else:
            return "{}".format(self.name)
    
    ##Must be loaded later becaouse usermanager searches in users and is not yet loaded
    def load_last_biometrics(self):
        #Loads biometrics
        if self.id==None:
            self.last_biometrics=Biometrics(self.mem)
        else:
            biometrics=BiometricsManager(self.mem, self.mem.con.mogrify("select * from biometrics where users_id= %s order by datetime desc limit 1", (self.id, )), False)
            if biometrics.length()==1:
                self.last_biometrics=biometrics.first()
            else:
                self.last_biometrics=Biometrics(self.mem)
           
    def is_deletable(self):
        biometrics=self.mem.con.cursor_one_field("select count(*) from biometrics")
        meals=self.mem.con.cursor_one_field("select count(*) from meals")
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
    def __init__(self, *args):
        def load_from_db(sql,  progress):
            self.clean()
            cur=self.mem.con.cursor()
            cur.execute(sql)
            if progress==True:
                pd= QProgressDialog(self.tr("Loading {0} users from database").format(cur.rowcount),None, 0,cur.rowcount)
                pd.setWindowIcon(QIcon(":/caloriestracker/coins.png"))
                pd.setModal(True)
                pd.setWindowTitle(self.tr("Loading users..."))
                pd.forceShow()
            for rowms in cur:
                if progress==True:
                    pd.setValue(cur.rownumber)
                    pd.update()
                    QApplication.processEvents()
                self.append(User(self.mem, rowms))
            cur.close()
        # ####################################################
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=args[0]
        if len(args)==3:
            load_from_db(*args[1:])
    
    def load_last_biometrics(self):
        for user in self.arr:
            user.load_last_biometrics()

    ## It's a staticmethod due to it will be used in ProductAllManager
    def qtablewidget(self, wdg):                
        data=[]
        for i, o in enumerate(self.arr):
            data.append([
                o.name,
                o.male,
                o.birthday, 
                o.starts, 
            ])
        wdg.setData(
            [self.tr("Name"), self.tr("Male"), self.tr("Birthday"), self.tr("Starts")], 
            None, 
            data, 
            zonename=self.mem.localzone
        )
