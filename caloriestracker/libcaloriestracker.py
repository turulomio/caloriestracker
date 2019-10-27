## @namespace caloriestracker.libcaloriestracker
## @brief Package with all caloriestracker core classes .
from PyQt5.QtCore import Qt,  QObject
from PyQt5.QtGui import QIcon,  QColor
from PyQt5.QtWidgets import QTableWidgetItem, QApplication, QProgressDialog, QCompleter
from datetime import date,  timedelta, datetime

from decimal import Decimal
from caloriestracker.libcaloriestrackerfunctions import a2s, ca2s, n2s, rca2s
from caloriestracker.casts import str2bool, b2s
from caloriestracker.text_inputs import input_boolean, input_integer_or_none
from caloriestracker.libcaloriestrackertypes import eProductComponent, eActivity, eWeightWish
from caloriestracker.ui.qtablewidgetitems import qtime, qleft, qright, qnumber_limited, qnumber, qdatetime, qdate, qbool
from caloriestracker.libmanagers import ObjectManager_With_Id_Selectable,  ManagerSelectionMode, ObjectManager_With_IdName_Selectable, ObjectManager_With_IdDatetime_Selectable
from colorama import Fore, Style
from logging import debug

## TMB x 1,2: Poco o ningún ejercicio                     +
##        |                                |       |          |            | TMB x 1,375: Ejercicio ligero (1 a 3 días a la semana) +
##        |                                |       |          |            | TMB x 1,55: Ejercicio moderado (3 a 5 días a la semana)+
##        |                                |       |          |            | TMB x 1,72: Deportista (6 -7 días a la semana)         +
##        |                                |       |          |            | TMB x 1,9: Atleta (Entrenamientos mañana y tarde)
##    Sedentary. 
##    Lightly active. If you exercise lightly one to three days a week, multiply your BMR by 1.375.
##    Moderately active. If you exercise moderately three to five days a week, multiply your BMR by 1.55.
##    Very active. If you engage in hard exercise six to seven days a week, multiply your BMR by 1.725.
##    Extra active. If you engage in very hard exercise six to seven days a week or have a physical job, multiply your BMR by 1.9.
class Activity(QObject):
    ##Biometrics(mem)
    ##Biometrics(mem,id,name, description,multiplier)
    def __init__(self, mem, name, description, multiplier, id):
            self.mem=mem
            self.name=name
            self.description=description
            self.multiplier=multiplier
            self.id=id

class ActivityManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=mem
        self.append(Activity(self.mem, self.tr("Sedentary"), self.tr("If you get minimal or no exercise"), Decimal(1.2), eActivity.Sedentary))
        self.append(Activity(self.mem, self.tr("Lightly active"), self.tr("If you exercise moderately three to five days a week"), Decimal(1.375), eActivity.LightlyActive))
        self.append(Activity(self.mem, self.tr("Moderately active"), self.tr("If you exercise moderately three to five days a week"), Decimal(1.55), eActivity.ModeratelyActive))
        self.append(Activity(self.mem, self.tr("Very active"), self.tr("If you engage in hard exercise six to seven days a week"), Decimal(1.725), eActivity.VeryActive))
        self.append(Activity(self.mem, self.tr("Extra active"), self.tr("If you engage in very hard exercise six to seven days a week or have a physical job"), Decimal(1.9), eActivity.ExtraActive))

class WeightWish(QObject):
    def __init__(self, mem, name, id):
            self.mem=mem
            self.name=name
            self.id=id

class WeightWishManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=mem
        self.append(WeightWish(self.mem, self.tr("Lose weight"), eWeightWish.Lose))
        self.append(WeightWish(self.mem, self.tr("Mantain weight"), eWeightWish.Mantain))
        self.append(WeightWish(self.mem, self.tr("Gain weight"), eWeightWish.Gain))

class Percentage:
    def __init__(self, numerator=None, denominator=None):
        self.value=None
        self.setValue(self.toDecimal(numerator),self.toDecimal(denominator))

    def toDecimal(self, o):
        if o==None:
            return o
        elif o.__class__==Decimal:
            return o
        elif o.__class__ in ( int, float):
            return Decimal(o)
        elif o.__class__==Percentage:
            return o.value
        else:
            debug(o.__class__)
            return None
        
    def __repr__(self):
        return self.string()
            
    def __neg__(self):
        """Devuelve otro money con el amount con signo cambiado"""
        if self.value==None:
            return self
        return Percentage(-self.value, 1)
        
    def __lt__(self, other):
        if self.value==None:
            value1=Decimal('-Infinity')
        else:
            value1=self.value
        if other.value==None:
            value2=Decimal('-Infinity')
        else:
            value2=other.value
        if value1<value2:
            return True
        return False
        
    def __mul__(self, value):
        if self.value==None or value==None:
            r=None
        else:
            r=self.value*self.toDecimal(value)
        return Percentage(r, 1)

    def __truediv__(self, value):
        try:
            r=self.value/self.toDecimal(value)
        except:
            r=None
        return Percentage(r, 1)
        
    def setValue(self, numerator,  denominator):
        try:
            self.value=Decimal(numerator/denominator)
        except:
            self.value=None

    def value_100(self):
        if self.value==None:
            return None
        else:
            return self.value*Decimal(100)

    def string(self, rnd=2):
        if self.value==None:
            return "None %"
        return "{} %".format(round(self.value_100(), rnd))
        
    def qtablewidgetitem(self, rnd=2):
        a=QTableWidgetItem(self.string(rnd))
        a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
        if self.value==None:
            a.setForeground(QColor(0, 0, 255))
        elif self.value<0:
            a.setForeground(QColor(255, 0, 0))
        return a
        
    def isValid(self):
        if self.value!=None:
            return True
        return False
        
    def isGETZero(self):
        if self.value>=0:
            return True
        return False
    def isGTZero(self):
        if self.value>0:
            return True
        return False
    def isLTZero(self):
        if self.value<0:
            return True
        return False


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
        
    ## It's a staticmethod due to it will be used in ProductAllManager
    @staticmethod
    def qtablewidget(self, table):        
        table.setColumnCount(3)
        table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Name")))
        table.setHorizontalHeaderItem(1, QTableWidgetItem(self.tr("Number of products")))   
        table.setHorizontalHeaderItem(2, QTableWidgetItem(self.tr("Last update")))
        table.applySettings()
        table.clearContents()
        table.setRowCount(self.length())
        for i, o in enumerate(self.arr):
            table.setItem(i, 0, qleft(o.fullName()))
            table.item(i, 0).setIcon(o.qicon())
            table.setItem(i, 1, qnumber(self.mem.con.cursor_one_field("select count(*) from companies, products where companies.id=products.companies_id and companies.id=%s", (o.id, ))))
            table.setItem(i, 2, qdatetime(o.last, self.mem.localzone))


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

    def qtablewidget(self, table):
        CompanySystemManager.qtablewidget(self, table)
## Clase parar trabajar con las opercuentas generadas automaticamente por los movimientos de las inversiones

