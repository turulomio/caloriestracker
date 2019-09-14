## @namespace caloriestracker.libcaloriestracker
## @brief Package with all caloriestracker core classes .
from PyQt5.QtCore import Qt,  QObject
from PyQt5.QtGui import QIcon,  QColor
from PyQt5.QtWidgets import QTableWidgetItem, QApplication,   qApp,  QProgressDialog, QCompleter
from datetime import date,  timedelta, datetime

import os
from decimal import Decimal
from caloriestracker.github import get_file_modification_dtaware
from caloriestracker.libcaloriestrackerfunctions import str2bool, dtaware2string, package_filename, is_there_internet, input_boolean, input_integer_or_none, a2s, ca2s, n2s, rca2s
from caloriestracker.libcaloriestrackertypes import eProductComponent
from caloriestracker.ui.qtablewidgetitems import qtime, qleft, qright, qnumber_limited, qnumber
from caloriestracker.libmanagers import  ObjectManager_With_Id_Selectable,  ManagerSelectionMode, ObjectManager_With_IdName_Selectable, ObjectManager_With_IdDatetime, ObjectManager_With_IdDatetime_Selectable
from colorama import Fore, Style
from officegenerator import OpenPyXL
from logging import debug, info

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
        
        
        
class CompanyAllManager(ObjectManager_With_IdName_Selectable):
    ## ProductAllManager(mem)#Loads all database
    def __init__(self, *args):
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=args[0]
        if len(args)==1:
            system=CompanySystemManager(self.mem)
            system.load_from_db("select * from companies")
            for o in system.arr:
                self.append(o)
            personal=CompanyPersonalManager(self.mem)
            personal.load_from_db("select * from personalcompanies")
            for o in personal.arr:
                self.append(o)

    def find_by_id_system(self,  id ,  system):
        for o in self.arr:
            if o.id==id and o.system_company==system:
                return o
        return None
            
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
        
    ## It's a staticmethod due to it will be used in ProductAllManager
    @staticmethod
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
        table.setRowCount(self.length())
        for i, o in enumerate(self.arr):
            table.setItem(i, 0, qleft(o.fullName(True)))
            table.item(i, 0).setIcon(o.qicon())
            table.setItem(i, 1, qnumber(100))
            table.setItem(i, 2, qnumber(o.component_in_100g(eProductComponent.Calories)))
            table.setItem(i, 3, qnumber(o.component_in_100g(eProductComponent.Carbohydrate)))
            table.setItem(i, 4, qnumber(o.component_in_100g(eProductComponent.Protein)))
            table.setItem(i, 5, qnumber(o.component_in_100g(eProductComponent.Fat)))
            table.setItem(i, 6, qnumber(o.component_in_100g(eProductComponent.Fiber)))

        
    ## Passes product.needStatus method to all products in arr
    ## @param needstatus Status needed
    ## @param progress Boolean. If true shows a progress bar
    def needStatus(self, needstatus,  downgrade_to=None, progress=False):
        if progress==True:
            pd= QProgressDialog(self.tr("Loading additional data to {0} products from database").format(self.length()),None, 0,self.length())
            pd.setWindowIcon(QIcon(":/caloriestracker/coins.png"))
            pd.setModal(True)
            pd.setWindowTitle(self.tr("Loading products..."))
            pd.forceShow()
        for i, product in enumerate(self.arr):
            if progress==True:
                pd.setValue(i)
                pd.update()
                QApplication.processEvents()
            product.needStatus(needstatus, downgrade_to)

    def order_by_datetime(self):
        """Orders the Set using self.arr"""
        try:
            self.arr=sorted(self.arr, key=lambda c: c.result.basic.last.datetime,  reverse=False)  
            return True
        except:
            return False
        
    def order_by_dividend(self):
        """Return a boolean if the sort can be done"""
        try:
            self.arr=sorted(self.arr, key=lambda p: p.estimations_dps.currentYear().percentage(),  reverse=True) 
            return True
        except:
            return False
        
    def order_by_daily_tpc(self):
        """Return a boolean if the sort can be done"""
        try:
            self.arr=sorted(self.arr, key=lambda p: p.result.basic.tpc_diario(),  reverse=True) 
            return True
        except:
            return False
                
    def order_by_annual_tpc(self):
        """Return a boolean if the sort can be done"""
        try:
            self.arr=sorted(self.arr, key=lambda p: p.result.basic.tpc_anual(),  reverse=True) 
            return True
        except:
            return False
            
    ## Fills a qcombobox with product nume in upper case
    ## @param combo QComboBox to fill
    ## @param selected Product object to select in the QComboBox
    def qcombobox_not_obsolete(self, combo,  selected=None):
        self.order_by_name()
        combo.clear()
        for a in self.arr:
            if a.obsolete==False:
                combo.addItem(a.name.upper(), a.id)

        if selected!=None:
            combo.setCurrentIndex(combo.findData(selected.id))

    ## Returns a ProductManager with all products with the type passed as parameter.
    ## @param type ProductType object
    ## @return ProductManager
    def ProductManager_with_same_type(self, type):
        result=ProductManager(self.mem)
        for a in self.arr:
            if a.type.id==type.id:
                result.append(a)
        return result

    ## Generate a new ProductManager object finding ids of parameter array in self.arr
    ## @param arrInt Array of integers to seach in self.arr
    ## @return ProductManager with the products matchind ids in arrInt.
    def ProductManager_with_id_in_list(self, arrInt):
        result=ProductManager(self.mem)
        for i, id in enumerate(arrInt):
            selected=self.mem.data.products.find_by_id(id)
            if selected!=None:
                result.append(selected)
        return result
        

    ## Generate a new ProductManager object with products that contains parameter string
    ## @param s String to seach
    ## @return ProductManager that is a subset of this class
    def ProductManager_contains_string(self, s):
        def find_attribute(att, s):
            if att==None:
                return False
            if att.upper().find(s)!=-1:
                return True
            return False
        # #############################################
        s=s.upper()
        result=ProductManager(self.mem)
        for o in self.arr:
            if find_attribute(o.name, s) or find_attribute(o.isin, s) or any(find_attribute(ticker, s) for ticker in o.tickers) or find_attribute(o.comment, s):
                result.append(o)
        return result
        
    ## Removes a product and return a boolean. NO HACE COMMIT
    def remove(self, o):
        if o.remove():
            ObjectManager_With_Id_Selectable.remove(self, o)
            return True
        return False
        
    ## Returns products.xlsx modification datetime or None if it can't find it
    def dtaware_internet_products_xlsx(self):
        aware= get_file_modification_dtaware("turulomio","caloriestracker","products.xlsx")
        if aware==None:
            return aware
        else:
            return aware.replace(second=0)#Due to in database globals we only save minutes


    ## Function that downloads products.xlsx from github repository and compares sheet data with database products.arr
    ## If detects modifications or new products updates database.
    def update_from_internet(self):
        def product_xlsx(row):
            try:
                p=Product(self.mem)
                tickers=[None]*5
                p.id=row[0].value
                p.name=row[1].value
                p.high_low=str2bool(row[2].value)
                p.isin=row[3].value
                p.stockmarket=self.mem.stockmarkets.find_by_name(row[4].value)
                if p.stockmarket==None:
                    raise
                p.currency=self.mem.currencies.find_by_id(row[5].value)
                if p.currency==None:
                    raise
                p.type=self.mem.types.find_by_name(row[6].value)
                if p.type==None:
                    raise
                p.agrupations=self.mem.agrupations.clone_from_dbstring(row[7].value)
                if p.agrupations==None:
                    raise
                p.web=row[8].value
                p.address=row[9].value
                p.phone=row[10].value
                p.mail=row[11].value
                p.percentage=row[12].value
                p.mode=self.mem.investmentsmodes.find_by_id(row[13].value)
                if p.mode==None:
                    raise
                p.leveraged=self.mem.leverages.find_by_name(row[14].value)
                if p.leveraged==None:
                    raise
                p.decimals=row[15].value
                p.comment=row[16].value
                p.obsolete=str2bool(row[17].value)
                tickers[0]=row[18].value
                tickers[1]=row[19].value
                tickers[2]=row[20].value
                tickers[3]=row[21].value
                tickers[4]=row[22].value
                p.tickers=tickers
                return p
            except:
                print("Error creando ProductODS con Id: {}".format(p.id))
                return None
        #---------------------------------------------------
        #Checks if there is Internet
        if is_there_internet()==False:
            return
        #Download file 
        from urllib.request import urlretrieve
        urlretrieve ("https://github.com/Turulomio/caloriestracker/blob/master/products.xlsx?raw=true", "product.xlsx")
        
        oldlanguage=self.mem.language.id
        self.mem.languages.cambiar("es")
        
        #Load database products
        products=ProductManager(self.mem)
        products.load_from_db("select * from products order by id")
        
        #Iterate ods and load in product object
        xlsx=OpenPyXL("product.xlsx","product.xlsx")  
        xlsx.setCurrentSheet(0)
        # for each row
        changed=[]
        added=[]
        for row in xlsx.ws_current.iter_rows():
            p_xlsx=product_xlsx(row)
            if p_xlsx==None:
                continue

            p_db=products.find_by_id(p_xlsx.id)       
       
            if p_db==None:
                added.append(p_xlsx)
            elif (  
                        p_db.id!=p_xlsx.id or
                        p_db.name!=p_xlsx.name or
                        p_db.high_low!=p_xlsx.high_low or
                        p_db.isin!=p_xlsx.isin or
                        p_db.stockmarket.id!=p_xlsx.stockmarket.id or
                        p_db.currency.id!=p_xlsx.currency.id or
                        p_db.type.id!=p_xlsx.type.id or
                        p_db.agrupations.dbstring()!=p_xlsx.agrupations.dbstring() or 
                        p_db.web!=p_xlsx.web or
                        p_db.address!=p_xlsx.address or
                        p_db.phone!=p_xlsx.phone or
                        p_db.mail!=p_xlsx.mail or
                        p_db.percentage!=p_xlsx.percentage or
                        p_db.mode.id!=p_xlsx.mode.id or
                        p_db.leveraged.id!=p_xlsx.leveraged.id or
                        p_db.decimals!=p_xlsx.decimals or
                        p_db.comment!=p_xlsx.comment or 
                        p_db.obsolete!=p_xlsx.obsolete or
                        p_db.tickers[0]!=p_xlsx.tickers[0] or
                        p_db.tickers[1]!=p_xlsx.tickers[1] or
                        p_db.tickers[2]!=p_xlsx.tickers[2] or
                        p_db.tickers[3]!=p_xlsx.tickers[3] or
                        p_db.tickers[4]!=p_xlsx.tickers[4]
                    ):
                changed.append(p_xlsx)

        #Sumary
        debug("{} Products changed".format(len(changed)))
        for p in changed:
            print("  +", p,  p.currency.id ,  p.type.name, p.high_low, p.isin, p.agrupations.dbstring(), p.percentage, p.mode.name, p.leveraged.name, p.decimals,   p.obsolete, p.tickers)
            p.save()
        debug("{} Products added".format(len(added)))
        for p in added:
            print("  +", p,  p.currency.id ,  p.type.name, p.high_low, p.isin, p.agrupations.dbstring(), p.percentage, p.mode.name, p.leveraged.name,  p.decimals, p.obsolete, p.tickers)
            ##Como tiene p.id del xlsx,save haría un update, hago un insert mínimo y luego vuelvo a grabar para que haga update
            cur=self.mem.con.cursor()
            cur.execute("insert into products (id,stockmarkets_id) values (%s,%s)",  (p.id, 1))
            cur.close()
            p.save()
        self.mem.con.commit()
        self.mem.languages.cambiar(oldlanguage)
        os.remove("product.xlsx")
        
        dt_string=dtaware2string(self.dtaware_internet_products_xlsx(), type=1)
        info("Product list version set to {}".format(dt_string))
        self.mem.settingsdb.setValue("Version of products.xlsx", dt_string)
        self.mem.data.load()


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
    ##Biometrics(mem,id)
    def __init__(self, *args):        
        def init__create(name, id):
            self.name=name
            self.id=id
        self.mem=args[0]
        if len(args)==1:
            init__create(None,None)
        elif len(args)==2:
            row=self.mem.con.cursor_one_row("select id,name from elaboratedproducts where id=%s",(args[1],))
            init__create(row[1],row[0])
            self.products_in=ProductsInElaboratedProduct(self.mem, self, self.mem.con.mogrify("select * from products_in_elaboratedproducts where elaboratedproducts_id=%s",(args[1],)))

    def show_table(self):
        self.products_in.show_table()

    def register_in_personal_products(self):
        selected=None
        for p in self.mem.data.products.arr:
            if p.elaboratedproducts_id==self.id:
                 selected=p
        if selected==None:
            o=ProductPersonal(
            self.mem,
            self.name, 
            self.products_in.grams(), 
            self.products_in.fat(), 
            self.products_in.protein(), 
            self.products_in.carbohydrate(), 
            None, 
            None, 
            datetime.now(), 
            self.id, 
            None, 
            self.products_in.calories(), 
            None, 
            None, 
            None, 
            None, 
            self.products_in.fiber(), 
            None, 
            None, 
            None,
            None)
            o.save()
        else:#It's already in personalproducts
            selected.name=self.name
            selected.amount=self.products_in.grams()
            selected.fat=self.products_in.fat()
            selected.protein=self.products_in.protein()
            selected.carbohydrate=self.products_in.carbohydrate()
            selected.calories=self.products_in.calories()
            selected.fiber=self.products_in.fiber()
            selected.save()



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

    def fullName(self,  with_id=False):
        return self.product.fullName(with_id) 

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
        print("MAL·")
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("insert into meals(datetime,products_id,name, amount, users_id, system_product) values (%s, %s,%s,%s,%s,%s) returning id",(self.datetime, self.product.id, self.name, self.amount, self.user.id, self.system_product))
        else:
            self.mem.con.cursor_one_field("update from meals set datetime=%s,products_id=%s,name=%s,amount=%s,users_id=%s, system_product=%s where id=%s", (self.datetime, self.product.id, self.name, self.amount, self.user.id, self.system_product,  self.id))


