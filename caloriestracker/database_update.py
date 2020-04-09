from .package_resources import package_listdir, package_filename
from .datetime_functions import string2dtnaive
from .casts import str2bool, list2string, string2list_of_integers, string2list_of_strings
from decimal import Decimal
from logging import debug
from sys import exit
_=str


class SettingsDB:
    def __init__(self, con):
        self.con=con

    def exists(self, name):
        """Returns true if globals is saved in database"""
        cur=self.con.cursor()
        cur.execute("select global from globals where global=%s", (name, ))
        num=cur.rowcount
        cur.close()
        if num==0:
            return False
        else:
            return True

    ## All keys values are stored as strings.
    ## Only when a key doesn't exist returns default
    ## @param default must be always a string to avoid import clases
    def value(self, name, default):
        """Search in database if not use default"""
        if self.exists(name)==False:
            return default
        else:            
            return self.con.cursor_one_field("select value from globals where global=%s", (name, ))

    def value_decimal(self, name, default):
        try:
            value=self.value(name, default)
            return Decimal(value)
        except:
            debug("I couldn't convert to Decimal {} ({})".format(value, value.__class__))

    def value_float(self, name, default):
        try:
            value=self.value(name, default)
            return float(value)
        except:
            debug("I couldn't convert to float {} ({})".format(value, value.__class__))

    def value_integer(self, name, default):
        try:
            value=self.value(name, default)
            return int(value)
        except:
            debug("I couldn't convert to int {} ({})".format(value, value.__class__))

    def value_boolean(self, name, default):
        try:
            value=self.value(name, default)
            return str2bool(value)
        except:
            debug("I couldn't convert to boolean {} ({})".format(value, value.__class__))

    ## Example: self.value_datetime_naive("Version", "197001010000", "%Y%m%d%H%M")
    def value_datetime_naive(self, name, default, format):
        try:
            value=self.value(name, default)
            return string2dtnaive(value, format)
        except:
            debug("I couldn't convert to datetime naive {} ({})".format(value, value.__class__))

    def value_list(self, name, default):
        try:
            value=self.value(name, default)
            return string2list_of_strings(value)
        except:
            debug("I couldn't convert to list of strings {} ({})".format(value, value.__class__))

    def value_list_of_integers(self, name, default):
        try:
            value=self.value(name, default)
            return string2list_of_integers(value)
        except:
            debug("I couldn't convert to list of integers {} ({})".format(value, value.__class__))

    ## All values are stored as string in database. This class makes automatic conversions, so value can be:
    ## - String. You can recover it with self.value
    ## - Integer. You can recover it with self.value_int
    ## - List. If it's a list of strings you can recover it with self.value_list. If it's a list of integers you can recovert it with self.value_list_of_integers
    def setValue(self, name, value):
        if isinstance(value, list):
            value=list2string(value)

        if self.exists(name)==False:
            self.con.execute("insert into globals (global,value) values(%s,%s)", (name, value))
        else:
            self.con.execute("update globals set value=%s where global=%s", (value, name))
        self.con.commit()

#    def need_update(self):
#        """Returns a tuple (boolean, problem) if update must be done
#        None, returns a problem
#        True needs to update
#        False doesn't need to update"""
#        
#        ## id_globals column exists in globals table old ssystem. So column id in globals is for new system (See old system last step)
#        
#        cur=self.con.cursor()
#        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='globals' and column_name='id'")
#        cur.close()
#        if cur.rowcount==1: #Exists id column so is new system
#            print ("Database update new system")
#            database_update(self.con, "xulpymoney", __versiondatetime__, self.mode)
#            return   


## @param con Connection object
## @param package string with the name of the package where sql directory is
## @param software_version Datetime naive with the software version
## @param environment can be "Qt","Console"
def database_update(con, package, software_version, environment="Console"):
    sqls=[]
    for name in package_listdir(package, 'sql'):
        if name[-3:]=="sql":
            sqls.append(int(name[:-4]))
    sqls.sort()

    for sql in sqls:
        globals_exists=con.cursor_one_field("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'globals');")
        if globals_exists==True:
            database_version=int(con.cursor_one_field("select value from public.globals where global='Version'"))
        else: #If database is empty
            database_version=0

        if database_version<sql:
            con.load_script(package_filename(package,  "sql/{}.sql".format(sql)))
            con.cursor_one_field("update public.globals set value=%s where global='Version' returning global",(sql,))
            con.commit()
            print("  + Updated database version from {} to {}".format(database_version, sql))

    #Checks software version
    database_version=string2dtnaive(con.cursor_one_field("select value from public.globals where global='Version'"),"%Y%m%d%H%M")
    if software_version<database_version:
        s="Your software version '{}' is older than your database version '{}'. You must update it".format(software_version,database_version)
        if environment=="Console":
            print(s)
        elif environment=="Qt":
            from .ui.myqwidgets import qmessagebox
            qmessagebox(s)
        exit(1)
