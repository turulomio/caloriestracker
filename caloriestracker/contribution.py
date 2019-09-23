from caloriestracker.datetime_functions import dtnaive2string
from caloriestracker.libcaloriestracker import Product, CompanySystem, CompanySystemManager, ProductManager, Format
from caloriestracker.libcaloriestrackerfunctions import b2s
from caloriestracker.admin_pg import AdminPG
from caloriestracker.database_update import database_update
from caloriestracker.text_inputs import input_YN, input_string
from colorama import Style, Fore
from datetime import datetime
from os import system

def print_table_status(con):
    personalproducts=con.cursor_one_field("select count(*) from personalproducts")
    products=con.cursor_one_field("select count(*) from products")
    companies=con.cursor_one_field("select count(*) from companies")
    formats=con.cursor_one_field("select count(*) from formats")
    return (companies, products, personalproducts, formats)

## Generate a dump for the collaborator
## @param mem Current database to extract personal data only
def generate_contribution_dump(mem):
    database_version=int(mem.con.cursor_one_field("select value from globals where id=1"))
    filename="caloriestracker_collaboration_{}.sql".format(database_version)
    f=open(filename, "w")
    f.write("select;\n")#For no personal data empty files
    for company in mem.data.companies.arr:
        if company.system_company==False:
            f.write(company.insert_string("personalcompanies") + ";\n")
    for product in mem.data.products.arr:
        product.needStatus(1)
        if product.system_product==False and product.elaboratedproducts_id==None:
            f.write(product.insert_string("personalproducts") + ";\n")
            for format in product.formats.arr:
                f.write(format.insert_string("personalformats") + ";\n")
    f.close()
    print(Style.BRIGHT + Fore.GREEN + "Generated '{}'. Please send to '' without rename it".format(filename)+ Style.RESET_ALL)
    return filename

## Parses generated dump of the collborator. 
## 1. Uses mem.con to generate a new conexión an database
## 2. Load personal data from collaborator
## 3. Generates files to pass personal data to system data
## 4. Tries generated files and shows results

## auxiliar_con, it's only used to generate admin and new connection with same parameters, but it's not used
def parse_contribution_dump(auxiliar_con, contribution_dump):
        datestr=dtnaive2string(datetime.now(), 3).replace(" ", "")
        database="caloriestracker"+datestr
        admin=AdminPG(auxiliar_con.user, auxiliar_con.password, auxiliar_con.server, auxiliar_con.port)
        newcon=admin.create_new_database_and_return_new_conexion(database)
        database_update(newcon)        
        print ("1. After setting database to default",  *print_table_status(newcon))
        
        newcon.load_script(contribution_dump)
        newcon.commit()
        print ("2. After loading personal data from collaborator",  *print_table_status(newcon))
        
        new_database_generates_files_from_personal_data(datestr, newcon)
        print ("3. After generating files collaboration. Emulates launching update_table",  *print_table_status(newcon))

        newcon.load_script("XXXXXXXXXXXX.sql")
        print ("4. After trying XXXXXXXXXXXX.sql",  *print_table_status(newcon))
        
        newcon.load_script("XXXXXXXXXXXX_version_needed_update_first_in_github.sql")
        print("5. After updating collaborator database", *print_table_status(newcon))
       
        newcon.commit()
        newcon.disconnect()
        input_string("Press ENTER to delete database: " + database)
        admin.drop_db(database)
        
        question=input_YN("Do you want to add {}.sql to caloriestracker/sql/?".format(datestr),  "?")
        if question==True:
            system("mv XXXXXXXXXXXX.sql caloriestracker/sql/{}.sql".format(datestr))
            system("mv XXXXXXXXXXXX_version_needed_update_first_in_github.sql {}_version_needed_update_first_in_github.sql".format(datestr))

