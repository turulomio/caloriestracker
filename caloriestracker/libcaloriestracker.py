## @namespace caloriestracker.libcaloriestracker
## @brief Package with all caloriestracker core classes .

from PyQt5.QtCore import Qt,  QSettings, QCoreApplication, QTranslator, QObject
from PyQt5.QtGui import QIcon,  QColor,  QPixmap
from PyQt5.QtWidgets import QTableWidgetItem, QApplication,   qApp,  QProgressDialog

from datetime import date,  timedelta, datetime
import logging
import pytz
import sys
import argparse
import getpass
import os
from decimal import Decimal
from caloriestracker.connection_pg_qt import ConnectionQt
from caloriestracker.github import get_file_modification_dtaware
from caloriestracker.libcaloriestrackerfunctions import str2bool, dtaware2string, list2string, dirs_create, package_filename, is_there_internet, qtime, qleft, qright
from caloriestracker.libmanagers import Object_With_IdName, ObjectManager_With_Id_Selectable,  ManagerSelectionMode, ObjectManager_With_IdName_Selectable, ObjectManager_With_IdDatetime
from officegenerator import OpenPyXL

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
            logging.debug(o.__class__)
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


class CompanyManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=mem


    def load_from_db(self, sql,  progress=False):
        """sql es una query sobre la tabla inversiones
        Carga estimations_dbs, y basic
        """
        self.clean()
        cur=self.mem.con.cursor()
        cur.execute(sql)#"select * from products where id in ("+lista+")" 
        if progress==True:
            pd= QProgressDialog(self.tr("Loading {0} companies from database").format(cur.rowcount),None, 0,cur.rowcount)
            pd.setWindowIcon(QIcon(":/caloriestracker/coins.png"))
            pd.setModal(True)
            pd.setWindowTitle(self.tr("Loading companies..."))
            pd.forceShow()
        for rowms in cur:
            if progress==True:
                pd.setValue(cur.rownumber)
                pd.update()
                QApplication.processEvents()
                
            inv=Company(self.mem).init__db_row(rowms)
            self.append(inv)
        cur.close()
        
## Clase parar trabajar con las opercuentas generadas automaticamente por los movimientos de las inversiones

## Class to manage products
class ProductManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.setSelectionMode(ManagerSelectionMode.List)
        self.mem=mem

    def load_from_db(self, sql,  progress=False):
        """sql es una query sobre la tabla inversiones
        Carga estimations_dbs, y basic
        """
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
                
            inv=Product(self.mem).init__db_row(rowms)
            self.append(inv)
        cur.close()
        

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
        logging.debug("{} Products changed".format(len(changed)))
        for p in changed:
            print("  +", p,  p.currency.id ,  p.type.name, p.high_low, p.isin, p.agrupations.dbstring(), p.percentage, p.mode.name, p.leveraged.name, p.decimals,   p.obsolete, p.tickers)
            p.save()
        logging.debug("{} Products added".format(len(added)))
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
        logging.info("Product list version set to {}".format(dt_string))
        self.mem.settingsdb.setValue("Version of products.xlsx", dt_string)
        self.mem.data.load()


class CountryManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=mem   
        
    def load_all(self):
        self.append(Country("es",self.tr("Spain")))
        self.append(Country("be",self.tr("Belgium")))
        self.append(Country("cn",self.tr("China")))
        self.append(Country("de",self.tr("Germany")))
        self.append(Country("earth",self.tr("Earth")))
        self.append(Country("en",self.tr("United Kingdom")))
        self.append(Country("eu",self.tr("Europe")))
        self.append(Country("fi",self.tr("Finland")))
        self.append(Country("fr",self.tr("France")))
        self.append(Country("ie",self.tr("Ireland")))
        self.append(Country("it",self.tr("Italy")))
        self.append(Country("jp",self.tr("Japan")))
        self.append(Country("nl",self.tr("Netherlands")))
        self.append(Country("pt",self.tr("Portugal")))
        self.append(Country("us",self.tr("United States of America")))
        self.append(Country("ro",self.tr("Romanian")))
        self.append(Country("ru",self.tr("Rusia")))
        self.append(Country("lu",self.tr("Luxembourg")))
        self.order_by_name()

    def qcombobox(self, combo,  country=None):
        """Función que carga en un combo pasado como parámetro y con un AccountManager pasado como parametro
        Se ordena por nombre y se se pasa el tercer parametro que es un objeto Account lo selecciona""" 
        for cu in self.arr:
            combo.addItem(cu.qicon(), cu.name, cu.id)

        if country!=None:
                combo.setCurrentIndex(combo.findData(country.id))

    def qcombobox_translation(self, combo,  country=None):
        """Función que carga en un combo pasado como parámetro con los pa´ises que tienen traducción""" 
        for cu in [self.find_by_id("es"),self.find_by_id("fr"),self.find_by_id("ro"),self.find_by_id("ru"),self.find_by_id("en") ]:
            combo.addItem(cu.qicon(), cu.name, cu.id)

        if country!=None:
                combo.setCurrentIndex(combo.findData(country.id))

class DBData:
    def __init__(self, mem):
        self.mem=mem

    def load(self, progress=True):
        start=datetime.now()
        self.companies=CompanyManager(self.mem)
        self.companies.load_from_db("select * from companies")
        
        self.products=ProductManager(self.mem)
        self.products.load_from_db("select * from products", progress)
        logging.debug("DBData took {}".format(datetime.now()-start))



class Company:
    def __init__(self, mem):
        self.mem=mem
        self.name=None
        self.id=None
                
    def init__db_row(self, row):
        self.name=row['name']
        self.id=row['id']
        return self
        
class Product:
    def __init__(self, mem):
        self.mem=mem
        self.name=None
        self.id=None
        
        
