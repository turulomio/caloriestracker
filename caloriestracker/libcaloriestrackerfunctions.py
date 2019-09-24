## @namespace caloriestracker.libcaloriestrackerfunctions
## @brief Package with all xulpymoney auxiliar functions.
from PyQt5.QtCore import Qt,  QLocale
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget,  QMessageBox, QApplication, QCheckBox, QHBoxLayout
from colorama import Fore
from decimal import Decimal
from os import path, makedirs, remove
import inspect
import socket

def qmessagebox(text):
    m=QMessageBox()
    m.setWindowIcon(QIcon(":/xulpymoney/coins.png"))
    m.setIcon(QMessageBox.Information)
    m.setText(text)
    m.exec_()   

 
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

## Converts a string  to a decimal
def string2decimal(s, type=1):
    if type==1: #2.123,25
        try:
            return Decimal(s.replace(".","").replace(",", "."))
        except:
            return None


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


## Converts strings True or False to boolean
## @param s String
## @return Boolean
def str2bool(s):
    if s=="True":
        return True
    return False    

### Returns the path searching in a pkg_resource model and a url. Due to PYinstaller packager doesn't supportpkg_resource
### filename is differet if we are in LInux, Windows --onefile or Windows --onedir
### @param module String
### @param url String
### @return string with the filename
#def package_filename(module, url):
#    for filename in [
#        pkg_resources.resource_filename(module, url), #Used in pypi and Linux
#        url, #Used in pyinstaller --onedir, becaouse pkg_resources is not supported
#        pkg_resources.resource_filename(module,"../{}".format(url)), #Used in pyinstaller --onefile, becaouse pkg_resources is not supported
#    ]:
#        if filename!=None and path.exists(filename):
#            info("Package filename '{}' found".format(filename)) #When debugging in windows, change logging for printt
#            return filename
#    debug("Not found {} in module {}".format(url, module))

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

## Shows amount with a2s in red if amount is over the limit
def ca2s(amount,limit):
    if amount <= limit:
        return Fore.GREEN + a2s(amount) + Fore.RESET
    else:
        return Fore.RED + a2s(amount) + Fore.RESET

## Reverse ca2s. Shows amount with a2s in green if amount is over the limit
def rca2s(amount,limit):
    if amount > limit:
        return Fore.GREEN + a2s(amount) + Fore.RESET
    else:
        return Fore.RED + a2s(amount) + Fore.RESET
## None2string
def n2s():
    return str("").rjust(7)