class ProductsInElaboratedProduct(QObject, ObjectManager_With_IdDatetime):
    ##MealManager(mem)
    ##MealManager(mem,elaboratedproduct,sql)
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
    def grams(self):
        r=Decimal(0)
        for product_in in self.arr:
            r=r+product_in.amount
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
        print (Style.BRIGHT+ "ELABORATED PRODUCT '{}' NUTRICIONAL REPORT".format(self.elaboratedproduct.name.upper()).center(maxlength,' ') + Style.RESET_ALL)
        print (Style.BRIGHT+ "="*(maxlength) + Style.RESET_ALL)

        print (Style.BRIGHT+ "{}  {}  {}  {}  {}  {}  {}".format("NAME".ljust(maxname," "),"GRAMS".rjust(7,' '), "CALORIE".rjust(7,' '), "CARBOHY".rjust(7,' '), "PROTEIN".rjust(7,' '), "FAT".rjust(7,' '), "FIBER".rjust(7,' ')) + Style.RESET_ALL)
        for product_in in self.arr:
            print ( "{}  {}  {}  {}  {}  {}  {}".format(product_in.fullName().ljust(maxname), a2s(product_in.amount),a2s(product_in.calories()), a2s(product_in.carbohydrate()), a2s(product_in.protein()), a2s(product_in.fat()),a2s(product_in.fiber())) + Style.RESET_ALL)

        print (Style.BRIGHT+ "-"*(maxlength) + Style.RESET_ALL)
        total="ELABORATED WITH {} PRODUCTS".format(self.length())
        print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(total.ljust(maxname), a2s(self.grams()), a2s(self.calories()), a2s(self.carbohydrate()), a2s(self.protein()), a2s(self.fat()), a2s(self.fiber())) + Style.RESET_ALL)
