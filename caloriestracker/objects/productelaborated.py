from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from caloriestracker.libcaloriestrackerfunctions import a2s
from caloriestracker.libcaloriestrackertypes import eProductComponent
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable, ObjectManager_With_IdDatetime_Selectable
from caloriestracker.objects.additives import AdditiveManager
from caloriestracker.objects.product import ProductPersonal
from colorama import Style
from datetime import datetime
from decimal import Decimal
from logging import debug, error

class ProductElaborated:
    ##Biometrics(mem)
    ##Biometrics(mem,row)
    def __init__(self, mem=None, name=None, final_amount=None, last=None, foodtype=None, obsolete=None,  id=None):
        self.mem=mem
        self.name=name
        self.final_amount=final_amount
        self.last=last
        self.foodtype=foodtype
        self.obsolete=obsolete
        self.id=id
        self.status=0
        ## To avoid crashes when there is a produc elaborated without a personalproducts, I alwaysregenerate it
        if self.id is not None and self.product() is None:
            self.load_products_in()
            self.register_in_personal_products()
            error("Fixing an elaborated product with id, without a personal product.")
            self.mem.con.commit()
        
    def __repr__(self):
        return self.fullName()
        
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
            self.products_in=ProductInElaboratedProductManager_from_sql(self.mem, self, self.mem.con.mogrify("select * from products_in_elaboratedproducts where elaboratedproducts_id=%s",(self.id,)))

    def show_table(self):
        self.products_in.show_table()

    def register_in_personal_products(self):
        selected=self.product()
        if selected is None:
            selected=ProductPersonal(self.mem)
            self.mem.data.products.append(selected)
        selected.name=self.name
        selected.last=datetime.now()
        selected.amount=self.final_amount
        selected.fat=self.products_in.fat()
        selected.protein=self.products_in.protein()
        selected.carbohydrate=self.products_in.carbohydrate()
        selected.calories=self.products_in.calories()
        selected.fiber=self.products_in.fiber()
        selected.salt=self.products_in.salt()
        selected.cholesterol=self.products_in.cholesterol()
        selected.sodium=self.products_in.sodium()
        selected.potassium=self.products_in.potassium()
        selected.sugars=self.products_in.sugars()
        selected.foodtype=self.foodtype
        selected.glutenfree=self.products_in.is_glutenfree()
        selected.ferrum=self.products_in.ferrum()
        selected.magnesium=self.products_in.magnesium()
        selected.phosphor=self.products_in.phosphor()
        selected.obsolete=self.obsolete
        selected.additives=self.products_in.additives()
        selected.elaboratedproducts_id=self.id
        selected.save()
        selected.needStatus(1, downgrade_to=0)
        self.mem.data.products.order_by_name()

    def save(self):
        foodtypes_id=None if self.foodtype==None else self.foodtype.id
        if self.id is None:
            self.id=self.mem.con.cursor_one_field("""insert into elaboratedproducts (
                    name, final_amount, last, foodtypes_id, obsolete
                    )values (%s, %s, %s, %s,%s) returning id""",  
                    (self.name, self.final_amount, self.last,  foodtypes_id, self.obsolete))
        else:
            self.mem.con.execute("""update elaboratedproducts set name=%s, final_amount=%s, last=%s, foodtypes_id=%s, obsolete=%s where id=%s""", 
            (self.name, self.final_amount, self.last, foodtypes_id, self.obsolete, self.id))
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
        

class ProductElaboratedManager(ObjectManager_With_IdName_Selectable, QObject):
    def __init__(self, mem):
        ObjectManager_With_IdName_Selectable.__init__(self)
        QObject.__init__(self)
        self.setConstructorParameters(mem)
        self.mem=mem

    ## It's a staticmethod due to it will be used in ProductAllManager
    def qtablewidget(self, wdg):        
        data=[]
        for i, o in enumerate(self.arr):
            foodtype=None if o.foodtype==None else o.foodtype.name
            data.append([
                o.fullName(),
                foodtype, 
                o.last, 
                o, 
            ])
        wdg.setDataWithObjects(
            [self.tr("Name"), self.tr("Food type"), self.tr("Last update")], 
            None, 
            data, 
            zonename=self.mem.localzone, 
            additional=self.qtablewidget_additional, 
        )

    def qtablewidget_additional(self, wdg):
        for i, o in enumerate(wdg.objects()):
            wdg.table.item(i, 0).setIcon(o.qicon())

