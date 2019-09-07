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
        self.product_fiber=row['fiber']
        self.meal_amount=row['m_amount']
        self.personalproducts_id=row['personalproducts_id']
        self.companies_id=row['companies_id']
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
        return self.meal_amount * self.product_salt/self.product_amoun
    def meal_fiber(self):
        return self.meal_amount * self.product_fiber/self.product_amount

    def meal_hour(self):
        return str(self.datetime.time())[0:5]

    def product_type(self):
        if self.personalproducts_id==None and self.companies_id==None:
            return "Basic"
        elif self.personalproducts_id!=None:
            return "Personal"
        elif self.companies_id!=None:
            return "Manufactured"
        else:
            return "Rare"

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
    def fiber(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.meal_fiber()
        return r
    def grams(self):
        r=Decimal(0)
        for meal in self.arr:
            r=r+meal.meal_amount
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
        row=con.cursor_one_row("select * from biometrics where users_id=%s order by datetime desc limit 1",(self.id,))
        self.height=row['height']
        self.weight=row['weight']
        #0 Loss weight   
        #1 Mantein widght 45H 35P 20G
        #2 Gain weight
        #self.dietwish=row['dietwish']
        # 0 TMB x 1,2: Poco o ningún ejercicio
        # 1 TMB x 1,375: Ejercicio ligero (1 a 3 días a la semana)
        # 2 TMB x 1,55: Ejercicio moderado (3 a 5 días a la semana)
        # 3 TMB x 1,72: Deportista (6 -7 días a la semana)
        # 4 TMB x 1,9: Atleta (Entrenamientos mañana y tarde)

        self.activity=row['activity']
        return self 

    ##basal metabolic rate
    def bmr(self):
        if self.activity==0:
            mult=Decimal(1.2)
        elif self.activity==1:
            mult=Decimal(1.375)
        elif self.activity==2:
            mult=Decimal(1.55)
        elif self.activity==3:
            mult=Decimal(1.72)
        elif self.activity==4:
            mult=Decimal(1.9)

        if self.male==True:
            return mult*(Decimal(10)*self.weight + Decimal(6.25)*self.height - Decimal(5)*self.age() + 5)
        else: #female
            return mult*(Decimal(10)*self.weight + Decimal(6.25)*self.height - Decimal(5)*self.age() - 161)

    ##    https://www.healthline.com/nutrition/how-much-protein-per-day#average-needs
    ## If you’re at a healthy weight, don't lift weights and don't exercise much, then aiming for 0.36–0.6 grams per pound (0.8–1.3 gram per kg) is a reasonable estimate.
    ##
    ##This amounts to:
    ##
    ##56–91 grams per day for the average male.
    ##46–75 grams per day for the average female.
    ##
    ## But given that there is no evidence of harm and a significant evidence of benefit, it’s likely better for most people to err on the side of more protein rather than less.
    def protein(self):
        return self.bmr()*Decimal(0.175)/Decimal(4)


    ## The Mediterranean diet includes a wide variety of plant and animal foods such as fish, meat, eggs, dairy, extra virgin olive oil, fruits, vegetables, legumes and whole grains.
    ## 
    ## It typically provides 35–40% of calories from fat, including plenty of monounsaturated fat from olive oil.
    ##
    ## Here are a few examples of suggested daily fat ranges for a Mediterranean diet, based on different calorie goals:
    ##
    ##     1,500 calories: About 58–67 grams of fat per day.
    ##     2,000 calories: About 78–89 grams of fat per day.
    ##     2,500 calories: About 97–111 grams of fat per day.
    ## Segun https://www.tuasaude.com/es/calorias-de-los-alimentos/ cada gramo grasa tiene 9 calorias
    ## 60% hidratos, 17.5% proteínas y 22.5% de grasas. SERA SELECCIONABLE
    def fat(self):
        return self.bmr()*Decimal(0.225)/Decimal(9)

    def carbohydrate(self):
        return self.bmr()*Decimal(0.60)/Decimal(4)


    def fiber(self):
        return Decimal(25)

    def age(self):
        return (date.today() - self.birthday) // timedelta(days=365.2425)

class Product:
    def __init__(self):
        pass
    
    def init__row(self):
        pass
## amount2string
def a2s(amount):
    return str(round(amount, 2)).rjust(7)

def ca2s(amount,limit):
    if amount <= limit:
        return Fore.GREEN + a2s(amount) + Fore.RESET
    else:
        return Fore.RED + a2s(amount) + Style.RESET_ALL
## None2string
def n2s():
    return str("").rjust(7)


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
group.add_argument('--users_id', help=_('User id'), action="store", default=1)
args=parser.parse_args()

con=Connection()
con.user=args.user
con.server=args.server
con.port=args.port
con.db=args.db
con.get_password()
con.connect()

args.date=string2date(args.date)
args.users_id=int(args.users_id)

user=User().init__from_db(args.users_id)

meals=Meals().init__from_db(con.mogrify("""
select
    products.personalproducts_id,
    products.companies_id,
    products.calories,
    products.name,
    products.fat,
    products.protein,
    products.carbohydrate,
    products.amount as p_amount,
    products.salt,
    products.fiber,
    meals.amount as m_amount,
    meals.datetime 
from 
    meals, 
    products 
where products.id=meals.products_id and datetime::date=%s and users_id=%s order by datetime""",(args.date, args.users_id)))

con.disconnect()

maxname=meals.max_name_len()
if maxname<17:#For empty tables totals
    maxname=17
maxlength=5+2+maxname+2+7+2+7+2+7+2+7+2+7+2+7

print (Style.BRIGHT+ "="*(maxlength) + Style.RESET_ALL)
print (Style.BRIGHT+ "{} NUTRICIONAL REPORT AT {}".format(user.name.upper(), args.date).center(maxlength," ") + Style.RESET_ALL)
print (Style.BRIGHT+ Fore.YELLOW + "{} Kg. {} cm. {} years".format(user.weight, user.height, user.age()).center(maxlength," ") + Style.RESET_ALL)
print (Style.BRIGHT+ "="*(maxlength) + Style.RESET_ALL)

print (Style.BRIGHT+ "{}  {}  {}  {}  {}  {}  {}  {}".format("HOUR ","NAME".ljust(maxname," "),"GRAMS".rjust(7,' '), "CALORIE".rjust(7,' '), "CARBOHY".rjust(7,' '), "PROTEIN".rjust(7,' '), "FAT".rjust(7,' '), "FIBER".rjust(7,' ')) + Style.RESET_ALL)
for meal in meals.arr:
    print ( "{}  {}  {}  {}  {}  {}  {}  {}".format(meal.meal_hour(), meal.name.ljust(maxname), a2s(meal.meal_amount),a2s(meal.meal_calories()), a2s(meal.meal_carbohydrate()), a2s(meal.meal_protein()), a2s(meal.meal_fat()),a2s(meal.meal_fiber())) + Style.RESET_ALL)

print (Style.BRIGHT+ "-"*(maxlength) + Style.RESET_ALL)
total="{} MEALS WITH THIS TOTALS".format(meals.length())
print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(total.ljust(maxname+7), a2s(meals.grams()), ca2s(meals.calories(),user.bmr()), ca2s(meals.carbohydrate(),user.carbohydrate()), ca2s(meals.protein(), user.protein()), ca2s(meals.fat(),user.fat()), ca2s(meals.fiber(),user.fiber())) + Style.RESET_ALL)
recomendations="RECOMMENDATIONS"
print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(recomendations.ljust(maxname+7), n2s(), a2s(user.bmr()), a2s(user.carbohydrate()), a2s(user.protein()), a2s(user.fat()), a2s(user.fiber())) + Style.RESET_ALL)
print (Style.BRIGHT + "="*(maxlength) + Style.RESET_ALL)
