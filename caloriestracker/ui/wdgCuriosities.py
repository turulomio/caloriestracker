from PyQt5.QtWidgets import QWidget, QSpacerItem, QSizePolicy
from caloriestracker.libcaloriestrackertypes import eProductComponent
from caloriestracker.ui.Ui_wdgCuriosities import Ui_wdgCuriosities
from caloriestracker.ui.wdgCuriosity import wdgCuriosity

class wdgCuriosities(QWidget, Ui_wdgCuriosities):
    def __init__(self, mem,  parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.mem=mem

        c=wdgCuriosity(self.mem)
        c.setTitle(self.tr("Since when there is data in the database?"))
        c.setText("The first data is from {}".format(self.mem.con.cursor_one_field("select min(datetime) from meals where users_id=%s", (self.mem.user.id, ))))
        self.layout.addWidget(c)

        c=wdgCuriosity(self.mem)
        c.setTitle(self.tr("Which is the product with highest calories in 100 gramos?"))
        selected=None
        amount=0
        for product in self.mem.data.products.arr:
            productamount=product.component_in_100g(eProductComponent.Calories)
            if productamount>amount:
                selected=product
                amount=productamount
        c.setText(self.tr("The product with highest calories is {} with {} calories.".format(selected.fullName(), selected.component_in_100g(eProductComponent.Calories))))
        self.layout.addWidget(c)


        c=wdgCuriosity(self.mem)
        c.setTitle(self.tr("Which is the meal with highest calories I had eaten"))
        c.setText(self.tr(""))
        self.layout.addWidget(c)

        self.layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding))
