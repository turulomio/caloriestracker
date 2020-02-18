
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QApplication, QProgressDialog, QCompleter
from caloriestracker.casts import b2s, str2bool
from caloriestracker.text_inputs import input_boolean, input_integer_or_none
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable

from datetime import datetime
from logging import debug
class CompanySystem:
    ##CompanySystem(mem)
    ##CompanySystem(mem,rows)
    ##CompanySystem(mem,name,last, id)
    def __init__(self, *args):        
        def init__create(name,  last, id):
            self.name=name
            self.last=last
            self.id=id
            return self
        # #########################################
        self.mem=args[0]
        if len(args)==1:#CompanySystem(mem)
            init__create(*[None]*4)
        elif len(args)==2:#CompanySystem(mem,rows)
            init__create(args[1]['name'], args[1]['last'], args[1]['id'])
        elif len(args)==4:#CompanySystem(mem,name,last,id)
            init__create(*args[1:])
        self.system_company=True

    def __repr__(self):
        return self.fullName()

    def is_deletable(self):
        products=self.mem.con.cursor_one_field("select count(*) from allproducts where companies_id =%s and system_company=%s", (self.id, self.system_company))
        personalproducts=self.mem.con.cursor_one_field("select count(*) from allproducts where companies_id =%s and system_company=%s", (self.id, self.system_company))
        sum=products+personalproducts
        if self.system_company==True or sum>0:
            return False
        return True

    def fullName(self):
        if self.mem.debuglevel=="DEBUG":
            system="S" if self.system_company==True else "P"
            return "{}. #{}{}".format(self.name, system, self.id)
        else:
            return "{}".format(self.name)

    def save(self):
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("insert into companies(name,last) values (%s, %s) returning id", (self.name, self.last))
        else:
            self.mem.con.execute("update companies set name=%s,last=%s where id=%s", (self.name, datetime.now(), self.id))
    
    def sql_insert(self, table="companies"):
        return b2s(self.mem.con.mogrify("insert into "+table +"(name, last, id) values (%s, %s, %s);", (self.name, self.last, self.id)))
    def sql_update(self, table="companies"):
        return b2s(self.mem.con.mogrify("update "+table +" set name=%s, last=%s where id=%s;", (self.name, self.last, self.id)))

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
                
            o=CompanySystem(self.mem, row)
            self.append(o)
        cur.close()

class CompanyPersonal(CompanySystem):
    def __init__(self, *args):
        CompanySystem.__init__(self, *args)
        self.system_company=False
        
    def save(self):
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("insert into personalcompanies(name,last) values (%s, %s) returning id", (self.name, self.last))
        else:
            self.mem.con.execute("update personalcompanies set name=%s, last=%s where id=%s", (self.name, self.last, self.id))

    def delete(self):
        if self.is_deletable()==True:
            self.mem.con.execute("delete from personalcompanies where id=%s", (self.id, ))
        else:
            debug("I didn't delete this company because is not deletable")

class CompanyAllManager(QObject, ObjectManager_With_IdName_Selectable):
    ## ProductAllManager(mem)#Loads all database
    def __init__(self, *args):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=args[0]

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
        wdg.setDataFromManager(
            [self.tr("Name"), self.tr("Number of products"), self.tr("Last update")], 
            None,
            self, 
            [
                ["fullName", []], 
                ["get_number_products", []], 
                "last", 
            ], 
        )   
        for i, o in enumerate(self.arr):
            wdg.table.item(i, 0).setIcon(o.qicon())


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
                
            o=CompanyPersonal(self.mem, row)
            self.append(o)
        cur.close()
   

