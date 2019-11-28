## @brief Module with objects managers as list or as dictionary.
## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README
##
## This file is from Xulpymoney project. Do not edit, It will be overriden.
##
## You have to use list objects if you are going to make selections and secuential access.
##
## You have to use dictionary objects i f you are going to make unordered access to the dictionary. It consumes more memory. To access a selected item in a table you have to hide a column with the id and getit when selecting a row
##

from datetime import datetime, timedelta, date
from logging import debug
from .datetime_functions import dtaware_day_end_from_date, dtaware_day_start_from_date, dtnaive_day_end_from_date, dtnaive_day_start_from_date


## Defines who self.selected is managed
## If can take the following values
## - Object self.selected is a object
## - List self.selected is a list of objects
## - Manager. Selef selected is an object
class ManagerSelectionMode:
    Object=0
    List=1
    Manager=2

class MyMem:
    def __init__(self):
        self.mem=None
        
    def setMem(self, mem):
        self.mem=mem

class ObjectManager(object):
    def __init__(self):
        self.arr=[]       
        self.selected=None#Used to select a item in the set. Usefull in tables. Its a item

    def append(self,  obj):
        self.arr.append(obj)

    def remove(self, obj):
        self.arr.remove(obj)

    def length(self):
        return len(self.arr)
        
    #To use the same name as DictObjectManager
    def values(self):
        return self.arr

    def clean(self):
        """Deletes all items"""
        self.arr=[]
                
    def clone(self,  *initparams):
        """Returns other Set object, with items referenced, ojo con las formas de las instancias
        initparams son los parametros de iniciación de la clase"""
        result=self.__class__(*initparams)#Para que coja la clase del objeto que lo invoca
        for a in self.arr:
            result.append(a)
        return result
   
    def first(self):
        if self.length()>0:
            return self.arr[0]
        else:
            print ("There is no first item")
            return None
        
    def last(self):
        return self.arr[self.length()-1]

        
        
    def print(self):
        print ("Objects in {}".format(self.__class__))
        for q in self.arr:
            print(" * {}".format(q))


## Manager Selection class
## By default selectionmode is
class ManagerSelection(object):
    def __init__(self):
        self.__selected=None
        self.__selectionmode=ManagerSelectionMode.Object
        
    @property
    def selected(self):
        return self.__selected
        
    @selected.setter
    def selected(self, value):
        self.__selected=value
        
    def selectionMode(self):
        return self.__selectionmode
        
    def setSelectionMode(self, value):
        self.__selectionmode=value
        if value==ManagerSelectionMode.Object:
            self.selected=None
        elif value==ManagerSelectionMode.List:
            self.selected=[]
        elif value==ManagerSelectionMode.Manager:#Returns parent __class__
            self.selected=self.__class__.__bases__[0]()
        
    def cleanSelection(self):
        if self.selectionMode()==ManagerSelectionMode.Object:
            self.selected=None
        elif self.selectionMode()==ManagerSelectionMode.List:
            self.selected=[]
        elif self.selectionMode()==ManagerSelectionMode.Manager:#Returns parent __class__
            self.selected.clean()

    ## Useful to setselection without interactivvite ui
    ## @param list Can be, list, manager or object
    def setSelected(self, list):
        self.cleanSelection()
        if self.selectionMode()==ManagerSelectionMode.List:
            for o in list:
                self.selected.append(o)
        elif self.selectionMode()==ManagerSelectionMode.Manager:
            for o in list.arr:
                self.selected.append(o)
        else:#Object
            self.selected=list

