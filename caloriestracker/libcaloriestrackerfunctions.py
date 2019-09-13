## @namespace caloriestracker.libcaloriestrackerfunctions
## @brief Package with all xulpymoney auxiliar functions.
from PyQt5.QtCore import Qt,  QLocale
from PyQt5.QtGui import QIcon,  QColor
from PyQt5.QtWidgets import QTableWidgetItem,  QWidget,  QMessageBox, QApplication, QCheckBox, QHBoxLayout
from colorama import Fore, Style
from decimal import Decimal
from os import path, makedirs, remove
import datetime
import time
import functools
import warnings
import inspect
import logging
import pkg_resources
import pytz
import socket
from caloriestracker.libcaloriestrackertypes import eDtStrings


_=str


## Changes zoneinfo from a dtaware object
## For example:
## - datetime.datetime(2018, 5, 18, 8, 12, tzinfo=<DstTzInfo 'Europe/Madrid' CEST+2:00:00 DST>)
## - libcaloriestrackerfunctions.dtaware_changes_tz(a,"Europe/London")
## - datetime.datetime(2018, 5, 18, 7, 12, tzinfo=<DstTzInfo 'Europe/London' BST+1:00:00 DST>)
## @param dt datetime aware object
## @tzname String with datetime zone. For example: "Europe/Madrid"
## @return datetime aware object
def dtaware_changes_tz(dt,  tzname):
    if dt==None:
        return None
    tzt=pytz.timezone(tzname)
    tarjet=tzt.normalize(dt.astimezone(tzt))
    return tarjet

## Creates a QTableWidgetItem with the date
def qdate(date):
    if date==None:
        return qempty()
    return qcenter(str(date))

def qmessagebox(text):
    m=QMessageBox()
    m.setWindowIcon(QIcon(":/xulpymoney/coins.png"))
    m.setIcon(QMessageBox.Information)
    m.setText(text)
    m.exec_()   

def dtaware2epochms(d):
    """
        Puede ser dateime o date
        Si viene con zona datetime zone aware, se convierte a UTC y se da el valor en UTC
        return datetime.datetime.now(pytz.timezone(self.name))
    """
    if d.__class__==datetime.datetime:
        if d.tzname()==None:#unaware datetine
            logging.critical("Must be aware")
        else:#aware dateime changed to unawar
            utc=dtaware_changes_tz(d, 'UTC')
            return utc.timestamp()*1000
    logging.critical("{} can't be converted to epochms".format(d.__class__))
    
## Return a UTC datetime aware
def epochms2dtaware(n):
    utc_unaware=datetime.datetime.utcfromtimestamp(n/1000)
    utc_aware=utc_unaware.replace(tzinfo=pytz.timezone('UTC'))
    return utc_aware


## Returns a formated string of a dtaware string formatting with a zone name
## @param dt datetime aware object
## @return String
def dtaware2string(dt, type=eDtStrings.QTableWidgetItem):
    if dt==None:
        return "None"
    elif dt.tzname()==None:
        return "Naive date and time"
    else:
        return dtnaive2string(dt, type)

## Returns a formated string of a dtaware string formatting with a zone name
## @param dt datetime aware object
## @return String
def dtnaive2string(dt, type=eDtStrings.QTableWidgetItem):
    if dt==None:
        resultado="None"
    elif type==eDtStrings.QTableWidgetItem:
        if dt.microsecond==4 :
            resultado="{}-{}-{}".format(dt.year, str(dt.month).zfill(2), str(dt.day).zfill(2))
        else:
            resultado="{}-{}-{} {}:{}:{}".format(dt.year, str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2),  str(dt.second).zfill(2))
    elif type==eDtStrings.Filename:
            resultado="{}{}{} {}{}".format(dt.year, str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2))
    elif type==eDtStrings.String:
        resultado="{}{}{}{}{}".format(dt.year, str(dt.month).zfill(2), str(dt.day).zfill(2), str(dt.hour).zfill(2), str(dt.minute).zfill(2))
    return resultado
    
## allows you to measure the execution time of the method/function by just adding the @timeit decorator on the method.
## @timeit
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return timed

def deprecated(func):
     """This is a decorator which can be used to mark functions
     as deprecated. It will result in a warning being emitted
     when the function is used."""
     @functools.wraps(func)
     def new_func(*args, **kwargs):
         warnings.simplefilter('always', DeprecationWarning)  # turn off filter
         warnings.warn("Call to deprecated function {}.".format(func.__name__),
                       category=DeprecationWarning,
                       stacklevel=2)
         warnings.simplefilter('default', DeprecationWarning)  # reset filter
         return func(*args, **kwargs)
     return new_func
 