## Class to manage products
class ProductManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.setSelectionMode(ManagerSelectionMode.List)
        self.mem=mem

    def load_from_db(self, sql,  progress=False):
        self.clean()
        cur=self.mem.con.cursor()
        cur.execute(sql)#"select * from products where id in ("+lista+")" 
        if progress==True:
            pd= QProgressDialog(self.tr("Loading {0} products from database").format(cur.rowcount),None, 0,cur.rowcount)
            pd.setWindowIcon(QIcon(":/caloriestracker/coins.png"))
            pd.setModal(True)
            pd.setWindowTitle(self.tr("Loading products..."))
            pd.forceShow()
        for rowms in cur:
            if progress==True:
                pd.setValue(cur.rownumber)
                pd.update()
                QApplication.processEvents()
                
            oo=Product(self.mem, rowms)
            self.append(oo)
        cur.close()
        
    @staticmethod
    def find_by_id_system(self,  id ,  system):
        for o in self.arr:
            if o.id==id and o.system_product==system:
                return o
        return None
    
    ## Find by generated string with id and system_product
    @staticmethod
    def find_by_string_id(self, stringid):
        tuple=Product.string_id2tuple(stringid)
        if stringid==None or tuple==None:
            return None
        return ProductManager.find_by_id_system(self, *tuple)
                
    @staticmethod
    def find_by_elaboratedproducts_id(self,  elaboratedproducts_id):
        for p in self.arr:
            if p.elaboratedproducts_id==elaboratedproducts_id:
                return p
        return None

    ## It's a staticmethod due to it will be used in ProductAllManager
    @staticmethod
    def qtablewidget(self, table):        
        table.setColumnCount(9)
        table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Name")))
        table.setHorizontalHeaderItem(1, QTableWidgetItem(self.tr("Company")))
        table.setHorizontalHeaderItem(2, QTableWidgetItem(self.tr("Last update")))
        table.setHorizontalHeaderItem(3, QTableWidgetItem(self.tr("Grams")))
        table.setHorizontalHeaderItem(4, QTableWidgetItem(self.tr("Calories")))
        table.setHorizontalHeaderItem(5, QTableWidgetItem(self.tr("Carbohydrates")))
        table.setHorizontalHeaderItem(6, QTableWidgetItem(self.tr("Protein")))
        table.setHorizontalHeaderItem(7, QTableWidgetItem(self.tr("Fat")))
        table.setHorizontalHeaderItem(8, QTableWidgetItem(self.tr("Fiber")))
   
        table.applySettings()
        table.clearContents()
        table.setRowCount(self.length())
        for i, o in enumerate(self.arr):
            table.setItem(i, 0, qleft(o.fullName()))
            table.item(i, 0).setIcon(o.qicon())
            if o.company==None:
                company=""
            else:
                company=o.company.fullName()
                
            table.setItem(i, 1, qleft(company))
            table.setItem(i, 2, qdatetime(o.last, self.mem.localzone))
            table.setItem(i, 3, qnumber(100))
            table.setItem(i, 4, qnumber(o.component_in_100g(eProductComponent.Calories)))
            table.setItem(i, 5, qnumber(o.component_in_100g(eProductComponent.Carbohydrate)))
            table.setItem(i, 6, qnumber(o.component_in_100g(eProductComponent.Protein)))
            table.setItem(i, 7, qnumber(o.component_in_100g(eProductComponent.Fat)))
            table.setItem(i, 8, qnumber(o.component_in_100g(eProductComponent.Fiber)))

   
    ## Removes a product and return a boolean. NO HACE COMMIT
    def remove(self, o):
        if o.remove():
            ObjectManager_With_Id_Selectable.remove(self, o)
            return True
        return False
        

class ProductPersonalManager(ProductManager):
    def __init__(self, mem):
        ProductManager.__init__(self, mem)

    def load_from_db(self, sql,  progress=False):
        self.clean()
        cur=self.mem.con.cursor()
        cur.execute(sql)#"select * from products where id in ("+lista+")" 
        if progress==True:
            pd= QProgressDialog(self.tr("Loading {0} personal products from database").format(cur.rowcount),None, 0,cur.rowcount)
            pd.setWindowIcon(QIcon(":/caloriestracker/coins.png"))
            pd.setModal(True)
            pd.setWindowTitle(self.tr("Loading personal products..."))
            pd.forceShow()
        for rowms in cur:
            if progress==True:
                pd.setValue(cur.rownumber)
                pd.update()
                QApplication.processEvents()
                
            oo=ProductPersonal(self.mem, rowms)
            self.append(oo)
        cur.close()


class ProductElaborated:
    ##Biometrics(mem)
    ##Biometrics(mem,row)
    def __init__(self, *args):        
        def init__create(name, final_amount, id):
            self.name=name
            self.final_amount=final_amount
            self.id=id
        self.mem=args[0]
        if len(args)==1:
            init__create(None,None, None)
        elif len(args)==2:
            init__create(args[1]['name'],args[1]['final_amount'], args[1]['id'])
        self.status=0
        
    ## ESTA FUNCION VA AUMENTANDO STATUS SIN MOLESTAR LOS ANTERIORES, SOLO CARGA CUANDO stsatus_to es mayor que self.status
    ## @param statusneeded  Integer with the status needed 
    ## @param downgrade_to Integer with the status to downgrade before checking needed status. If None it does nothing
    ## 0 campos del producto
    ## 1  products in 
    def needStatus(self, statusneeded, downgrade_to=None):
        if downgrade_to!=None:
            self.status=downgrade_to
        
        if self.status==statusneeded:
            return
        #0
        if self.status==0 and statusneeded==1: #MAIN            
            self.load_products_in()
            self.status=1

    def load_products_in(self):
            self.products_in=ProductInElaboratedProductManager(self.mem, self, self.mem.con.mogrify("select * from products_in_elaboratedproducts where elaboratedproducts_id=%s",(self.id,)))

    def show_table(self):
        self.products_in.show_table()

    def register_in_personal_products(self):
        selected=self.mem.data.products.find_by_elaboratedproducts_id(self.id)
        if selected==None:
            o=ProductPersonal(
            self.mem,
            self.name, 
            self.final_amount, 
            self.products_in.fat(), 
            self.products_in.protein(), 
            self.products_in.carbohydrate(), 
            None, 
            datetime.now(), 
            self.id, 
            None, 
            self.products_in.calories(), 
            self.products_in.salt(), 
            self.products_in.cholesterol(), 
            self.products_in.sodium(), 
            self.products_in.potassium(), 
            self.products_in.fiber(), 
            self.products_in.sugars(), 
            self.products_in.saturated_fat(), 
            False,
            None)
            o.save() 
            self.mem.data.products.append(o)
            self.mem.data.products.order_by_name()
        else:#It's already in personalproducts
            selected.name=self.name
            selected.amount=self.final_amount
            selected.fat=self.products_in.fat()
            selected.protein=self.products_in.protein()
            selected.carbohydrate=self.products_in.carbohydrate()
            selected.calories=self.products_in.calories()
            selected.fiber=self.products_in.fiber()
            selected.save()

    #DO NOT EDIT THIS ONE COPY FROM PRODUCT AND CHANGE TABLE
    def save(self):
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("""insert into elaboratedproducts (
                    name, final_amount
                    )values (%s, %s) returning id""",  
                    (self.name, self.final_amount))
        else:
            self.mem.con.execute("""update elaboratedproducts set name=%s, final_amount=%s
            where id=%s""", 
            (self.name, self.final_amount, self.id))
        self.needStatus(1)
        self.register_in_personal_products()

            
    def is_deletable(self):
        self.needStatus(1)
        if self.products_in.length()>0:
            return False
        
        selected=self.mem.data.products.find_by_elaboratedproducts_id(self.id)
        if selected!=None and selected.is_deletable()==False:
            return False
        return True

    def delete(self):
        if self.is_deletable()==True:
            self.mem.con.execute("delete from elaboratedproducts where id=%s", (self.id, ))
        else:
            debug("I did not delete the elaborated product because is not deletable")
        

class ProductElaboratedManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=mem

    def load_from_db(self, sql,  progress=False):
        self.clean()
        cur=self.mem.con.cursor()
        cur.execute(sql)#"select * from products where id in ("+lista+")" 
        if progress==True:
            pd= QProgressDialog(self.tr("Loading {0} elaborated products from database").format(cur.rowcount),None, 0,cur.rowcount)
            pd.setWindowIcon(QIcon(":/caloriestracker/coins.png"))
            pd.setModal(True)
            pd.setWindowTitle(self.tr("Loading elaborated products..."))
            pd.forceShow()
        for rowms in cur:
            if progress==True:
                pd.setValue(cur.rownumber)
                pd.update()
                QApplication.processEvents()
                
            oo=ProductElaborated(self.mem, rowms)
            self.append(oo)
        cur.close()
        
    ## It's a staticmethod due to it will be used in ProductAllManager
    def qtablewidget(self, table):        
        table.setColumnCount(1)
        table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Name")))
        table.applySettings()
        table.clearContents()
        table.setRowCount(self.length())
        for i, o in enumerate(self.arr):
            table.setItem(i, 0, qleft(o.name))
            #table.item(i, 0).setIcon(o.qicon())

class ProductInElaboratedProduct:
    ##Biometrics(mem)
    ##Biometrics(mem,elaborated_product,row)
    def __init__(self, *args):        
        def init__create(product, system_product, amount, elaboratedproduct,id):
            self.product=product
            self.system_product=system_product
            self.amount=amount
            self.elaboratedproduct=elaboratedproduct
            self.id=id
        self.mem=args[0]
        if len(args)==1:
            init__create(None,None,None,None,None)
        elif len(args)==3:
            self.elaboratedproduct=args[1]
            product=self.mem.data.products.find_by_id_system(args[2]['products_id'],args[2]['system_product'])
            init__create(product, args[2]['system_product'], args[2]['amount'], self.elaboratedproduct, args[2]['id'])
        elif len(args)==6:
            init__create(*args[1:])

    def fullName(self):
        return self.product.fullName() 

    def calories(self):
        return self.amount * self.product.calories/self.product.amount
        
    def fat(self):
        return self.amount * self.product.fat/self.product.amount

    def protein(self):
        return self.amount * self.product.protein/self.product.amount

    def carbohydrate(self):
        return self.amount * self.product.carbohydrate/self.product.amount

    def salt(self):
        return self.amount * self.product.salt/self.product.amount

    def fiber(self):
        return self.amount * self.product.fiber/self.product.amount
    def sugars(self):
        return self.amount * self.product.sugars/self.product.amount
    def sodium(self):
        return self.amount * self.product.sodium/self.product.amount
    def potassium(self):
        return self.amount * self.product.potassium/self.product.amount
    def cholesterol(self):
        return self.amount * self.product.cholesterol/self.product.amount
    def saturated_fat(self):
        return self.amount * self.product.saturated_fat/self.product.amount

    def product_type(self):
        if self.elaboratedproducts_id==None and self.companies_id==None:
            return "Basic"
        elif self.elaboratedproducts_id!=None:
            return "Personal"
        elif self.companies_id!=None:
            return "Manufactured"
        else:
            return "Rare"
            
    def save(self):
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("""
                insert into products_in_elaboratedproducts
                    (products_id, amount, elaboratedproducts_id, system_product) 
                values (%s, %s,%s,%s) returning id""",
                (self.product.id, self.amount, self.elaboratedproduct.id, self.system_product))
        else:
            self.mem.con.execute("""
                update products_in_elaboratedproducts set 
                    products_id=%s,
                    amount=%s,
                    elaboratedproducts_id=%s, 
                    system_product=%s
                where id=%s""", 
                (self.product.id, self.amount, self.elaboratedproduct.id, self.system_product,  self.id))
        self.elaboratedproduct.needStatus(1)
        self.elaboratedproduct.register_in_personal_products()

    def delete(self):
        self.mem.con.execute("delete from products_in_elaboratedproducts where id=%s", (self.id, ))
        
class ProductInElaboratedProductManager(QObject, ObjectManager_With_IdDatetime_Selectable):
    ##ProductInElaboratedProductManager(mem)
    ##ProductInElaboratedProductManager(mem,elaboratedproduct,sql)
    def __init__(self, *args ):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=args[0]
        if len(args)==3:
            self.elaboratedproduct=args[1]
            self.load_db_data(args[2])

    def load_db_data(self, sql):
        rows=self.mem.con.cursor_rows(sql)
        for row in rows:
            self.append(ProductInElaboratedProduct(self.mem, self.elaboratedproduct, row))
        return self

    def calories(self):
        r=Decimal(0)
        for product_in in self.arr:
            r=r+product_in.calories()
        return r
        
    def fat(self):
        r=Decimal(0)
        for product_in in self.arr:
            r=r+product_in.fat()
        return r
        
    def protein(self):
        r=Decimal(0)
        for product_in in self.arr:
            r=r+product_in.protein()
        return r
        
    def carbohydrate(self):
        r=Decimal(0)
        for product_in in self.arr:
            r=r+product_in.carbohydrate()
        return r
        
    def salt(self):
        r=Decimal(0)
        for product_in in self.arr:
            r=r+product_in.salt()
        return r
        
    def fiber(self):
        r=Decimal(0)
        for product_in in self.arr:
            r=r+product_in.fiber()
        return r
        
    def cholesterol(self):
        r=Decimal(0)
        for product_in in self.arr:
            r=r+product_in.cholesterol()
        return r
        
    def sugars(self):
        r=Decimal(0)
        for product_in in self.arr:
            r=r+product_in.sugars()
        return r
        
    def saturated_fat(self):
        r=Decimal(0)
        for product_in in self.arr:
            r=r+product_in.saturated_fat()
        return r
        
    def sodium(self):
        r=Decimal(0)
        for product_in in self.arr:
            r=r+product_in.sodium()
        return r
        
    def potassium(self):
        r=Decimal(0)
        for product_in in self.arr:
            r=r+product_in.potassium()
        return r
        
    def grams(self):
        r=Decimal(0)
        for product_in in self.arr:
            r=r+product_in.amount
        if r==Decimal(0):
            r=Decimal(1)#To avoid division zero errors
        return r

    def max_name_len(self):
        r=0
        for product_in in self.arr:
            if len(product_in.fullName())>r:
                r=len(product_in.fullName())
        return r
        
    def show_table(self):
        maxname=self.max_name_len()
        if maxname<17:#For empty tables totals
            maxname=17
        maxlength=maxname+2+7+2+7+2+7+2+7+2+7+2+7
    
        print (Style.BRIGHT+ "="*(maxlength) + Style.RESET_ALL)
        print (Style.BRIGHT+ self.tr("ELABORATED PRODUCT '{}' NUTRICIONAL REPORT").format(self.elaboratedproduct.name.upper()).center(maxlength,' ') + Style.RESET_ALL)
        print (Style.BRIGHT+ "="*(maxlength) + Style.RESET_ALL)

        print (Style.BRIGHT+ "{}  {}  {}  {}  {}  {}  {}".format(self.tr("NAME").ljust(maxname," "),self.tr("GRAMS").rjust(7,' '), self.tr("CALORIE").rjust(7,' '), self.tr("CARBOHY").rjust(7,' '), self.tr("PROTEIN").rjust(7,' '), self.tr("FAT").rjust(7,' '), self.tr("FIBER").rjust(7,' ')) + Style.RESET_ALL)
        for product_in in self.arr:
            print ( "{}  {}  {}  {}  {}  {}  {}".format(product_in.fullName().ljust(maxname), a2s(product_in.amount),a2s(product_in.calories()), a2s(product_in.carbohydrate()), a2s(product_in.protein()), a2s(product_in.fat()),a2s(product_in.fiber())) + Style.RESET_ALL)

        print (Style.BRIGHT+ "-"*(maxlength) + Style.RESET_ALL)
        total=self.tr("ELABORATED WITH {} PRODUCTS").format(self.length())
        print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(total.ljust(maxname), a2s(self.grams()), a2s(self.calories()), a2s(self.carbohydrate()), a2s(self.protein()), a2s(self.fat()), a2s(self.fiber())) + Style.RESET_ALL)
        recomendations=self.tr("FINAL PRODUCT")
        product=self.mem.data.products.find_by_elaboratedproducts_id(self.elaboratedproduct.id)
        print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(recomendations.ljust(maxname), a2s(product.amount), a2s(product.calories), a2s(product.carbohydrate), a2s(product.protein), a2s(product.fat), a2s(product.fiber)) + Style.RESET_ALL)
        print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(self.tr("FINAL PRODUCT (100G)").ljust(maxname), a2s(100), a2s(product.component_in_100g(eProductComponent.Calories)), a2s(product.component_in_100g(eProductComponent.Carbohydrate)), a2s(product.component_in_100g(eProductComponent.Protein)), a2s(product.component_in_100g(eProductComponent.Fat)), a2s(product.component_in_100g(eProductComponent.Fiber))) + Style.RESET_ALL)
        print (Style.BRIGHT + "="*(maxlength) + Style.RESET_ALL)


    def qtablewidget(self, table):        
        table.setColumnCount(7)
        table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Name")))
        table.setHorizontalHeaderItem(1, QTableWidgetItem(self.tr("Grams")))
        table.setHorizontalHeaderItem(2, QTableWidgetItem(self.tr("Calories")))
        table.setHorizontalHeaderItem(3, QTableWidgetItem(self.tr("Carbohydrates")))
        table.setHorizontalHeaderItem(4, QTableWidgetItem(self.tr("Protein")))
        table.setHorizontalHeaderItem(5, QTableWidgetItem(self.tr("Fat")))
        table.setHorizontalHeaderItem(6, QTableWidgetItem(self.tr("Fiber")))
   
        table.applySettings()
        table.clearContents()
        table.setRowCount(self.length()+1)
        for i, o in enumerate(self.arr):
            table.setItem(i, 0, qleft(o.product.fullName()))
            table.setItem(i, 1, qright(o.amount))
            table.setItem(i, 2, qright(o.calories()))
            table.setItem(i, 3, qright(o.carbohydrate()))
            table.setItem(i, 4, qright(o.protein()))
            table.setItem(i, 5, qright(o.fat()))
            table.setItem(i, 6, qright(o.fiber()))
        #Totals
        table.setItem(self.length(), 0, qleft(self.tr("Total")))
        table.setItem(self.length(), 1, qnumber(self.grams()))
        table.setItem(self.length(), 2, qnumber(self.calories()))
        table.setItem(self.length(), 3, qnumber(self.carbohydrate()))
        table.setItem(self.length(), 4, qnumber(self.protein()))
        table.setItem(self.length(), 5, qnumber(self.fat()))
        table.setItem(self.length(), 6, qnumber(self.fiber()))