## Objects in DictListObjectManager has and id. The Id can be a integer or a string or ...
class ObjectManager_With_Id(ObjectManager):
    def __init__(self):
        ObjectManager.__init__(self)
        
    def arr_position(self, id):
        """Returns arr position of the id, useful to select items with unittests"""
        for i, a in enumerate(self.arr):
            if a.id==id:
                return i
        return None
        
    ##Returns an array with all object ids
    def array_of_ids(self):
        r=[]
        for o in self.arr:
            r.append(o.id)
        return r
    

    ## Search by id iterating array
    def find_by_id(self, id):
        for a in self.arr:
            if a.id==id:
                return a
        return None
                
    def order_by_id(self):
        """Orders the Set using self.arr"""
        try:
            self.arr=sorted(self.arr, key=lambda c: c.id,  reverse=False)     
            return True
        except:
            return False
        
    def union(self,  set,  *initparams):
        """Returns a new set, with the union comparing id
        initparams son los parametros de iniciación de la clse"""        
        resultado=self.__class__(*initparams)#Para que coja la clase del objeto que lo invoca SetProduct(self.mem), luego será self.mem
        for p in self.arr:
            resultado.append(p)
        for p in set.arr:
            if resultado.find_by_id(p.id, False)==None:
                resultado.append(p)
        return resultado

    ## Searches the objects id in the array and mak selected. ReturnsTrue if the o.id exists in the arr and False if don't
    ## It's used when I want to mark an item in a table and I only have an id
    def setSelected(self, sel):
        for i, o in enumerate(self.arr):
            if o.id==sel.id:
                self.selected=o
                return True
        self.selected=None
        return False        
        
    ## Searches the objects id in the array and mak selected. ReturnsTrue if the o.id exists in the arr and False if don't
    ## It's used when I want to mark an item in a table and I only have the list of ids
    def setSelectedList(self, lista):
        assert type(lista) is list, "id is not a list {}".format(lista)
        self.arr=[]
        for i, o in enumerate(self.arr):
            for l in lista:
                if o.id==l.id:
                    self.append(o)
        self.selected=None
        return False

## Objects in DictListObjectManager has and id and a date attribute
class ObjectManager_With_IdDate(ObjectManager_With_Id):
    def __init__(self):
        ObjectManager_With_Id.__init__(self)

    def order_by_date(self):       
        self.arr=sorted(self.arr, key=lambda e: e.date,  reverse=False) 
        
## Objects in DictListObjectManager has and id and a datetime
class ObjectManager_With_IdDatetime(ObjectManager_With_Id):
    def __init__(self):
        ObjectManager_With_Id.__init__(self)

    def order_by_datetime(self):       
        self.arr=sorted(self.arr, key=lambda e: e.datetime,  reverse=False) 
                
    ## Function that returns the same object manager, with a pointer to the of the objects that contains from the datetime given in the parameter.
    ## For example the constuctor of InvemestOperationHomogeneous is InvesmentOperationHomogeneous(mem,investment). so to use this function you need ObjectManager_from_datetime(dt,mem,investment)
    ## @param datetime. This function copies all object with datetime until this parameter
    ## @param initparams. Parameters of the constructor of the ManagerObject class
    def ObjectManager_from_datetime(self, dt, *initparams):
        result=self.__class__(*initparams)#Para que coja la clase del objeto que lo invoca
        if dt==None:
            dt=self.mem.localzone.now()
        for a in self.arr:
            if a.datetime>=dt:
                result.append(a)
        return result         
        
    ## Function that returns the same object manager, with a pointer to the of the objects that contains from the datetime given in the parameter.
    ## For example the constuctor of InvemestOperationHomogeneous is InvesmentOperationHomogeneous(mem,investment). so to use this function you need ObjectManager_from_datetime(dt,mem,investment)
    ## @param datetime. This function copies all object with datetime until this parameter
    ## @param initparams. Parameters of the constructor of the ManagerObject class
    def ObjectManager_until_datetime(self, dt, *initparams):        
        result=self.__class__(*initparams)#Para que coja la clase del objeto que lo invoca
        if dt==None:
            dt=self.mem.localzone.now()
        for a in self.arr:
            if a.datetime<=dt:
                result.append(a)
        return result
        
    def ObjectManager_copy_from_datetime(self, dt, *initparams):
        """Función que devuelve otro SetInvestmentOperations con las oper que tienen datetime mayor o igual a la pasada como parametro tambien copiadas."""
        result=self.__class__(*initparams)#Para que coja la clase del objeto que lo invoca
        if dt==None:
            dt=self.mem.localzone.now()
        for a in self.arr:
            if a.datetime>=dt:
                result.append(a.copy())
        return result
        
    ## Function that returns the same object manager, but with a copy of the objects that contains until the datetime given in the parameter.
    ## For exemple the constuctor of InvemestOperationHomogeneous is InvemestOperationHomogeneous(mem,investment). so to use this function you need ObjectManager_copy_until_datetime(dt,mem,investment)
    ## @param datetime. This function copies all object with datetime until this parameter
    ## @param initparams. Parameters of the constructor of the ManagerObject class
    def ObjectManager_copy_until_datetime(self, dt, *initparams):
        result=self.__class__(*initparams)#Para que coja la clase del objeto que lo invoca
        if dt==None:
            dt=self.mem.localzone.now()
        for a in self.arr:
            if a.datetime<=dt:
                result.append(a.copy())
        return result

