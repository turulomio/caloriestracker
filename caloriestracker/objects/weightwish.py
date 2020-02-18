from PyQt5.QtCore import QObject
from caloriestracker.libcaloriestrackertypes import eWeightWish
from caloriestracker.libmanagers import ObjectManager_With_IdName_Selectable

class WeightWish(QObject):
    def __init__(self, mem, name, id):
            self.mem=mem
            self.name=name
            self.id=id
    def __str__(self):
        return self.name

class WeightWishManager(QObject, ObjectManager_With_IdName_Selectable):
    def __init__(self, mem):
        QObject.__init__(self)
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.mem=mem
        self.append(WeightWish(self.mem, self.tr("Lose weight"), eWeightWish.Lose))
        self.append(WeightWish(self.mem, self.tr("Mantain weight"), eWeightWish.Mantain))
        self.append(WeightWish(self.mem, self.tr("Gain weight"), eWeightWish.Gain))
