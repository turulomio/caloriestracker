from colorama import __version__ as colorama__version__
from officegenerator import __version__ as officegenerator__version__
from platform import python_version
from psycopg2 import __version__ as psycopg2__version__
from pytz import __version__ as pytz__version__
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, PYQT_VERSION_STR
from PyQt5.QtChart import PYQT_CHART_VERSION_STR
from caloriestracker.objects.company_product import CompaniesAndProducts
from caloriestracker.ui.Ui_frmAbout import Ui_frmAbout
from caloriestracker.version import __version__,  __versiondatetime__

class frmAbout(QDialog, Ui_frmAbout):
    def __init__(self, mem):
        self.mem=mem
        QDialog.__init__(self)
        self.setModal(True)
        self.setupUi(self)
        
        s="<html><body>"
        s=s + self.tr("""Web page is in <a href="http://github.com/turulomio/caloriestracker/">http://github.com/turulomio/caloriestracker/</a>""")
        s=s + "<p>"
        s=s + self.tr("This program has been developed by Mariano Mu\xf1oz") + "<p>"
        s=s + self.tr("It has been translated to the following languages:")
        s=s + "<ul>"
        s=s + "<li>English</li>"
        s=s + "<li>Espa\xf1ol</li>"
        s=s + "</ul>"
        s=s + "<p>"
        s=s + self.tr("""Avatars are from <a href="http://www.nobleavatar.com/">http://www.nobleavatar.com/</a>""")
        s=s + "</body></html>"
        
        self.textBrowser.setHtml(s)
        self.lblVersion.setText("{} ({})".format(__version__, __versiondatetime__.date()))
        dbversion=self.mem.con.cursor_one_field("select value from globals where id=1")
        self.lblProductsVersion.setText(self.tr("Database version is: {}").format(dbversion))
        self.tblSoftware.setSettings(self.mem.settings, "frmAbout", "tblSoftware")
        self.tblStatistics.setSettings(self.mem.settings, "frmAbout", "tblStatistics")
        cp=CompaniesAndProducts(self.mem)
        cp.qtablewdiget_database_registers(self.tblStatistics)
        self.load_tblSoftware()
        self.tblSoftware.table.itemClicked.connect(self.OpenLink)


    def OpenLink(self,item):
        if item.column() == 1:
            QDesktopServices.openUrl(QUrl(item.text()));

    ##Function that fills tblSoftware with data 
    def load_tblSoftware(self):        
        data=[]
        postgres_version=self.mem.con.cursor_one_field("show server_version")
        data.append(["Colorama", colorama__version__,  "https://github.com/tartley/colorama"])
        data.append(["Officegenerator", officegenerator__version__, "https://github.com/turulomio/officegenerator"])
        data.append(["PostgreSQL", postgres_version, "https://www.postgresql.org/"])
        data.append(["Psycopg2", psycopg2__version__.split(" ")[0], "http://initd.org/psycopg/"])
        data.append(["PyQt5", PYQT_VERSION_STR, "https://riverbankcomputing.com/software/pyqt/intro"])
        data.append(["PyQtChart",  PYQT_CHART_VERSION_STR, "https://www.riverbankcomputing.com/software/pyqtchart/intro"])
        data.append(["Python", python_version(), "https://www.python.org"])
        data.append(["Pytz", pytz__version__, "https://pypi.org/project/pytz"])
        self.tblSoftware.setData(
            [self.tr("Program"), self.tr("Version"), self.tr("Url")], 
            None, 
            data,        
        )


1
