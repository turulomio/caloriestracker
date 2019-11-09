#from os import system
from subprocess import run, PIPE
#from xulpymoney.libmanagers import ObjectManager_With_IdName, Object_With_IdName

def menubox_manager_id_name(title, text, manager_id_name):
    options_s=""
    for o in manager_id_name.arr:
       options_s=options_s + " '{}' ''".format(o.name)

    try:
        r=run("""dialog --clear --title "{}" --menu "{}" 40 51 20 {}""".format(title, text, options_s),shell=True, stderr=PIPE)
    except:
        return None
#    print(r.stderr)
    return manager_id_name.find_by_name(r.stderr.decode('UTF-8'))

#manager=ObjectManager_With_IdName()
#manager.append(Object_With_IdName(1,"Uno Uno Uno"))
#manager.append(Object_With_IdName(2,"Dos Dos Dos"))
#r=menubox_manager_id_name("Titulo","Texto", manager)
#print(r.id,r.name)