class ProductInElaboratedProduct:
    def __init__(self, mem, product=None, system_product=None, amount=None, elaboratedproduct=None, id=None):
        self.mem=mem
        self.product=product
        self.system_product=system_product
        self.amount=amount
        self.elaboratedproduct=elaboratedproduct
        self.id=id

    def fullName(self):
        return self.product.fullName() 

    def calories(self):
        try:
            return self.amount * self.product.calories/self.product.amount
        except:
            return None
        
    def fat(self):
        try:
            return self.amount * self.product.fat/self.product.amount
        except:
            return None

    def protein(self):
        try:
            return self.amount * self.product.protein/self.product.amount
        except:
            return None

    def carbohydrate(self):
        try:
            return self.amount * self.product.carbohydrate/self.product.amount
        except:
            return None

    def salt(self):
        try:
            return self.amount * self.product.salt/self.product.amount
        except:
            return None

    def fiber(self):
        try:
            return self.amount * self.product.fiber/self.product.amount
        except:
            return None

    def sugars(self):
        try:
            return self.amount * self.product.sugars/self.product.amount
        except:
            return None

    def sodium(self):
        try:
            return self.amount * self.product.sodium/self.product.amount
        except:
            return None

    def potassium(self):
        try:
            return self.amount * self.product.potassium/self.product.amount
        except:
            return None

    def cholesterol(self):
        try:
            return self.amount * self.product.cholesterol/self.product.amount
        except:
            return None

    def saturated_fat(self):
        try:
            return self.amount * self.product.saturated_fat/self.product.amount
        except:
            return None

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
        
