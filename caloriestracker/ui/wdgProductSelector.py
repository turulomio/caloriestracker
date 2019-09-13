from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QDialog, QLabel, QLineEdit, QHBoxLayout, QToolButton, QVBoxLayout, QSizePolicy, QSpacerItem, QAbstractItemView
from caloriestracker.ui.myqtablewidget import myQTableWidget
from caloriestracker.libcaloriestracker import ProductManager, ManagerSelectionMode
from caloriestracker.libcaloriestrackerfunctions import qmessagebox

class wdgProductSelector(QWidget):
    """Para usarlo promocionar un qwidget en designer y darle los comportamientos de tamaña que neceseite
    incluso añadirlo a un layout."""
    selectionChanged=pyqtSignal()
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.selected=None
    
    def setupUi(self, mem, investment=None):
        """Investement is used to set investment pointer. It's usefull to see investment data in product report"""
        self.mem=mem
        self.investment=investment#Optional
        
        self.horizontalLayout_2 = QHBoxLayout(self)
        self.horizontalLayout = QHBoxLayout()
        self.label = QLabel(self)
        self.label.setText(self.tr("Select a product"))
        self.horizontalLayout.addWidget(self.label)                                                                                                                                 
        self.txt = QLineEdit(self)                                                                                                                                       
        self.txt.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)                                                                             
        self.txt.setReadOnly(True)      
        self.txt.setToolTip(self.tr("Press the search button"))           
        self.horizontalLayout.addWidget(self.txt)                                                                                                                                 
        self.cmd= QToolButton(self)               
        icon = QIcon()
        icon.addPixmap(QPixmap(":/xulpymoney/document-preview-archive.png"), QIcon.Normal, QIcon.Off)
        self.cmd.setIcon(icon)                                                                                                                                   
        self.horizontalLayout.addWidget(self.cmd)                                                                                                                            
        self.horizontalLayout_2.addLayout(self.horizontalLayout)                
        self.cmd.released.connect(self.on_cmd_released)
        self.cmd.setToolTip(self.tr("Press to select a product"))
                                                                                                          
        self.cmdProduct= QToolButton(self)    
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(":/xulpymoney/books.png"), QIcon.Normal, QIcon.Off)
        self.cmdProduct.setIcon(icon2)                                                                                                       
        self.horizontalLayout.addWidget(self.cmdProduct)  
        self.cmdProduct.setToolTip(self.tr("Press to see selected product information"))                    
        self.cmdProduct.released.connect(self.on_cmdProduct_released)
        self.cmdProduct.setEnabled(False)

    def on_cmd_released(self):
        d=frmProductSelector(self, self.mem)
        d.exec_()
        self.setSelected(d.products.selected)
        
    def on_cmdProduct_released(self):
        w=frmProductReport(self.mem, self.selected, self.investment,  self)
        w.exec_()
            
    def setSelected(self, product):
        """Recibe un objeto Product. No se usará posteriormente, por lo que puede no estar completo con get_basic.:."""
        self.selected=product
        if self.selected==None:
            self.txt.setText(self.tr("Not selected"))
            self.cmdProduct.setEnabled(False)     
            self.txt.setToolTip(self.tr("Press the search button"))                                                                                                                                                           
        else:      
            self.txt.setText("{0} ({1})".format(self.selected.name, self.selected.id))
            self.cmdProduct.setEnabled(True)
            self.txt.setToolTip(self.tr("Selected product"))    
            self.selectionChanged.emit()
        
    def showProductButton(self, boolean):
        if boolean==True:#Default
            self.cmdProduct.show()
        else:
            self.cmdProduct.hide()

class frmProductSelector(QDialog):
    def __init__(self, parent, mem):
        QDialog.__init__(self, parent)
        self.mem=mem
        self.products=ProductManager(self.mem)
        self.resize(1024, 500)
        self.horizontalLayout_2 = QHBoxLayout(self)
        self.verticalLayout = QVBoxLayout()
        self.lbl = QLabel(self)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl.setFont(font)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.lbl)
        self.horizontalLayout = QHBoxLayout()
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.widget = wdgProductSelector(self)
        self.horizontalLayout.addWidget(self.widget)
        self.label = QLabel(self)
        self.horizontalLayout.addWidget(self.label)
        self.txt = QLineEdit(self)
        self.horizontalLayout.addWidget(self.txt)
        self.cmd = QToolButton(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/xulpymoney/document-preview-archive.png"), QIcon.Normal, QIcon.Off)
        self.cmd.setIcon(icon)
        self.horizontalLayout.addWidget(self.cmd)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tblInvestments = myQTableWidget(self)
        self.tblInvestments.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tblInvestments.setAlternatingRowColors(True)
        self.tblInvestments.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tblInvestments.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tblInvestments.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tblInvestments.settings(self.mem, "frmProductReport")

        self.tblInvestments.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tblInvestments)
        self.lblFound = QLabel(self)
        self.verticalLayout.addWidget(self.lblFound)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.setWindowTitle(self.tr("Select a product"))
        self.lbl.setText(self.tr("Product list"))
        self.label.setText(self.tr("Search by code, ISIN, ticker or product name"))
        self.lblFound.setText(self.tr("Found registers"))

        self.setTabOrder(self.txt, self.cmd)
        self.setTabOrder(self.cmd, self.tblInvestments)
        self.cmd.released.connect(self.on_cmd_released)
        self.txt.returnPressed.connect(self.on_cmd_released)                    
        self.tblInvestments.itemSelectionChanged.connect(self.on_tblInvestments_itemSelectionChanged)
        self.tblInvestments.cellDoubleClicked.connect(self.on_tblInvestments_cellDoubleClicked)
        
    def on_cmd_released(self):
        if len(self.txt.text().upper())<=2:            
            qmessagebox(self.tr("Search too wide. You need more than 2 characters"))
            return
                
        self.products=self.mem.data.products.ProductManager_contains_string(self.txt.text().upper())
        self.products.setSelectionMode(ManagerSelectionMode.Object)
        self.products.needStatus(1, progress=True)
        self.products.order_by_name()
        self.lblFound.setText(self.tr("Found {0} registers").format(self.products.length()))
        self.products.myqtablewidget(self.tblInvestments)  
        
    def on_tblInvestments_cellDoubleClicked(self, row, column):
        self.done(0)
    
    def on_tblInvestments_itemSelectionChanged(self):
        self.products.selected=None
        for i in self.tblInvestments.selectedItems():
            if i.column()==0:
                self.products.selected=self.products.arr[i.row()]

from caloriestracker.ui.frmProductReport import frmProductReport