## Objects in DictListObjectManager has and id and a name
class ObjectManager_With_IdName(ObjectManager_With_Id):
    def __init__(self):
        ObjectManager_With_Id.__init__(self)
        
    ##Returns an array with all object name
    ## @param sort Boolean to sort or not the array
    ## @oaram nones Boolean. If True adds None and empty strings values to the list. If False it doesn't
    def array_of_names(self, sort=True, nones=False):
        r=[]
        for o in self.arr:
            if nones==False:
                if o.name==None or o.name=="":
                    continue
            r.append(o.name)
        if sort==True:
            r.sort()
        return r

    ## Find an object searching in its name to match the parameter
    def find_by_name(self, name,  log=False):
        """self.find_by_id() search by id (number).
        This function replaces  it and searches by name (Europe/Madrid)"""
        for a in self.arr:
            if a.name==name:
                return a
        debug("{} didn't find the name: {}".format(self.__class__, name))
        return None


    ## Returns another object manager of the same class with the elements that contains a string in the name
    ## @param s string to search
    ## @casesensitive Boolean if it's a case sensitive search    
    def ObjectManager_with_name_contains_string(self, s, casesensitive, *initparams):
        result=self.__class__(*initparams)#Para que coja la clase del objeto que lo invoca
        if casesensitive==True:
            for a in self.arr:
                if s in a.name:
                    result.append(a)
            return result
        else:
            for a in self.arr:
                if s.upper() in a.name.upper():
                    result.append(a)
            return result
        
    def order_by_name(self):
        """Orders the Set using self.arr"""
        try:
            self.arr=sorted(self.arr, key=lambda c: c.name,  reverse=False)       
            return True
        except:
            return False        

    def order_by_upper_name(self):
        """Orders the Set using self.arr"""
        try:
            self.arr=sorted(self.arr, key=lambda c: c.name.upper(),  reverse=False)       
            return True
        except:
            return False

    ## @param selected it's an object
    ## @param needtoselect Adds a foo item with value==None with the text select one
    ## @param icons Boolean. If it's true uses o.qicon() method to add an icon to the item
    def qcombobox(self, combo,  selected=None, needtoselect=False, icons=False):
        self.order_by_name()
        combo.clear()

        if needtoselect==True:
            if self.length()>0:
                combo.addItem(combo.tr("Select an option"), None)
            else:
                combo.addItem(combo.tr("No options to select"), None)

        for a in self.arr:
            if icons==True:
                combo.addItem(a.qicon(), a.name, a.id)
            else:
                combo.addItem(a.name, a.id)

        if selected!=None:
            combo.setCurrentIndex(combo.findData(selected.id))

    ## Creates a libreoffice sheet from the ObjectManager
    ##
    ## This function needs the officegenerator package
    ## @param sheetname String with the name of the libreoffice sheet
    ## @param Officegenerator ODS_Write object
    ## @param titles List of strings with the titles of the columns
    ## @param order_by_name Boolean. True: orders by name. False: orders by id
    ## @returns Officegenerator OdfSheet
    def ods_sheet(self, ods, sheetname, titles=["Id", "Name"],  order_by_name=True):
        from officegenerator import Coord
        if order_by_name==True:
            self.order_by_name()
        else:
            self.order_by_id()
        s=ods.createSheet(sheetname)
        s.setColumnsWidth([80, 240])
        s.add("A1", [titles], "OrangeCenter")
        for number, o in enumerate(self.arr):
            s.add(Coord("A2").addRow(number), o.id, "WhiteRight")        
            s.add(Coord("B2").addRow(number), o.name, "WhiteLeft")
        s.setSplitPosition("A1")
        s.setCursorPosition(Coord("B2").addRow(self.length()))
        return s

