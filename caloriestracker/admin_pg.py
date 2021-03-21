## @brief Package to manage postgresql admin functionss
## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

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
            return True
        else:
            logging.critical ("You need to be superuser to create database")
            return False
        
    #Creates a new database and return conexion to new database
    def create_new_database_and_return_new_conexion(self,  database):
        if self.db_exists(database)==True:
            print("Database exists")
            exit(1)
        self.create_db(database)
        return self.connect_to_database(database)

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
                cur=self.con.cursor()
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
    def connect_to_database(self, database, connectionqt=False):
        if connectionqt is False:
            con=Connection().init__create(self.con.user, self.con.password, self.con.server, self.con.port, database)
            con.connect()
        else:
            from .connection_pg_qt import ConnectionQt
            con=ConnectionQt().init__create(self.con.user, self.con.password, self.con.server, self.con.port, database)
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
