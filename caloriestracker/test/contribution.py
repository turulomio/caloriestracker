from PyQt5.QtCore import  QCoreApplication
import unittest
from caloriestracker.admin_pg import AdminPG
from caloriestracker.database_update import database_update
from caloriestracker.mem import MemConsole
from caloriestracker.libcaloriestracker import CompanyPersonal
from datetime import datetime
from os import environ
from sys import argv

class TestCollaborationProcess(unittest.TestCase):
    def testCollaborationProcess(self):
        mem=MemConsole()
#        self.args=self.parse_arguments()
#        self.addDebugSystem(self.args.debug) #Must be before QCoreApplication
        mem.app=QCoreApplication(argv)
        mem.app.setOrganizationName("caloriestracker")
        mem.app.setOrganizationDomain("caloriestracker")
        mem.app.setApplicationName("caloriestracker")
        mem.load_translation()
        
        database="caloriestracker_test"
        admin=AdminPG("postgres", environ['PGPASSWORD'], "127.0.0.1", "5432")
        admin.drop_db(database)
        mem.con=admin.create_new_database_and_return_new_conexion(database)
        database_update(mem.con)
        mem.load_db_data(False)
        mem.user=mem.data.users.find_by_id(1)
        c1=CompanyPersonal(mem, "CompanyPersonal1", datetime.now(), None)
        c1.save()
        
#        newcon.load_script(mem.args.parse_contribution_dump)
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
