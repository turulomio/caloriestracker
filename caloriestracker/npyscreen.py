from datetime import datetime
from decimal import Decimal
from time import sleep
from caloriestracker.objects.meal import Meal
from caloriestracker.objects.biometrics import Biometrics
from npyscreen import  NPSAppManaged, TitleSelectOne, Form, TitleText, notify

class MealAddApp(NPSAppManaged):
    def __init__(self, mem):
        self.mem=mem
        self.object=None
        self.log=[]
        NPSAppManaged.__init__(self)
    def onStart(self):
        self.registerForm("MAIN", MealAddForm(self.mem))

class MealAddForm(Form):
    def __init__(self, mem):
        self.mem=mem
        Form.__init__(self)
        self.name="Add a meal"
    
    def create(self):
        self.cmbUsers  = self.add(TitleSelectOne, name = "Select a user:", scroll_exit=True, max_height=3, values=self.mem.data.users.arr)
        self.cmbProducts  = self.add(TitleSelectOne, name = "Select a product:", scroll_exit=True, max_height=5, values=self.mem.data.products.arr)
        self.txtAmount  = self.add(TitleText, name = "Meal amount:",)

    def afterEditing(self):
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
        
        self.parentApp.log.append([product, amount, user])
            
        
        if product==None or user==None or amount==None:
            self.edit()
            return
        self.parentApp.setNextForm(None)
        self.editing = False

        self.parentApp.object=Meal(self.mem, datetime.now(), product,  amount, user, product.system_product, None)
        self.parentApp.object.save()
        self.mem.con.commit()
        notify("Meal added")
        sleep(2)

class BiometricDataAddApp(NPSAppManaged):
    def __init__(self, mem):
        self.mem=mem
        self.object=None
        self.log=[]
        NPSAppManaged.__init__(self)
    def onStart(self):
        self.registerForm("MAIN", BiometricDataAddForm(self.mem))

class BiometricDataAddForm(Form):
    def __init__(self, mem):
        self.mem=mem
        Form.__init__(self)
        self.name="Add biometric data"
    
    def create(self):
        last_weight=self.mem.con.cursor_one_field("select weight from biometrics order by datetime desc limit 1")
        last_height=self.mem.con.cursor_one_field("select height from biometrics order by datetime desc limit 1")
        self.cmbUsers  = self.add(TitleSelectOne, name = "Select a user:", scroll_exit=True, max_height=3, values=self.mem.data.users.arr)
        self.txtWeight=self.add(TitleText, name = "Add your weight:",value=str(last_weight))
        self.txtHeight=self.add(TitleText, name = "Add your height:",value=str(last_height))
        self.cmbActivities  = self.add(TitleSelectOne, name = "Select an activity:", scroll_exit=True, max_height=7, values=self.mem.data.activities.arr)
        self.cmbWeightWishes  = self.add(TitleSelectOne, name = "Select a weight wish:", scroll_exit=True, max_height=7, values=self.mem.data.weightwishes.arr)

    def afterEditing(self):
        
        try:
            activity=self.mem.data.activities.arr[self.cmbActivities.value[0]]
        except:
            activity=None
            
        try:
            weightwish=self.mem.data.weightwishes.arr[self.cmbWeightWishes.value[0]]
        except:
            weightwish=None

        try:
            height=Decimal(self.txtHeight.value)
        except:
            height=None

        try:
            weight=Decimal(self.txtWeight.value)
        except:
            weight=None

        try:
            user=self.mem.data.users.arr[self.cmbUsers.value[0]]
        except:
            user=None
    
        if user==None or weight==None or height==None or activity==None or weightwish==None:
            self.edit()
            return
        self.parentApp.setNextForm(None)
        self.editing = False

        self.parentApp.object=Biometrics(self.mem, datetime.now(), height,  weight, user, activity, weightwish, None)
        self.parentApp.object.save()
        self.mem.con.commit()
        notify("Biometric data added")
        sleep(2)
