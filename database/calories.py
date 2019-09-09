from argparse import ArgumentParser, RawTextHelpFormatter
from colorama import Fore, Style
from connection_pg import Connection, argparse_connection_arguments_group
from datetime import datetime, date, timedelta
from decimal import Decimal
from glob import glob
from libmanagers import ObjectManager_With_IdDatetime
from sys import exit
_=str

class Meal:
    def __init__(self):
        pass
    def init__from_row(self,row):
        self.id=row['id']
        self.companies_id=row['companies_id']
        if self.companies_id!=None:
            self.companies_name=con.cursor_one_field("select name from companies where id=%s",(self.companies_id,))
        self.datetime=row['datetime']
        self._name=row['name']
        self.product_calories=row['calories']
        self.product_fat=row['fat']
        self.product_protein=row['protein']
        self.product_amount=row['p_amount']
        self.product_carbohydrate=row['carbohydrate']
        self.product_salt=row['salt']
        self.product_fiber=row['fiber']
        self.meal_amount=row['m_amount']
        self.personalproducts_id=row['personalproducts_id']
        return self

    def name(self):
        if self.companies_id==None:
            return "{}".format(self._name)
        else:
            return "{} ({})".format(self._name, self.companies_name)

    def __repr__(self):
        return "{}. #{}".format(self.name(),self.id)

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
            if len(meal.name())>r:
                r=len(meal.name())
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
        return Fore.RED + a2s(amount) + Fore.RESET
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



parser=ArgumentParser(prog='calories', description=_('Report of calories'), epilog=_("Developed by Mariano Muñoz 2012-{}".format(datetime.now().year)), formatter_class=RawTextHelpFormatter)
argparse_connection_arguments_group(parser, default_db="caloriestracker")
group = parser.add_argument_group("productrequired=True")
group.add_argument('--date', help=_('Date to show'), action="store", default=str(date.today()))
group.add_argument('--users_id', help=_('User id'), action="store", default=1)
group.add_argument('--find', help=_('Find data'), action="store", default=None)
group.add_argument('--add_company', help=_("Adds a company"), action="store_true", default=False)
group.add_argument('--add_product', help=_("Adds a product"), action="store_true", default=False)
group.add_argument('--add_meal', help=_("Adds a company"), action="store_true", default=False)
group.add_argument('--add_biometrics', help=_("Adds biometrics"), action="store_true", default=False)

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

if args.find!=None:
    result=[]
    rows=con.cursor_rows("select products.name || ' (' || companies.name || '). #' || products.id from products, companies where products.companies_id=companies.id")
    for row in rows:
        result.append(row[0])
    rows=con.cursor_rows("select products.name || '. #' || products.id from products where products.companies_id is Null")
    for row in rows:
        result.append(row[0])
    result.sort()
    for r in result:
        if r.upper().find(args.find.upper())!=-1:
            print (r)
    exit(0)

if args.add_company==True:
    name=input_string("Name of the company: ")
    id=con.cursor_one_field("insert into companies(name,starts) values (%s, now()) returning id",(name,))
    con.commit()
    print("Company added with id={}".format(id))
    exit(0)
if args.add_meal==True:
    users_id=input_int("Add a user: ",1)
    print("Selected:", con.cursor_one_field("select name from users where id=%s",(users_id,)))
    products_id=input_int("Add the product id: ")
    print("Selected:", con.cursor_one_field("select name from products where id=%s",(products_id,)))
    amount=input_decimal("Add the product amount: ")
    dt=input_string("Add the time: ", str(datetime.now()))
    id=con.cursor_one_field("insert into meals(users_id, amount, products_id, datetime) values (%s, %s,%s,%s) returning id",(users_id,amount, products_id,dt))
    con.commit()
    print("Meal added with id={}".format(id))
    exit(0)
if args.add_product==True:
    name=input_string("Add a name: ")
    company_id=input_string("Add a company: ", "")
    if company_id=="":
        company_id=None
    else:
        company_id=int(company_id)
        print("Selected:", con.cursor_one_field("select name from companies where id=%s",(company_id,)))
    amount=input_decimal("Add the product amount: ", 100)
    carbohydrate=input_decimal("Add carbohydrate amount: ",0)
    protein=input_decimal("Add protein amount: ",0)
    fat=input_decimal("Add fat amount: ",0)
    fiber=input_decimal("Add fiber amount: ",0)
    calories=input_decimal("Add calories amount: ",0)
    id=con.cursor_one_field("insert into products(name, amount, fat, protein, carbohydrate, starts, calories, fiber, companies_id) values(%s, %s,%s,%s,%s,now(),%s,%s,%s) returning id",(name, amount, fat, protein, carbohydrate, calories, fiber, company_id))
    con.commit()
    print("Meal added with id={}".format(id))
    exit(0)

if args.add_biometrics==True:
    users_id=input_int("Add a user: ",1)
    print("Selected:", con.cursor_one_field("select name from users where id=%s",(users_id,)))
    last_weight=con.cursor_one_field("select weight from biometrics order by datetime desc limit 1")
    weight=input_decimal("Add your weight: ", last_weight)
    last_height=con.cursor_one_field("select height from biometrics order by datetime desc limit 1")
    height=input_decimal("Add your height: ",last_height)
    activity=input_int("Add activity: ", 0)
    id=con.cursor_one_field("insert into biometrics(users_id, height, weight, activity, datetime) values( %s, %s,%s, %s,now()) returning id",(users_id,height, weight, activity))
    con.commit()
    print("Biometrics added with id={}".format(id))
    exit(0)



user=User().init__from_db(args.users_id)

meals=Meals().init__from_db(con.mogrify("""
select
    products.id,
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
    print ( "{}  {}  {}  {}  {}  {}  {}  {}".format(meal.meal_hour(), meal.name().ljust(maxname), a2s(meal.meal_amount),a2s(meal.meal_calories()), a2s(meal.meal_carbohydrate()), a2s(meal.meal_protein()), a2s(meal.meal_fat()),a2s(meal.meal_fiber())) + Style.RESET_ALL)

print (Style.BRIGHT+ "-"*(maxlength) + Style.RESET_ALL)
total="{} MEALS WITH THIS TOTALS".format(meals.length())
print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(total.ljust(maxname+7), a2s(meals.grams()), ca2s(meals.calories(),user.bmr()), ca2s(meals.carbohydrate(),user.carbohydrate()), ca2s(meals.protein(), user.protein()), ca2s(meals.fat(),user.fat()), ca2s(meals.fiber(),user.fiber())) + Style.RESET_ALL)
recomendations="RECOMMENDATIONS"
print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(recomendations.ljust(maxname+7), n2s(), a2s(user.bmr()), a2s(user.carbohydrate()), a2s(user.protein()), a2s(user.fat()), a2s(user.fiber())) + Style.RESET_ALL)
print (Style.BRIGHT + "="*(maxlength) + Style.RESET_ALL)