#        recomendations="RECOMMENDATIONS"
#        print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(recomendations.ljust(maxname+7), n2s(), a2s(user.bmr()), a2s(user.carbohydrate()), a2s(user.protein()), a2s(user.fat()), a2s(user.fiber())) + Style.RESET_ALL)
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
        table.setRowCount(self.length())
        for i, o in enumerate(self.arr):
            table.setItem(i, 0, qtime(o.datetime))
            table.setItem(i, 1, qleft(o.product.name))
            table.setItem(i, 2, qright(o.amount))
            table.setItem(i, 3, qright(o.calories()))
            table.setItem(i, 4, qright(o.carbohydrate()))
            table.setItem(i, 5, qright(o.protein()))
            table.setItem(i, 6, qright(o.fat()))
            table.setItem(i, 7, qright(o.fiber()))



class ProductAllManager(QObject, ObjectManager_With_IdName_Selectable):
    ## ProductAllManager(mem)#Loads all database
    def __init__(self, *args):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
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

    def find_by_id_system(self,  id ,  system):
        for o in self.arr:
            if o.id==id and o.system_product==system:
                return o
        return None
    
    def qcombobox(self, combo, selected=None):
        combo.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.order_by_name()
        for o in self.arr:
            icon=QIcon(":/caloriestracker/pepa.png") if o.system_product==False else QIcon(":/caloriestracker/book.png")
            combo.addItem(icon, o.fullName(), o.string_id())
        if selected!=None:
            combo.setCurrentIndex(combo.findData(selected.string_id()))
            
    def qtablewidget(self, table):
        ProductManager.qtablewidget(self, table)
        
        
    ## Find by generated string with id and system_product
    def find_by_string_id(self, stringid):
        id=int(stringid.split("#")[0])
        system_product=str2bool(stringid.split("#")[1])
        return self.find_by_id_system(id, system_product)
        
    ## Returns another ProductAllManager with the products that contains a string
    def ProductAllManager_contains_string(self, s):
        r=ProductAllManager(self.mem)
        for o in self.arr:
            if s.upper() in o.fullName().upper():
                r.append(o)
        return r


