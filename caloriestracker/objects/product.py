from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QApplication, QProgressDialog, QCompleter
from caloriestracker.casts import b2s
from caloriestracker.datetime_functions import dtnaive2string
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable, ManagerSelectionMode, ObjectManager_With_Id_Selectable
from caloriestracker.libcaloriestrackertypes import eProductComponent
from caloriestracker.objects.additives import AdditiveManager_from_integer_list__mem
from caloriestracker.objects.company import CompanySystem
from caloriestracker.objects.format import FormatAllManager
from decimal import Decimal
from logging import debug

class Product(QObject):
    def __init__(self, mem=None,  name=None, amount=None, fat=None, protein=None, carbohydrate=None, company=None, last=None, 
            elaboratedproducts_id=None, languages_id=None, calories=None, salt=None, cholesterol=None, sodium=None, potassium=None, 
            fiber=None, sugars=None, saturated_fat=None, system_company=None, foodtype=None, additives=None, glutenfree=None, 
            ferrum=None, magnesium=None, phosphor=None, obsolete=None,  id=None):
        QObject.__init__(self)
        self.mem=mem
        self.name=name
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
        self.foodtype=foodtype
        self.additives=additives
        self.glutenfree=glutenfree
        self.ferrum=ferrum
        self.magnesium=magnesium
        self.phosphor=phosphor
        self.obsolete=obsolete
        self.id=id
        
        self.system_product=True
        self.status=0

    def __repr__(self):
        return self.fullName()

    ## Returns the highest risk of its additives. It's product's risk
    def risk(self):
        risk=None
        for additive in self.additives.arr:
            if additive.risk is not None:
                if risk==None:
                    risk=additive.risk
                else:
                    if risk.id<additive.risk.id:
                        risk=additive.risk
        return risk
            
    def risk_qicon(self):
        if self.risk()==None:
            return QIcon(":/caloriestracker/circle_white.png")
        return self.risk().qicon()

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
        #This function is used for products and personal products, only changes the name of the table
        if self.__class__.__name__=="ProductPersonal":
            table="personalproducts"
        else:
            table="products"
        
        if self.id==None:
            #print(self.sql_insert(table, returning_id=True))
            if table=="products":# id it's not linked to a sequence, so I must add a id. Only used for maintenance mode. Can't be two editors at the same time
                self.id=self.mem.con.cursor_one_field("select max(id)+1 from products")
                self.mem.con.execute(self.sql_insert(table, returning_id=False))
            else:# personalproducts has sequence
                self.id=self.mem.con.cursor_one_field(self.sql_insert(table, returning_id=True))
        else:
            self.mem.con.execute(self.sql_update(table))

    ## Generates an string with id and system_product
    def string_id(self):
        return "{}#{}".format(self.id, self.system_product)
        
    @staticmethod
    def string_id2tuple(string_id):
        return CompanySystem.string_id2tuple(string_id)
        
    ## @param returning_id True sql with returning id (normal insert). False without returning_id and id inside sql. Used for automatic inserts
    def sql_insert(self, table="products", returning_id=True):
        companies_id=None if self.company==None else self.company.id
        foodtypes_id=None if self.foodtype==None else self.foodtype.id
        
        sql= """insert into """+table+""" (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, obsolete
                    ) values (%s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,%s ) returning id;"""
        sql_parameters=(self.name, self.amount, self.fat, self.protein, self.carbohydrate, companies_id, self.last, 
                    self.elaboratedproducts_id, self.languages, self.calories, self.salt, self.cholesterol, self.sodium, 
                    self.potassium, self.fiber, self.sugars, self.saturated_fat, self.system_company, foodtypes_id, self.additives.array_of_ids(), 
                    self.glutenfree, self.ferrum, self.magnesium, self.phosphor, self.obsolete)

        if returning_id==True:
            r=self.mem.con.mogrify(sql, sql_parameters)
        else:
            sql=sql.replace(") values (", ", id ) values (")
            sql=sql.replace(") returning id", ", %s)")
