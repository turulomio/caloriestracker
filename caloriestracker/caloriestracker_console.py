from datetime import datetime
from caloriestracker.libcaloriestracker import MealManager, CompanyPersonal, Meal, ProductPersonal, CompaniesAndProducts
from caloriestracker.text_inputs import input_boolean, input_decimal, input_int, input_string
from caloriestracker.mem import MemConsole
from caloriestracker.contribution import generate_contribution_dump, parse_contribution_dump_generate_files_and_validates_them
from logging import debug
from sys import exit

def main():
    mem=MemConsole()
    mem.run()   
    debug(mem.tr("Start mem took {}".format(datetime.now()-mem.inittime)))

    if mem.args.find!=None:
        cp=CompaniesAndProducts(mem)
        cp.find_report(mem.args.find)
        exit(0)

    if mem.args.add_company==True:
        name=input_string("Name of the company: ")
        o=CompanyPersonal(mem, name, datetime.now(), None, None)
        o.save()
        mem.con.commit()
        print("CompanySystem added with id={}".format(o.id))
        exit(0)
    if mem.args.elaborated!=None:
       elaborated=mem.data.elaboratedproducts.find_by_id(mem.args.elaborated)
       elaborated.load_products_in()
       elaborated.show_table()
       exit(0)
    if mem.args.add_meal==True:
        users_id=input_int("Add a user: ",1)
        user=mem.data.users.find_by_id(users_id)
        print("Selected:", mem.con.cursor_one_field("select name from users where id=%s",(users_id,)))
        products_id=input_int("Add the product id")
        system=input_boolean("It's a system product?", "T")
        product=mem.data.products.find_by_id_system(products_id, system)
        print("Selected:",  product)
        amount=input_decimal("Add the product amount: ")
        dt=input_string("Add the time: ", str(datetime.now()))
        o=Meal(mem, dt, product, amount, user, product.system_product, None)
        o.save()
        mem.con.commit()
        print("Meal added with id={}".format(o.id))
        exit(0)
    if mem.args.add_product==True:
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

    if mem.args.add_biometrics==True:
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

    if mem.args.contribution_dump==True:
        generate_contribution_dump(mem)
        exit(0)
    
    if mem.args.parse_contribution_dump!=None:
        print(mem.args)
        parse_contribution_dump_generate_files_and_validates_them(mem.con, mem.args.parse_contribution_dump)
        exit(0)
        
    if mem.args.update_after_contribution!=None:
        mem.con.load_script(mem.args.update_after_contribution)
        mem.con.commit()
        exit(0)

    user=mem.data.users.find_by_id(mem.args.users_id)

    meals=MealManager(mem, mem.con.mogrify("select * from meals where datetime::date=%s and users_id=%s", (mem.args.date, user.id))) 
    meals.order_by_datetime()
    meals.show_table(mem.args.date)
