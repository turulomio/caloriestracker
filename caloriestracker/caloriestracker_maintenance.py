from caloriestracker.mem import MemMaintenanceProductSystem2Personal
from datetime import datetime
from logging import debug

def products_system2personal():
    mem=MemMaintenanceProductSystem2Personal()
    mem.run()   
    debug(mem.tr("Start mem took {}".format(datetime.now()-mem.inittime)))
    system=mem.data.products.find_by_id_system(mem.args.system, True)
    system.sqlfile_convert_to_personal()
