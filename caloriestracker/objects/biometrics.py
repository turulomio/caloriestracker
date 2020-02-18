
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import  QApplication, QProgressDialog
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable
from decimal import Decimal

class Biometrics:    
    ##Biometrics(mem)
    ##Biometrics(mem,rows)
    ##Biometrics(mem,dt, height, weight, user, activity, weightwish, id):
    def __init__(self, *args):        
        def init__create(dt, height, weight, user, activity, weightwish, id):
            self.datetime=dt
            self.height=height
            self.weight=weight
            self.user=user
            self.activity=activity
            self.weightwish=weightwish
            self.id=id
        # #########################################
        self.mem=args[0]
        if len(args)==1:#Biometrics(mem)
            init__create(*[None]*7)
        elif len(args)==2:#Biometrics(mem,rows)
            user=self.mem.data.users.find_by_id(args[1]['users_id'])
            activity=self.mem.data.activities.find_by_id(args[1]['activity'])
            weightwish=self.mem.data.weightwishes.find_by_id(args[1]['weightwish'])
            init__create(args[1]['datetime'], args[1]['height'], args[1]['weight'], user, activity, weightwish,  args[1]['id'])
        elif len(args)==8:#Biometrics(mem,dt, height, weight, user, activity, id):
            init__create(*args[1:])
    
    def __repr__(self):
        return "{} {}".format(self.height, self.weight)
        
    def delete(self):
        self.mem.con.execute("delete from biometrics where id=%s", (self.id, ))
        
    def save(self):
        if self.id==None:
            self.id=self.mem.con.cursor_one_field("insert into biometrics(datetime,weight,height,users_id,activity,weightwish) values (%s, %s, %s, %s, %s, %s) returning id", (self.datetime, self.weight, self.height, self.user.id, self.activity.id, self.weightwish.id))
        else:
            self.mem.con.execute("update biometrics set datetime=%s, weight=%s, height=%s, users_id=%s, activity=%s, weightwish=%s where id=%s", (self.datetime, self.weight, self.height, self.user.id, self.activity.id, self.weightwish.id, self.id))
                ##basal metabolic rate
    def bmr(self):
        if self.user.male==True:
            return self.activity.multiplier*(Decimal(10)*self.weight + Decimal(6.25)*self.height - Decimal(5)*self.user.age() + 5)
        else: #female
            return self.activity.multiplier*(Decimal(10)*self.weight + Decimal(6.25)*self.height - Decimal(5)*self.user.age() - 161)

    ##    https://www.healthline.com/nutrition/how-much-protein-per-day#average-needs
    ## If you’re at a healthy weight, don't lift weights and don't exercise much, then aiming for 0.36–0.6 grams per pound (0.8–1.3 gram per kg) is a reasonable estimate.
    ##
    ##This amounts to:
    ##
    ##56–91 grams per day for the average male.
    ##46–75 grams per day for the average female.
    ##
    ## But given that there is no evidence of harm and a significant evidence of benefit, it’s likely better for most people to err on the side of more protein rather than less.
    def protein(self):
        return self.bmr()*Decimal(0.175)/Decimal(4)


    ## The Mediterranean diet includes a wide variety of plant and animal foods such as fish, meat, eggs, dairy, extra virgin olive oil, fruits, vegetables, legumes and whole grains.
    ## 
    ## It typically provides 35–40% of calories from fat, including plenty of monounsaturated fat from olive oil.
    ##
    ## Here are a few examples of suggested daily fat ranges for a Mediterranean diet, based on different calorie goals:
    ##
    ##     1,500 calories: About 58–67 grams of fat per day.
    ##     2,000 calories: About 78–89 grams of fat per day.
    ##     2,500 calories: About 97–111 grams of fat per day.
    ## Segun https://www.tuasaude.com/es/calorias-de-los-alimentos/ cada gramo grasa tiene 9 calorias
    ## 60% hidratos, 17.5% proteínas y 22.5% de grasas. SERA SELECCIONABLE
    def fat(self):
        return self.bmr()*Decimal(0.225)/Decimal(9)

    def carbohydrate(self):
        return self.bmr()*Decimal(0.60)/Decimal(4)


    def fiber(self):
        return Decimal(25)
    # Índice de masa corporal
    def imc(self):
        return self.weight/((self.height/100)**2)
    
    ## https://www.seedo.es/index.php/pacientes/calculo-imc
    def imc_comment(self):
        imc=self.imc()
        if imc <18.5:
            return "Peso insuficiente"
        elif imc<24.9:
            return "Peso normal"
        elif imc<26.9:
            return "Sobrepeso grado I"
        elif imc<29.9:
            return "Sobrepeso grado II (preobesidad)"
        elif imc<34.9:
            return "Obesidad grado I"
        elif imc<39.9:
            return "Obesidad grado II"
        elif imc<50:
            return "Obesidad grado III (mórbida)"
        elif imc>=50:
            return "Obesidad grado IV (extrema"

class BiometricsManager(QObject, ObjectManager_With_IdName_Selectable):
    ##Biometrics(mem)
    ##Biometrics(mem,sql, progress)
    def __init__(self, *args ):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=args[0]
        if len(args)==3:
            self.load_from_db(*args[1:])

    def load_from_db(self, sql,  progress=False):
        self.clean()
        cur=self.mem.con.cursor()
        cur.execute(sql)
        if progress==True:
            pd= QProgressDialog(self.tr("Loading {0} biometric data from database").format(cur.rowcount),None, 0,cur.rowcount)
            pd.setWindowIcon(QIcon(":/caloriestracker/coins.png"))
            pd.setModal(True)
            pd.setWindowTitle(self.tr("Loading biometric data..."))
            pd.forceShow()
        for row in cur:
            if progress==True:
                pd.setValue(cur.rownumber)
                pd.update()
                QApplication.processEvents()
            o=Biometrics(self.mem, row)
            self.append(o)
        cur.close()

    def myqtablewidget(self, table):
        data=[]
        for i, o in enumerate(self.arr):
            data.append([
                o.datetime, 
                o.weight, 
                o.height, 
                o.activity.name, 
                o.weightwish.name, 
                o.imc_comment(), 
            ])
        table.setData(
            [self.tr("Date and time"), self.tr("Weight"), self.tr("Height"), self.tr("Activity"), self.tr("weightwish"), self.tr("Situation")], 
            None, 
            data
        )
