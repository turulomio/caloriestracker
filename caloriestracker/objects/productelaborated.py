from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QApplication, QProgressDialog
from caloriestracker.libcaloriestrackerfunctions import a2s
from caloriestracker.libcaloriestrackertypes import eProductComponent
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable, ObjectManager_With_IdDatetime_Selectable
from caloriestracker.objects.product import ProductPersonal
from caloriestracker.ui.myqtablewidget import qcenter, qleft, qright, qnumber
from colorama import Style
from datetime import datetime
from decimal import Decimal
from logging import debug

class ProductElaborated:
    ##Biometrics(mem)
    ##Biometrics(mem,row)
    def __init__(self, mem=None, name=None, final_amount=None, last=None, foodtype=None, id=None):
        self.mem=mem
        self.name=name
        self.final_amount=final_amount
        self.last=last
        self.foodtype=foodtype
        self.id=id
        self.status=0
        
    def fullName(self):
        if self.mem.debuglevel=="DEBUG":
            str_with_id=". #E{}".format(self.id)
        else:
            str_with_id=""
        return "{}{}".format(self.name, str_with_id)

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
            foodtypes_id=None if self.foodtype==None else self.foodtype.id
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
            foodtypes_id, 
            [], 
            None)
            o.save() 
            self.mem.data.products.append(o)
            self.mem.data.products.order_by_name()
            o.needStatus(1, downgrade_to=0)
        else:#It's already in personalproducts
            selected.name=self.name
            selected.amount=self.final_amount
            selected.fat=self.products_in.fat()
            selected.protein=self.products_in.protein()
            selected.carbohydrate=self.products_in.carbohydrate()
            selected.calories=self.products_in.calories()
            selected.fiber=self.products_in.fiber()
            selected.foodtype=self.foodtype
            selected.save()
            selected.needStatus(1, downgrade_to=0)

    #DO NOT EDIT THIS ONE COPY FROM PRODUCT AND CHANGE TABLE
    def save(self):
        foodtypes_id=None if self.foodtype==None else self.foodtype.id
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("""insert into elaboratedproducts (
                    name, final_amount, last, foodtypes_id
                    )values (%s, %s, %s, %s) returning id""",  
                    (self.name, self.final_amount, self.last, foodtypes_id))
        else:
            self.mem.con.execute("""update elaboratedproducts set name=%s, final_amount=%s, last=%s, foodtypes_id=%s where id=%s""", 
            (self.name, self.final_amount, self.last, foodtypes_id,  self.id))
        self.needStatus(1, downgrade_to=0)
        self.register_in_personal_products()
        
    ## Returns the product asociated to this elaboratedproduct
    def product(self):
        return self.mem.data.products.find_by_elaboratedproducts_id(self.id)

    def is_deletable(self):
        self.needStatus(1)
        if self.products_in.length()>0:
            return False
        
        selected=self.product()
        if selected!=None and selected.is_deletable()==False:
            return False
        return True

    def delete(self):
        if self.is_deletable()==True:
            self.mem.con.execute("delete from elaboratedproducts where id=%s", (self.id, ))
            self.mem.con.execute("delete from personalproducts where elaboratedproducts_id=%s", (self.id, ))
        else:
            debug("I did not delete the elaborated product because is not deletable")
            
    def qicon(self):
        return QIcon(":/caloriestracker/cooking.png")
        

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
    def qtablewidget(self, wdg):        
        data=[]
        for i, o in enumerate(self.arr):
            data.append([
                o.fullName(),
                o.last, 
            ])
        wdg.setData(
            [self.tr("Name"), self.tr("Last update")], 
            None, 
            data, 
            zonename=self.mem.localzone
        )   
        for i, o in enumerate(self.arr):
            wdg.table.item(i, 0).setIcon(o.qicon())


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


    def qtablewidget(self, wdg):        
        wdg.table.setColumnCount(7)
        wdg.table.setHorizontalHeaderItem(0, qcenter(self.tr("Name")))
        wdg.table.setHorizontalHeaderItem(1, qcenter(self.tr("Grams")))
        wdg.table.setHorizontalHeaderItem(2, qcenter(self.tr("Calories")))
        wdg.table.setHorizontalHeaderItem(3, qcenter(self.tr("Carbohydrates")))
        wdg.table.setHorizontalHeaderItem(4, qcenter(self.tr("Protein")))
        wdg.table.setHorizontalHeaderItem(5, qcenter(self.tr("Fat")))
        wdg.table.setHorizontalHeaderItem(6, qcenter(self.tr("Fiber")))
   
        wdg.applySettings()
        wdg.table.clearContents()
        wdg.table.setRowCount(self.length()+2)
        for i, o in enumerate(self.arr):
            wdg.table.setItem(i, 0, qleft(o.product.fullName()))
            wdg.table.item(i, 0).setIcon(o.product.qicon())
            wdg.table.setItem(i, 1, qright(o.amount))
            wdg.table.setItem(i, 2, qright(o.calories()))
            wdg.table.setItem(i, 3, qright(o.carbohydrate()))
            wdg.table.setItem(i, 4, qright(o.protein()))
            wdg.table.setItem(i, 5, qright(o.fat()))
            wdg.table.setItem(i, 6, qright(o.fiber()))
        #Totals
        wdg.table.setItem(self.length(), 0, qleft(self.tr("Total")))
        wdg.table.setItem(self.length(), 1, qnumber(self.grams()))
        wdg.table.setItem(self.length(), 2, qnumber(self.calories()))
        wdg.table.setItem(self.length(), 3, qnumber(self.carbohydrate()))
        wdg.table.setItem(self.length(), 4, qnumber(self.protein()))
        wdg.table.setItem(self.length(), 5, qnumber(self.fat()))
        wdg.table.setItem(self.length(), 6, qnumber(self.fiber()))
        #Amounts in 100 grams of elaboratedproduct
        product=self.mem.data.products.find_by_elaboratedproducts_id(self.elaboratedproduct.id)
        wdg.table.setItem(self.length()+1, 0, qleft(self.tr("Values in 100 g")))
        wdg.table.setItem(self.length()+1, 1, qnumber(100))
        wdg.table.setItem(self.length()+1, 2, qnumber(product.component_in_100g(eProductComponent.Calories)))
        wdg.table.setItem(self.length()+1, 3, qnumber(product.component_in_100g(eProductComponent.Carbohydrate)))
        wdg.table.setItem(self.length()+1, 4, qnumber(product.component_in_100g(eProductComponent.Protein)))
        wdg.table.setItem(self.length()+1, 5, qnumber(product.component_in_100g(eProductComponent.Fat)))
        wdg.table.setItem(self.length()+1, 6, qnumber(product.component_in_100g(eProductComponent.Fiber)))

def ProductElaborated_from_row(mem, row):
    foodtype=None if row['foodtypes_id']==None else mem.data.foodtypes.find_by_id(row['foodtypes_id'])
    return ProductElaborated(mem, row['name'], row['final_amount'], row['last'], foodtype, row['id'])
