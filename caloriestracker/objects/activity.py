
from PyQt5.QtCore import QObject
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable
from caloriestracker.libcaloriestrackertypes import eActivity
from decimal import Decimal
## TMB x 1,2: Poco o ningún ejercicio                     +
##        |                                |       |          |            | TMB x 1,375: Ejercicio ligero (1 a 3 días a la semana) +
##        |                                |       |          |            | TMB x 1,55: Ejercicio moderado (3 a 5 días a la semana)+
##        |                                |       |          |            | TMB x 1,72: Deportista (6 -7 días a la semana)         +
##        |                                |       |          |            | TMB x 1,9: Atleta (Entrenamientos mañana y tarde)
##    Sedentary. 
##    Lightly active. If you exercise lightly one to three days a week, multiply your BMR by 1.375.
##    Moderately active. If you exercise moderately three to five days a week, multiply your BMR by 1.55.
##    Very active. If you engage in hard exercise six to seven days a week, multiply your BMR by 1.725.
##    Extra active. If you engage in very hard exercise six to seven days a week or have a physical job, multiply your BMR by 1.9.
class Activity(QObject):
    ##Biometrics(mem)
    ##Biometrics(mem,id,name, description,multiplier)
    def __init__(self, mem, name, description, multiplier, id):
            self.mem=mem
            self.name=name
            self.description=description
            self.multiplier=multiplier
            self.id=id
            
    def __str__(self):
        return self.name

class ActivityManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=mem
        self.append(Activity(self.mem, self.tr("Sedentary"), self.tr("If you get minimal or no exercise"), Decimal(1.2), eActivity.Sedentary))
        self.append(Activity(self.mem, self.tr("Lightly active"), self.tr("If you exercise moderately three to five days a week"), Decimal(1.375), eActivity.LightlyActive))
        self.append(Activity(self.mem, self.tr("Moderately active"), self.tr("If you exercise moderately three to five days a week"), Decimal(1.55), eActivity.ModeratelyActive))
        self.append(Activity(self.mem, self.tr("Very active"), self.tr("If you engage in hard exercise six to seven days a week"), Decimal(1.725), eActivity.VeryActive))
        self.append(Activity(self.mem, self.tr("Extra active"), self.tr("If you engage in very hard exercise six to seven days a week or have a physical job"), Decimal(1.9), eActivity.ExtraActive))