class ProductAllManager(QObject, ObjectManager_With_IdName_Selectable):
    ## ProductAllManager(mem)#Loads all database
    def __init__(self, *args):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.args=args#To launch ObjectManagers
        self.mem=args[0]
        
    def load_all(self):
        system=ProductManager(self.mem)
        system.load_from_db("select * from products")
        for o in system.arr:
            self.append(o)
        personal=ProductPersonalManager(self.mem)
        personal.load_from_db("select * from personalproducts")
        for o in personal.arr:
            self.append(o)
        self.order_by_name()

    
    def qcombobox(self, combo, selected=None):
        combo.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.order_by_name()
        for o in self.arr:
            combo.addItem(o.qicon(), o.fullName(), o.string_id())
        if selected!=None:
            combo.setCurrentIndex(combo.findData(selected.string_id()))
            
    def qtablewidget(self, table):
        ProductManager.qtablewidget(self, table)
        
        
    def find_by_id_system(self,  id ,  system):
        return ProductManager.find_by_id_system(self, id, system)
    ## Find by generated string with id and system_product
    def find_by_string_id(self, stringid):
        return ProductManager.find_by_string_id(self, stringid)
    ## Find by generated string with id and system_product
    def find_by_elaboratedproducts_id(self, elaboratedproducts_id):
        return ProductManager.find_by_elaboratedproducts_id(self, elaboratedproducts_id)


class DBData:
    def __init__(self, mem):
        self.mem=mem

    def load(self, progress=True):
        start=datetime.now()
        
        self.activities=ActivityManager(self.mem)
        self.weightwishes=WeightWishManager(self.mem)
        
        self.companies=CompanyAllManager(self.mem)
        self.companies.load_all()

        self.products=ProductAllManager(self.mem)
        self.products.load_all()
        
        self.elaboratedproducts=ProductElaboratedManager(self.mem)
        self.elaboratedproducts.load_from_db("select * from elaboratedproducts order by name", progress)
        
        self.users=UserManager(self.mem, "select * from users", progress)
        self.users.load_last_biometrics()
        self.mem.user=self.mem.data.users.find_by_id(int(self.mem.settings.value("mem/currentuser", 1)))
        if self.mem.user==None:
            self.mem.user=self.mem.data.users.find_by_id(1)#For empty databases (contribution)            
        
        debug("DBData took {}".format(datetime.now()-start))

class Biometrics:    
    ##Biometrics(mem)
    ##Biometrics(mem,rows)
    ##Biometrics(mem,dt, height, weight, user, activity, weightwish, id):
    def __init__(self, *args):        
        def init__create(dt, height, weight, user, activity, weightwish, id):
            self.datetime=dt
            self.height=height
            self.weight=weight
            self.user=user
            self.activity=activity
            self.weightwish=weightwish
            self.id=id
        # #########################################
        self.mem=args[0]
        if len(args)==1:#Biometrics(mem)
            init__create(*[None]*7)
        elif len(args)==2:#Biometrics(mem,rows)
            user=self.mem.data.users.find_by_id(args[1]['users_id'])
            activity=self.mem.data.activities.find_by_id(args[1]['activity'])
            weightwish=self.mem.data.weightwishes.find_by_id(args[1]['weightwish'])
            init__create(args[1]['datetime'], args[1]['height'], args[1]['weight'], user, activity, weightwish,  args[1]['id'])
        elif len(args)==8:#Biometrics(mem,dt, height, weight, user, activity, id):
            init__create(*args[1:])
    
    def __repr__(self):
        return "{} {}".format(self.height, self.weight)
        
    def delete(self):
        self.mem.con.execute("delete from biometrics where id=%s", (self.id, ))
        
    def save(self):
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("insert into biometrics(datetime,weight,height,users_id,activity,weightwish) values (%s, %s, %s, %s, %s, %s) returning id", (self.datetime, self.weight, self.height, self.user.id, self.activity.id, self.weightwish.id))
        else:
            self.mem.con.execute("update biometrics set datetime=%s, weight=%s, height=%s, users_id=%s, activity=%s, weightwish=%s where id=%s", (self.datetime, self.weight, self.height, self.user.id, self.activity.id, self.weightwish.id, self.id))
                ##basal metabolic rate
    def bmr(self):
        if self.user.male==True:
            return self.activity.multiplier*(Decimal(10)*self.weight + Decimal(6.25)*self.height - Decimal(5)*self.user.age() + 5)
        else: #female
            return self.activity.multiplier*(Decimal(10)*self.weight + Decimal(6.25)*self.height - Decimal(5)*self.user.age() - 161)

    ##    https://www.healthline.com/nutrition/how-much-protein-per-day#average-needs
    ## If you’re at a healthy weight, don't lift weights and don't exercise much, then aiming for 0.36–0.6 grams per pound (0.8–1.3 gram per kg) is a reasonable estimate.
    ##
    ##This amounts to:
    ##
    ##56–91 grams per day for the average male.
    ##46–75 grams per day for the average female.
    ##
    ## But given that there is no evidence of harm and a significant evidence of benefit, it’s likely better for most people to err on the side of more protein rather than less.
    def protein(self):
        return self.bmr()*Decimal(0.175)/Decimal(4)


    ## The Mediterranean diet includes a wide variety of plant and animal foods such as fish, meat, eggs, dairy, extra virgin olive oil, fruits, vegetables, legumes and whole grains.
    ## 
    ## It typically provides 35–40% of calories from fat, including plenty of monounsaturated fat from olive oil.
    ##
    ## Here are a few examples of suggested daily fat ranges for a Mediterranean diet, based on different calorie goals:
    ##
    ##     1,500 calories: About 58–67 grams of fat per day.
    ##     2,000 calories: About 78–89 grams of fat per day.
    ##     2,500 calories: About 97–111 grams of fat per day.
    ## Segun https://www.tuasaude.com/es/calorias-de-los-alimentos/ cada gramo grasa tiene 9 calorias
    ## 60% hidratos, 17.5% proteínas y 22.5% de grasas. SERA SELECCIONABLE
    def fat(self):
        return self.bmr()*Decimal(0.225)/Decimal(9)

    def carbohydrate(self):
        return self.bmr()*Decimal(0.60)/Decimal(4)


    def fiber(self):
        return Decimal(25)
    # Índice de masa corporal
    def imc(self):
        return self.weight/((self.height/100)**2)
    
    ## https://www.seedo.es/index.php/pacientes/calculo-imc
    def imc_comment(self):
        imc=self.imc()
        if imc <18.5:
            return "Peso insuficiente"
        elif imc<24.9:
            return "Peso normal"
        elif imc<26.9:
            return "Sobrepeso grado I"
        elif imc<29.9:
            return "Sobrepeso grado II (preobesidad)"
        elif imc<34.9:
            return "Obesidad grado I"
        elif imc<39.9:
            return "Obesidad grado II"
        elif imc<50:
            return "Obesidad grado III (mórbida)"
        elif imc>=50:
            return "Obesidad grado IV (extrema"
