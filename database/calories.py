from argparse import ArgumentParser, RawTextHelpFormatter
from colorama import Fore, Style
from connection_pg import Connection, argparse_connection_arguments_group
from datetime import datetime, date, timedelta
from decimal import Decimal
from glob import glob
from libmanagers import ObjectManager_With_IdDatetime
_=str

class Meal:
    def __init__(self):
        pass
    def init__from_row(self,row):
        self.datetime=row['datetime']
        self.name=row['name']
        self.product_calories=row['calories']
        self.product_fat=row['fat']
        self.product_protein=row['protein']
        self.product_amount=row['p_amount']
        self.product_carbohydrate=row['carbohydrate']
        self.product_salt=row['salt']
        self.meal_amount=row['m_amount']
        return self
    def meal_calories(self):
        return self.meal_amount * self.product_calories/self.product_amount
    def meal_fat(self):
        return self.meal_amount * self.product_fat/self.product_amount
    def meal_protein(self):
        return self.meal_amount * self.product_protein/self.product_amount
    def meal_carbohydrate(self):
        return self.meal_amount * self.product_carbohydrate/self.product_amount
    def meal_salt(self):
        return self.meal_amount * self.product_salt/self.product_amount

    def meal_hour(self):
        return str(self.datetime.time())[0:5]

class Meals(ObjectManager_With_IdDatetime):
    def __init__(self):
        ObjectManager_With_IdDatetime.__init__(self)
    def init__from_db(self, sql):
        rows=con.cursor_rows(sql)
        for row in rows:
            self.append(Meal().init__from_row(row))
        return self
    def calories(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.meal_calories()
        return r
    def fat(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.meal_fat()
        return r
    def protein(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.meal_protein()
        return r
    def carbohydrate(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.meal_carbohydrate()
        return r
    def salt(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.meal_salt()
        return r
    def max_name_len(self):
        r=0
        for meal in self.arr:
            if len(meal.name)>r:
                r=len(meal.name)
        return r

class User:
    def __init__(self):
        pass
    def init__from_db(self,id):
        row=con.cursor_one_row("select * from users where id=%s",(id,))
        self.id=row['id']
        self.name=row['name']
        self.male=row['male']
        self.birthday=row['birthday']
        row=con.cursor_one_row("select * from biometrics where id=%s order by datetime desc limit 1",(self.id,))
        self.height=row['height']
        self.weight=row['weight']
        return self 

    ##basal metabolic rate
    def bmr(self):
        if self.male==True:
            return Decimal(10)*self.weight + Decimal(6.25)*self.height - Decimal(5)*self.age() + 5
        else: #female
            return Decimal(10)*self.weight + Decimal(6.25)*self.height - Decimal(5)*self.age() - 161

    def age(self):
        return (date.today() - self.birthday) // timedelta(days=365.2425)

class Product:
    def __init__(self):
        pass
    
    def init__row(self):
        pass
## amount2string
def a2s(amount):
    return str(round(amount, 2)).rjust(6)


def string2date(iso, type=1):
    """
        date string to date, with type formats
    """
    if type==1: #YYYY-MM-DD
        d=iso.split("-")
        return date(int(d[0]), int(d[1]),  int(d[2]))
    if type==2: #DD/MM/YYYY
        d=iso.split("/")
        return date(int(d[2]), int(d[1]),  int(d[0]))
    if type==3: #DD.MM.YYYY
        d=iso.split(".")
        return date(int(d[2]), int(d[1]),  int(d[0]))
    if type==4: #DD/MM
        d=iso.split("/")
        return date(date.today().year, int(d[1]),  int(d[0]))

parser=ArgumentParser(prog='calories', description=_('Report of calories'), epilog=_("Developed by Mariano Muñoz 2012-{}".format(datetime.now().year)), formatter_class=RawTextHelpFormatter)
argparse_connection_arguments_group(parser, default_db="caloriestracker")
group = parser.add_argument_group("productrequired=True")
group.add_argument('--date', help=_('Date to show'), action="store", default=str(date.today()))
group.add_argument('--user_id', help=_('User id'), action="store", default=1)
args=parser.parse_args()

con=Connection()
con.user=args.user
con.server=args.server
con.port=args.port
con.db=args.db
con.get_password()
con.connect()

args.date=string2date(args.date)
args.user_id=int(args.user_id)

user=User().init__from_db(args.user_id)

meals=Meals().init__from_db(con.mogrify("""
select
    products.calories,
    products.name,
    products.fat,
    products.protein,
    products.carbohydrate,
    products.amount as p_amount,
    products.salt,
    meals.amount as m_amount,
    meals.datetime 
from 
    meals, 
    products 
where products.id=meals.products_id and datetime::date=%s and user_id=%s""",(args.date, args.user_id)))

con.disconnect()

print("Hi {}, you are {} old with {} Kg and {} cm tall".format(user.name, user.age(), user.weight, user.height))
print("Your BMR is {}".format(user.bmr()))

print("This is your meal for {}:".format(args.date))
for meal in meals.arr:
    print("{} {}. Fat {}. Protein {}, Carbohydrate {}".format(meal.datetime, meal.name, meal.meal_fat(), meal.meal_protein(), meal.meal_carbohydrate()))



maxname=meals.max_name_len()
maxlength=5+2+maxname+2+6+2+6+2+6
print (Style.BRIGHT+ "="*(maxlength) + Style.RESET_ALL)
print (Style.BRIGHT+ "{} MEALS AT {}".format(meals.length(), args.date).center(maxlength," ") + Style.RESET_ALL)
print (Style.BRIGHT+ "="*(maxlength) + Style.RESET_ALL)

print (Style.BRIGHT+ "{}  {}  {}  {}  {}".format(" HOUR".center(5,' '),"NAME".center(maxname," "),"CAL".center(6,' '), "FAT".center(6,' '), "PRO".center(6,' ')) + Style.RESET_ALL)
for meal in meals.arr:
    print (Style.BRIGHT + "{}  {}  {}  {}  {}".format(meal.meal_hour(), meal.name.ljust(maxname), a2s(meal.meal_calories()), a2s(meal.meal_fat()), a2s(meal.meal_protein())) + Style.RESET_ALL)
#    print ("{}  {}  {}  {}  {}".format(h.ip.ljust(16), h.type.name.ljust(maxtype),  mac.center(17),   Style.BRIGHT+Fore.YELLOW +  alias.ljust(maxalias), Style.NORMAL+Fore.WHITE+ h.oui.ljust(maxoui)) + Style.RESET_ALL)
print (Style.BRIGHT+ "-"*(maxlength) + Style.RESET_ALL)
print (Style.BRIGHT + "TOTAL  {}  {}  {}  {}".format("".ljust(maxname), a2s(meals.calories()), a2s(meals.fat()), a2s(meals.protein())) + Style.RESET_ALL)

print (Style.BRIGHT + "="*(maxlength) + Style.RESET_ALL)

print ("Calories {} of {}".format(meals.calories(),user.bmr()))