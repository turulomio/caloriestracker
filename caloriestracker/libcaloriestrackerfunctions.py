## @namespace caloriestracker.libcaloriestrackerfunctions
## @brief Package with all xulpymoney auxiliar functions.
from colorama import Fore
from os import path, makedirs
import inspect

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

    
def function_name(clas):
    #    print (inspect.stack()[0][0].f_code.co_name)
    #    print (inspect.stack()[0][3],  inspect.stack())
    #    print (inspect.stack()[1][3],  inspect.stack())
    #    print (clas.__class__.__name__)
    #    print (clas.__module__)
    return "{0}.{1}".format(clas.__class__.__name__,inspect.stack()[1][3])
    

## Check if a number is positive
## @param number Number used in check
## @return bool True if number is positive, else False
def is_positive(number):
    if number>=0:
        return True
    return False

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
