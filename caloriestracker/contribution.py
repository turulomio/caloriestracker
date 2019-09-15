from caloriestracker.mem import MemConsole
from caloriestracker.libcaloriestracker import Product, CompanySystem
from caloriestracker.text_inputs import input_YN
from colorama import Style, Fore


def generate_contribution_dump(mem):
    database_version=int(mem.con.cursor_one_field("select value from globals where id=1"))
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


def generate_files_from_personal_data(datestr, newcon):
    package_sql_filename="mal{}.sql".format(datestr)        
    package_sql=open(package_sql_filename, "w")
    mem=MemConsole(newcon)
    new_system_companies_id=newcon.cursor_one_field("select max(id)+1 from companies")
    new_system_products_id=newcon.cursor_one_field("select max(id)+1 from products")
    for company in mem.data.companies.arr:
        if company.system_company==False:
            question=input_YN("Do you want to convert this company '{}' to a system one?".format(company), "Y")
            if question==True:
                system_company=CompanySystem(mem, company.name, company.starts, company.ends, new_system_companies_id)
                new_system_companies_id=new_system_companies_id+1
                package_sql.write(system_company.insert_string("companies").decode('UTF-8') + ";\n")
    for product in mem.data.products.arr:
        if product.system_product==False:
            question=input_YN("Do you want to convert this product '{}' to a system one?".format(product.fullName(True)), "Y")
            if question==True:
                system_product=Product(
                    mem, 
                    product.name, 
                    product.amount, 
                    product.fat, 
                    product.protein, 
                    product.carbohydrate, 
                    product.company, 
                    product.ends, 
                    product.starts, 
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
                    product.system_company,  
                    new_system_products_id)
                new_system_products_id=new_system_products_id+1
                print("company mal")
                package_sql.write(system_product.insert_string("products").decode('UTF-8') + ";\n")
    package_sql.close()
