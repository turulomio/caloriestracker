## @brief my Percentage object
## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from logging import error
from sys import exit
from decimal import Decimal

## Class to manage currencies in officegenerator
##
## The symbol is defined by code with self.symbol()
class Currency:
    def __init__(self, amount=None,  currency='EUR') :
        if amount==None:
            self.amount=Decimal(0)
        else:
            self.amount=Decimal(str(amount))
        if currency==None:
            self.currency='EUR'
        else:
            self.currency=currency


    def __add__(self, money):
        """Si las divisas son distintas, queda el resultado con la divisa del primero"""
        if self.currency==money.currency:
            return Currency(self.amount+money.amount, self.currency)
        else:
            error("Before adding, please convert to the same currency")
            raise "OdfMoneyOperationException"

    def __sub__(self, money):
        """Si las divisas son distintas, queda el resultado con la divisa del primero"""
        if self.currency==money.currency:
            return Currency(self.amount-money.amount, self.currency)
        else:
            error("Before substracting, please convert to the same currency")
            raise "CurrencyOperationException"

    def __lt__(self, money):
        if self.currency==money.currency:
            if self.amount < money.amount:
                return True
            return False
        else:
            error("Before lt ordering, please convert to the same currency")
            exit(1)

    ## Si las divisas son distintas, queda el resultado con la divisa del primero
    ##
    ## En caso de querer multiplicar por un numero debe ser despues. For example: money*4
    def __mul__(self, money):
        if money.__class__ in (int,  float, Decimal):
            return Currency(self.amount*money, self.currency)
        if self.currency==money.currency:
            return Currency(self.amount*money.amount, self.currency)
        else:
            error("Before multiplying, please convert to the same currency")
            exit(1)

    def __truediv__(self, money):
        """Si las divisas son distintas, queda el resultado con la divisa del primero"""
        if self.currency==money.currency:
            return Currency(self.amount/money.amount, self.currency)
        else:
            error("Before true dividing, please convert to the same currency")
            exit(1)

    def __repr__(self):
        return self.string(2)

    ## Returs a typical currency string
    ## @param digits int that defines the number of decimals. 2 by default
    ## @return string
    def string(self,   digits=2):
        return "{} {}".format(round(self.amount, digits), self.symbol())

    ## Returns the symbol of the currency
    def symbol(self):
        if self.currency=="EUR":
            return "€"
        elif self.currency=="USD":
            return "$"

    def isZero(self):
        if self.amount==Decimal(0):
            return True
        else:
            return False

    def isGETZero(self):
        if self.amount>=Decimal(0):
            return True
        else:
            return False

    def isGTZero(self):
        if self.amount>Decimal(0):
            return True
        else:
            return False

    def isLTZero(self):
        if self.amount<Decimal(0):
            return True
        else:
            return False

    def isLETZero(self):
        if self.amount<=Decimal(0):
            return True
        else:
            return False

    def __neg__(self):
        """Devuelve otro money con el amount con signo cambiado"""
        return Currency(-self.amount, self.currency)

    def round(self, digits=2):
        return round(self.amount, digits)
