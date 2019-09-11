from pkg_resources import resource_listdir, resource_filename
_=str

def database_update(con):
    sqls=[]
    for name in resource_listdir('caloriestracker', 'sql'):
        if name[-3:]=="sql":
            sqls.append(int(name[:-4]))
    sqls.sort()

    for sql in sqls:
        globals_exists=con.cursor_one_field("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'globals');")
        if globals_exists==True:
            database_version=int(con.cursor_one_field("select value from globals where id=1"))
        else: #If database is empty
            database_version=0

        if database_version<sql:
            con.load_script(resource_filename('caloriestracker',  "sql/{}.sql".format(sql)))
            con.cursor_one_field("update globals set value=%s where id=1 returning id",(sql,))
            con.commit()
            print("  + Updated database version from {} to {}".format(database_version, sql))
