from PyQt5.QtWidgets import QWidget, QSpacerItem, QSizePolicy
from xulpymoney.ui.Ui_wdgCuriosities import Ui_wdgCuriosities
from xulpymoney.ui.wdgCuriosity import wdgCuriosity
from xulpymoney.libxulpymoney import Assets,  Money, AccountOperationManager

class wdgCuriosities(QWidget, Ui_wdgCuriosities):
    def __init__(self, mem,  parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem

        self.mem.data.benchmark.needStatus(2)

        c=wdgCuriosity(self.mem)
        c.setTitle(self.tr("Since when there is data in the database?"))
        c.setText("The first data is from {}".format(Assets(self.mem).first_datetime_with_user_data()))
        self.layout.addWidget(c)

        c=wdgCuriosity(self.mem)
        c.setTitle(self.tr("Which is the investment I gain more money in the last three years?"))
        selected=None
        maxgains=Money(self.mem, 0, self.mem.localcurrency)
        for inv in self.mem.data.investments.arr:
            consolidado=inv.op_historica.consolidado_bruto(type=3)
            if maxgains<consolidado:
                maxgains=consolidado
                selected=inv
        if selected==None:
            c.setText(self.tr("You still hasn't gains"))
        else:
            c.setText(self.tr("The investment I gain more money is {} in {} ({}). I got {}.".format(selected.name,selected.account.name, selected.account.eb.name, maxgains)))
        self.layout.addWidget(c)


        c=wdgCuriosity(self.mem)
        c.setTitle(self.tr("Which is the product I gain more money in the last three years?"))
        c.setText(self.tr(""))
        self.layout.addWidget(c)

        c=wdgCuriosity(self.mem)
        c.setTitle(self.tr("Which is the benchmark highest and lowest price?"))
        if self.mem.data.benchmark.result.ohclDaily.length()==0:
            c.setText(self.tr("Current benchmarck hasn't data."))
        else:            
            highest=self.mem.data.benchmark.result.ohclDaily.highest()
            lowest=self.mem.data.benchmark.result.ohclDaily.lowest()
            c.setText(self.tr("Current benchmarck ({}) highest price is {}. It took place at {}. Lowest price is {} and took place at {}.".format(self.mem.data.benchmark.name,self.mem.data.benchmark.currency.string(highest.high), highest.date, self.mem.data.benchmark.currency.string(lowest.low), lowest.date)))
        self.layout.addWidget(c)

        c=wdgCuriosity(self.mem)
        c.setTitle(self.tr("How many quotes are there in the database?"))
        c.setText(self.tr("There are {} quotes in this Xulpymoney database.".format(self.mem.con.cursor_one_field("select count(*) from quotes"))))
        self.layout.addWidget(c)

        c=wdgCuriosity(self.mem)
        c.setTitle(self.tr("Which product has the highest quote?"))
        c.setText(self.tr(""))
        self.layout.addWidget(c)

        c=wdgCuriosity(self.mem)
        operations=AccountOperationManager(self.mem)
        operations.load_from_db("select * from opercuentas where importe = (select max(importe) from opercuentas) order by datetime desc limit 1")
        c.setTitle(self.tr("Which is the amount of the largest account operation?"))
        if operations.length()==1:
            o=operations.only()
            c.setText(self.tr("The largest account operation took place at {}. It's concept was '{}' and it's amount was {}.".format(o.datetime, o.concepto.name, o.account.currency.string(o.importe))))
        else:
            c.setText(self.tr("There are not account operations yet."))
        self.layout.addWidget(c)

        c=wdgCuriosity(self.mem)
        c.setTitle(self.tr("Which is the amount of the largest credit card operation?"))
        c.setText(self.tr(""))
        self.layout.addWidget(c)

        c=wdgCuriosity(self.mem)
        c.setTitle(self.tr("Which is the amount of the largest investment operation?"))
        c.setText(self.tr(""))
        self.layout.addWidget(c)
        self.layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding))
