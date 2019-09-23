from PyQt5.QtCore import  QCoreApplication
import unittest
from caloriestracker.admin_pg import AdminPG
from caloriestracker.database_update import database_update
from caloriestracker.mem import MemConsole
from caloriestracker.libcaloriestracker import CompanyPersonal, ProductPersonal, FormatPersonal, Meal
from caloriestracker.contribution import generate_contribution_dump, parse_contribution_dump
from datetime import datetime
from os import environ
from sys import argv

class TestCollaborationProcess(unittest.TestCase):
    def testCollaborationProcess(self):
        mem_to_test=MemConsole()
        mem_to_test.app=QCoreApplication(argv)
        mem_to_test.app.setOrganizationName("caloriestracker")
        mem_to_test.app.setOrganizationDomain("caloriestracker")
        mem_to_test.app.setApplicationName("caloriestracker")
        mem_to_test.load_translation()
        
        database="caloriestracker_test"
        admin=AdminPG("postgres", environ['PGPASSWORD'], "127.0.0.1", "5432")
        
        if admin.db_exists(database)==True:
            admin.drop_db(database)
        admin.create_db(database)
        mem_to_test.con=admin.connect_to_database(database)
        database_update(mem_to_test.con)
        mem_to_test.load_db_data(False)
        mem_to_test.user=mem_to_test.data.users.find_by_id(1)
        c1=CompanyPersonal(mem_to_test, "CompanyPersonal1", datetime.now(), None)
        c1.save()            
        mem_to_test.data.companies.append(c1)
        p1=ProductPersonal(
            mem_to_test,
            "ProductPersonal1", 
            100, 
            1,
            2, 
            3,  
            None, 
            datetime.now(), 
            None, 
            None, 
            4,
            5, 
            6, 
            7, 
            8, 
            9, 
            10, 
            11, 
            False, 
            None)
        p1.save()  
        mem_to_test.data.products.append(p1)
        p2=ProductPersonal(
            mem_to_test,
            "ProductPersonal2 CompanyPersonal1", 
            100, 
            1,
            2, 
            3,  
            c1, 
            datetime.now(), 
            None, 
            None, 
            4,
            5, 
            6, 
            7, 
            8, 
            9, 
            10, 
            11, 
            False, 
            None)
        p2.save()
        mem_to_test.data.products.append(p2)
        p1.needStatus(1)
        p2.needStatus(1)
        
        f1=FormatPersonal(mem_to_test, "Format 1 of PersonalProduct2", p2, p2.system_product,  100,  datetime.now(), None )
        f1.save()
        p2.formats.append(f1)
        f2=FormatPersonal(mem_to_test, "Format 2 of PersonalProduct2", p2, p2.system_product,  200,  datetime.now(), None )
        f2.save()
        p2.formats.append(f2)
        
        m1=Meal(mem_to_test, datetime.now(), p1, 100, mem_to_test.user, p1.system_product, None)
        m1.save()
        m2=Meal(mem_to_test, datetime.now(), p2, 200, mem_to_test.user, p2.system_product, None)
        m2.save()
        mem_to_test.con.commit()
        
        filename_dump=generate_contribution_dump(mem_to_test)

        ##Creates other database
        parse_contribution_dump(mem_to_test.con, filename_dump)


#        newcon.commit()
#        
#        new_database_generates_files_from_personal_data(datestr, newcon)
#
#        newcon.load_script("XXXXXXXXXXXX.sql")
#        
#        newcon.load_script("XXXXXXXXXXXX_version_needed_update_first_in_github.sql")
       
        mem_to_test.con.disconnect()
#        input_string("Press ENTER to delete database: " + database)
#        
#        generate_contribution_dump(mem)
#    
#        parse_contribution_dump(mem)
#        mem.con.load_script(mem.args.update_after_contribution)
#        mem.con.commit()

if __name__ == '__main__':
    unittest.main()
