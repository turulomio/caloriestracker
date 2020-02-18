from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from caloriestracker.casts import b2s
from caloriestracker.objects.company import CompanySystem
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable, ManagerSelectionMode
from caloriestracker.ui.myqtablewidget import qcenter, qleft, qnumber

## There is no need of system_formats or personal_formats because it's relacionated with the product as its properties
class Format(QObject):
    ##Format(mem)
    ##Format(mem,rows) #Uses products_id and users_id in row
    ##Format(mem, name, product, system_product,amount, last,  id):
    def __init__(self, *args):        
        def init__create( name, product, system_product,amount, last,  id):
            self.name=self.mem.trHS(name)
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

    def sql_insert(self, table="formats"):
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

class FormatAllManager(QObject, ObjectManager_With_IdName_Selectable):
    ## ProductAllManager(mem,product)#Loads all database
    def __init__(self, *args):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=args[0]
        self.product=args[1]

    def load_all(self):
        system=FormatSystemManagerHomogeneus(self.mem, self.product)
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
        FormatSystemManagerHeterogeneus.qtablewidget(self, table)


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

class FormatSystemManagerHeterogeneus(ObjectManager_With_IdName_Selectable, QObject):
    ##FormatSystemManagerHomogeneus(mem,product)
    def __init__(self, mem ):
        ObjectManager_With_IdName_Selectable.__init__(self)
        QObject.__init__(self)
        self.mem=mem
        self.setSelectionMode(ManagerSelectionMode.Object)

    def load_from_db(self, sql):
        rows=self.mem.con.cursor_rows(sql)
        for row in rows:
            self.append(Format(self.mem, row))
        return self

    @staticmethod
    def qtablewidget(self, table):        
        table.setColumnCount(2)
        table.setHorizontalHeaderItem(0, qcenter(self.tr("Name")))
        table.setHorizontalHeaderItem(1, qcenter(self.tr("Grams")))
        table.applySettings()
        table.clearContents()
        table.setRowCount(self.length())
        for i, o in enumerate(self.arr):
            table.setItem(i, 0, qleft(o.fullName(grams=False)))
            table.item(i, 0).setIcon(o.qicon())
            table.setItem(i, 1, qnumber(o.amount))

    def sql_insert(self, table="formats"):
        return b2s(self.mem.con.mogrify("insert into "+table +"(name, amount, products_id, system_product, last, id) values (%s, %s, %s, %s, %s, %s);", 
        (self.name, self.amount, self.product.id, self.system_product, self.last, self.id)))
        
    def sql_update(self, table="formats"):
        return b2s(self.mem.con.mogrify("update "+table +" set name=%s, amount=%s, products_id=%s, system_product=%s,last=%s where id=%s;", 
        (self.name, self.amount, self.product.id, self.system_product, self.last, self.id)))
        
class FormatSystemManagerHomogeneus(FormatSystemManagerHeterogeneus):
    def __init__(self, mem, product ):
        FormatSystemManagerHeterogeneus.__init__(self, mem)
        self.product=product
        

class FormatPersonalManager(FormatSystemManagerHomogeneus):
    def __init__(self, *args):
        FormatSystemManagerHomogeneus.__init__(self, *args)
    def load_from_db(self, sql):
        rows=self.mem.con.cursor_rows(sql)
        for row in rows:
            self.append(FormatPersonal(self.mem, row))
        return self