## dt es un datetime con timezone, que se mostrara con la zone pasado como parametro
## Convierte un datetime a string, teniendo en cuenta los microsehgundos, para ello se convierte a datetime local
def qdatetime(dt, zone):
    newdt=dtaware_changes_tz(dt, zone.name)
    if newdt==None:
        return qempty()
    a=QTableWidgetItem(dtaware2string(newdt))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    return a

def qtime(dt):
    """
        Shows the time of a datetime
    """
    if dt==None:
        return qempty()
    if dt.microsecond==5:
        item=qleft(str(dt)[11:-13])
        item.setBackground(QColor(255, 255, 148))
    elif dt.microsecond==4:
        item=qleft(str(dt)[11:-13])
        item.setBackground(QColor(148, 148, 148))
    else:
        item=qleft(str(dt)[11:-6])
    return item
    
def list2string(lista):
        """Covierte lista a string"""
        if  len(lista)==0:
            return ""
        if str(lista[0].__class__) in ["<class 'int'>", "<class 'float'>"]:
            resultado=""
            for l in lista:
                resultado=resultado+ str(l) + ", "
            return resultado[:-2]
        elif str(lista[0].__class__) in ["<class 'str'>",]:
            resultado=""
            for l in lista:
                resultado=resultado+ "'" + str(l) + "', "
            return resultado[:-2]
            
def string2list_of_integers(s, separator=", "):
    """Convers a string of integer separated by comma, into a list of integer"""
    arr=[]
    if s!="":
        arrs=s.split(separator)
        for a in arrs:
            arr.append(int(a))
    return arr
    
def string2date(iso, type=1):
    """
        date string to date, with type formats
    """
    if type==1: #YYYY-MM-DD
        d=iso.split("-")
        return datetime.date(int(d[0]), int(d[1]),  int(d[2]))
    if type==2: #DD/MM/YYYY
        d=iso.split("/")
        return datetime.date(int(d[2]), int(d[1]),  int(d[0]))
    if type==3: #DD.MM.YYYY
        d=iso.split(".")
        return datetime.date(int(d[2]), int(d[1]),  int(d[0]))
    if type==4: #DD/MM
        d=iso.split("/")
        return datetime.date(datetime.date.today().year, int(d[1]),  int(d[0]))

## Function to generate a datetime (aware or naive) from a string
## @param s String
## @param type Integer
## @param zone Name of the zone. By default "Europe Madrid" only in type 3and 4
## @return Datetime
def string2datetime(s, type, zone="Europe/Madrid"):
    if type==1:#2017-11-20 23:00:00+00:00  ==> Aware
        s=s[:-3]+s[-2:]
        dat=datetime.datetime.strptime( s, "%Y-%m-%d %H:%M:%S%z" )
        return dat
    if type==2:#20/11/2017 23:00 ==> Naive
        dat=datetime.datetime.strptime( s, "%d/%m/%Y %H:%M" )
        return dat
    if type==3:#20/11/2017 23:00 ==> Aware, using zone parameter
        dat=datetime.datetime.strptime( s, "%d/%m/%Y %H:%M" )
        z=pytz.timezone(zone)
        return z.localize(dat)
    if type==4:#27 1 16:54 2017==> Aware, using zone parameter . 1 es el mes convertido con month2int
        dat=datetime.datetime.strptime( s, "%d %m %H:%M %Y")
        z=pytz.timezone(zone)
        return z.localize(dat)
    if type==5:#2017-11-20 23:00:00.000000+00:00  ==> Aware with microsecond
        s=s[:-3]+s[-2:]#quita el :
        arrPunto=s.split(".")
        s=arrPunto[0]+s[-5:]
        micro=int(arrPunto[1][:-5])
        dat=datetime.datetime.strptime( s, "%Y-%m-%d %H:%M:%S%z" )
        dat=dat+datetime.timedelta(microseconds=micro)
        return dat
    if type==6:#201907210725 ==> Naive
        dat=datetime.datetime.strptime( s, "%Y%m%d%H%M" )
        return dat
    if type==7:#01:02:03 ==> Aware
        tod=datetime.date.today()
        a=s.split(":")
        dat=datetime.datetime(tod.year, tod.month, tod.day, int(a[0]), int(a[1]), int(a[2]))
        z=pytz.timezone(zone)
        return z.localize(dat)

## Converts a string  to a decimal
def string2decimal(s, type=1):
    if type==1: #2.123,25
        try:
            return Decimal(s.replace(".","").replace(",", "."))
        except:
            return None

