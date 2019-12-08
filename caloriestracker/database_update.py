from .package_resources import package_listdir, package_filename
from .datetime_functions import string2dtnaive
from sys import exit
_=str


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
            database_version=int(con.cursor_one_field("select value from public.globals where id=1"))
        else: #If database is empty
            database_version=0

        if database_version<sql:
            con.load_script(package_filename(package,  "sql/{}.sql".format(sql)))
            con.cursor_one_field("update public.globals set value=%s where id=1 returning id",(sql,))
            con.commit()
            print("  + Updated database version from {} to {}".format(database_version, sql))

    #Checks software version
    database_version=string2dtnaive(con.cursor_one_field("select value from public.globals where id=1"),"%Y%m%d%H%M")
    if software_version<database_version:
        s="Your software version '{}' is older than your database version '{}'. You must update it".format(software_version,database_version)
        if environment=="Console":
            print(s)
        elif environment=="Qt":
            from .ui.myqwidgets import qmessagebox
            qmessagebox(s)
        exit(1)
