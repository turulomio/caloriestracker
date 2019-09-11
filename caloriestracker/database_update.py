from argparse import ArgumentParser, RawTextHelpFormatter
from connection_pg import Connection, argparse_connection_arguments_group
from datetime import datetime
from glob import glob
_=str


parser=ArgumentParser(prog='database_update', description=_('Updates database schema and static content'), epilog=_("Developed by Mariano Muñoz 2012-{}".format(datetime.now().year)), formatter_class=RawTextHelpFormatter)
argparse_connection_arguments_group(parser, default_db="caloriestracker")
args=parser.parse_args()

con=Connection()
con.user=args.user
con.server=args.server
con.port=args.port
con.db=args.db
con.get_password()
con.connect()

sqls=[]
for name in glob('*.sql'):
    sqls.append(int(name[:-4]))
sqls.sort()

for sql in sqls:
    globals_exists=con.cursor_one_field("SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'globals');")
    if globals_exists==True:
        database_version=int(con.cursor_one_field("select value from globals where id=1"))
    else: #If database is empty
        database_version=0

    if database_version<sql:
        con.load_script("{}.sql".format(sql))
        con.cursor_one_field("update globals set value=%s where id=1 returning id",(sql,))
        con.commit()
        print("  + Updated database version from {} to {}".format(database_version, sql))
con.disconnect()