## Converts a tring 12:23 to a datetime.time object
def string2time(s, type=1):
    if type==1:#12:12
        a=s.split(":")
        return datetime.time(int(a[0]), int(a[1]))
    elif type==2:#12:12:12
        a=s.split(":")
        return datetime.time(int(a[0]), int(a[1]), int(a[2]))

## Bytes 2 string
def b2s(b, code='UTF-8'):
    return b.decode(code)
    
def s2b(s, code='UTF8'):
    """String 2 bytes"""
    if s==None:
        return "".encode(code)
    else:
        return s.encode(code)

def c2b(state):
    """QCheckstate to python bool"""
    if state==Qt.Checked:
        return True
    else:
        return False

def b2c(booleano):
    """Bool to QCheckstate"""
    if booleano==True:
        return Qt.Checked
    else:
        return Qt.Unchecked     

def day_end(dattime, zone):
    """Saca cuando acaba el dia de un dattime en una zona concreta"""
    return dtaware_changes_tz(dattime, zone.name).replace(hour=23, minute=59, second=59)
    
def day_start(dattime, zone):
    return dtaware_changes_tz(dattime, zone.name).replace(hour=0, minute=0, second=0)
    
def day_end_from_date(date, zone):
    """Saca cuando acaba el dia de un dattime en una zona concreta"""
    return dtaware(date, datetime.time(23, 59, 59), zone.name)
    
def day_start_from_date(date, zone):
    return dtaware(date, datetime.time(0, 0, 0), zone.name)
    
def month_start(year, month, zone):
    """datetime primero de un mes
    """
    return day_start_from_date(datetime.date(year, month, 1), zone)
    
def month2int(s):
    """
        Converts a month string to a int
    """
    if s in ["Jan", "Ene", "Enero", "January", "enero", "january"]:
        return 1
    if s in ["Feb", "Febrero", "February", "febrero", "february"]:
        return 2
    if s in ["Mar", "Marzo", "March", "marzo", "march"]:
        return 3
    if s in ["Apr", "Abr", "April", "Abril", "abril", "april"]:
        return 4
    if s in ["May", "Mayo", "mayo", "may"]:
        return 5
    if s in ["Jun", "June", "Junio", "junio", "june"]:
        return 6
    if s in ["Jul", "July", "Julio", "julio", "july"]:
        return 7
    if s in ["Aug", "Ago", "August", "Agosto", "agosto", "august"]:
        return 8
    if s in ["Sep", "Septiembre", "September", "septiembre", "september"]:
        return 9
    if s in ["Oct", "October", "Octubre", "octubre", "october"]:
        return 10
    if s in ["Nov", "Noviembre", "November", "noviembre", "november"]:
        return 11
    if s in ["Dic", "Dec", "Diciembre", "December", "diciembre", "december"]:
        return 12

def month_end(year, month, zone):
    """datetime último de un mes
    """
    return day_end_from_date(month_last_date(year, month), zone)
    
## Returns a date with the last day of a month
## @return datetime.date object
def month_last_date(year, month):
    if month == 12:
        return datetime.date(year, month, 31)
    return datetime.date(year, month+1, 1) - datetime.timedelta(days=1)

## Returns an aware datetime with the start of year
def year_start(year, zone):
    return day_start_from_date(datetime.date(year, 1, 1), zone)
    
## Returns an aware datetime with the last of year
def year_end(year, zone):
    return day_end_from_date(datetime.date(year, 12, 31), zone)
    
## Function that converts a number of days to a string showing years, months and days
## @param days Integer with the number of days
## @return String like " 0 years, 1 month and 3 days"
def days2string(days):
    years=days//365
    months=(days-years*365)//30
    days=int(days -years*365 -months*30)
    if years==1:
        stryears=QApplication.translate("Core", "year")
    else:
        stryears=QApplication.translate("Core", "years")
    if months==1:
        strmonths=QApplication.translate("Core", "month")
    else:
        strmonths=QApplication.translate("Core", "months")
    if days==1:
        strdays=QApplication.translate("Core", "day")
    else:
        strdays=QApplication.translate("Core", "days")
    return QApplication.translate("Core", "{} {}, {} {} and {} {}").format(years, stryears,  months,  strmonths, days,  strdays)


def dirs_create():
    """
        Returns xulpymoney_tmp_dir, ...
    """
    dir_tmp=path.expanduser("~/.caloriestracker/tmp/")
    try:
        makedirs(dir_tmp)
    except:
        pass
    return dir_tmp

## Function to create a datetime aware object
## @param date datetime.date object
## @param hour datetime.hour object
## @param zonename String with datetime zone name. For example "Europe/Madrid"
## @return datetime aware
def dtaware(date, hour, zonename):
    z=pytz.timezone(zonename)
    a=datetime.datetime(date.year,  date.month,  date.day,  hour.hour,  hour.minute,  hour.second, hour.microsecond)
    a=z.localize(a)
    return a
    
