
from datetime import datetime
from caloriestracker.contribution import generate_contribution_dump, generate_files_from_personal_data
from caloriestracker.admin_pg import AdminPG
from caloriestracker.database_update import database_update
from caloriestracker.libcaloriestracker import MemConsole, MealManager, CompanyPersonal, Meal, ProductPersonal, ProductElaborated
from caloriestracker.libcaloriestrackerfunctions import input_boolean, input_decimal, input_int, input_string, dtnaive2string
from sys import exit


def main():

    
    mem=MemConsole()
    mem.run()


    if mem.args.find!=None:
        mem.data.products.order_by_name()
        
        for o in mem.data.products.arr:
            if o.fullName().upper().find(mem.args.find.upper())!=-1:
                print (o.fullName(True))
        exit(0)

    if mem.args.add_company==True:
        name=input_string("Name of the company: ")
        o=CompanyPersonal(mem, name, datetime.now(), None, None)
        o.save()
        mem.con.commit()
        print("CompanySystem added with id={}".format(o.id))
        exit(0)
    if mem.args.elaborated!=None:
       elaborated=ProductElaborated(mem,mem.args.elaborated)
       elaborated.register_in_personal_products()
       mem.con.commit()
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
        o=Meal(mem, dt, product, None, amount, user, product.system_product, None)
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

    if mem.args.collaboration_dump==True:
        generate_contribution_dump(mem)
        exit(0)
    
    if mem.args.parse_collaboration_dump!=None:
        datestr=dtnaive2string(datetime.now(), 3).replace(" ", "")
        database="caloriestracker"+datestr
        admin=AdminPG(mem.con.user, mem.con.password, mem.con.server, mem.con.port)
        newcon=admin.create_new_database_and_return_new_conexion(mem.con, database)
        database_update(newcon)        
        newcon.load_script(mem.args.parse_collaboration_dump)
        newcon.commit()
        generate_files_from_personal_data(datestr, newcon)
        newcon.disconnect()
        input_string("Press ENTER to delete database: " + database)
        admin.drop_db(database)
        exit(0)
        
    if mem.args.update_after_collaboration==True:
        exit(0)

    user=mem.data.users.find_by_id(mem.args.users_id)
    user.load_last_biometrics()

    meals=MealManager(mem, mem.con.mogrify("select * from meals where datetime::date=%s and users_id=%s", (mem.args.date, user.id))) 
    meals.order_by_datetime()
    meals.show_table(mem.args.date)