#            print(sql)
#            print(sql_parameters)
            r=self.mem.con.mogrify(sql, sql_parameters+(self.id, ))
        return b2s(r)

    def sql_update(self, table="products"):
        companies_id=None if self.company==None else self.company.id
        foodtypes_id=None if self.foodtype==None else self.foodtype.id
        sql="""update public.""" +table+ """ set name=%s, amount=%s, fat=%s, protein=%s, carbohydrate=%s, companies_id=%s, last=%s,
            elaboratedproducts_id=%s, languages=%s, calories=%s, salt=%s, cholesterol=%s, sodium=%s, potassium=%s, fiber=%s, sugars=%s, saturated_fat=%s, 
            system_company=%s, foodtypes_id=%s, additives=%s, glutenfree=%s, ferrum=%s, magnesium=%s, phosphor=%s, obsolete=%s
            where id=%s;"""
        sql_parameters=(self.name, self.amount, self.fat, self.protein, self.carbohydrate, companies_id, self.last, 
            self.elaboratedproducts_id, self.languages, self.calories, self.salt, self.cholesterol, self.sodium, self.potassium, self.fiber, self.sugars, self.saturated_fat, 
            self.system_company,  foodtypes_id, self.additives.array_of_ids(), self.glutenfree, self.ferrum, self.magnesium, self.phosphor, self.obsolete, 
            self.id)

#        print(sql)
#        print(sql_parameters)
        return b2s(self.mem.con.mogrify(sql, sql_parameters))
        
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
        try:
            return Decimal(100)*Decimal(component_amount)/Decimal(self.amount)
        except:
            return None


    ## Generates a sql file to convert this system product to a new personal product
    def sqlfile_convert_to_personal(self):
        personal=ProductPersonal(self.mem)         
        personal.name=self.name
        personal.amount=self.amount
        personal.fat=self.fat
        personal.protein=self.protein
        personal.carbohydrate=self.carbohydrate
        personal.company=self.company
        personal.last=self.last
        personal.elaboratedproducts_id=self.elaboratedproducts_id
        personal.languages=self.languages
        personal.calories=self.calories
        personal.salt=self.salt
        personal.cholesterol=self.cholesterol
        personal.sodium=self.sodium
        personal.potassium=self.potassium
        personal.fiber=self.fiber
        personal.sugars=self.sugars
        personal.saturated_fat=self.saturated_fat
        personal.system_company=self.system_company
        personal.foodtype=self.foodtype
        personal.glutenfree=self.glutenfree
        personal.ferrum=self.ferrum
        personal.magnesium=self.magnesium
        personal.phosphor=self.phosphor
        personal.obsolete=self.obsolete
        personal.save()
        
        datestr=dtnaive2string(self.mem.inittime, "%Y%m%d%H%M")
        sql_filename="{}.sql".format(datestr)
        sql=open(sql_filename, "w")
        
        #Delete old personal products
        sql.write("-- caloriestracker_maintenance_products_system2personal\n")
        sql.write(personal.sql_insert("personalproducts")+"\n")
        #UPDATING PRODUCTS IN THE REST OF TABLES
        for table in ['formats', 'meals', 'products_in_elaboratedproducts']:
            sql.write(b2s(self.mem.con.mogrify("update "+table+" set products_id=%s, system_product=%s where products_id=%s and system_product=%s;", 
                (personal.id, personal.system_product, self.id, self.system_product)))+"\n")
        sql.write(b2s(self.mem.con.mogrify("delete from products where id=%s;", (self.id, )))+"\n")
        sql.write("\n")
        sql.close()
        self.mem.con.rollback()#Save it's in script, not in database.
        print(self.tr("We have generated '{}' to convert the system product '{}' to a personal product '{}'").format(sql_filename, self.fullName(), personal.fullName()))
        print(self.tr("You mustn't use this file if your are not a caloriestracker developer ;)"))

    def qicon(self):
        if self.system_product==True:
            return QIcon(":/caloriestracker/books.png")
        else:
            if self.elaboratedproducts_id==None:
                return QIcon(":/caloriestracker/meal.png")
            else:
                return QIcon(":/caloriestracker/cooking.png")

## Class to manage products
class ProductManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.setConstructorParameters(mem)
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
            self.append(Product_from_row(self.mem, rowms, system=True))
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

    def qtablewidget(self, wdg):
        myQTableWidget_ProductManagers(self.mem, self, wdg)

    ## Removes a product and return a boolean. NO HACE COMMIT
    def remove(self, o):
        if o.remove():
            ObjectManager_With_Id_Selectable.remove(self, o)
            return True
        return False
        
## ONLY CHANGES table name
class ProductPersonal(Product):

    def __init__(self, *args):
        Product.__init__(self, *args)
        self.system_product=False

    def init__db(self, id):
        cur=self.mem.con.cursor()
        cur.execute("select * from personalproducts where id=%s", (id, ))
        row=cur.fetchone()
        cur.close()
        return self.init__db_row(row)

    def delete(self):
        if self.is_deletable()==True:
            self.mem.con.execute("delete from personalproducts where id=%s", (self.id, ))
        else:
            debug("I did not delete personalproducts because is not deletable")