class DBData:
    def __init__(self, mem):
        self.mem=mem

    def load(self, progress=True):
        start=datetime.now()
        
        self.companies=CompanyAllManager(self.mem)

        self.products=ProductAllManager(self.mem)
        self.products.load_all()
        
        self.users=UserManager(self.mem, "select * from users", progress)
        self.users.load_last_biometrics()
        
        debug("DBData took {}".format(datetime.now()-start))

class Biometrics:    
    ##Biometrics(mem)
    ##Biometrics(mem,rows)
    ##Biometrics(mem,dt, height, weight, user, activity, id):
    def __init__(self, *args):        
        def init__create(dt, height, weight, user, activity, id):
            self.datetime=dt
            self.height=height
            self.weight=weight
            self.user=user
            self.activity=activity
            self.id=id
        # #########################################
        self.mem=args[0]
        if len(args)==1:#Biometrics(mem)
            init__create(*[None]*6)
        elif len(args)==2:#Biometrics(mem,rows)
            user=self.mem.data.users.find_by_id(args[1]['users_id'])
            init__create(args[1]['datetime'], args[1]['height'], args[1]['weight'], user, args[1]['activity'],  args[1]['id'])
        elif len(args)==5:#Biometrics(mem,dt, height, weight, user, activity, id):
            init__create(args[1], args[2], args[3], args[4])
    
    def __repr__(self):
        return "{} {}".format(self.height, self.weight)
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
        cur.execute(sql)#"select * from products where id in ("+lista+")" 
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

