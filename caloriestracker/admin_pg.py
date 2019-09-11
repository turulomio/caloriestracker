## @brief Package to manage postgresql admin functionss
## THIS IS FROM XULPYMONEY PACKAGE IF YOU NEED THIS MODULE PLEASE SYNC IT FROM THERE, FOR EXAMPLE
## @code
##       print ("Copying admin_pg.py from Xulpymoney project")
##        os.chdir("your directory)
##        os.remove("admin_pg.py")
##        os.system("wget https://raw.githubusercontent.com/Turulomio/xulpymoney/master/xulpymoney/admin_pg.py  --no-clobber")
##        os.system("sed -i -e '3i ## THIS FILE HAS BEEN DOWNLOADED AT {} FROM https://github.com/Turulomio/xulpymoney/xulpymoney/admin_pg.py.' admin_pg.py".format(datetime.datetime.now()))
## @encode

import io
import logging
from .connection_pg import Connection

class AdminPG:
    def __init__(self, user, password, server, port):
        """connection is an object Connection to a database"""
        self.con=Connection().init__create(user, password, server, port, "postgres")
        self.con.connect()
        self.con.setAutocommit(True)

    def create_db(self, database):
        """It has database parameter, due to I connect to template to create database"""
        if self.con.is_superuser():
            cur=self.con.cursor()
            cur.execute("create database {0};".format(database))
        else:
            logging.critical ("You need to be superuser to create database")
            return False
        
        
    def db_exists(self, database):
        """Hace conexi´on automatica a template usando la con """
        cur=self.con.cursor()
        cur.execute("SELECT 1 AS result FROM pg_database WHERE datname=%s", (database, ))
        
        if cur.rowcount==1:
            cur.close()
            return True
        cur.close()
        return False

    def drop_db(self, database):
        """It has database parameter, due to I connect to template to drop database"""
        
        if self.db_exists(database)==False:
            logging.info("Database doesn't exist")
            return True
        
        if self.con.is_superuser():
            try:
                cur=self.cursor()
                cur.execute("drop database {0};".format(database))
            except:
                logging.error ("Error in drop()")
            finally:
                cur.close()
                return False
            logging.info("Database droped")
            return True
        else:
            logging.warning ("You need to be superuser to drop a database")
            return False
        

        
    ## Returns a Connection object to a database using Admin connection information
    def connect_to_database(self, database):
        con=Connection().init__create(self.con.user, self.con.password, self.con.server, self.con.port, database)
        con.connect()
        return con
        
    ## Used to copy between tables, and sql to table_destiny, table origin and destiny must have the same structure
    def copy(self, con_origin, con_destiny, sql_origin,  table_destiny , schema="public."):
        if sql_origin.__class__==bytes:
            sql_origin=sql_origin.decode('UTF-8')
        f=io.StringIO()
        cur_origin=con_origin.cursor()
        cur_origin.copy_expert("copy ({}) to stdout".format(sql_origin), f)
        cur_origin.close()
        f.seek(0)
        cur_destiny=con_destiny.cursor()
        cur_destiny.copy_from(f, schema + table_destiny)
        cur_destiny.close()
        f.close()
