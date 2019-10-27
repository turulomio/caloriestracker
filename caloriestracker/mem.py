from PyQt5.QtCore import  QSettings, QCoreApplication, QTranslator, QObject
from PyQt5.QtGui import QIcon,  QPixmap
from PyQt5.QtWidgets import  QApplication, qApp
from argparse import ArgumentParser, RawTextHelpFormatter
from datetime import date,  datetime

from caloriestracker.connection_pg import argparse_connection_arguments_group, Connection
from caloriestracker.libcaloriestracker import DBData
from caloriestracker.datetime_functions import  string2date
from caloriestracker.version import __version__, __versiondate__
from colorama import Fore, Style
from caloriestracker.database_update import database_update
from caloriestracker.package_resources import package_filename
from signal import signal, SIGINT
from sys import argv, exit
from caloriestracker.translationlanguages import TranslationLanguageManager
from logging import basicConfig, DEBUG, INFO, CRITICAL, ERROR, WARNING, info


class Mem(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.con=None
        self.inittime=datetime.now()
        signal(SIGINT, self.signal_handler)

    def epilog(self):
        return self.tr("If you like this app, please give me a star in GitHub (https://github.com/turulomio/caloriestracker).")+"\n" + self.tr("Developed by Mariano Mu\xf1oz 2019-{} \xa9".format(__versiondate__.year))
        
    def load_db_data(self, progress=True):
        """Esto debe ejecutarse una vez establecida la conexión"""
        inicio=datetime.now()

        self.data=DBData(self)
        self.data.load(progress)

        info("Loading db data took {}".format(datetime.now()-inicio))

    def __del__(self):
        if self.con:#Cierre por reject en frmAccess
            self.con.disconnect()
            

    ## Sets debug sustem, needs
    ## @param args It's the result of a argparse     args=parser.parse_args()        
    def addDebugSystem(self, level):
        logFormat = "%(asctime)s.%(msecs)03d %(levelname)s %(message)s [%(module)s:%(lineno)d]"
        dateFormat='%F %I:%M:%S'

        if level=="DEBUG":#Show detailed information that can help with program diagnosis and troubleshooting. CODE MARKS
            basicConfig(level=DEBUG, format=logFormat, datefmt=dateFormat)
        elif level=="INFO":#Everything is running as expected without any problem. TIME BENCHMARCKS
            basicConfig(level=INFO, format=logFormat, datefmt=dateFormat)
        elif level=="WARNING":#The program continues running, but something unexpected happened, which may lead to some problem down the road. THINGS TO DO
            basicConfig(level=WARNING, format=logFormat, datefmt=dateFormat)
        elif level=="ERROR":#The program fails to perform a certain function due to a bug.  SOMETHING BAD LOGIC
            basicConfig(level=ERROR, format=logFormat, datefmt=dateFormat)
        elif level=="CRITICAL":#The program encounters a serious error and may stop running. ERRORS
            basicConfig(level=CRITICAL, format=logFormat, datefmt=dateFormat)
        info("Debug level set to {}".format(level))
        self.debuglevel=level
        
    ## Adds the commons parameter of the program to argparse
    ## @param parser It's a argparse.ArgumentParser
    def addCommonToArgParse(self, parser):
        parser.add_argument('--version', action='version', version="{} ({})".format(__version__, __versiondate__))
        parser.add_argument('--debug', help="Debug program information", choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"], default="ERROR")

    def signal_handler(self, signal, frame):
            print(Style.BRIGHT+Fore.RED+"You pressed 'Ctrl+C', exiting...")
            exit(1)
            
    def trHS(self, s):
        return qApp.translate("HardcodedStrings", s)

class MemGui(Mem):
    def __init__(self):
        Mem.__init__(self)
        
    def app_resource(self):
        return ":/caloriestracker/caloriestracker.svg"

    def qicon(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/caloriestracker/caloriestracker.svg"), QIcon.Normal, QIcon.Off)
        return icon

    ## Returns an icon for admin 
    def qicon_admin(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/caloriestracker/admin.png"), QIcon.Normal, QIcon.Off)
        return icon

class MemInit(MemGui):
    def __init__(self):
        MemGui.__init__(self)
        
        self.settings=QSettings()
        
    def __del__(self):
        self.settings.sync()

    def run(self):
        self.args=self.parse_arguments()
        self.addDebugSystem(self.args.debug) #Must be before QCoreApplication
        self.app=QApplication(argv)
        self.app.setOrganizationName("caloriestracker")
        self.app.setOrganizationDomain("caloriestracker")
        self.app.setApplicationName("caloriestracker")
        self.load_translation()
                
    def load_translation(self):
        self.qtranslator=QTranslator(self.app)
        self.languages=TranslationLanguageManager()
        self.languages.load_all()
        self.languages.selected=self.languages.find_by_id(self.settings.value("frmAccess/language", "en"))
        filename=package_filename("caloriestracker", "i18n/caloriestracker_{}.qm".format(self.languages.selected.id))
        self.qtranslator.load(filename)
        info("TranslationLanguage changed to {}".format(self.languages.selected.id))
        self.app.installTranslator(self.qtranslator)

    def parse_arguments(self):
        self.parser=ArgumentParser(prog='caloriestracker_init', description=self.tr('Create a new caloriestracker database'), epilog=self.epilog(), formatter_class=RawTextHelpFormatter)
        self. addCommonToArgParse(self.parser)
        argparse_connection_arguments_group(self.parser, default_db="caloriestracker")
        args=self.parser.parse_args()
        return args

class MemConsole(Mem):
    def __init__(self):
        Mem.__init__(self)
        

    def __del__(self):
        if hasattr(self, "settings")==True:
            self.settings.sync()

    def run(self, args=None):        
        self.app=QCoreApplication(argv)
        self.app.setOrganizationName("caloriestracker")
        self.app.setOrganizationDomain("caloriestracker")
        self.app.setApplicationName("caloriestracker")
        
        self.settings=QSettings()
        self.args=self.parse_arguments(args)
        self.addDebugSystem(self.args.debug) #Must be before QCoreApplication
        

        self.localzone=self.settings.value("mem/localzone", "Europe/Madrid")
        self.load_translation()
        
        self.con=self.connection()
        if self.con.is_active()==False:
            exit(1)
        
        database_update(self.con, "caloriestracker")
        
        self.load_db_data(False)
        
        self.user=self.data.users.find_by_id(1)
        
                
    def load_translation(self):
        self.languages=TranslationLanguageManager()
        self.languages.load_all()
        self.languages.selected=self.languages.find_by_id(self.settings.value("frmAccess/language", "en"))
        self.languages.cambiar(self.languages.selected.id, "caloriestracker")

    def connection(self):
        con=Connection()
        con.user=self.args.user
        con.server=self.args.server
        con.port=self.args.port
        con.db=self.args.db
        con.get_password()
        con.connect()
        return con

    def parse_arguments(self, args):
        self.parser=ArgumentParser(prog='caloriestracker_console', description=self.tr('Report of calories'), epilog=self.epilog(), formatter_class=RawTextHelpFormatter)
        self. addCommonToArgParse(self.parser)
        argparse_connection_arguments_group(self.parser, default_db="caloriestracker")
        group = self.parser.add_argument_group("Find parameters")
        group.add_argument('--date', help=self.tr('Date to show'), action="store", default=str(date.today()))
        group.add_argument('--users_id', help=self.tr('User id'), action="store", default=1)
        group.add_argument('--find', help=self.tr('Find data'), action="store", default=None)
        group.add_argument('--add_company', help=self.tr("Adds a company"), action="store_true", default=False)
        group.add_argument('--add_product', help=self.tr("Adds a product"), action="store_true", default=False)
        group.add_argument('--add_meal', help=self.tr("Adds a company"), action="store_true", default=False)
        group.add_argument('--add_biometrics', help=self.tr("Adds biometrics"), action="store_true", default=False)
        group.add_argument('--contribution_dump', help=self.tr("Generate a dump to collaborate updating companies and products"), action="store_true", default=False)
        group.add_argument('--parse_contribution_dump', help=self.tr("Parses a dump and generates sql files for the package and for the dump owner"), action="store", default=None)
        group.add_argument('--update_after_contribution',  help=self.tr("Converts personal data to system data in the database using generated sql file of the dump owner"),  action="store", default=None)
        group.add_argument('--elaborated', help=self.tr("Show elaborated product"), action="store", default=None)

        args=self.parser.parse_args(args)
        #Changing types of args
        args.date=string2date(args.date)
        args.users_id=int(args.users_id)
        if args.elaborated!=None:
            args.elaborated=int(args.elaborated)
        return args

class MemCaloriestracker(MemGui):
    def __init__(self):        
        MemGui.__init__(self)
    
    def run(self):
        self.args=self.parse_arguments()
        self.addDebugSystem(self.args.debug)
        self.app=QApplication(argv)
        self.app.setOrganizationName("caloriestracker")
        self.app.setOrganizationDomain("caloriestracker")
        self.app.setApplicationName("caloriestracker")
        self.con=None

        self.frmMain=None #Pointer to mainwidget
        self.closing=False#Used to close threads
        self.url_wiki="https://github.com/turulomio/caloriestracker/wiki"
    
    def parse_arguments(self):
        self.parser=ArgumentParser(prog='caloriestracker', description=self.tr('Report of calories'), epilog=self.epilog(), formatter_class=RawTextHelpFormatter)
        self. addCommonToArgParse(self.parser)
        args=self.parser.parse_args()
        return args
        
    def setLocalzone(self):
        self.localzone=self.settings.value("mem/localzone", "Europe/Madrid")

