from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QApplication, QProgressDialog, QCompleter
from caloriestracker.casts import b2s, str2bool
from caloriestracker.text_inputs import input_boolean, input_integer_or_none
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable
from datetime import datetime
from logging import debug

class CompanySystem:
    def __init__(self, mem=None, name=None,  last=None, obsolete=None, id=None):
        self.mem=mem
        self.name=name
        self.last=last
        self.obsolete=obsolete
        self.id=id
        self.system_company=True

    def __repr__(self):
        return self.fullName()

    def is_deletable(self):
        products=self.mem.con.cursor_one_field("select count(*) from allproducts where companies_id =%s and system_company=%s", (self.id, self.system_company))
        personalproducts=self.mem.con.cursor_one_field("select count(*) from allproducts where companies_id =%s and system_company=%s", (self.id, self.system_company))
        if products+personalproducts>0:
            return False
        return True

    def logical_delete(self):        
        self.obsolete=True
        self.last=datetime.now()
        self.save()
            
    def delete(self):
        if self.__class__.__name__=="CompanyPersonal":
            table="personalcompanies"
        else:
            table="companies"
        if self.is_deletable()==True:
            self.mem.con.execute(self.sql_delete(table))
        else:
            debug("I didn't delete this company because is not deletable")

    def fullName(self):
        if self.mem.debuglevel=="DEBUG":
            system="S" if self.system_company==True else "P"
            return "{}. #{}{}".format(self.name, system, self.id)
        else:
            return "{}".format(self.name)

    def save(self):
        if self.__class__.__name__=="CompanyPersonal":
            table="personalcompanies"
        else:
            table="companies"
        
        if self.id==None:
            #print(self.sql_insert(table, returning_id=True))
            if table=="companies":# id it's not linked to a sequence, so I must add a id. Only used for maintenance mode. Can't be two editors at the same time
                self.id=self.mem.con.cursor_one_field("select max(id)+1 from companies")
                self.mem.con.execute(self.sql_insert(table, returning_id=False))
            else:# personalproducts has sequence
                self.id=self.mem.con.cursor_one_field(self.sql_insert(table, returning_id=True))
        else:
            self.mem.con.execute(self.sql_update(table))
    
    def sql_insert(self, table="companies", returning_id=True):
        sql="insert into public."+table +"(name, last, obsolete) values (%s, %s, %s) returning id;"
        sql_parameters=(self.name, self.last, self.obsolete)
        if returning_id==True:
            r=self.mem.con.mogrify(sql, sql_parameters)
        else:
            sql=sql.replace(") values (", ", id ) values (")
            sql=sql.replace(") returning id", ", %s)")
#            print(sql)
#            print(sql_parameters)
            r=self.mem.con.mogrify(sql, sql_parameters+(self.id, ))
        return b2s(r)
        
    def sql_update(self, table="companies"):
        return b2s(self.mem.con.mogrify("update public."+table +" set name=%s, last=%s, obsolete=%s where id=%s;", (self.name, self.last, self.obsolete, self.id)))

    ## @param table String with the name of table used to generate sql command
    def sql_delete(self, table):
        return b2s(self.mem.con.mogrify("delete from public."+ table + " where id=%s;", (self.id, )))
            
    def qicon(self):
        if self.system_company==True:
            return QIcon(":/caloriestracker/company.png")
        else:
            return QIcon(":/caloriestracker/hucha.png")

    ## Generates an string with id and system_product
    def string_id(self):
        return "{}#{}".format(self.id, self.system_company)

    @staticmethod
    def string_id2tuple(string_id):
        if string_id==None:
            return None
        a=string_id.split("#")
        return int(a[0]), str2bool(a[1])
        
    ## Function to get the number of products in mem
    def get_number_products(self):
        r=0
        for p in self.mem.data.products.arr:
            if p.company is not None and p.company.id==self.id and p.company.system_company==self.system_company:
                r=r+1
        return r

class CompanySystemManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=mem


    def find_by_id_system(self,  id ,  system):
        for o in self.arr:
            if o.id==id and o.system_company==system:
                return o
        return None

    ## Find by generated string with id and system_product
    def find_by_string_id(self, stringid):
        if stringid==None:
            return None
        return self.find_by_id_system(*CompanySystem.string_id2tuple(stringid))
        
    def load_from_db(self, sql,  progress=False):
        self.clean()
        cur=self.mem.con.cursor()
        cur.execute(sql)
        if progress==True:
            pd= QProgressDialog(self.tr("Loading {0} system companies from database").format(cur.rowcount),None, 0,cur.rowcount)
            pd.setWindowIcon(QIcon(":/caloriestracker/coins.png"))
            pd.setModal(True)
            pd.setWindowTitle(self.tr("Loading system companies..."))
            pd.forceShow()
        for row in cur:
            if progress==True:
                pd.setValue(cur.rownumber)
                pd.update()
                QApplication.processEvents()
            self.append(CompanySystem_from_row(self.mem, row))
        cur.close()
        
    def myqtablewidget(self, wdg):
        myQTableWidget_CompanyManagers(self, wdg)

class CompanyPersonal(CompanySystem):
    def __init__(self, mem=None, name=None,  last=None, obsolete=None, id=None):
        CompanySystem.__init__(self, mem, name, last, obsolete, id)
        self.system_company=False


class CompanyAllManager(QObject, ObjectManager_With_IdName_Selectable):
    ## ProductAllManager(mem)#Loads all database
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.setConstructorParameters(mem)
        self.mem=mem

    def load_all(self):
        system=CompanySystemManager(self.mem)
        system.load_from_db("select * from companies")
        for o in system.arr:
            self.append(o)
        personal=CompanyPersonalManager(self.mem)
        personal.load_from_db("select * from personalcompanies")
        for o in personal.arr:
            self.append(o)
        self.order_by_name()

    def find_by_id_system(self,  id ,  system):
        for o in self.arr:
            if o.id==id and o.system_company==system:
                return o
        return None
                    
    ## Find by generated string with id and system_product
    def find_by_string_id(self, stringid):
        if stringid==None:
            return None
        return self.find_by_id_system(*CompanySystem.string_id2tuple(stringid))
        
    def find_by_input(self, log=True):
        input=input_integer_or_none("Add a company", "")
        if input==None:
            return None
        else:
            system_company=input_boolean("Is a system company?", "T")
            company=self.mem.data.companies.find_by_id_system(int(input), system_company)
            if log:
                print ("  - Selected: {}".format(company))
            return company

    def qcombobox(self, combo, selected=None):
        combo.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.order_by_name()
        for o in self.arr:
            combo.addItem(o.qicon(), o.fullName(), o.string_id())
        if selected!=None:
            combo.setCurrentIndex(combo.findData(selected.string_id()))
    
    def myqtablewidget(self, wdg):
        myQTableWidget_CompanyManagers(self, wdg)
        
class CompanyPersonalManager(CompanySystemManager):
    def __init__(self, mem):
        CompanySystemManager.__init__(self, mem)

    def load_from_db(self, sql,  progress=False):
        self.clean()
        cur=self.mem.con.cursor()
        cur.execute(sql)#"select * from products where id in ("+lista+")" 
        if progress==True:
            pd= QProgressDialog(self.tr("Loading {0} personal companies from database").format(cur.rowcount),None, 0,cur.rowcount)
            pd.setWindowIcon(QIcon(":/caloriestracker/coins.png"))
            pd.setModal(True)
            pd.setWindowTitle(self.tr("Loading personal companies..."))
            pd.forceShow()
        for row in cur:
            if progress==True:
                pd.setValue(cur.rownumber)
                pd.update()
                QApplication.processEvents()
            self.append(CompanyPersonal_from_row(self.mem, row))
        cur.close()
   
def CompanySystem_from_row(mem, row):
    return CompanySystem(mem, row['name'], row['last'], row['obsolete'], row['id'])

def CompanyPersonal_from_row(mem, row):
    return CompanyPersonal(mem, row['name'], row['last'], row['obsolete'], row['id'])

def myQTableWidget_CompanyManagers(manager, wdg):     
    wdg.setDataFromManager(
        [wdg.tr("Name"), wdg.tr("Number of products"), wdg.tr("Last update")], 
        None,
        manager, 
        [
            ["fullName", []], 
            ["get_number_products", []], 
            "last", 
        ], 
        additional=myQTableWidget_CompanyManagers_additional
    )

def myQTableWidget_CompanyManagers_additional(wdg):     
    for i, o in enumerate(wdg.manager.arr):
        wdg.table.item(i, 0).setIcon(o.qicon())
        if o.obsolete==True:
            wdg.setRowStrikeOut(i)