class CompanySystem:
    ##CompanySystem(mem)
    ##CompanySystem(mem,rows)
    ##CompanySystem(mem,name,starts,ends,id)
    def __init__(self, *args):        
        def init__create(name,  starts, ends, id):
            self.name=name
            self.starts=starts
            self.ends=ends
            self.id=id
            return self
        # #########################################
        self.mem=args[0]
        if len(args)==1:#CompanySystem(mem)
            init__create(*[None]*4)
        elif len(args)==2:#CompanySystem(mem,rows)
            init__create(args[1]['name'], args[1]['starts'], args[1]['ends'], args[1]['id'])
        elif len(args)==5:#CompanySystem(mem,name,starts,ends,id)
            init__create(args[1], args[2], args[3], args[4])
        self.system_company=True

        
    def __repr__(self):
        return self.fullName()
        
    def fullName(self):
        system="S" if self.system_company==True else "P"
        return "{}. #{}{}".format(self.name, system, self.id)
        
    def save(self):
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("insert into companies(name,starts,ends) values (%s, %s, %s) returning id", (self.name, self.starts, self.ends))
        else:
            self.mem.con.cursor_one_field("update companies set name=%s,starts=%s, ends=%s where id=%s", (self.name, self.starts, self.ends, self.id))
            
    def insert_string(self, table="companies"):
        return self.mem.con.mogrify("insert into "+table +"(name,starts,ends, id) values (%s, %s, %s, %s)", (self.name, self.starts, self.ends, self.id))