#    ## Compares this product with other products
#    ## Logs differences
#    def __eq__(self, other):
#        if (self.id!=other.id or
#            self.name!=other.name or
#            self.isin!=other.isin or
#            self.stockmarket.id!=other.stockmarket.id or
#            self.currency.id!=other.currency.id or
#            self.type.id!=other.type.id or
#            self.agrupations.dbstring()!=other.agrupations.dbstring() or 
#            self.web!=other.web or
#            self.address!=other.address or
#            self.phone!=other.phone or
#            self.mail!=other.mail or
#            self.percentage!=other.percentage or
#            self.mode.id!=other.mode.id or
#            self.leveraged.id!=other.leveraged.id or
#            self.comment!=other.comment or 
#            self.obsolete!=other.obsolete or
#            self.tickers[0]!=other.tickers[0] or
#            self.tickers[1]!=other.tickers[1] or
#            self.tickers[2]!=other.tickers[2] or
#            self.tickers[3]!=other.tickers[3]):
#            return False
#        return True
#        
#    def __ne__(self, other):
#        return not self.__eq__(other)
    def __repr__(self):
        return "{0} ({1}) de la {2}".format(self.name , self.id, self.stockmarket.name)
                
    def init__db_row(self, row):
        if row['companies_id']==None:
            self.company=None
        else:
            self.company=self.mem.data.companies.find_by_id(row['companies_id']) 
        self.name=row['name']
        self.id=row['id']
        self.calories=row['calories']
        self.fat=row['fat']
        self.protein=row['protein']
        self.amount=row['amount']
        self.carbohydrate=row['carbohydrate']
        self.salt=row['salt']
        self.fiber=row['fiber']
        return self


    def init__create(self, name,  isin, currency, type, agrupations, active, web, address, phone, mail, percentage, mode, leveraged, decimals, stockmarket, tickers, comment, obsolete, high_low, id=None):

        return self        

    def init__db(self, id):
        """Se pasa id porque se debe usar cuando todavía no se ha generado."""
        cur=self.mem.con.cursor()
        cur.execute("select * from products where id=%s", (id, ))
        row=cur.fetchone()
        cur.close()
        return self.init__db_row(row)

    def save(self):
        """
            Esta función inserta una inversión manua
            Los arrays deberan pasarse como parametros ARRAY[1,2,,3,] o None
        """
        
        cur=self.mem.con.cursor()
        if self.id==None:
            cur.execute("select min(id)-1 from products")
            id=cur.fetchone()[0]
            if id>=0:
                id=-1
            cur.execute("insert into products (id, name,  isin,  currency,  type,  agrupations,   web, address,  phone, mail, percentage, pci,  leveraged, decimals, stockmarkets_id, tickers, comment, obsolete, high_low) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",  (id, self.name,  self.isin,  self.currency.id,  self.type.id,  self.agrupations.dbstring(), self.web, self.address,  self.phone, self.mail, self.percentage, self.mode.id,  self.leveraged.id, self.decimals, self.stockmarket.id, self.tickers, self.comment, self.obsolete, self.high_low))
            self.id=id
        else:
            cur.execute("update products set name=%s, isin=%s,currency=%s,type=%s, agrupations=%s, web=%s, address=%s, phone=%s, mail=%s, percentage=%s, pci=%s, leveraged=%s, decimals=%s, stockmarkets_id=%s, tickers=%s, comment=%s, obsolete=%s,high_low=%s where id=%s", ( self.name,  self.isin,  self.currency.id,  self.type.id,  self.agrupations.dbstring(),  self.web, self.address,  self.phone, self.mail, self.percentage, self.mode.id,  self.leveraged.id, self.decimals, self.stockmarket.id, self.tickers, self.comment, self.obsolete, self.high_low,  self.id))
        cur.close()
    
    
    ## Return if the product has autoupdate in some source
    def has_autoupdate(self):
        if self.obsolete==True:
            return False
        if self.id in self.mem.autoupdate:
            return True
        return False


    def hasSameLocalCurrency(self):
        """
            Returns a boolean
            Check if product currency is the same that local currency
        """
        if self.currency.id==self.mem.localcurrency.id:
            return True
        return False

    def is_deletable(self):
        if self.is_system():
            return False
            
        #Search in all investments
        for i in self.mem.data.investments.arr:
            if i.product.id==self.id:
                return False
        
        #Search in benchmark
        if self.mem.data.benchmark.id==self.id:
            return False
        
        return True       

    def is_system(self):
        """Returns if the product is a system product or a user product"""
        if self.id>=0:
            return True
        return False

    ## @return boolen if could be done
    ## NO HACE COMMIT
    def remove(self):     
        if self.is_deletable()==True and self.is_system()==False:
            cur=self.mem.con.cursor()
            cur.execute("delete from quotes where id=%s", (self.id, ))
            cur.execute("delete from estimations_dps where id=%s", (self.id, ))
            cur.execute("delete from estimations_eps where id=%s", (self.id, ))
            cur.execute("delete from dps where id=%s", (self.id, ))
            cur.execute("delete from splits where products_id=%s", (self.id, ))
            cur.execute("delete from opportunities where products_id=%s", (self.id, ))
            cur.execute("delete from products where id=%s", (self.id, ))
            cur.close()
            self.needStatus(0, downgrade_to=0)
            return True
        return False