## Objects has a field called id, whose string is the key of the item of dict
## It Can be a DictObjectManager without id
## It doesn't need to cfreate DictListObjectManager_With_IdName, because all funcions are used with ObjectManager_With_IdName
class DictObjectManager_With_Id(object):
    def __init__(self):
        self.dic={}

    def append(self,  obj):
        self.dic[str(obj.id)]=obj

    def values(self):
        return self.dic.values()

    def keys(self):
        return self.dic.keys()

    def items(self):
        return self.dic.items()

    def remove(self, obj):
        del self.dic[str(obj.id)]

    def clean(self):
        self.dic={}

    def length(self):
        return len(self.dic)

    ## Sometimes there is a dictionary with a unique valor. This function returns the value, not the key.
    ## I dón't use first because dict has no orders.
    def only(self):
        return self.dic[next(iter(self.dic))]

    ## Find by object passing o that is an object        
    def find(self, o,  log=False):
        """o is and object with id parameter"""
        print("find is deprecated")
        try:
            return self.dic[str(o.id)]    
        except:
            if log:
                print ("DictObjectManager_With_IdName ({}) fails finding {}".format(self.__class__.__name__, o.id))
            return None        

    def find_by_id(self, id,  log=False):
        """Finds by id"""
        try:
            return self.dic[str(id)]    
        except:
            if log:
                print ("DictObjectManager_With_IdName ({}) fails finding {}".format(self.__class__.__name__, id))
            return None
            
    def values_order_by_id(self):
        return sorted(self.dic.values(), key=lambda o: o.id)


class DictObjectManager_With_IdName(DictObjectManager_With_Id):
    """Base clase to create Sets, it needs id and name attributes, as index. It has a list arr and a dics dict to access objects of the set"""
    def __init__(self):
        DictObjectManager_With_Id.__init__(self)

    ## Uses dict because is faster
    def values_order_by_name(self):
        return sorted(self.dic.values(), key=lambda o: o.name)
        
class DictObjectManager_With_IdDate(DictObjectManager_With_Id):
    """Base clase to create Sets, it needs id and name attributes, as index. It has a list arr and a dics dict to access objects of the set"""
    def __init__(self):
        DictObjectManager_With_Id.__init__(self)

    ## Uses dict because is faster
    def values_order_by_date(self):
        return sorted(self.dic.values(), key=lambda o: o.date)

class DictObjectManager_With_IdDatetime(DictObjectManager_With_Id):
    """Base clase to create Sets, it needs id and name attributes, as index. It has a list arr and a dics dict to access objects of the set"""

    def __init__(self):
        DictObjectManager_With_Id.__init__(self)

    ## Uses dict because is faster
    def values_order_by_datetime(self):
        return sorted(self.dic.values(), key=lambda o: o.datetime)

## Usefull when creating a class with two attributes self.id and self.name only
class Object_With_IdName:
    ## Constructor with the following attributes combination
    ## 1. Object_With_IdName(). Create an Object_With_IdName with all attributes to None
    ## 2. Object_With_IdName( id,  name). Create an Object_With_IdName settings all attributes.
    ## @param name String with the name of the Object_With_IdName
    ## @param id Integer that sets the id of the Object_With_IdName
    def __init__(self, *args):
        def init__create( id,  name):
            self.id=id
            self.name=name
        if len(args)==0:
            init__create(None, None)
        if len(args)==2:
            init__create(*args)


class DictObjectManager_With_Id_Selectable(DictObjectManager_With_Id, ManagerSelection):
    def __init__(self):
        DictObjectManager_With_Id.__init__(self)
        ManagerSelection.__init__(self)

class DictObjectManager_With_IdDate_Selectable(DictObjectManager_With_IdDate, ManagerSelection):
    def __init__(self):
        DictObjectManager_With_IdDate.__init__(self)
        ManagerSelection.__init__(self)

class DictObjectManager_With_IdDatetime_Selectable(DictObjectManager_With_IdDatetime, ManagerSelection):
    def __init__(self):
        DictObjectManager_With_IdDatetime.__init__(self)
        ManagerSelection.__init__(self)

class DictObjectManager_With_IdName_Selectable(DictObjectManager_With_IdName, ManagerSelection):
    def __init__(self):
        DictObjectManager_With_IdName.__init__(self)
        ManagerSelection.__init__(self)

class ObjectManager_Selectable(ObjectManager, ManagerSelection):
    def __init__(self):
        ObjectManager.__init__(self)
        ManagerSelection.__init__(self)

class ObjectManager_With_Id_Selectable(ObjectManager_With_Id, ManagerSelection):
    def __init__(self):
        ObjectManager_With_Id.__init__(self)
        ManagerSelection.__init__(self)

class ObjectManager_With_IdDate_Selectable(ObjectManager_With_IdDate, ManagerSelection):
    def __init__(self):
        ObjectManager_With_IdDate.__init__(self)
        ManagerSelection.__init__(self)

class ObjectManager_With_IdDatetime_Selectable(ObjectManager_With_IdDatetime, ManagerSelection):
    def __init__(self):
        ObjectManager_With_IdDatetime.__init__(self)
        ManagerSelection.__init__(self)