class CompanyPersonal(CompanySystem):
    def __init__(self, *args):
        CompanySystem.__init__(self, *args)
        self.system_company=False
        
    def save(self):
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("insert into personalcompanies(name,starts,ends) values (%s, %s, %s) returning id", (self.name, self.starts, self.ends))
        else:
            self.mem.con.cursor_one_field("update personalcompanies set name=%s,starts=%s, ends=%s where id=%s", (self.name, self.starts, self.ends, self.id))


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
                print ("  + {}".format(o.fullName(True)))

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


class Product(QObject):
    ##Product(mem)
    ##Product(mem,rows) #Uses products_id and users_id in row
    ##Product(mem,datetime,product,name,amount,users_id,id)
    def __init__(self, *args):        
        def init__create( name, amount, fat, protein, carbohydrate, company, ends, starts, elaboratedproducts_id, languages_id, calories, salt, cholesterol, sodium, potassium, fiber, sugars, saturated_fat, system_company, id):
            self.name=name
            self.amount=amount
            self.fat=fat
            self.protein=protein
            self.carbohydrate=carbohydrate
            self.company=company
            self.ends=ends
            self.starts=starts
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
            init__create(*[None]*20)
        elif len(args)==2:#Product(mem,rows)
            company=self.mem.data.companies.find_by_id_system(args[1]['companies_id'], args[1]['system_company'])
            init__create(args[1]['name'], args[1]['amount'], args[1]['fat'], args[1]['protein'], args[1]['carbohydrate'], company, 
            args[1]['ends'], args[1]['starts'], args[1]['elaboratedproducts_id'], args[1]['languages'], args[1]['calories'], args[1]['salt'], 
            args[1]['cholesterol'], args[1]['sodium'], args[1]['potassium'], args[1]['fiber'], args[1]['sugars'], args[1]['saturated_fat'], args[1]['system_company'], args[1]['id'])
        elif len(args)==21:#Product(mem,datetime,product,name,amount,users_id,id)
            init__create(*args[1:])
        self.system_product=True

    def __repr__(self):
        return self.fullName(True)


    def fullName(self,  with_id=False):
        if with_id==True:
            system="S" if self.system_product==True else "P"
            str_with_id=". #{}{}".format(system,self.id)
        else:
            str_with_id=""
        if self.company==None:
            if self.elaboratedproducts_id==None:
                return "{}{}".format(self.name, str_with_id)
            else:
                elaborated=self.tr("Elaborated by me")
                return "{}{} ({})".format(self.name, str_with_id, elaborated)
        else:
            return "{} ({}){}".format(self.name, self.company.name, str_with_id)

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
                    name, amount, fat, protein, carbohydrate, companies_id, ends, starts, 
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company
                    )values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id""",  
                    (self.name, self.amount, self.fat, self.protein, self.carbohydrate, companies_id, self.ends, self.starts, 
                    self.elaboratedproducts_id, self.languages, self.calories, self.salt, self.cholesterol, self.sodium, 
                    self.potassium, self.fiber, self.sugars, self.saturated_fat, self.system_company))
        else:
            self.mem.con.cursor_one_field("""update products set name=%s, amount=%s, fat=%s, protein=%s, carbohydrate=%s, companies_id=%s, ends=%s, starts=%s, 
            elaboratedproducts_id=%s, languages=%s, calories=%s, salt=%s, cholesterol=%s, sodium=%s, potassium=%s, fiber=%s, sugars=%s, saturated_fat=%s, system_company=%s
            where id=%s returning id""", 
            (self.name, self.amount, self.fat, self.protein, self.carbohydrate, companies_id, self.ends, self.starts, 
            self.elaboratedproducts_id, self.languages, self.calories, self.salt, self.cholesterol, self.sodium, self.potassium, self.fiber, self.sugars, self.saturated_fat, self.system_company,  self.id))

    ## Generates an string with id and system_product
    def string_id(self):
        return "{}#{}".format(self.id, self.system_product)
        
    def insert_string(self, table="products"):
        companies_id=None if self.company==None else self.company.id
        return self.mem.con.mogrify("insert into " + table +" (name, amount, fat, protein, carbohydrate, companies_id, ends, starts, elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, potassium, fiber, sugars, saturated_fat,system_company, id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",  
            (self.name, self.amount, self.fat, self.protein, self.carbohydrate, companies_id, self.ends, self.starts, self.elaboratedproducts_id, self.languages, self.calories, self.salt, self.cholesterol, self.sodium, self.potassium, self.fiber, self.sugars, self.saturated_fat, self.system_company, self.id))

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
        return Decimal(100)*component_amount/self.amount

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
                    name, amount, fat, protein, carbohydrate, companies_id, ends, starts, 
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company
                    )values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id""",  
                    (self.name, self.amount, self.fat, self.protein, self.carbohydrate, companies_id, self.ends, self.starts, 
                    self.elaboratedproducts_id, self.languages, self.calories, self.salt, self.cholesterol, self.sodium, 
                    self.potassium, self.fiber, self.sugars, self.saturated_fat, self.system_company))
        else:
            self.mem.con.cursor_one_field("""update personalproducts set name=%s, amount=%s, fat=%s, protein=%s, carbohydrate=%s, companies_id=%s, ends=%s, starts=%s, 
            elaboratedproducts_id=%s, languages=%s, calories=%s, salt=%s, cholesterol=%s, sodium=%s, potassium=%s, fiber=%s, sugars=%s, saturated_fat=%s, system_company=%s
            where id=%s returning id""", 
            (self.name, self.amount, self.fat, self.protein, self.carbohydrate, companies_id, self.ends, self.starts, 
            self.elaboratedproducts_id, self.languages, self.calories, self.salt, self.cholesterol, self.sodium, self.potassium, self.fiber, self.sugars, self.saturated_fat, self.system_company,  self.id))
           