## Converts strings True or False to boolean
## @param s String
## @return Boolean
def str2bool(s):
    if s=="True":
        return True
    return False    

## Returns the path searching in a pkg_resource model and a url. Due to PYinstaller packager doesn't supportpkg_resource
## filename is differet if we are in LInux, Windows --onefile or Windows --onedir
## @param module String
## @param url String
## @return string with the filename
def package_filename(module, url):
    for filename in [
        pkg_resources.resource_filename(module, url), #Used in pypi and Linux
        url, #Used in pyinstaller --onedir, becaouse pkg_resources is not supported
        pkg_resources.resource_filename(module,"../{}".format(url)), #Used in pyinstaller --onefile, becaouse pkg_resources is not supported
    ]:
        if filename!=None and path.exists(filename):
            logging.info("FOUND " +  filename) #When debugging in windows, change logging for printt
            return filename
        else:
            logging.debug("NOT FOUND" + filename)

## Converts boolean to  True or False string
## @param s String
## @return Boolean
def bool2string(b):
    if b==True:
        return "VERDADERO"
    return "FALSO"
    
## Function that converts a None value into a Decimal('0')
## @param dec Should be a Decimal value or None
## @return Decimal
def none2decimal0(dec):
    if dec==None:
        return Decimal('0')
    return dec

def qbool(bool):
    """Prints bool and check. Is read only and enabled"""
    if bool==None:
        return qempty()
    a=QTableWidgetItem()
    a.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )#Set no editable
    if bool:
        a.setCheckState(Qt.Checked);
        a.setText(QApplication.translate("Core","True"))
    else:
        a.setCheckState(Qt.Unchecked);
        a.setText(QApplication.translate("Core","False"))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
    return a
    
def wdgBool(bool):
    """Center checkbox
    Yo must use with table.setCellWidget(0,0,wdgBool)
    Is disabled to be readonly"""
    pWidget = QWidget()
    pCheckBox = QCheckBox();
    if bool:
        pCheckBox.setCheckState(Qt.Checked);
    else:
        pCheckBox.setCheckState(Qt.Unchecked);
    pLayout = QHBoxLayout(pWidget);
    pLayout.addWidget(pCheckBox);
    pLayout.setAlignment(Qt.AlignCenter);
    pLayout.setContentsMargins(0,0,0,0);
    pWidget.setLayout(pLayout);
    pCheckBox.setEnabled(False)
    return pWidget
    
## Returns a QTableWidgetItem representing an empty value
def qempty():
    a=QTableWidgetItem("---")
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    return a

def qcenter(string, digits=None):
    if string==None:
        return qempty()
    a=QTableWidgetItem(str(string))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
    return a
    
def qleft(string):
    if string==None:
        return qempty()
    a=QTableWidgetItem(str(string))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
    return a

def qright(string, digits=None):
    """When digits, limits the number to """
    if string==None:
        return qempty()
    if string!=None and digits!=None:
        string=round(string, digits)
    a=QTableWidgetItem(str(string))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    try:#If is a number corized it
        if string==None:
            a.setForeground(QColor(0, 0, 255))
        elif string<0:
            a.setForeground(QColor(255, 0, 0))
    except:
        pass
    return a
        
def web2utf8(cadena):
    cadena=cadena.replace('&#209;','Ñ')
    cadena=cadena.replace('&#241;','ñ')
    cadena=cadena.replace('&#252;','ü')
    cadena=cadena.replace('&#246;','ö')
    cadena=cadena.replace('&#233;','é')
    cadena=cadena.replace('&#228;','ä')
    cadena=cadena.replace('&#214;','Ö')
    cadena=cadena.replace('&amp;','&')
    cadena=cadena.replace('&AMP;','&')
    cadena=cadena.replace('&Ntilde;','Ñ')
    
    return cadena
    
## Converts a decimal to a localized number string
def l10nDecimal(dec, digits=2):
    l=QLocale()
    
    return l.toCurrencyString(float(dec))
    
    
def function_name(clas):
    #    print (inspect.stack()[0][0].f_code.co_name)
    #    print (inspect.stack()[0][3],  inspect.stack())
    #    print (inspect.stack()[1][3],  inspect.stack())
    #    print (clas.__class__.__name__)
    #    print (clas.__module__)
    return "{0}.{1}".format(clas.__class__.__name__,inspect.stack()[1][3])
    
