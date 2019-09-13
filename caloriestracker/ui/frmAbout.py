from colorama import __version__ as colorama__version__
from officegenerator import __version__ as officegenerator__version__
from platform import python_version
from stdnum import __version__ as stdnum__version__
from psycopg2 import __version__ as psycopg2__version__
from pytz import __version__ as pytz__version__
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl, PYQT_VERSION_STR
from PyQt5.QtChart import PYQT_CHART_VERSION_STR
from caloriestracker.libcaloriestrackerfunctions import qcenter, qempty, qright, string2datetime, qleft
from caloriestracker.libcaloriestrackertypes import eProductType
from caloriestracker.ui.Ui_frmAbout import Ui_frmAbout
from caloriestracker.version import __version__,  __versiondate__

class frmAbout(QDialog, Ui_frmAbout):
    def __init__(self, mem):
        self.mem=mem
        QDialog.__init__(self)
        self.setModal(True)
        self.setupUi(self)
        
        s="<html><body>"
        s=s + self.tr("""Web page is in <a href="http://github.com/turulomio/xulpymoney/">http://github.com/turulomio/xulpymoney/</a>""")
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
        
        self.textEdit.setHtml(s)
        self.lblVersion.setText("{} ({})".format(__version__, __versiondate__))
        productsversion=string2datetime(self.mem.settingsdb.value("Version of products.xlsx", 190001010000), type=6)
        self.lblProductsVersion.setText(self.tr("Last products synchronization was at {}").format(productsversion))
        self.tblSoftware.settings(self.mem, "frmAbout")
        self.tblStatistics.settings(self.mem, "frmAbout")
        self.load_tblStatistics() 
        self.load_tblSoftware()
        self.tblSoftware.itemClicked.connect(self.OpenLink)
        self.tblStatistics.applySettings()    
    
    def load_tblStatistics(self):
        def pais(cur, columna, bolsa):
            """Si pais es Null es para todos"""
            total=0
            cur.execute("select count(*) from products where type=1 and obsolete=false and stockmarkets_id=%s", (bolsa.id,))
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(0, columna , qcenter(tmp))
            cur.execute("select count(*) from products where type=2 and obsolete=false and stockmarkets_id=%s", (bolsa.id,))
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(1, columna , qcenter(tmp))
            cur.execute("select count(*) from products where type=3 and obsolete=false and stockmarkets_id=%s", (bolsa.id,))
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(2, columna , qcenter(tmp))
            cur.execute("select count(*) from products where type=4 and obsolete=false and stockmarkets_id=%s", (bolsa.id,))
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(3, columna , qcenter(tmp))
            cur.execute("select count(*) from products where type=5 and obsolete=false and stockmarkets_id=%s", (bolsa.id,))
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(4, columna , qcenter(tmp))
            cur.execute("select count(*) from products where type=7 and obsolete=false and stockmarkets_id=%s", (bolsa.id,))
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(5, columna , qcenter(tmp))
            cur.execute("select count(*) from products where type=9 and obsolete=false and stockmarkets_id=%s", (bolsa.id,))
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(6, columna , qcenter(tmp))
            cur.execute("select count(*) from products where type=%s and obsolete=false and stockmarkets_id=%s", (eProductType.CFD.value, bolsa.id,))
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(7, columna , qcenter(tmp))
            cur.execute("select count(*) from products where type=%s and obsolete=false and stockmarkets_id=%s", (eProductType.Future.value, bolsa.id,))
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(8, columna , qcenter(tmp))
            self.tblStatistics.setItem(9, columna , qempty())
            cur.execute("select count(*) from products where obsolete=true and stockmarkets_id=%s", (bolsa.id,))
            tmp=cur.fetchone()[0]
            self.tblStatistics.setItem(10, columna , qcenter(tmp))
            self.tblStatistics.setItem(11, columna , qempty())
            self.tblStatistics.setItem(12, columna , qcenter(total))
            self.tblStatistics.horizontalHeaderItem (columna).setIcon(bolsa.country.qicon())
            self.tblStatistics.horizontalHeaderItem (columna).setToolTip((bolsa.country.name))

        def todos(cur):
            """Si pais es Null es para todos"""
            total=0
            cur.execute("select count(*) from products where type=1 and obsolete=false")
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(0, 0 , qcenter(tmp))
            cur.execute("select count(*) from products where type=2  and obsolete=false")
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(1, 0 , qcenter(tmp))
            cur.execute("select count(*) from products where type=3  and obsolete=false")
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(2, 0 , qcenter(tmp))
            cur.execute("select count(*) from products where type=4  and obsolete=false")
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(3, 0 , qcenter(tmp))
            cur.execute("select count(*) from products where type=5  and obsolete=false")
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(4, 0 , qcenter(tmp))
            cur.execute("select count(*) from products where type=7  and obsolete=false")
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(5, 0 , qcenter(tmp))
            cur.execute("select count(*) from products where type=9  and obsolete=false")
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(6, 0 , qcenter(tmp))
            cur.execute("select count(*) from products where type=%s  and obsolete=false", (eProductType.CFD.value, ))
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(7, 0 , qcenter(tmp))
            cur.execute("select count(*) from products where type=%s  and obsolete=false", (eProductType.Future.value, ))
            tmp=cur.fetchone()[0]
            total=total+tmp
            self.tblStatistics.setItem(8, 0 , qcenter(tmp))
            self.tblStatistics.setItem(9, 0 , qempty())
            cur.execute("select count(*) from products where obsolete=true ")
            tmp=cur.fetchone()[0]
            self.tblStatistics.setItem(10, 0 , qcenter(tmp))
            self.tblStatistics.setItem(11, 0 , qempty())
            self.tblStatistics.setItem(12, 0 , qcenter(total))

    
        cur = self.mem.con.cursor()
        todos(cur)
        pais(cur, 1, self.mem.stockmarkets.find_by_id(1))
        pais(cur, 2, self.mem.stockmarkets.find_by_id(2))
        pais(cur, 3, self.mem.stockmarkets.find_by_id(3))
        pais(cur, 4, self.mem.stockmarkets.find_by_id(4))
        pais(cur, 5, self.mem.stockmarkets.find_by_id(5))
        pais(cur, 6,self.mem.stockmarkets.find_by_id(6))
        pais(cur, 7, self.mem.stockmarkets.find_by_id(7))
        pais(cur, 8, self.mem.stockmarkets.find_by_id(8))
        pais(cur, 9, self.mem.stockmarkets.find_by_id(9))
        pais(cur, 10, self.mem.stockmarkets.find_by_id(10))
        pais(cur, 11, self.mem.stockmarkets.find_by_id(11))
        pais(cur, 12, self.mem.stockmarkets.find_by_id(12))
        pais(cur, 13, self.mem.stockmarkets.find_by_id(13))
        pais(cur, 14, self.mem.stockmarkets.find_by_id(14))
        pais(cur, 15, self.mem.stockmarkets.find_by_id(15))
        cur.close()
        self.tblStatistics.applySettings()

    def OpenLink(self,item):
        print(item.text())
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
        
        self.tblSoftware.setItem(7, 0, qright(stdnum__version__))
        self.tblSoftware.setItem(7, 1, qleft("https://arthurdejong.org/python-stdnum"))
        
        self.tblSoftware.setItem(8, 0, qright(pytz__version__))
        self.tblSoftware.setItem(8, 1, qleft("https://pypi.org/project/pytz"))
        
        self.tblSoftware.applySettings()

