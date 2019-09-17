from caloriestracker.mem import MemInit
from caloriestracker.ui.frmInit import frmInit
from sys import exit

def main():
    mem=MemInit()
    mem.run()
    frm = frmInit(mem)
    frm.show()
    exit(mem.app.exec_())
