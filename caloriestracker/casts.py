## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from PyQt5.QtCore import QLocale, Qt
from decimal import Decimal

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


## Converts a decimal to a localized number string
def l10nDecimal(dec, digits=2):
    l=QLocale()
    
    return l.toCurrencyString(float(dec))
    
   
## Converts strings True or False to boolean
## @param s String
## @return Boolean
def str2bool(s):
    if s=="True":
        return True
    return False    

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
    return none2alt(dec,Decimal('0'))

## If a value is None, returns an alternative
def none2alt(value, alternative):
    if value==None:
        return alternative
    return value

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