## Check if two numbers has the same sign
## @param number1 First number used in check
## @param number2 Second number used in check
## @return bool True if they have the same sign
def have_same_sign(number1, number2):
    if (is_positive(number1)==True and is_positive(number2)==True) or (is_positive(number1)==False and is_positive(number2)==False):
        return True
    return False

## Check if a number is positive
## @param number Number used in check
## @return bool True if number is positive, else False
def is_positive(number):
    if number>=0:
        return True
    return False

## Checks if there is internet
def is_there_internet():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False

## Asks a a question to delete a file
## Returns True or False if file has been deleted
def question_delete_file(filename):
    reply = QMessageBox.question(
                    None, 
                    QApplication.translate("Core", 'File deletion question'), 
                    QApplication.translate("Core", "Do you want to delete this file:\n'{}'?").format(filename), 
                    QMessageBox.Yes, 
                    QMessageBox.No
                )
    if reply==QMessageBox.Yes:
        remove(filename)
        if path.exists(filename)==False:
            return True
    return False
        
def setReadOnly(wdg, boolean):
    if wdg.__class__.__name__=="QCheckBox":
        wdg.blockSignals(boolean)
        wdg.setAttribute(Qt.WA_TransparentForMouseEvents)
        wdg.setFocusPolicy(Qt.NoFocus)
## amount2string
def a2s(amount):
    return str(round(amount, 2)).rjust(7)

def ca2s(amount,limit):
    if amount <= limit:
        return Fore.GREEN + a2s(amount) + Fore.RESET
    else:
        return Fore.RED + a2s(amount) + Fore.RESET
## None2string
def n2s():
    return str("").rjust(7)




def input_decimal(text, default=None):
    while True:
        if default==None:
            res=input(Style.BRIGHT+text+": ")
        else:
            print(Style.BRIGHT+ Fore.WHITE+"{} [{}]: ".format(text, Fore.GREEN+str(default)+Fore.WHITE), end="")
            res=input()
        try:
            if res==None or res=="":
                res=default
            res=Decimal(res)
            return res
        except:
            pass
            

def input_int(text, default=None):
    while True:
        if default==None:
            res=input(Style.BRIGHT+text+": ")
        else:
            print(Style.BRIGHT+ Fore.WHITE+"{} [{}]: ".format(text, Fore.GREEN+str(default)+Fore.WHITE), end="")
            res=input()
        try:
            if res==None or res=="":
                res=default
            res=int(res)
            return res
        except:
            pass
def input_integer_or_none(text, default=""):
    while True:
        print(Style.BRIGHT+ Fore.WHITE+"{} (Empty:None,Integer) [{}]: ".format(text, Fore.GREEN+str(default)+Fore.WHITE), end="")
        res=input()
        if res=="":
            return None
        else:
            try:
                return int(res)
            except:
                continue

def input_boolean_or_none(text, default="N"):
    while True:
        print(Style.BRIGHT+ Fore.WHITE+"{} (N:None,T:True,F:False) [{}]: ".format(text, Fore.GREEN+str(default)+Fore.WHITE), end="")
        res=input()
        if res not in ('NFT'):
            continue
        if res=="N":
            return None
        elif res=="T":
            return True
        else:
            return False            
def input_boolean(text, default="T"):
    while True:
        print(Style.BRIGHT+ Fore.WHITE+"{} (T:True,F:False) [{}]: ".format(text, Fore.GREEN+str(default)+Fore.WHITE), end="")
        res=input().upper()
        if res=="":
            res=default
        if res not in ('FT'):
            continue
        
        if res=="T":
            return True
        else:
            return False
            

def input_YN(pregunta, default="Y"):
    ansyes=_("Y")
    ansno=_("N")
    
    bracket="{}|{}".format(ansyes.upper(), ansno.lower()) if default.upper()==ansyes else "{}|{}".format(ansyes.lower(), ansno.upper())
    while True:
        print(Style.BRIGHT+ Fore.WHITE+"{} [{}]: ".format(pregunta,  Fore.GREEN+bracket+Fore.WHITE), end="")
        user_input = input().strip().upper()
        if not user_input or user_input=="":
            user_input=default
        if user_input == ansyes:
                return True
        elif user_input == ansno:
                return False
        else:
                print (_("Please enter '{}' or '{}'".format(ansyes, ansno)))

def input_string(text,default=None):
    while True:
        if default==None:
            res=input(Style.BRIGHT+text+": ")
        else:
            print(Style.BRIGHT+ Fore.WHITE+"{} [{}]: ".format(text, Fore.GREEN+str(default)+Fore.WHITE), end="")
            res=input()
        try:
            if res==None or res=="":
                res=default
            res=str(res)
            return res
        except:
            pass
