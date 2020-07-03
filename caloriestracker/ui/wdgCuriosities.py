from PyQt5.QtWidgets import QWidget, QSpacerItem, QSizePolicy, QFrame
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

        self.addSeparator()

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
        c.setTitle(self.tr("Which is the meal with highest calories I had eaten?"))
        print(*self.query_meal_with_the_highest_calories())
        c.setText(self.tr("The meal with the highest calories I ate was '{}' with '{}' calories. I ate at {}.").format(*self.query_meal_with_the_highest_calories()))
        self.layout.addWidget(c)

        c=wdgCuriosity(self.mem)
        c.setTitle(self.tr("When did I take the highest calories amount in a day?"))
        c.setText(self.tr("The day I took the highest amount of calories was {} and I took {}.").format(*self.query_day_i_took_the_highest_amount_of_calories()))
        self.layout.addWidget(c)
        
        self.addSeparator()
        
        c=wdgCuriosity(self.mem)
        dt, weight=self.mem.con.cursor_one_row("select datetime, max(weight) from biometrics where users_id=%s group by datetime order by max(weight) desc limit 1", (self.mem.user.id, ))
        c.setTitle(self.tr("When did I have my highest weight?"))
        c.setText(self.tr("My highest weight was {} at {}").format(weight, dt))
        self.layout.addWidget(c)
        
        c=wdgCuriosity(self.mem)
        dt, weight=self.mem.con.cursor_one_row("select datetime, min(weight) from biometrics where users_id=%s group by datetime order by min(weight) limit 1", (self.mem.user.id, ))
        c.setTitle(self.tr("When did I have my lowest weight?"))
        c.setText(self.tr("My lowest weight was {} at {}").format(weight, dt))
        self.layout.addWidget(c)

        c=wdgCuriosity(self.mem)
        weight=self.mem.con.cursor_one_field("select percentile_disc(0.5) within group (order by weight) from biometrics where users_id=%s;", (self.mem.user.id, ))
        c.setTitle(self.tr("Which is my median weight?"))
        c.setText(self.tr("My median weight is {}").format(weight))
        self.layout.addWidget(c)

        self.layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Expanding))

    def query_day_i_took_the_highest_amount_of_calories(self):
        return self.mem.con.cursor_one_row("""
select 
    datetime::date,
    round(sum(meals.amount*allproducts.calories/allproducts.amount),0) as mealcalories
from 
    meals, 
    allproducts 
where 
    meals.products_id=allproducts.id and 
    meals.system_product=allproducts.system_product and 
    users_id={}
group by 
    datetime::date 
order by 
    mealcalories desc 
limit 1
""".format(self.mem.user.id))

    def query_meal_with_the_highest_calories(self):
        return self.mem.con.cursor_one_row("""
select 
    allproducts.name, 
    round(meals.amount*allproducts.calories/allproducts.amount, 0) as mealcalories,
    datetime
from 
    meals, 
    allproducts 
where 
    meals.products_id=allproducts.id and 
    meals.system_product=allproducts.system_product   and 
    users_id={}
order by 
    mealcalories desc, 
    datetime desc
limit 1
""".format(self.mem.user.id))


    def addSeparator(self):
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine);
        line.setFrameShadow(QFrame.Sunken);
        self.layout.addWidget(line);