class ProductAllManager(QObject, ObjectManager_With_IdName_Selectable):
    ## ProductAllManager(mem)#Loads all database
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.setConstructorParameters(mem)
        self.mem=mem
        
    def load_all(self):
        system=ProductManager(self.mem)
        system.load_from_db("select * from products")
        for o in system.arr:
            self.append(o)
        if self.mem.isProductsMaintainerMode()==False:
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
            
    def qtablewidget(self, wdg):
        myQTableWidget_ProductManagers(self.mem, self, wdg)
        
        
    def find_by_id_system(self,  id ,  system):
        return ProductManager.find_by_id_system(self, id, system)
    ## Find by generated string with id and system_product
    def find_by_string_id(self, stringid):
        return ProductManager.find_by_string_id(self, stringid)
    ## Find by generated string with id and system_product
    def find_by_elaboratedproducts_id(self, elaboratedproducts_id):
        return ProductManager.find_by_elaboratedproducts_id(self, elaboratedproducts_id)

    ## Returns a ProductAllManager with all the products of the same company
    ## @param company. It's a Company object
    def ProductAllManager_of_same_company(self, company):
        r=ProductAllManager(self.mem)
        for o in self.arr:
            if o.company is not None and o.company.id==company.id and o.system_company==company.system_company:
                r.append(o)
        return r
        
    ## Return a ProductManager with the system products of the arr
    def ProductManager(self):
        r=ProductManager(self.mem)
        for o in self.arr:
            if o.system_product==True:
                r.append(o)
        return r

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
                
            self.append(Product_from_row(self.mem, rowms, system=False))
        cur.close()

   
def myQTableWidget_ProductManagers(mem, manager, wdg):     
        data=[]
        for i, o in enumerate(manager.arr):
            company="" if o.company==None else o.company.fullName()
            food_type="" if o.foodtype==None else o.foodtype.name
            data.append([
                o.fullName(), 
                company, 
                food_type, 
                o.last, 
                100, 
                o.component_in_100g(eProductComponent.Calories), 
                o.component_in_100g(eProductComponent.Carbohydrate), 
                o.component_in_100g(eProductComponent.Protein), 
                o.component_in_100g(eProductComponent.Fat), 
                o.component_in_100g(eProductComponent.Fiber), 
            ])
        wdg.setData(
            [wdg.tr("Name"), wdg.tr("Company"), wdg.tr("Food type"), wdg.tr("Last update"), 
            wdg.tr("Grams"), wdg.tr("Calories"), wdg.tr("Carbohydrates"), wdg.tr("Protein"), 
            wdg.tr("Fat"), wdg.tr("Fiber")], 
            None, 
            data, 
            zonename=mem.localzone
        )   
        for i, o in enumerate(manager.arr):
            wdg.table.item(i, 0).setIcon(o.qicon())
            wdg.table.item(i, 2).setIcon(o.risk_qicon())

## @param system boolean If true returns a Product, else a ProductPersonal
def Product_from_row(mem, row, system):
    company=mem.data.companies.find_by_id_system(row['companies_id'], row['system_company'])
    foodtype=mem.data.foodtypes.find_by_id(row['foodtypes_id'])
    additives=AdditiveManager_from_integer_list__mem(mem, row['additives'])
    if system==True:
        r=Product(mem)
    else:
        r=ProductPersonal(mem)
    r.name=row['name']
    r.amount=row['amount']
    r.fat=row['fat']
    r.protein=row['protein']
    r.carbohydrate=row['carbohydrate']
    r.company=company
    r.last=row['last']
    r.elaboratedproducts_id=row['elaboratedproducts_id']
    r.languages=row['languages']
    r.calories=row['calories']
    r.salt=row['salt']
    r.cholesterol=row['cholesterol']
    r.sodium=row['sodium']
    r.potassium=row['potassium']
    r.fiber=row['fiber']
    r.sugars=row['sugars']
    r.saturated_fat=row['saturated_fat']
    r.system_company=row['system_company']
    r.foodtype=foodtype
    r.additives=additives
    r.glutenfree=row['glutenfree']
    r.ferrum=row['ferrum']
    r.magnesium=row['magnesium']
    r.phosphor=row['phosphor']
    r.obsolete=row['obsolete']
    r.id=row['id']
    return r