class BiometricsManager(QObject, ObjectManager_With_IdName_Selectable):
    ##Biometrics(mem)
    ##Biometrics(mem,sql, progress)
    def __init__(self, *args ):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=args[0]
        if len(args)==3:
            self.load_from_db(*args[1:])

    def load_from_db(self, sql,  progress=False):
        self.clean()
        cur=self.mem.con.cursor()
        cur.execute(sql)
        if progress==True:
            pd= QProgressDialog(self.tr("Loading {0} biometrics from database").format(cur.rowcount),None, 0,cur.rowcount)
            pd.setWindowIcon(QIcon(":/caloriestracker/coins.png"))
            pd.setModal(True)
            pd.setWindowTitle(self.tr("Loading biometrics..."))
            pd.forceShow()
        for row in cur:
            if progress==True:
                pd.setValue(cur.rownumber)
                pd.update()
                QApplication.processEvents()
            o=Biometrics(self.mem, row)
            self.append(o)
        cur.close()

    def qtablewidget(self, table):     
        table.setColumnCount(6)
        table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Date and time")))
        table.setHorizontalHeaderItem(1, QTableWidgetItem(self.tr("Weight")))
        table.setHorizontalHeaderItem(2, QTableWidgetItem(self.tr("Height")))
        table.setHorizontalHeaderItem(3, QTableWidgetItem(self.tr("Activity")))
        table.setHorizontalHeaderItem(4, QTableWidgetItem(self.tr("weightwish")))
        table.setHorizontalHeaderItem(5, QTableWidgetItem(self.tr("Situation")))
   
        table.applySettings()
        table.clearContents()
        table.setRowCount(self.length())
        for i, o in enumerate(self.arr):
            table.setItem(i, 0, qdatetime(o.datetime, self.mem.localzone))
            table.setItem(i, 1, qnumber(o.weight))
            table.setItem(i, 2, qnumber(o.height))
            table.setItem(i, 3, qleft(o.activity.name))
            table.setItem(i, 4, qleft(o.weightwish.name))
            table.setItem(i, 5, qleft(o.imc_comment()))

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
        products=self.mem.con.cursor_one_field("select count(*) from companies where companies_id =%s and system_company=%s", (self.id, self.system_company))
        personalproducts=self.mem.con.cursor_one_field("select count(*) from personalcompanies where companies_id =%s and system_company=%s", (self.id, self.system_company))
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
    
    def insert_string(self, table="companies"):
        return b2s(self.mem.con.mogrify("insert into "+table +"(name, last, id) values (%s, %s, %s);", (self.name, self.last, self.id)))

    def qicon(self):
        if self.system_company==True:
            return QIcon(":/caloriestracker/companies.png")
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

class CompaniesAndProducts(QObject):
    def __init__(self, mem):
        QObject.__init__(self)
        self.mem=mem
        
    ## Generates a report finding in fullNames in companies and products
    def find_report(self, find):
        self.mem.data.products.order_by_name()
        print (self.mem.tr("Companies:"))
        for o in self.mem.data.companies.arr:
            if o.fullName().upper().find(find.upper())!=-1:
                print ("  + {}".format( o.fullName()))
        print (self.mem.tr("Products:"))
        for o in self.mem.data.products.arr:
            if o.fullName().upper().find(find.upper())!=-1:
                print ("  + {}".format(o.fullName()))

    ## Used in frmAbout statistics
    def qtablewidget_products_in_companies(self, table):
        rows=self.mem.con.cursor_rows("select companies.name, count(allproducts.id) from allproducts LEFT OUTER JOIN companies ON allproducts.companies_id=companies.id group by companies.name order by count desc")
        table.setColumnCount(2)
        table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Company name")))
        table.setHorizontalHeaderItem(1, QTableWidgetItem(self.tr("Products")))
        table.applySettings()
        table.clearContents()
        table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            name="Personal products" if row[0]==None else row[0]
            table.setItem(i, 0, qleft(name))
            table.setItem(i, 1, qright(row[1], digits=0))
            
    def qtablewdiget_database_registers(self, table):
        rows=self.mem.con.cursor_one_column("SELECT tablename FROM pg_catalog.pg_tables where schemaname='public' order by tablename") 
        table.setColumnCount(2)
        table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Table")))
        table.setHorizontalHeaderItem(1, QTableWidgetItem(self.tr("Number of registers")))
        table.applySettings()
        table.clearContents()
        table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            table.setItem(i, 0, qleft(row))
            table.setItem(i, 1, qnumber(self.mem.con.cursor_one_field("select count(*) from "+ row), digits=0))



