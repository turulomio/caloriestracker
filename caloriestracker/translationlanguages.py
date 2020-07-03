## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from .libmanagers import ObjectManager_With_IdName_Selectable
from .package_resources import package_filename
from logging import info
## Translation files must be in a i18n subir with the same name of the modules. For example: i18n/caloriestracker_es.qm
## Manages languages
class TranslationLanguageManager(ObjectManager_With_IdName_Selectable):
    def __init__(self):
        ObjectManager_With_IdName_Selectable.__init__(self)
        self.qtranslator=None

    def load_all(self):
        self.append(TranslationLanguage("en","English" ))
        self.append(TranslationLanguage("es","Español" ))
        self.append(TranslationLanguage("fr","Français" ))
        self.append(TranslationLanguage("ro","Rom\xe2n" ))
        self.append(TranslationLanguage("ru",'\u0420\u0443\u0441\u0441\u043a\u0438\u0439' ))

    ## @param id string
    ## @param module string
    def cambiar(self, id, module):
        from PyQt5.QtCore import QTranslator
        from PyQt5.QtWidgets import qApp
        if self.qtranslator!=None:
            qApp.removeTranslator(self.qtranslator)
        self.qtranslator=QTranslator(qApp)
        filename=package_filename(module, "i18n/{}_{}.qm".format(module,id))
        self.qtranslator.load(filename)
        info("TranslationLanguage changed to {}".format(id))
        qApp.installTranslator(self.qtranslator)

 
class TranslationLanguage:
    def __init__(self, id, name):
        self.id=id
        self.name=name
