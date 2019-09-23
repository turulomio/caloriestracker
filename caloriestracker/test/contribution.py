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
        mem=MemConsole()
        mem.app=QCoreApplication(argv)
        mem.app.setOrganizationName("caloriestracker")
        mem.app.setOrganizationDomain("caloriestracker")
        mem.app.setApplicationName("caloriestracker")
        mem.load_translation()
        
        database="caloriestracker_test"
        admin=AdminPG("postgres", environ['PGPASSWORD'], "127.0.0.1", "5432")
        
        if admin.db_exists(database)==True:
            admin.drop_db(database)
        admin.create_db(database)
        mem.con=admin.connect_to_database(database)
        database_update(mem.con)
        mem.load_db_data(False)
        mem.user=mem.data.users.find_by_id(1)
        c1=CompanyPersonal(mem, "CompanyPersonal1", datetime.now(), None)
        c1.save()            
        p1=ProductPersonal(
            mem,
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
        p2=ProductPersonal(
            mem,
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
        
        f1=FormatPersonal(mem, "Format 1 of PersonalProduct2", p2, p2.system_product,  100,  datetime.now(), None )
        f1.save()
        f2=FormatPersonal(mem, "Format 2 of PersonalProduct2", p2, p2.system_product,  200,  datetime.now(), None )
        f2.save()
        
        m1=Meal(mem, datetime.now(), p1, 100, mem.user, p1.system_product, None)
        m1.save()
        m2=Meal(mem, datetime.now(), p2, 200, mem.user, p2.system_product, None)
        m2.save()
        
        filename_dump=generate_contribution_dump(mem)

        ##Creates other database
        parse_contribution_dump(mem, filename_dump, ['--db', 'caloriestracker_test', 'test'])


#        newcon.commit()
#        
#        new_database_generates_files_from_personal_data(datestr, newcon)
#
#        newcon.load_script("XXXXXXXXXXXX.sql")
#        
#        newcon.load_script("XXXXXXXXXXXX_version_needed_update_first_in_github.sql")
       
        mem.con.commit()
        mem.con.disconnect()
#        input_string("Press ENTER to delete database: " + database)
#        
#        generate_contribution_dump(mem)
#    
#        parse_contribution_dump(mem)
#        mem.con.load_script(mem.args.update_after_contribution)
#        mem.con.commit()

if __name__ == '__main__':
    unittest.main()