## Manages languages
class TranslationLanguageManager(ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=mem
        
    def load_all(self):
        self.append(TranslationLanguage(self.mem, "en","English" ))
        self.append(TranslationLanguage(self.mem, "es","Español" ))
        self.append(TranslationLanguage(self.mem, "fr","Français" ))
        self.append(TranslationLanguage(self.mem, "ro","Rom\xe2n" ))
        self.append(TranslationLanguage(self.mem, "ru",'\u0420\u0443\u0441\u0441\u043a\u0438\u0439' ))

    def qcombobox(self, combo, selected=None):
        """Selected is the object"""
        self.order_by_name()
        for l in self.arr:
            combo.addItem(l.name, l.id)
        if selected!=None:
                combo.setCurrentIndex(combo.findData(selected.id))

    ## @param id String
    def cambiar(self, id):
        filename=package_filename("caloriestracker", "i18n/caloriestracker_{}.qm".format(id))
        self.mem.qtranslator.load(filename)
        info("TranslationLanguage changed to {}".format(id))
        qApp.installTranslator(self.mem.qtranslator)
 
class TranslationLanguage:
    def __init__(self, mem, id, name):
        self.id=id
        self.name=name

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

    def fullName(self,  with_id=False):
        return self.product.fullName(with_id) 

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
        print (Style.BRIGHT+ Fore.BLUE + "IMC: {} ==> {}".format(round(self.mem.user.imc(),2),self.mem.user.imc_comment()).center(maxlength," ") + Style.RESET_ALL)
        print (Style.BRIGHT+ "="*(maxlength) + Style.RESET_ALL)

        print (Style.BRIGHT+ "{}  {}  {}  {}  {}  {}  {}  {}".format("HOUR ","NAME".ljust(maxname," "),"GRAMS".rjust(7,' '), "CALORIE".rjust(7,' '), "CARBOHY".rjust(7,' '), "PROTEIN".rjust(7,' '), "FAT".rjust(7,' '), "FIBER".rjust(7,' ')) + Style.RESET_ALL)
        for meal in self.arr:
            print ( "{}  {}  {}  {}  {}  {}  {}  {}".format(meal.meal_hour(), meal.fullName().ljust(maxname), a2s(meal.amount),a2s(meal.calories()), a2s(meal.carbohydrate()), a2s(meal.protein()), a2s(meal.fat()),a2s(meal.fiber())) + Style.RESET_ALL)

        print (Style.BRIGHT+ "-"*(maxlength) + Style.RESET_ALL)
        total="{} MEALS WITH THIS TOTALS".format(self.length())
        print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(total.ljust(maxname+7), a2s(self.grams()), ca2s(self.calories(),self.mem.user.bmr()), ca2s(self.carbohydrate(),self.mem.user.carbohydrate()), ca2s(self.protein(), self.mem.user.protein()), ca2s(self.fat(),self.mem.user.fat()), rca2s(self.fiber(),self.mem.user.fiber())) + Style.RESET_ALL)
        recomendations="RECOMMENDATIONS"
        print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(recomendations.ljust(maxname+7), n2s(), a2s(self.mem.user.bmr()), a2s(self.mem.user.carbohydrate()), a2s(self.mem.user.protein()), a2s(self.mem.user.fat()), a2s(self.mem.user.fiber())) + Style.RESET_ALL)
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
            table.setItem(i, 2, qnumber(o.amount))
            table.setItem(i, 3, qnumber(o.calories()))
            table.setItem(i, 4, qnumber(o.carbohydrate()))
            table.setItem(i, 5, qnumber(o.protein()))
            table.setItem(i, 6, qnumber(o.fat()))
            table.setItem(i, 7, qnumber(o.fiber()))
        #Totals
        table.setItem(self.length(), 1, qleft(self.tr("Total")))
        table.setItem(self.length(), 2, qnumber(self.grams()))
        table.setItem(self.length(), 3, qnumber_limited(self.calories(), self.mem.user.bmr()))
        table.setItem(self.length(), 4, qnumber_limited(self.carbohydrate(), self.mem.user.carbohydrate()))
        table.setItem(self.length(), 5, qnumber_limited(self.protein(), self.mem.user.protein()))
        table.setItem(self.length(), 6, qnumber_limited(self.fat(), self.mem.user.fat()))
        table.setItem(self.length(), 7, qnumber_limited(self.fiber(), self.mem.user.fiber(), reverse=True))
        #Recomendatios
        table.setItem(self.length()+1, 1, qleft(self.tr("Recomendatios")))
        table.setItem(self.length()+1, 3, qnumber(self.mem.user.bmr()))
        table.setItem(self.length()+1, 4, qnumber(self.mem.user.carbohydrate()))
        table.setItem(self.length()+1, 5, qnumber(self.mem.user.protein()))
        table.setItem(self.length()+1, 6, qnumber(self.mem.user.fat()))
        table.setItem(self.length()+1, 7, qnumber(self.mem.user.fiber()))
        
