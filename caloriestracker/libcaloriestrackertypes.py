## @namespace xulpymoney.libxulpymoneytypes
## @brief Package with all xulpymoney types.
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QApplication
from enum import IntEnum

## Class with used QColors in app
class eQColor:
    Red=QColor(255, 148, 148)
    Green=QColor(148, 255, 148)
        
class eProductType(IntEnum):
    """
        IntEnum permite comparar 1 to eProductType.Share
    """
    Share=1
    Fund=2
    Index=3
    ETF=4
    Warrant=5
    Currency=6
    PublicBond=7
    PensionPlan=8
    PrivateBond=9
    Deposit=10
    Account=11
    CFD=12
    Future=13
    
## Operation tipes
class eOperationType:
    Expense=1
    Income=2
    Transfer=3
    SharesPurchase=4
    SharesSale=5
    SharesAdd=6
    CreditCardBilling=7
    TransferFunds=8
    TransferSharesOrigin=9
    TransferSharesDestiny=10
    HlContract=11
    
class eTickerPosition(IntEnum):
    """It's the number to access to a python list,  not to postgresql. In postgres it will be +1"""
    Yahoo=0
    Morningstar=1
    Google=2
    QueFondos=3
    InvestingCom=4
    
    def postgresql(etickerposition):
        return etickerposition.value+1
        
    ## Returns the number of atributes
    def length():
        return len(eTickerPosition.__dict__)


class eComment:
    InvestmentOperation=10000
    Dividend=10004
    HlContract=10007
    AccountTransferOrigin=10001
    AccountTransferDestiny=10002
    AccountTransferOriginCommission=10003
    CreditCardBilling=10005
    CreditCardRefund=10006# Estaba en 10007


## System concepts tipified
class eConcept:
    OpenAccount=1
    TransferOrigin=4
    TransferDestiny=5
    TaxesReturn=6
    BuyShares=29
    SellShares=35
    TaxesPayment=37
    BankCommissions=38
    Dividends=39
    CreditCardBilling=40
    AddShares=43
    AssistancePremium=50
    CommissionCustody=59
    DividendsSaleRights=62
    BondsCouponRunPayment=63
    BondsCouponRunIncome=65
    BondsCoupon=66
    CreditCardRefund=67
    HlAdjustmentIincome=68
    HlAdjustmentExpense=69
    HlGuaranteePaid=70
    HlGuaranteeReturned=71
    HlCommission=72
    HlInterestPaid=73
    HlInterestReceived=74
    RolloverPaid=75
    RolloverReceived=76

## Types for dt strings. Used in dtaware2string function
class eDtStrings:
    ## Parsed for ui
    QTableWidgetItem=1
    
    ## 20190909 0909
    Filename=2
    
    ## 201909090909
    String=3

## Sets if a Historical Chart must adjust splits or dividends with splits or do nothing
class eHistoricalChartAdjusts:
    ## Without splits nor dividens
    NoAdjusts=0
    ## WithSplits
    Splits=1
    ##With splits and dividends
    SplitsAndDividends=2#Dividends with splits.        
    
class eOHCLDuration:
    Day=1
    Week=2
    Month=3
    Year=4

    @classmethod
    def qcombobox(self, combo, selected_eOHCLDuration):
        combo.addItem(QApplication.translate("Core", "Day"), 1)
        combo.addItem(QApplication.translate("Core", "Week"), 2)
        combo.addItem(QApplication.translate("Core", "Month"), 3)
        combo.addItem(QApplication.translate("Core", "Year"), 4)
        combo.setCurrentIndex(combo.findData(selected_eOHCLDuration))

class eLeverageType:
    Variable=-1
    NotLeveraged=1
    X2=2
    X3=3
    X4=4
    X5=5
    X10=10
    X50=50
    X100=100

class eMoneyCurrency:
    Product=1
    Account=2
    User=3

## Type definition to refer to long /short invesment type positions
class eInvestmentTypePosition:
    Long=1
    Short=2

    @classmethod
    def qicon_boolean(self, boolean):
        e=eInvestmentTypePosition.to_eInvestmentTypePosition(boolean)
        return eInvestmentTypePosition.qicon(e)

    @classmethod
    def qicon(self, einvestmenttypeposition):
        if einvestmenttypeposition==eInvestmentTypePosition.Long:
            return QIcon(":/xulpymoney/up.png")
        else:
            return QIcon(":/xulpymoney/down.png")
            

    @classmethod
    def qcombobox(self, combo, selected_eInvestmentTypePosition=None):
        combo.addItem(eInvestmentTypePosition.qicon(eInvestmentTypePosition.Long), QApplication.translate("Core", "Long"), eInvestmentTypePosition.Long)
        combo.addItem(eInvestmentTypePosition.qicon(eInvestmentTypePosition.Short), QApplication.translate("Core", "Short"), eInvestmentTypePosition.Short)
        combo.setCurrentIndex(combo.findData(selected_eInvestmentTypePosition))

    ## Return True if it's short. Due to postgres database has this definition
    @classmethod
    def to_boolean(self, einvestmenttypeposition):
        if einvestmenttypeposition==1:
            return False
        return True

    ## Returns Short if boolean is true
    @classmethod
    def to_eInvestmentTypePosition(self, boolean):
        if boolean==True:
            return eInvestmentTypePosition.Short
        return eInvestmentTypePosition.Long
