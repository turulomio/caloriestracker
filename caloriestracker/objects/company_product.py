
from PyQt5.QtCore import QObject
from caloriestracker.ui.myqtablewidget import qcenter, qleft, qright
class CompaniesAndProducts(QObject):
    def __init__(self, mem):
        QObject.__init__(self)
        self.mem=mem
        
    ## Generates a report finding in fullNames in companies and products
    def find_report(self, find):
        self.mem.data.products.order_by_name()
        print (self.mem.tr("Companies:"))
        for o in self.mem.data.companies.arr:
            if o.fullName().upper().find(find.upper())!=-1:
                print ("  + {}".format( o.fullName()))
        print (self.mem.tr("Products:"))
        for o in self.mem.data.products.arr:
            if o.fullName().upper().find(find.upper())!=-1:
                print ("  + {}".format(o.fullName()))

    ## Used in frmAbout statistics
    def qtablewidget_products_in_companies(self, table):
        rows=self.mem.con.cursor_rows("select companies.name, count(allproducts.id) from allproducts LEFT OUTER JOIN companies ON allproducts.companies_id=companies.id group by companies.name order by count desc")
        table.setColumnCount(2)
        table.setHorizontalHeaderItem(0, qcenter(self.tr("Company name")))
        table.setHorizontalHeaderItem(1, qcenter(self.tr("Products")))
        table.applySettings()
        table.clearContents()
        table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            name="Personal products" if row[0]==None else row[0]
            table.setItem(i, 0, qleft(name))
            table.setItem(i, 1, qright(row[1], digits=0))
            
    def qtablewdiget_database_registers(self, wdg):
        rows=self.mem.con.cursor_one_column("SELECT tablename FROM pg_catalog.pg_tables where schemaname='public' order by tablename") 
        data=[]
        for i, row in enumerate(rows):
            data.append([
                row, 
                self.mem.con.cursor_one_field("select count(*) from "+ row), 
            ])
        wdg.setData(
            [self.tr("Table"), self.tr("Number of registers")], 
            None, 
            data, 
            decimals=0            
        )