class Product(QObject):
    ##Product(mem)
    ##Product(mem,rows) #Uses products_id and users_id in row
    ##Product(mem,datetime,product,name,amount,users_id,id)
    def __init__(self, *args):        
        def init__create( name, amount, fat, protein, carbohydrate, company, last, elaboratedproducts_id, languages_id, calories, salt, cholesterol, sodium, potassium, fiber, sugars, saturated_fat, system_company, id):
            self.name=self.tr(name)
            self.amount=amount
            self.fat=fat
            self.protein=protein
            self.carbohydrate=carbohydrate
            self.company=company
            self.last=last
            self.elaboratedproducts_id=elaboratedproducts_id
            self.languages=languages_id
            self.calories=calories
            self.salt=salt
            self.cholesterol=cholesterol
            self.sodium=sodium
            self.potassium=potassium
            self.fiber=fiber
            self.sugars=sugars
            self.saturated_fat=saturated_fat
            self.system_company=system_company
            self.id=id
            return self
        # #########################################
        QObject.__init__(self)
        self.mem=args[0]
        if len(args)==1:#Product(mem)
            init__create(*[None]*19)
        elif len(args)==2:#Product(mem,rows)
            company=self.mem.data.companies.find_by_id_system(args[1]['companies_id'], args[1]['system_company'])
            init__create(args[1]['name'], args[1]['amount'], args[1]['fat'], args[1]['protein'], args[1]['carbohydrate'], company, 
            args[1]['last'], args[1]['elaboratedproducts_id'], args[1]['languages'], args[1]['calories'], args[1]['salt'], 
            args[1]['cholesterol'], args[1]['sodium'], args[1]['potassium'], args[1]['fiber'], args[1]['sugars'], args[1]['saturated_fat'], args[1]['system_company'], args[1]['id'])
        elif len(args)==20:#Product(mem,datetime,product,name,amount,users_id,id)
            init__create(*args[1:])
        self.system_product=True
        self.status=0

    def __repr__(self):
        return self.fullName()

    ## ESTA FUNCION VA AUMENTANDO STATUS SIN MOLESTAR LOS ANTERIORES, SOLO CARGA CUANDO stsatus_to es mayor que self.status
    ## @param statusneeded  Integer with the status needed 
    ## @param downgrade_to Integer with the status to downgrade before checking needed status. If None it does nothing
    ## 0 campos del producto
    ## 1 formats
    def needStatus(self, statusneeded, downgrade_to=None):
        if downgrade_to!=None:
            self.status=downgrade_to
        
        if self.status==statusneeded:
            return
        #0
        if self.status==0 and statusneeded==1: #MAIN
            self.formats=FormatAllManager(self.mem, self)
            self.formats.load_all()
            self.status=1

    def fullName(self):
        if self.mem.debuglevel=="DEBUG":
            system="S" if self.system_product==True else "P"
            str_with_id=". #{}{}".format(system,self.id)
        else:
            str_with_id=""
            
        if self.company==None:
            if self.elaboratedproducts_id==None:
                return "{}{}".format(self.mem.trHS(self.name), str_with_id)
            else:
                elaborated=self.tr("Elaborated by me")
                return "{}{} ({})".format(self.mem.trHS(self.name), str_with_id, elaborated)
        else:
            return "{} ({}){}".format(self.mem.trHS(self.name), self.company.name, str_with_id)

    def init__db(self, id):
        """Se pasa id porque se debe usar cuando todavía no se ha generado."""
        cur=self.mem.con.cursor()
        cur.execute("select * from products where id=%s", (id, ))
        row=cur.fetchone()
        cur.close()
        return self.init__db_row(row)
    

    def save(self):
        companies_id=None if self.company==None else self.company.id
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("""insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company
                    )values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id""",  
                    (self.name, self.amount, self.fat, self.protein, self.carbohydrate, companies_id, self.last, 
                    self.elaboratedproducts_id, self.languages, self.calories, self.salt, self.cholesterol, self.sodium, 
                    self.potassium, self.fiber, self.sugars, self.saturated_fat, self.system_company))
        else:
            self.mem.con.cursor_one_field("""update products set name=%s, amount=%s, fat=%s, protein=%s, carbohydrate=%s, companies_id=%s, last=%s,
            elaboratedproducts_id=%s, languages=%s, calories=%s, salt=%s, cholesterol=%s, sodium=%s, potassium=%s, fiber=%s, sugars=%s, saturated_fat=%s, system_company=%s
            where id=%s returning id""", 
            (self.name, self.amount, self.fat, self.protein, self.carbohydrate, companies_id, datetime.now(), 
            self.elaboratedproducts_id, self.languages, self.calories, self.salt, self.cholesterol, self.sodium, self.potassium, self.fiber, self.sugars, self.saturated_fat, self.system_company,  self.id))

    ## Generates an string with id and system_product
    def string_id(self):
        return "{}#{}".format(self.id, self.system_product)
        
    @staticmethod
    def string_id2tuple(string_id):
        return CompanySystem.string_id2tuple(string_id)
        
    def insert_string(self, table="products"):
        companies_id=None if self.company==None else self.company.id
        return b2s(self.mem.con.mogrify("insert into " + table +" (name, amount, fat, protein, carbohydrate, companies_id, last, elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, potassium, fiber, sugars, saturated_fat,system_company, id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);",  
            (self.name, self.amount, self.fat, self.protein, self.carbohydrate, companies_id, self.last, self.elaboratedproducts_id, self.languages, self.calories, self.salt, self.cholesterol, self.sodium, self.potassium, self.fiber, self.sugars, self.saturated_fat, self.system_company, self.id)))
           
    def is_deletable(self):
        self.needStatus(1)
        meals=self.mem.con.cursor_one_field("select count(*) from meals where products_id =%s and system_product=%s", (self.id, self.system_product))
        products_in=self.mem.con.cursor_one_field("select count(*) from products_in_elaboratedproducts where products_id =%s and system_product=%s", (self.id, self.system_product))
        sum=meals+products_in
        if self.system_product==True or self.formats.length()>0 or sum>0:
            return False
        return True
        
    def is_system(self):
        """Returns if the product is a system product or a user product"""
        if self.id>=0:
            return True
        return False

    ## Gets the amount of a component in 100 grams of product
    def component_in_100g(self, eproductcomponent):
        if eproductcomponent==eProductComponent.Fat:
            component_amount=self.fat
        elif eproductcomponent==eProductComponent.Fiber:
            component_amount=self.fiber
        elif eproductcomponent==eProductComponent.Carbohydrate:
            component_amount=self.carbohydrate
        elif eproductcomponent==eProductComponent.Protein:
            component_amount=self.protein
        elif eproductcomponent==eProductComponent.Calories:
            component_amount=self.calories
        return Decimal(100)*Decimal(component_amount)/Decimal(self.amount)

    def qicon(self):
        if self.system_product==True:
            return QIcon(":/caloriestracker/books.png")
        else:
            if self.elaboratedproducts_id==None:
                return QIcon(":/caloriestracker/meal.png")
            else:
                return QIcon(":/caloriestracker/keko.png")

## ONLY CHANGES table name
class ProductPersonal(Product):
    ##ProductPersonal(mem)
    ##ProductPersonal(mem,rows) #Uses products_id and users_id in row
    ##ProductPersonal(mem,datetime,product,name,amount,users_id,id)
    def __init__(self, *args):
        Product.__init__(self, *args)
        self.system_product=False

    def init__db(self, id):
        cur=self.mem.con.cursor()
        cur.execute("select * from personalproducts where id=%s", (id, ))
        row=cur.fetchone()
        cur.close()
        return self.init__db_row(row)

    #DO NOT EDIT THIS ONE COPY FROM PRODUCT AND CHANGE TABLE
    def save(self):
        companies_id=None if self.company==None else self.company.id
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("""insert into personalproducts (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company
                    )values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id""",  
                    (self.name, self.amount, self.fat, self.protein, self.carbohydrate, companies_id, self.last, 
                    self.elaboratedproducts_id, self.languages, self.calories, self.salt, self.cholesterol, self.sodium, 
                    self.potassium, self.fiber, self.sugars, self.saturated_fat, self.system_company))
        else:
            self.mem.con.cursor_one_field("""update personalproducts set name=%s, amount=%s, fat=%s, protein=%s, carbohydrate=%s, companies_id=%s, last=%s,
            elaboratedproducts_id=%s, languages=%s, calories=%s, salt=%s, cholesterol=%s, sodium=%s, potassium=%s, fiber=%s, sugars=%s, saturated_fat=%s, system_company=%s
            where id=%s returning id""", 
            (self.name, self.amount, self.fat, self.protein, self.carbohydrate, companies_id, datetime.now(), 
            self.elaboratedproducts_id, self.languages, self.calories, self.salt, self.cholesterol, self.sodium, self.potassium, self.fiber, self.sugars, self.saturated_fat, self.system_company,  self.id))

    def delete(self):
        if self.is_deletable()==True:
            self.mem.con.execute("delete from personalproducts where id=%s", (self.id, ))
        else:
            debug("I did not delete personalproducts because is not deletable")