class ProductInElaboratedProductManager(ObjectManager_With_IdDatetime_Selectable, QObject):
    ##ProductInElaboratedProductManager(mem)
    ##ProductInElaboratedProductManager(mem,elaboratedproduct,sql)
    def __init__(self, mem, elaboratedproduct ):
        ObjectManager_With_IdName_Selectable.__init__(self)
        QObject.__init__(self)
        self.mem=mem
        self.elaboratedproduct=elaboratedproduct
        
    ## If one product in arr is not glutenfree elaboratedproduct will be not gluten free
    def is_glutenfree(self):
        r=True
        for o in self.arr:
            if o.product.glutenfree==False:
                r=False
                break
        return r
        
        
    def additives(self):
        r=AdditiveManager(self.mem)
        # Create a set
        se=set()
        for o in self.arr:
            for a in o.additives.arr:
                se.add(a)
        
        for a in se:
            r.append(a)
        return r

    def calories(self):
        r=Decimal(0)
        for product_in in self.arr:
            try:
                r=r+product_in.calories()
            except:
                return None
        return r
        
    def fat(self):
        r=Decimal(0)
        for product_in in self.arr:
            try:
                r=r+product_in.fat()
            except:
                return None
        return r
        
    def protein(self):
        r=Decimal(0)
        for product_in in self.arr:
            try:
                r=r+product_in.protein()
            except:
                return None
        return r
        
    def carbohydrate(self):
        r=Decimal(0)
        for product_in in self.arr:
            try:
                r=r+product_in.carbohydrate()
            except:
                return None
        return r
        
    def salt(self):
        r=Decimal(0)
        for product_in in self.arr:
            try:
                r=r+product_in.salt()
            except:
                return None
        return r
        
    def fiber(self):
        r=Decimal(0)
        for product_in in self.arr:
            try:
                r=r+product_in.fiber()
            except:
                return None
        return r
    def ferrum(self):
        r=Decimal(0)
        for product_in in self.arr:
            try:
                r=r+product_in.ferrum()
            except:
                return None
        return r
    def magnesium(self):
        r=Decimal(0)
        for product_in in self.arr:
            try:
                r=r+product_in.magnesium()
            except:
                return None
        return r
    def phosphor(self):
        r=Decimal(0)
        for product_in in self.arr:
            try:
                r=r+product_in.phosphor()
            except:
                return None
        return r
        
    def cholesterol(self):
        r=Decimal(0)
        for product_in in self.arr:
            try:
                r=r+product_in.cholesterol()
            except:
                return None
        return r
        
    def sugars(self):
        r=Decimal(0)
        for product_in in self.arr:
            try:
                r=r+product_in.sugars()
            except:
                return None
        return r
        
    def saturated_fat(self):
        r=Decimal(0)
        for product_in in self.arr:
            try:
                r=r+product_in.saturated_fat()
            except:
                return None
        return r
        
    def sodium(self):
        r=Decimal(0)
        for product_in in self.arr:
            try:
                r=r+product_in.sodium()
            except:
                return None
        return r
        
    def potassium(self):
        r=Decimal(0)
        for product_in in self.arr:
            try:
                r=r+product_in.potassium()
            except:
                return None
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
        hh=[self.tr("Name"), self.tr("Grams"), self.tr("Calories"), self.tr("Carbohydrates"), self.tr("Protein"), self.tr("Fat"), 
            self.tr("Fiber"), self.tr("Gluten free")]
        data=[]
        for i, o in enumerate(self.arr):
            data.append([
                o.product.fullName(), 
                o.amount, 
                o.calories(), 
                o.carbohydrate(), 
                o.protein(), 
                o.fat(),
                o.fiber(), 
                o.product.glutenfree, 
                o
            ])
        wdg.setDataWithObjects(hh, None, data, additional=self.qtablewidget_additional)
            
    def qtablewidget_additional(self, wdg):
        wdg.table.setRowCount(wdg.length()+2)
        for i, o in enumerate(wdg.objects()):
            wdg.table.item(i, 0).setIcon(o.product.qicon())
        wdg.addRow(wdg.length(), [self.tr("Total"), self.grams(), self.calories(), self.carbohydrate(), self.protein(), self.fat(), self.fiber(), self.is_glutenfree()])
        #Amounts in 100 grams of elaboratedproduct
        print(self.elaboratedproduct.id, "ELABORATEDID")
        product=self.mem.data.products.find_by_elaboratedproducts_id(self.elaboratedproduct.id)
        wdg.addRow(wdg.length()+1, [self.tr("Values in 100 g"), 100, product.component_in_100g(eProductComponent.Calories), 
            product.component_in_100g(eProductComponent.Carbohydrate), product.component_in_100g(eProductComponent.Protein), 
            product.component_in_100g(eProductComponent.Fat), product.component_in_100g(eProductComponent.Fiber), "#crossedout"])
            

def ProductElaborated_from_row(mem, row):
    foodtype=None if row['foodtypes_id']==None else mem.data.foodtypes.find_by_id(row['foodtypes_id'])
    return ProductElaborated(mem, row['name'], row['final_amount'], row['last'], foodtype, row['obsolete'], row['id'])

def ProductInElaboratedProduct_from_row(mem, elaboratedproduct, row):
    product=mem.data.products.find_by_id_system(row['products_id'],row['system_product'])    
    return ProductInElaboratedProduct(mem, product, row['system_product'], row['amount'], elaboratedproduct, row['id'])


def ProductInElaboratedProductManager_from_sql(mem, elaboratedproduct, sql):
    r=ProductInElaboratedProductManager(mem, elaboratedproduct)
    rows=mem.con.cursor_rows(sql)
    for row in rows:
        r.append(ProductInElaboratedProduct_from_row(mem, elaboratedproduct, row))
    return r

def ProductElaboratedManager_from_sql(mem, sql):
    r=ProductElaboratedManager(mem)
    rows=mem.con.cursor_rows(sql)
    for row in rows:
        r.append(ProductElaborated_from_row(mem, row))
    return r