## With th new database generate files to convert local to string, asking wich one
def new_database_generates_files_from_personal_data(datestr, mem, args):   
    ## GENERATING XXXXXXXXXXXX.sql
    package_sql_filename="XXXXXXXXXXXX.sql".format(datestr)        
    package_sql=open(package_sql_filename, "w")
    package_sql.write("select;\n")#For no personal data empty files

    companies_map={}
    products_map={}
    formats_map={}
    
    #companies
    new_system_companies_id=mem.con.cursor_one_field("select max(id)+1 from companies")
    new_system_companies=CompanySystemManager(mem)
    for company in mem.data.companies.arr:
        if company.system_company==False:
            question=input_YN("Do you want to convert this company '{}' to a system one?".format(company), "Y")
            if question==True:
                system_company=CompanySystem(mem, company.name, company.last, new_system_companies_id)
                new_system_companies.append(system_company)
                companies_map[company.string_id()]=system_company.string_id()
                new_system_companies_id=new_system_companies_id+1
                package_sql.write(system_company.insert_string("companies")+ ";\n")
                mem.data.companies.append(system_company) ##Appends new sistem company to mem.data
                #print ("Company will change from {} to {}".format(company.string_id(), system_company.string_id()))

    #products
    new_system_products_id=mem.con.cursor_one_field("select max(id)+1 from products")
    new_system_products=ProductManager(mem)
    for product in mem.data.products.arr: 
        if product.system_product==False:
            question=input_YN("Do you want to convert this product '{}' to a system one?".format(product.fullName()), "Y")
            #Selects a company
            if product.company!=None:
                if product.system_company==False:
                    company=mem.data.companies.find_by_id_system(*CompanySystem.string_id2tuple(companies_map[product.company.string_id()]))
                else:
                    company=product.company
                system_company=True
            else:
                company=None
                system_company=None
            #Create product
            if question==True:
                system_product=Product(
                    mem, 
                    product.name, 
                    product.amount, 
                    product.fat, 
                    product.protein, 
                    product.carbohydrate, 
                    company, 
                    product.last,
                    product.elaboratedproducts_id, 
                    product.languages, 
                    product.calories, 
                    product.salt, 
                    product.cholesterol, 
                    product.sodium, 
                    product.potassium, 
                    product.fiber, 
                    product.sugars, 
                    product.saturated_fat, 
                    system_company,  
                    new_system_products_id)
                new_system_products.append(system_product)
                products_map[product.string_id()]=system_product.string_id()
                new_system_products_id=new_system_products_id+1
                #print ("Product will change from {} to {}".format(product, system_product))
                #if company!=None:
                #    print ("Its company will change from {} to {}".format(product.company.string_id(), company.string_id()))
                package_sql.write(system_product.insert_string("products") + ";\n")
    
    #formats
    new_system_formats_id=mem.con.cursor_one_field("select max(id)+1 from formats")
    for product in mem.data.products.arr:
        if product.system_product==False:
            product.needStatus(1)
            if product.formats.length()==0:
                continue
            for format in product.formats.arr:
                question=input_YN("Do you want to convert this format '{}' to a system one?".format(format), "Y")
                if question==True:
                    system_product=new_system_products.find_by_string_id(products_map[format.product.string_id()])#Recently created in systemproducts
                    system_format=Format(mem, format.name, system_product, system_product.system_product, format.amount, format.last, new_system_formats_id)
                    system_product.needStatus(1)#Creates empty format manager
                    system_product.formats.append(system_format)
                    formats_map[format.string_id()]=system_format.string_id()
                    new_system_formats_id=new_system_formats_id+1
                    package_sql.write(system_format.insert_string("formats")+ ";\n")
                    mem.data.formats.append(system_format) ##Appends new sistem format to mem.data
                    #print ("Format will change from {} to {}".format(format.string_id(), system_format.string_id()))

    package_sql.close()
    
    ## GENERATING COLLABORATION UPDATE FOR COLLABORATOR
    return_sql_filename="XXXXXXXXXXXX_version_needed_update_first_in_github.sql"  
    return_sql=open(return_sql_filename, "w")
    return_sql.write("select;\n")#For no personal data empty files
    #COMPANIES
    for origin, destiny in companies_map.items():#k,v strings_id
        origin_personal_company=mem.data.companies.find_by_string_id(origin)
        #destiny_system_company=new_system_companies.find_by_string_id(destiny)
        #Delete old personal companies
        return_sql.write("-- " + origin_personal_company.fullName() + "\n")
        return_sql.write("delete from personalcompanies where id=" + str(origin_personal_company.id) + ";\n")
        return_sql.write("\n")
        
    #PRODUCTS
    for origin, destiny in products_map.items():
        origin_personal_product=ProductManager.find_by_string_id(mem.data.products, origin)
        destiny_system_product=ProductManager.find_by_string_id(new_system_products, destiny)
        #Delete old personal products
        return_sql.write("-- " + origin_personal_product.fullName() + "\n")
        return_sql.write(b2s(mem.con.mogrify("delete from personalproducts where id=%s;", (origin_personal_product.id, )))+"\n")
        #UPDATING PRODUCTS IN THE REST OF TABLES
        for table in ['formats', 'meals', 'products_in_elaboratedproducts']:
            return_sql.write(b2s(mem.con.mogrify("update "+table+" set products_id=%s, system_product=%s where products_id=%s and system_product=%s;", 
                (destiny_system_product.id, destiny_system_product.system_product, origin_personal_product.id, origin_personal_product.system_product)))+"\n")
        #Formats
        for format in origin_personal_product.formats.arr:
            #Delete old personal formats
            return_sql.write("-- " + origin_personal_product.fullName() +  "-" + format.name+ "\n")
            return_sql.write(b2s(mem.con.mogrify("delete from personalformats where id=%s;", (format.id, )))+"\n")

        return_sql.write("\n")
    return_sql.close()
