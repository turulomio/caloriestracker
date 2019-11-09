from datetime import datetime
from decimal import Decimal
from caloriestracker.libcaloriestracker import Meal
from npyscreen import  NPSAppManaged, TitleSelectOne, Form, TitleText

class MealAddApp(NPSAppManaged):
    def __init__(self, mem):
        self.mem=mem
        self.object=None
        NPSAppManaged.__init__(self)
    def onStart(self):
        self.registerForm("MAIN", MealAddForm(self.mem))

class MealAddForm(Form):
    def __init__(self, mem):
        self.mem=mem
        self.log=""
        Form.__init__(self)
    
    def create(self):
        self.cmbUsers  = self.add(TitleSelectOne, name = "Select a user:", scroll_exit=True, max_height=3, values=self.mem.data.users.arr)
        self.cmbProducts  = self.add(TitleSelectOne, name = "Select a product:", scroll_exit=True, max_height=5, values=self.mem.data.products.arr)
        self.txtAmount  = self.add(TitleText, name = "Meal amount:",)

    def afterEditing(self):
        
        self.parentApp.setNextForm(None)
        try:
            product=self.mem.data.products.arr[self.cmbProducts.value[0]]
        except:
            product=None
        try:
            amount=Decimal(self.txtAmount.value)
        except:
            amount=None
        try:
            user=self.mem.data.users.arr[self.cmbUsers.value[0]]
        except:
            user=None
            
        if product==None or user==None or amount==None or amount=="":
            self.edit()
            return

        self.parentApp.object=Meal(self.mem, datetime.now(), product,  amount, user, product.system_product, None)
        self.parentApp.object.save()
        self.mem.con.commit()
