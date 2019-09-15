## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README
from colorama import Style, Fore
from decimal import Decimal

_=str

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