## There is no need of system_formats or personal_formats because it's relacionated with the product as its properties
class Format(QObject):
    ##Format(mem)
    ##Format(mem,rows) #Uses products_id and users_id in row
    ##Format(mem, name, product, system_product,amount, last,  id):
    def __init__(self, *args):        
        def init__create( name, product, system_product,amount, last,  id):
            self.name=name
            self.product=product
            self.system_product=system_product
            self.amount=amount
            self.last=last
            self.id=id
            return self
        # #########################################
        QObject.__init__(self)
        self.mem=args[0]
        if len(args)==1:#Format(mem)
            init__create(*[None]*7)
        elif len(args)==2:#Format(mem,rows)
            product=self.mem.data.products.find_by_id_system(args[1]['products_id'], args[1]['system_product'])
            init__create(args[1]['name'], product, args[1]['system_product'], args[1]['amount'], args[1]['last'], args[1]['id'])
        elif len(args)==7:#Format(mem, name, product, system_product,amount, last, id):
            init__create(*args[1:])
        self.system_format=True

    def __repr__(self):
        return self.fullName()

    def insert_string(self, table="formats"):
        return b2s(self.mem.con.mogrify("insert into "+table +"(name, amount, last, products_id, system_product, id) values (%s, %s, %s, %s, %s, %s);", (self.name, self.amount, self.last, self.product.id, self.product.system_product, self.id)))

    def is_deletable(self):
        if self.system_format==True:
            return False
        return True
        
    def fullName(self, grams=True):
        system="S" if self.system_format==True else "P"
        sgrams=self.tr(" ({} g)").format(self.amount) if grams==True else ""
        if self.mem.debuglevel=="DEBUG":
            return "{}{}. #{}{}".format(self.name, sgrams, system, self.id)
        else:
            return "{}{}".format(self.name, sgrams)

    def qicon(self):
        if self.system_format==True:
            return QIcon(":/caloriestracker/cube.png")
        else:
            return QIcon(":/caloriestracker/keko.png")

    ## Generates an string with id and system_product
    def string_id(self):
        return "{}#{}".format(self.id, self.system_format)

class FormatPersonal(Format):
    def __init__(self, *args):
        Format.__init__(self,  *args)
        self.system_format=False           

    def save(self):
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("insert into personalformats(name, products_id, system_product, amount, last) values (%s, %s, %s, %s, %s) returning id",
                    (self.name,  self.product.id, self.system_product, self.amount, self.last))
        else:
            self.mem.con.execute("update personalformats set name=%s, products_id=%s, system_product=%s, amount=%s, last=%s where id=%s", 
                    (self.name,  self.product.id, self.system_product, self.amount, self.last, self.id))

    def delete(self):
        self.mem.con.execute("delete from personalformats where id=%s", (self.id, ))

class FormatManager(QObject, ObjectManager_With_IdName_Selectable):
    ##FormatManager(mem,product)
    def __init__(self, *args ):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=args[0]
        self.product=args[1]
        self.setSelectionMode(ManagerSelectionMode.Object)

    def load_from_db(self, sql):
        rows=self.mem.con.cursor_rows(sql)
        for row in rows:
            self.append(Format(self.mem, row))
        return self

    @staticmethod
    def qtablewidget(self, table):        
        table.setColumnCount(2)
        table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Name")))
        table.setHorizontalHeaderItem(1, QTableWidgetItem(self.tr("Grams")))
        table.applySettings()
        table.clearContents()
        table.setRowCount(self.length())
        for i, o in enumerate(self.arr):
            table.setItem(i, 0, qleft(o.fullName(grams=False)))
            table.item(i, 0).setIcon(o.qicon())
            table.setItem(i, 1, qnumber(o.amount))

class FormatPersonalManager(FormatManager):
    def __init__(self, *args):
        FormatManager.__init__(self, *args)
    def load_from_db(self, sql):
        rows=self.mem.con.cursor_rows(sql)
        for row in rows:
            self.append(FormatPersonal(self.mem, row))
        return self

class FormatAllManager(QObject, ObjectManager_With_IdName_Selectable):
    ## ProductAllManager(mem,product)#Loads all database
    def __init__(self, *args):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=args[0]
        self.product=args[1]

    def load_all(self):
        system=FormatManager(self.mem, self.product)
        system.load_from_db(self.mem.con.mogrify("select * from formats where products_id=%s and system_product=%s", (self.product.id, self.product.system_product )))
        for o in system.arr:
            self.append(o)
        personal=FormatPersonalManager(self.mem, self.product)
        personal.load_from_db(self.mem.con.mogrify("select * from personalformats where products_id=%s and system_product=%s", (self.product.id, self.product.system_product)))
        for o in personal.arr:
            self.append(o)
        self.order_by_name()

    def find_by_id_system(self,  id ,  system):
        for o in self.arr:
            if o.id==id and o.system_format==system:
                return o
        return None
                    
    ## Find by generated string with id and system_product
    def find_by_string_id(self, stringid):
        if stringid==None:
            return None
        return self.find_by_id_system(*CompanySystem.string_id2tuple(stringid))#The same for formats
        
    def qcombobox(self, combo, selected=None, needtoselect=False):
        self.order_by_name()
        combo.clear()
        if needtoselect==True:
            if self.length()>0:
                combo.addItem(combo.tr("Select an option"), None)
            else:
                combo.addItem(combo.tr("No options to select"), None)
        for o in self.arr:
            combo.addItem(o.qicon(), o.fullName(), o.string_id())

        if selected!=None:
            combo.setCurrentIndex(combo.findData(selected.string_id()))

    def qtablewidget(self, table):
        FormatManager.qtablewidget(self, table)

## Clase parar trabajar con las opercuentas generadas automaticam
class Meal:
    ##Meal(mem)
    ##Meal(mem,rows) #Uses products_id and users_id in row
    ##Meal(mem,datetime,product,name,amount,users_id,id)
    def __init__(self, *args):        
        def init__create( dt, product, amount, user, system_product, id):
            self.datetime=dt
            self.product=product
            self.amount=amount
            self.user=user
            self.system_product=system_product
            self.id=id
            return self
        # #########################################
        self.mem=args[0]
        if len(args)==1:#Meal(mem)
            init__create(*[None]*6)
        elif len(args)==2:#Meal(mem,rows)
            product=self.mem.data.products.find_by_id_system(args[1]['products_id'], args[1]['system_product'])
            user=self.mem.data.users.find_by_id(args[1]['users_id'])
            init__create(args[1]['datetime'], product, args[1]['amount'], user, args[1]['system_product'], args[1]['id'])
        elif len(args)==7:#Meal(mem,datetime,product, amount,users_id,id)
            init__create(*args[1:])

    def fullName(self):
        return self.product.fullName() 

    def calories(self):
        return self.amount * self.product.calories/self.product.amount
        
    def fat(self):
        return self.amount * self.product.fat/self.product.amount

    def protein(self):
        return self.amount * self.product.protein/self.product.amount

    def carbohydrate(self):
        return self.amount * self.product.carbohydrate/self.product.amount

    def salt(self):
        return self.amount * self.product.salt/self.product.amoun

    def fiber(self):
        return self.amount * self.product.fiber/self.product.amount

    def meal_hour(self):
        return str(self.datetime.time())[0:5]

    def product_type(self):
        if self.elaboratedproducts_id==None and self.companies_id==None:
            return "Basic"
        elif self.elaboratedproducts_id!=None:
            return "Personal"
        elif self.companies_id!=None:
            return "Manufactured"
        else:
            return "Rare"
            
    def save(self):
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("insert into meals(datetime,products_id,amount, users_id, system_product) values (%s, %s,%s,%s,%s) returning id",(self.datetime, self.product.id, self.amount, self.user.id, self.system_product))
        else:
            self.mem.con.execute("update meals set datetime=%s,products_id=%s,amount=%s,users_id=%s, system_product=%s where id=%s", (self.datetime, self.product.id, self.amount, self.user.id, self.system_product,  self.id))

    def delete(self):
        self.mem.con.execute("delete from meals where id=%s", (self.id, ))


