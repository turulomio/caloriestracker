from argparse import ArgumentParser, RawTextHelpFormatter
from colorama import Fore, Style
from datetime import datetime, date
from caloriestracker.connection_pg import Connection, argparse_connection_arguments_group
from caloriestracker.libcaloriestracker import MemConsole, User, MealManager
from caloriestracker.libcaloriestrackerfunctions import a2s, ca2s, input_decimal, input_int, input_string, string2date, n2s
from sys import exit
_=str



def main():
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
    
    mem=MemConsole(con)

    args.date=string2date(args.date)
    args.users_id=int(args.users_id)

    if args.find!=None:
        result=[]
        rows=mem.con.cursor_rows("select products.name || ' (' || companies.name || '). #' || products.id from products, companies where products.companies_id=companies.id")
        for row in rows:
            result.append(row[0])
        rows=mem.con.cursor_rows("select products.name || '. #' || products.id from products where products.companies_id is Null")
        for row in rows:
            result.append(row[0])
        result.sort()
        for r in result:
            if r.upper().find(args.find.upper())!=-1:
                print (r)
        exit(0)

    if args.add_company==True:
        name=input_string("Name of the company: ")
        id=mem.con.cursor_one_field("insert into companies(name,starts) values (%s, now()) returning id",(name,))
        mem.con.commit()
        print("Company added with id={}".format(id))
        exit(0)
    if args.add_meal==True:
        users_id=input_int("Add a user: ",1)
        print("Selected:", mem.con.cursor_one_field("select name from users where id=%s",(users_id,)))
        products_id=input_int("Add the product id: ")
        print("Selected:", mem.con.cursor_one_field("select name from products where id=%s",(products_id,)))
        amount=input_decimal("Add the product amount: ")
        dt=input_string("Add the time: ", str(datetime.now()))
        id=mem.con.cursor_one_field("insert into meals(users_id, amount, products_id, datetime) values (%s, %s,%s,%s) returning id",(users_id,amount, products_id,dt))
        mem.con.commit()
        print("Meal added with id={}".format(id))
        exit(0)
    if args.add_product==True:
        name=input_string("Add a name: ")
        company_id=input_string("Add a company: ", "")
        if company_id=="":
            company_id=None
        else:
            company_id=int(company_id)
            print("Selected:", mem.con.cursor_one_field("select name from companies where id=%s",(company_id,)))
        amount=input_decimal("Add the product amount: ", 100)
        carbohydrate=input_decimal("Add carbohydrate amount: ",0)
        protein=input_decimal("Add protein amount: ",0)
        fat=input_decimal("Add fat amount: ",0)
        fiber=input_decimal("Add fiber amount: ",0)
        calories=input_decimal("Add calories amount: ",0)
        id=mem.con.cursor_one_field("insert into products(name, amount, fat, protein, carbohydrate, starts, calories, fiber, companies_id) values(%s, %s,%s,%s,%s,now(),%s,%s,%s) returning id",(name, amount, fat, protein, carbohydrate, calories, fiber, company_id))
        mem.con.commit()
        print("Meal added with id={}".format(id))
        exit(0)

    if args.add_biometrics==True:
        users_id=input_int("Add a user: ",1)
        print("Selected:", mem.con.cursor_one_field("select name from users where id=%s",(users_id,)))
        last_weight=mem.con.cursor_one_field("select weight from biometrics order by datetime desc limit 1")
        weight=input_decimal("Add your weight: ", last_weight)
        last_height=mem.con.cursor_one_field("select height from biometrics order by datetime desc limit 1")
        height=input_decimal("Add your height: ",last_height)
        activity=input_int("Add activity: ", 0)
        id=mem.con.cursor_one_field("insert into biometrics(users_id, height, weight, activity, datetime) values( %s, %s,%s, %s,now()) returning id",(users_id,height, weight, activity))
        mem.con.commit()
        print("Biometrics added with id={}".format(id))
        exit(0)



    user=User(mem).init__from_db(args.users_id)

    meals=MealManager(mem).init__from_db(mem.con.mogrify("select * from meals where datetime::date=%s", (args.date,))) 
    mem.con.disconnect()

    maxname=meals.max_name_len()
    if maxname<17:#For empty tables totals
        maxname=17
    maxlength=5+2+maxname+2+7+2+7+2+7+2+7+2+7+2+7

    print (Style.BRIGHT+ "="*(maxlength) + Style.RESET_ALL)
    print (Style.BRIGHT+ "{} NUTRICIONAL REPORT AT {}".format(user.name.upper(), args.date).center(maxlength," ") + Style.RESET_ALL)
    print (Style.BRIGHT+ Fore.YELLOW + "{} Kg. {} cm. {} years".format(user.weight, user.height, user.age()).center(maxlength," ") + Style.RESET_ALL)
    print (Style.BRIGHT+ Fore.BLUE + "IMC: {} ==> {}".format(round(user.imc(),2),user.imc_comment()).center(maxlength," ") + Style.RESET_ALL)
    print (Style.BRIGHT+ "="*(maxlength) + Style.RESET_ALL)

    print (Style.BRIGHT+ "{}  {}  {}  {}  {}  {}  {}  {}".format("HOUR ","NAME".ljust(maxname," "),"GRAMS".rjust(7,' '), "CALORIE".rjust(7,' '), "CARBOHY".rjust(7,' '), "PROTEIN".rjust(7,' '), "FAT".rjust(7,' '), "FIBER".rjust(7,' ')) + Style.RESET_ALL)
    for meal in meals.arr:
        print ( "{}  {}  {}  {}  {}  {}  {}  {}".format(meal.meal_hour(), meal.fullName().ljust(maxname), a2s(meal.amount),a2s(meal.calories()), a2s(meal.carbohydrate()), a2s(meal.protein()), a2s(meal.fat()),a2s(meal.fiber())) + Style.RESET_ALL)

    print (Style.BRIGHT+ "-"*(maxlength) + Style.RESET_ALL)
    total="{} MEALS WITH THIS TOTALS".format(meals.length())
    print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(total.ljust(maxname+7), a2s(meals.grams()), ca2s(meals.calories(),user.bmr()), ca2s(meals.carbohydrate(),user.carbohydrate()), ca2s(meals.protein(), user.protein()), ca2s(meals.fat(),user.fat()), ca2s(meals.fiber(),user.fiber())) + Style.RESET_ALL)
    recomendations="RECOMMENDATIONS"
    print (Style.BRIGHT + "{}  {}  {}  {}  {}  {}  {}".format(recomendations.ljust(maxname+7), n2s(), a2s(user.bmr()), a2s(user.carbohydrate()), a2s(user.protein()), a2s(user.fat()), a2s(user.fiber())) + Style.RESET_ALL)
    print (Style.BRIGHT + "="*(maxlength) + Style.RESET_ALL)
