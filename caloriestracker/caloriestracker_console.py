from argparse import ArgumentParser, RawTextHelpFormatter
from colorama import Fore, Style
from datetime import datetime, date
from caloriestracker.admin_pg import AdminPG
from caloriestracker.connection_pg import Connection, argparse_connection_arguments_group
from caloriestracker.libcaloriestracker import MemConsole,  MealManager, CompanyPersonal, Meal, ProductPersonal
from caloriestracker.libcaloriestrackerfunctions import a2s, ca2s, input_boolean, input_decimal, input_int, input_string, string2date, n2s, dtnaive2string
from caloriestracker.database_update import database_update
from signal import signal, SIGINT
from sys import exit
_=str

def signal_handler(signal, frame):
        print(Style.BRIGHT+Fore.RED+"You pressed 'Ctrl+C', exiting...")
        exit(1)

def main():
    signal(SIGINT, signal_handler)
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
    group.add_argument('--collaboration_dump', help=_("Generate a dump to collaborate updating companies and products"), action="store_true", default=False)
    group.add_argument('--parse_collaboration_dump', help=_("Parses a dump and generates sql for the package and other for the collaborator"), action="store", default=None)
    group.add_argument('--update_after_collaboration',  help=_("Converts data from personal database to system after collaboration"),  action="store_true", default=False)

    args=parser.parse_args()

    con=Connection()
    con.user=args.user
    con.server=args.server
    con.port=args.port
    con.db=args.db
    con.get_password()
    con.connect()
    
    database_update(con)
    
    mem=MemConsole(con)

    args.date=string2date(args.date)
    args.users_id=int(args.users_id)

    if args.find!=None:
        mem.data.products.order_by_name()
        
        for o in mem.data.products.arr:
            if o.fullName().upper().find(args.find.upper())!=-1:
                print (o.fullName(True))
        exit(0)

    if args.add_company==True:
        name=input_string("Name of the company: ")
        o=CompanyPersonal(mem, name, datetime.now(), None, None)
        o.save()
        mem.con.commit()
        print("CompanySystem added with id={}".format(o.id))
        exit(0)
    if args.add_meal==True:
        users_id=input_int("Add a user: ",1)
        user=mem.data.users.find_by_id(users_id)
        print("Selected:", mem.con.cursor_one_field("select name from users where id=%s",(users_id,)))
        products_id=input_int("Add the product id")
        system=input_boolean("It's a system product?", "T")
        product=mem.data.products.find_by_id_system(products_id, system)
        print("Selected:",  product)
        amount=input_decimal("Add the product amount: ")
        dt=input_string("Add the time: ", str(datetime.now()))
        o=Meal(mem, dt, product, None, amount, user, product.system_product, None)
        o.save()
        mem.con.commit()
        print("Meal added with id={}".format(o.id))
        exit(0)
    if args.add_product==True:
        name=input_string("Add a name: ")
        company=mem.data.companies.find_by_input()
        system_company=None if company==None else company.system_company
        amount=input_decimal("Add the product amount", 100)
        carbohydrate=input_decimal("Add carbohydrate amount",0)
        protein=input_decimal("Add protein amount", 0)
        fat=input_decimal("Add fat amount", 0)
        fiber=input_decimal("Add fiber amount", 0)
        calories=input_decimal("Add calories amount", 0)
        o=ProductPersonal(
            mem, 
            name, 
            amount, 
            fat, 
            protein, 
            carbohydrate, 
            company, 
            None, 
            datetime.now(), 
            None, 
            None, 
            calories, 
            None, 
            None, 
            None, 
            None, 
            fiber, 
            None, 
            None, 
            system_company,  
            None)
        o.save()
        mem.con.commit()
        print("Product added with id={}".format(o.id))
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

    if args.collaboration_dump==True:
        database_version=int(con.cursor_one_field("select value from globals where id=1"))
        filename="caloriestracker_collaboration_{}.sql".format(database_version)
        f=open(filename, "w")
        for company in mem.data.companies.arr:
            if company.system_company==False:
                f.write(company.insert_string("personalcompanies").decode('UTF-8') + ";\n")
        for product in mem.data.products.arr:
            if product.system_product==False:
                f.write(product.insert_string("personalproducts").decode('UTF-8') + ";\n")
        f.close()
        print(Style.BRIGHT + Fore.GREEN + "Generated '{}'. Please send to '' without rename it".format(filename)+ Style.RESET_ALL)
        exit(0)
    
    if args.parse_collaboration_dump!=None:
        database="caloriestracker"+dtnaive2string(datetime.now(), 3).replace(" ", "")
        
        admin=AdminPG(mem.con.user, mem.con.password, mem.con.server, mem.con.port)
        if admin.db_exists(database)==True:
            print("Database exists")
            exit(1)
            
        admin.create_db(database)
        newcon=Connection()
        newcon.user=mem.con.user
        newcon.server=mem.con.server
        newcon.port=mem.con.port
        newcon.db=database
        newcon.password=mem.con.password
        newcon.connect()
        database_update(newcon)        
        newcon.load_script(args.parse_collaboration_dump)
        newcon.commit()
        newcon.disconnect()
        input_string("Press ENTER to delete database: " + database)
        admin.drop_db(database)
        
        exit(0)
        
    if args.update_after_collaboration==True:
        exit(0)

    user=mem.data.users.find_by_id(args.users_id)
    user.load_last_biometrics()

    meals=MealManager(mem, mem.con.mogrify("select * from meals where datetime::date=%s and users_id=%s", (args.date, user.id))) 
    meals.order_by_datetime()
    mem.con.disconnect()

    maxname=meals.max_name_len()
    if maxname<17:#For empty tables totals
        maxname=17
    maxlength=5+2+maxname+2+7+2+7+2+7+2+7+2+7+2+7

    print (Style.BRIGHT+ "="*(maxlength) + Style.RESET_ALL)
    print (Style.BRIGHT+ "{} NUTRICIONAL REPORT AT {}".format(user.name.upper(), args.date).center(maxlength," ") + Style.RESET_ALL)
    print (Style.BRIGHT+ Fore.YELLOW + "{} Kg. {} cm. {} years".format(user.last_biometrics.weight, user.last_biometrics.height, user.age()).center(maxlength," ") + Style.RESET_ALL)
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