class ObjectManager_With_IdName_Selectable(ObjectManager_With_IdName, ManagerSelection):
    def __init__(self):
        ObjectManager_With_IdName.__init__(self)
        ManagerSelection.__init__(self)




## THIS IS A NEW SERIE OF MANAGERS DATETIME VALUE
class DatetimeValue:
    def __init__(self):
        self.datetime=None
        self.value=None

    def __repr__(self):
        return "DatetimeValue {} = {}".format(self.date,self.value)

class DatetimeValueManager(ObjectManager):
    def __init__(self):
        ObjectManager.__init__(self)
    def appendDV(self, datetime, value):
        o=DatetimeValue()
        o.datetime=datetime
        o.value=value
        self.append(o)    ## Returns a date value manager with the simple movil average 3 of weight
    
    ## Returns a DVManager with the simple movil average of the array
    def sma(self, period):
        r=DatetimeValueManager()
        for i in range(period, self.length()):
            sma=DatetimeValue()
            sma.value=0
            sma.datetime=self.arr[i].datetime
            for p in range(period):
                sma.value=sma.value+self.arr[i-p].value
            sma.value=sma.value/period
            r.append(sma)
        return r
        
## THIS IS A NEW SERIE OF MANAGERS DATE VALUE
class DateValue:
    def __init__(self):
        self.date=None
        self.value=None

    def __repr__(self):
        return "DateValue {} = {}".format(self.date,self.value)

class DateValueManager(ObjectManager):
    def __init__(self):
        ObjectManager.__init__(self)

    def appendDV(self, date, value):
        o=DateValue()
        o.date=date
        o.value=value
        self.append(o)    ## Returns a date value manager with the simple movil average 3 of weight
        
    ## Fills days without data  with the data before or after
    def DateValueManager_filling_empty(self, with_data_before=True):
        r=DateValueManager()
        last=self.first()
        r.append(last)
        for o in self.arr[1:]:
            while o.date!=last.date+timedelta(days=1):
                missing=DateValue()
                missing.date=last.date+timedelta(days=1)
                missing.value=last.value
                r.append(missing)
                last=missing
            r.append(o)
            last=o
            
        return r
        
    ## Converts a DateValueManager to a DatetimeValueManager.
    ## @param start Boolean. If true date is converted to the start of the day. If false to the end of the day
    ## @param timezone String with pytz timexone. If None datetimes will be naive, else datetimes will be aware
    def DatetimeValueManager(self, start=True, timezone=None):
        r=DatetimeValueManager()
        for o in self.arr:
            if start==True:
                if timezone==None:
                    r.appendDV(dtnaive_day_start_from_date(o.date), o.value)
                else:
                    r.appendDV(dtaware_day_start_from_date(o.date, timezone), o.value)
            else:#end of day
                if timezone==None:
                    r.appendDV(dtnaive_day_end_from_date(o.date), o.value)
                else:
                    r.appendDV(dtaware_day_end_from_date(o.date, timezone), o.value)
        return r

    ## Returns a DVManager with the simple movil average of the array
    def sma(self, period):
        r=DateValueManager()
        for i in range(period, self.length()):
            sma=DateValue()
            sma.value=0
            sma.date=self.arr[i].date
            for p in range(period):
                sma.value=sma.value+self.arr[i-p].value
            sma.value=sma.value/period
            r.append(sma)
        return r



if __name__ == "__main__":
    print("TESTING FILLING DATEVALUEMANAGER")
    r=DateValueManager()
    r.appendDV(date(2019, 1, 10), 1)
    r.appendDV(date(2019, 1, 17), 2)
    r.print()
    filled=r.DateValueManager_filling_empty()
    filled.print()

    sizes=(1,10,100,1000,10000,100000,1000000,3000000)
    for size in sizes:
        l=ObjectManager_With_Id()
        d=DictObjectManager_With_Id()
        for number in range(size):
            o=Object_With_IdName(number,"Name {}".format(number))
            l.append(o)
            d.append(o)
        middle=size*2//3
        start=datetime.now()
        l.find_by_id(middle)
        ltime=datetime.now()-start
        start=datetime.now()
        d.find_by_id(middle)
        dtime=datetime.now()-start
        print()
        print("Benchmarking search_by_id in to element {} with {} objects".format(middle,size))
        if ltime>=dtime:
            print("  * ObjectManager took {} more time than DictObjectManager".format(ltime-dtime))
        else:
            print("  * DictObjectManager took {} more time than ObjectManager".format(dtime-ltime))