## Manages languages
class LanguageManager(ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=mem
        
    def load_all(self):
        self.append(Language(self.mem, "en","English" ))
        self.append(Language(self.mem, "es","Español" ))
        self.append(Language(self.mem, "fr","Français" ))
        self.append(Language(self.mem, "ro","Rom\xe2n" ))
        self.append(Language(self.mem, "ru",'\u0420\u0443\u0441\u0441\u043a\u0438\u0439' ))

    def qcombobox(self, combo, selected=None):
        """Selected is the object"""
        self.order_by_name()
        for l in self.arr:
            combo.addItem(self.mem.countries.find_by_id(l.id).qicon(), l.name, l.id)
        if selected!=None:
                combo.setCurrentIndex(combo.findData(selected.id))

    ## @param id String
    def cambiar(self, id):
        filename=package_filename("caloriestracker", "i18n/caloriestracker_{}.qm".format(id))
        logging.debug(filename)
        self.mem.qtranslator.load(filename)
        logging.info("Language changed to {}".format(id))
        qApp.installTranslator(self.mem.qtranslator)
 


class Language:
    def __init__(self, mem, id, name):
        self.id=id
        self.name=name
    
            

class SettingsDB:
    def __init__(self, mem):
        self.mem=mem
    
    def in_db(self, name):
        """Returns true if globals is saved in database"""
        cur=self.mem.con.cursor()
        cur.execute("select value from globals where id_globals=%s", (self.id(name), ))
        num=cur.rowcount
        cur.close()
        if num==0:
            return False
        else:
            return True
  
    def value(self, name, default):
        """Search in database if not use default"""            
        cur=self.mem.con.cursor()
        cur.execute("select value from globals where id_globals=%s", (self.id(name), ))
        if cur.rowcount==0:
            cur.close()
            return default
        else:
            value=cur.fetchone()[0]
            cur.close()
            if value==None:
                return default
            return value
        
    def setValue(self, name, value):
        """Set the global value.
        It doesn't makes a commit, you must do it manually
        value can't be None
        """
        cur=self.mem.con.cursor()
        if self.in_db(name)==False:
            cur.execute("insert into globals (id_globals, global,value) values(%s,%s,%s)", (self.id(name),  name, value))     
        else:
            cur.execute("update globals set global=%s, value=%s where id_globals=%s", (name, value, self.id(name)))
        cur.close()
        self.mem.con.commit()
        
    def id(self,  name):
        """Converts section and name to id of table globals"""
        if name=="Version of products.xlsx":
            return 2
        elif name=="wdgIndexRange/spin":
            return 7
        elif name=="wdgIndexRange/invertir":
            return 8
        elif name=="wdgIndexRange/minimo":
            return 9
        elif name=="wdgLastCurrent/spin":
            return 10
        elif name=="mem/localcurrency":
            return 11
        elif name=="mem/localzone":
            return 12
        elif name=="mem/benchmarkid":
            return 13
        elif name=="mem/dividendwithholding":
            return 14
        elif name=="mem/taxcapitalappreciation":
            return 15
        elif name=="mem/taxcapitalappreciationbelow":
            return 16
        elif name=="mem/gainsyear":
            return 17
        elif name=="mem/favorites":
            return 18
        elif name=="mem/fillfromyear":
            return 19
        elif name=="frmSellingPoint/lastgainpercentage":
            return 20
        elif name=="wdgAPR/cmbYear":
            return 21
        elif name=="wdgLastCurrent/viewode":
            return 22
        return None

class MemSources:
    def __init__(self):
        self.data=DBData(self)
        
        self.countries=CountryManager(self)
        self.countries.load_all()
        
        self.zones=ZoneManager(self)
        self.zones.load_all()
        #self.localzone=self.zones.find_by_name(self.settingsdb.value("mem/localzone", "Europe/Madrid"))
       
        
        
class MemCaloriestracker:
    def __init__(self):                
        self.dir_tmp=dirs_create()
        
        self.qtranslator=None#Residirá el qtranslator
        self.settings=QSettings()
        self.settingsdb=SettingsDB(self)
        
        self.inittime=datetime.now()#Tiempo arranca el config
        self.dbinitdate=None#Fecha de inicio bd.
        self.con=None#Conexión        
        
        #Loading data in code
        self.countries=CountryManager(self)
        self.countries.load_all()
        self.languages=LanguageManager(self)
        self.languages.load_all()
        
        #Mem variables not in database
        self.language=self.languages.find_by_id(self.settings.value("mem/language", "en"))
        
        self.frmMain=None #Pointer to mainwidget
        self.closing=False#Used to close threads
        self.url_wiki="https://github.com/turulomio/caloriestracker/wiki"

    def init__script(self, title, tickers=False, sql=False):
        """
            Script arguments and autoconnect in mem.con, load_db_data
            
            type==1 #tickers
        """
        app = QCoreApplication(sys.argv)
        app.setOrganizationName("Mariano Muñoz ©")
        app.setOrganizationDomain("turulomio.users.sourceforge.net")
        app.setApplicationName("Xulpymoney")

        self.setQTranslator(QTranslator(app))
        self.languages.cambiar(self.language.id)

        parser=argparse.ArgumentParser(title)
        parser.add_argument('--user', help='Postgresql user', default='postgres')
        parser.add_argument('--port', help='Postgresql server port', default=5432)
        parser.add_argument('--host', help='Postgresql server address', default='127.0.0.1')
        parser.add_argument('--db', help='Postgresql database', default='caloriestracker')
        if tickers:
            parser.add_argument('--tickers', help='Generate tickers', default=False, action='store_true')
        if sql:
            parser.add_argument('--sql', help='Generate update sql', default=False, action='store_true')

        args=parser.parse_args()
        password=getpass.getpass()
        self.con=ConnectionQt().init__create(args.user,  password,  args.host, args.port, args.db)
        self.con.connect()
        if not self.con.is_active():
            logging.critical(QCoreApplication.translate("Core", "Error connecting to database"))
            sys.exit(255)        
        self.load_db_data(progress=False, load_data=False)
        return args


    def __del__(self):
        if self.con:#Cierre por reject en frmAccess
            self.con.disconnect()
            
    def setQTranslator(self, qtranslator):
        self.qtranslator=qtranslator

        

    def load_db_data(self, progress=True, load_data=True):
        """Esto debe ejecutarse una vez establecida la conexión"""
        inicio=datetime.now()

        self.zones=ZoneManager(self)
        self.zones.load_all()

        if load_data:
            self.data=DBData(self)
            self.data.load(progress)

        logging.info("Loading db data took {}".format(datetime.now()-inicio))
        
    def save_MemSettingsDB(self):
        self.settingsdb.setValue("mem/localcurrency", self.localcurrency.id)
        self.settingsdb.setValue("mem/localzone", self.localzone.name)
        self.settingsdb.setValue("mem/dividendwithholding", Decimal(self.dividendwithholding))
        self.settingsdb.setValue("mem/taxcapitalappreciation", Decimal(self.taxcapitalappreciation))
        self.settingsdb.setValue("mem/taxcapitalappreciationbelow", Decimal(self.taxcapitalappreciationbelow))
        self.settingsdb.setValue("mem/gainsyear", self.gainsyear)
        self.settingsdb.setValue("mem/favorites", list2string(self.favorites))
        self.settingsdb.setValue("mem/benchmarkid", self.data.benchmark.id)
        self.settingsdb.setValue("mem/fillfromyear", self.fillfromyear)
        logging.info ("Saved Database settings")
        
        
    def qicon_admin(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/caloriestracker/admin.png"), QIcon.Normal, QIcon.Off)
        return icon

class Country(Object_With_IdName):
    def __init__(self, *args):
        Object_With_IdName.__init__(self, *args)
            
    def qicon(self):
        icon=QIcon()
        icon.addPixmap(self.qpixmap(), QIcon.Normal, QIcon.Off)    
        return icon 
        
    def qpixmap(self):
        if self.id=="be":
            return QPixmap(":/countries/belgium.gif")
        elif self.id=="cn":
            return QPixmap(":/countries/china.gif")
        elif self.id=="fr":
            return QPixmap(":/countries/france.gif")
        elif self.id=="ie":
            return QPixmap(":/countries/ireland.gif")
        elif self.id=="it":
            return QPixmap(":/countries/italy.gif")
        elif self.id=="earth":
            return QPixmap(":/countries/earth.png")
        elif self.id=="es":
            return QPixmap(":/countries/spain.gif")
        elif self.id=="eu":
            return QPixmap(":/countries/eu.gif")
        elif self.id=="de":
            return QPixmap(":/countries/germany.gif")
        elif self.id=="fi":
            return QPixmap(":/countries/finland.gif")
        elif self.id=="nl":
            return QPixmap(":/countries/nethland.gif")
        elif self.id=="en":
            return QPixmap(":/countries/uk.gif")
        elif self.id=="jp":
            return QPixmap(":/countries/japan.gif")
        elif self.id=="pt":
            return QPixmap(":/countries/portugal.gif")
        elif self.id=="us":
            return QPixmap(":/countries/usa.gif")
        elif self.id=="ro":
            return QPixmap(":/countries/rumania.png")
        elif self.id=="ru":
            return QPixmap(":/countries/rusia.png")
        elif self.id=="lu":
            return QPixmap(":/countries/luxembourg.png")
        else:
            return QPixmap(":/caloriestracker/star.gif")
            
## Class to manage datetime timezone and its methods
class Zone:
    ## Constructor with the following attributes combination
    ## 1. Zone(mem). Create a Zone with all attributes set to None, except mem
    ## 2. Zone(mem, id, name, country). Create account passing all attributes
    ## @param mem MemXulpymoney object
    ## @param id Integer that represents the Zone Id
    ## @param name Zone Name
    ## @param country Country object asociated to the timezone
    def __init__(self, *args):
        def init__create(id, name, country):
            self.id=id
            self.name=name
            self.country=country
            return self
        self.mem=args[0]
        if len(args)==1:
            init__create(None, None, None)
        if len(args)==4:
            init__create(args[1], args[2], args[3])

    ## Returns a pytz.timezone
    def timezone(self):
        return pytz.timezone(self.name)
        
    ## Datetime aware with the pyttz.timezone
    def now(self):
        return datetime.now(pytz.timezone(self.name))
        
    ## Internal __repr__ function
    def __repr__(self):
        return "Zone ({}): {}".format(str(self.id), str(self.name))            

    ## Not all zones names are in pytz zone names. Sometimes we need a conversión
    ##
    ## It's a static method you can invoke with Zone.zone_name_conversion(name)
    ## @param name String with zone not in pytz
    ## @return String with zone name already converted if needed
    @staticmethod
    def zone_name_conversion(name):
        if name=="CEST":
            return "Europe/Berlin"
        if name.find("GMT")!=-1:
            return "Etc/{}".format(name)
        return name

class ZoneManager(ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=mem
        
    def load_all(self):
        self.append(Zone(self.mem,1,'Europe/Madrid', self.mem.countries.find_by_id("es")))
        self.append(Zone(self.mem,2,'Europe/Lisbon', self.mem.countries.find_by_id("pt")))
        self.append(Zone(self.mem,3,'Europe/Rome', self.mem.countries.find_by_id("it")))
        self.append(Zone(self.mem,4,'Europe/London', self.mem.countries.find_by_id("en")))
        self.append(Zone(self.mem,5,'Asia/Tokyo', self.mem.countries.find_by_id("jp")))
        self.append(Zone(self.mem,6,'Europe/Berlin', self.mem.countries.find_by_id("de")))
        self.append(Zone(self.mem,7,'America/New_York', self.mem.countries.find_by_id("us")))
        self.append(Zone(self.mem,8,'Europe/Paris', self.mem.countries.find_by_id("fr")))
        self.append(Zone(self.mem,9,'Asia/Hong_Kong', self.mem.countries.find_by_id("cn")))
        self.append(Zone(self.mem,10,'Europe/Brussels', self.mem.countries.find_by_id("be")))
        self.append(Zone(self.mem,11,'Europe/Amsterdam', self.mem.countries.find_by_id("nl")))
        self.append(Zone(self.mem,12,'Europe/Dublin', self.mem.countries.find_by_id("ie")))
        self.append(Zone(self.mem,13,'Europe/Helsinki', self.mem.countries.find_by_id("fi")))
        self.append(Zone(self.mem,14,'Europe/Lisbon', self.mem.countries.find_by_id("pt")))
        self.append(Zone(self.mem,15,'Europe/Luxembourg', self.mem.countries.find_by_id("lu")))
        
    def qcombobox(self, combo, zone=None):
        """Carga entidades bancarias en combo"""
        combo.clear()
        for a in self.arr:
            combo.addItem(a.country.qicon(), a.name, a.id)

        if zone!=None:
            combo.setCurrentIndex(combo.findText(zone.name))

class Meal:
    def __init__(self, mem):
        self.mem=mem
    def init__from_row(self,row):
        self.id=row['id']
        self.product=self.mem.data.products.find_by_id(row['products_id']) or None
        self.datetime=row['datetime']
        self.name=row['name']
        self.amount=row['amount']
        return self

    def name(self):
        if self.companies_id==None:
            return "{}".format(self._name)
        else:
            return "{} ({})".format(self._name, self.companies_name)

    def __repr__(self):
        return "{}. #{}".format(self.name(),self.id)

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
        return str(self.time())[0:5]

    def product_type(self):
        if self.personalproducts_id==None and self.companies_id==None:
            return "Basic"
        elif self.personalproducts_id!=None:
            return "Personal"
        elif self.companies_id!=None:
            return "Manufactured"
        else:
            return "Rare"

class MealManager(QObject, ObjectManager_With_IdDatetime):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdDatetime.__init__(self)
        self.mem=mem

    def init__from_db(self, sql):
        rows=self.mem.con.cursor_rows(sql)
        for row in rows:
            self.append(Meal(self.mem).init__from_row(row))
        return self
    def calories(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.meal_calories()
        return r
    def fat(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.meal_fat()
        return r
    def protein(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.meal_protein()
        return r
    def carbohydrate(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.meal_carbohydrate()
        return r
    def salt(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.meal_salt()
        return r
    def fiber(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.meal_fiber()
        return r
    def grams(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.meal_amount
        return r
    def max_name_len(self):
        r=0
        for meal in self.arr:
            if len(meal.name())>r:
                r=len(meal.name())
        return r
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
        
class User:
    def __init__(self, mem):
        self.mem=mem
        
    def init__from_db(self,id):
        row=self.mem.con.cursor_one_row("select * from users where id=%s",(id,))
        self.id=row['id']
        self.name=row['name']
        self.male=row['male']
        self.birthday=row['birthday']
        row=self.mem.con.cursor_one_row("select * from biometrics where users_id=%s order by datetime desc limit 1",(self.id,))
        self.height=row['height']
        self.weight=row['weight']
        #0 Loss weight   
        #1 Mantein widght 45H 35P 20G
        #2 Gain weight
        #self.dietwish=row['dietwish']
        # 0 TMB x 1,2: Poco o ningún ejercicio
        # 1 TMB x 1,375: Ejercicio ligero (1 a 3 días a la semana)
        # 2 TMB x 1,55: Ejercicio moderado (3 a 5 días a la semana)
        # 3 TMB x 1,72: Deportista (6 -7 días a la semana)
        # 4 TMB x 1,9: Atleta (Entrenamientos mañana y tarde)

        self.activity=row['activity']
        return self 

    ##basal metabolic rate
    def bmr(self):
        if self.activity==0:
            mult=Decimal(1.2)
        elif self.activity==1:
            mult=Decimal(1.375)
        elif self.activity==2:
            mult=Decimal(1.55)
        elif self.activity==3:
            mult=Decimal(1.72)
        elif self.activity==4:
            mult=Decimal(1.9)

        if self.male==True:
            return mult*(Decimal(10)*self.weight + Decimal(6.25)*self.height - Decimal(5)*self.age() + 5)
        else: #female
            return mult*(Decimal(10)*self.weight + Decimal(6.25)*self.height - Decimal(5)*self.age() - 161)

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