class User:
    ##User(mem)
    ##User(mem,rows) #Uses products_id and users_id in row
    ##User( name, male, birthday, starts, ends, dietwish, id):
    def __init__(self, *args):        
        def init__create( name, male, birthday, starts, ends, dietwish, id):
            self.name=name
            self.male=male
            self.birthday=birthday
            self.starts=starts
            self.ends=ends
            self.dietwish=dietwish
            self.id=id
        # #########################################
        self.mem=args[0]
        if len(args)==1:#User(mem)
            init__create(*[None]*7)
        elif len(args)==2:#User(mem,rows)
            init__create(args[1]['name'], args[1]['male'], args[1]['birthday'], args[1]['starts'],  args[1]['ends'],  args[1]['dietwish'],  args[1]['id'])
        elif len(args)==8:#User( name, male, birthday, starts, ends, dietwish, id):
            init__create(*args[1:])
    
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

    ##basal metabolic rate
    def bmr(self):
        if self.last_biometrics.activity==0:
            mult=Decimal(1.2)
        elif self.last_biometrics.activity==1:
            mult=Decimal(1.375)
        elif self.last_biometrics.activity==2:
            mult=Decimal(1.55)
        elif self.last_biometrics.activity==3:
            mult=Decimal(1.72)
        elif self.last_biometrics.activity==4:
            mult=Decimal(1.9)

        if self.male==True:
            return mult*(Decimal(10)*self.last_biometrics.weight + Decimal(6.25)*self.last_biometrics.height - Decimal(5)*self.age() + 5)
        else: #female
            return mult*(Decimal(10)*self.last_biometrics.weight + Decimal(6.25)*self.last_biometrics.height - Decimal(5)*self.age() - 161)

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

    def age(self):
        return (date.today() - self.birthday) // timedelta(days=365.2425)
    # Índice de masa corporal
    def imc(self):
        return self.last_biometrics.weight/((self.last_biometrics.height/100)**2)
    
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
            
## Class to manage users
## UserManager(mem)
## UserManager(mem,sql,progress)
class UserManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, *args):
        def load_from_db(sql,  progress=False):
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
                    
                inv=User(self.mem, rowms)
                self.append(inv)
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


        
