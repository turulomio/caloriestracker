from colorama import __version__ as colorama__version__
from officegenerator import __version__ as officegenerator__version__
from platform import python_version
from psycopg2 import __version__ as psycopg2__version__
from pytz import __version__ as pytz__version__
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, PYQT_VERSION_STR
from PyQt5.QtChart import PYQT_CHART_VERSION_STR
from caloriestracker.ui.qtablewidgetitems import  qright, qleft
from caloriestracker.libcaloriestracker import CompaniesAndProducts
from caloriestracker.ui.Ui_frmAbout import Ui_frmAbout
from caloriestracker.version import __version__,  __versiondate__

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
        self.lblVersion.setText("{} ({})".format(__version__, __versiondate__))
        dbversion=self.mem.con.cursor_one_field("select value from globals where id=1")
        self.lblProductsVersion.setText(self.tr("Database version is: {}").format(dbversion))
        self.tblSoftware.settings(self.mem, "frmAbout")
        self.tblStatistics.settings(self.mem, "frmAbout")
        cp=CompaniesAndProducts(self.mem)
        cp.qtablewdiget_database_registers(self.tblStatistics)
        self.load_tblSoftware()
        self.tblSoftware.itemClicked.connect(self.OpenLink)


    def OpenLink(self,item):
        if item.column() == 1:
            QDesktopServices.openUrl(QUrl(item.text()));

    ##Function that fills tblSoftware with data 
    def load_tblSoftware(self):
        #Postgres version
        cur=self.mem.con.cursor()
        postgres_version=self.mem.con.cursor_one_field("show server_version")
        cur.close()

        # Ui
        self.tblSoftware.setItem(0, 0, qright(colorama__version__))
        self.tblSoftware.setItem(0, 1, qleft("https://github.com/tartley/colorama"))
        
        self.tblSoftware.setItem(1, 0, qright(officegenerator__version__))
        self.tblSoftware.setItem(1, 1, qleft("https://github.com/turulomio/officegenerator"))
        
        self.tblSoftware.setItem(2, 0, qright(postgres_version))
        self.tblSoftware.setItem(2, 1, qleft("https://www.postgresql.org/"))
        
        self.tblSoftware.setItem(3, 0, qright(psycopg2__version__.split(" ")[0]))
        self.tblSoftware.setItem(3, 1, qleft("http://initd.org/psycopg/"))
        
        self.tblSoftware.setItem(4, 0, qright(PYQT_VERSION_STR))
        self.tblSoftware.setItem(4, 1, qleft("https://riverbankcomputing.com/software/pyqt/intro"))
        
        self.tblSoftware.setItem(5, 0, qright(PYQT_CHART_VERSION_STR))
        self.tblSoftware.setItem(5, 1, qleft("https://www.riverbankcomputing.com/software/pyqtchart/intro"))
        
        self.tblSoftware.setItem(6, 0, qright(python_version()))
        self.tblSoftware.setItem(6, 1, qleft("https://www.python.org"))
                
        self.tblSoftware.setItem(7, 0, qright(pytz__version__))
        self.tblSoftware.setItem(7, 1, qleft("https://pypi.org/project/pytz"))
        
        self.tblSoftware.applySettings()