class MealManager(QObject, ObjectManager_With_IdDatetime_Selectable):
    ##MealManager(mem)
    ##MealManager(mem,sql, progress)
    def __init__(self, *args ):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=args[0]
        if len(args)==2:
            self.load_db_data(*args[1:])
        self.setSelectionMode(ManagerSelectionMode.Object)

    def load_db_data(self, sql):
        rows=self.mem.con.cursor_rows(sql)
        for row in rows:
            self.append(Meal(self.mem, row))
        return self

    def calories(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.calories()
        return r
    def fat(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.fat()
        return r
    def protein(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.protein()
        return r
    def carbohydrate(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.carbohydrate()
        return r
    def salt(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.salt()
        return r
    def fiber(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.fiber()
        return r
    def grams(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.amount
        return r

    def max_name_len(self):
        r=0
        for meal in self.arr:
            if len(meal.fullName())>r:
                r=len(meal.fullName())
        return r
        
    def show_table(self, date):
        maxname=self.max_name_len()
        if maxname<17:#For empty tables totals
            maxname=17
        maxlength=5+2+maxname+2+7+2+7+2+7+2+7+2+7+2+7

        print (Style.BRIGHT+ "="*(maxlength) + Style.RESET_ALL)
        print (Style.BRIGHT+ "{} NUTRICIONAL REPORT AT {}".format(self.mem.user.name.upper(), date).center(maxlength," ") + Style.RESET_ALL)
        print (Style.BRIGHT+ Fore.YELLOW + "{} Kg. {} cm. {} years".format(self.mem.user.last_biometrics.weight, self.mem.user.last_biometrics.height, self.mem.user.age()).center(maxlength," ") + Style.RESET_ALL)
        print (Style.BRIGHT+ Fore.BLUE + "IMC: {} ==> {}".format(round(self.mem.user.last_biometrics.imc(),2),self.mem.user.last_biometrics.imc_comment()).center(maxlength," ") + Style.RESET_ALL)
        print (Style.BRIGHT+ "="*(maxlength) + Style.RESET_ALL)

        print (Style.BRIGHT+ "{}  {}  {}  {}  {}  {}  {}  {}".format("HOUR ","NAME".ljust(maxname," "),"GRAMS".rjust(7,' '), "CALORIE".rjust(7,' '), "CARBOHY".rjust(7,' '), "PROTEIN".rjust(7,' '), "FAT".rjust(7,' '), "FIBER".rjust(7,' ')) + Style.RESET_ALL)
        for meal in self.arr:
            print ( "{}  {}  {}  {}  {}  {}  {}  {}".format(meal.meal_hour(), meal.fullName().ljust(maxname), a2s(meal.amount),a2s(meal.calories()), a2s(meal.carbohydrate()), a2s(meal.protein()), a2s(meal.fat()),a2s(meal.fiber())) + Style.RESET_ALL)

        print (Style.BRIGHT+ "-"*(maxlength) + Style.RESET_ALL)
        total="{} MEALS WITH THIS TOTALS".format(self.length())
        print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(total.ljust(maxname+7), a2s(self.grams()), ca2s(self.calories(),self.mem.user.last_biometrics.bmr()), ca2s(self.carbohydrate(),self.mem.user.last_biometrics.carbohydrate()), ca2s(self.protein(), self.mem.user.last_biometrics.protein()), ca2s(self.fat(),self.mem.user.last_biometrics.fat()), rca2s(self.fiber(),self.mem.user.last_biometrics.fiber())) + Style.RESET_ALL)
        recomendations="RECOMMENDATIONS"
        print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(recomendations.ljust(maxname+7), n2s(), a2s(self.mem.user.last_biometrics.bmr()), a2s(self.mem.user.last_biometrics.carbohydrate()), a2s(self.mem.user.last_biometrics.protein()), a2s(self.mem.user.last_biometrics.fat()), a2s(self.mem.user.last_biometrics.fiber())) + Style.RESET_ALL)
        print (Style.BRIGHT + "="*(maxlength) + Style.RESET_ALL)

    def qtablewidget(self, table):        
        table.setColumnCount(8)
        table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Hour")))
        table.setHorizontalHeaderItem(1, QTableWidgetItem(self.tr("Name")))
        table.setHorizontalHeaderItem(2, QTableWidgetItem(self.tr("Grams")))
        table.setHorizontalHeaderItem(3, QTableWidgetItem(self.tr("Calories")))
        table.setHorizontalHeaderItem(4, QTableWidgetItem(self.tr("Carbohydrates")))
        table.setHorizontalHeaderItem(5, QTableWidgetItem(self.tr("Protein")))
        table.setHorizontalHeaderItem(6, QTableWidgetItem(self.tr("Fat")))
        table.setHorizontalHeaderItem(7, QTableWidgetItem(self.tr("Fiber")))
   
        table.applySettings()
        table.clearContents()
        table.setRowCount(self.length()+2)
        for i, o in enumerate(self.arr):
            table.setItem(i, 0, qtime(o.datetime))
            table.setItem(i, 1, qleft(o.product.fullName()))
            table.item(i, 1).setIcon(o.product.qicon())
            table.setItem(i, 2, qnumber(o.amount))
            table.setItem(i, 3, qnumber(o.calories()))
            table.setItem(i, 4, qnumber(o.carbohydrate()))
            table.setItem(i, 5, qnumber(o.protein()))
            table.setItem(i, 6, qnumber(o.fat()))
            table.setItem(i, 7, qnumber(o.fiber()))
        if self.mem.user.last_biometrics.height!=None:#Without last_biometrics
            #Totals
            table.setItem(self.length(), 1, qleft(self.tr("Total")))
            table.setItem(self.length(), 2, qnumber(self.grams()))
            table.setItem(self.length(), 3, qnumber_limited(self.calories(), self.mem.user.last_biometrics.bmr()))
            table.setItem(self.length(), 4, qnumber_limited(self.carbohydrate(), self.mem.user.last_biometrics.carbohydrate()))
            table.setItem(self.length(), 5, qnumber_limited(self.protein(), self.mem.user.last_biometrics.protein()))
            table.setItem(self.length(), 6, qnumber_limited(self.fat(), self.mem.user.last_biometrics.fat()))
            table.setItem(self.length(), 7, qnumber_limited(self.fiber(), self.mem.user.last_biometrics.fiber(), reverse=True))
            #Recomendatios
            table.setItem(self.length()+1, 1, qleft(self.tr("Recomendations")))
            table.setItem(self.length()+1, 3, qnumber(self.mem.user.last_biometrics.bmr()))
            table.setItem(self.length()+1, 4, qnumber(self.mem.user.last_biometrics.carbohydrate()))
            table.setItem(self.length()+1, 5, qnumber(self.mem.user.last_biometrics.protein()))
            table.setItem(self.length()+1, 6, qnumber(self.mem.user.last_biometrics.fat()))
            table.setItem(self.length()+1, 7, qnumber(self.mem.user.last_biometrics.fiber()))
        
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
    def qtablewidget(self, table):        
        table.setColumnCount(4)
        table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Name")))
        table.setHorizontalHeaderItem(1, QTableWidgetItem(self.tr("Male")))
        table.setHorizontalHeaderItem(2, QTableWidgetItem(self.tr("Birthday")))
        table.setHorizontalHeaderItem(3, QTableWidgetItem(self.tr("Starts")))
   
        table.applySettings()
        table.clearContents()
        table.setRowCount(self.length())
        for i, o in enumerate(self.arr):
            table.setItem(i, 0, qleft(o.name))
            table.setItem(i, 1, qbool(o.male))
            table.setItem(i, 2, qdate(o.birthday))
            table.setItem(i, 3, qdatetime(o.starts, self.mem.localzone))
