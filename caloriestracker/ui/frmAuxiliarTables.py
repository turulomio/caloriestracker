from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QMenu, QTableWidgetItem,  QInputDialog
from xulpymoney.libxulpymoney import Concept
from xulpymoney.libxulpymoneyfunctions import qmessagebox
from xulpymoney.ui.Ui_frmAuxiliarTables import Ui_frmAuxiliarTables

class frmAuxiliarTables(QDialog, Ui_frmAuxiliarTables):
    def __init__(self, mem,  parent = None, name = None, modal = False):
        """
        Constructor
        
        @param parent The parent widget of this dialog. (QWidget)
        @param name The name of this dialog. (QString)
        @param modal Flag indicating a modal dialog. (boolean)
        """
        QDialog.__init__(self,  parent)
        if name:
            self.setObjectName(name)
        self.setModal(True)
        self.setupUi(self)
        self.mem=mem

        self.tblConcepts.settings(self.mem, "frmAuxiliarTables")
        self.concepts=None
        self.regenerate_list()
        self.tblConcepts_reload()
    
    def regenerate_list(self):
        self.concepts=self.mem.conceptos.clone_editables()

    @pyqtSlot()  
    def on_actionChangeName_triggered(self):
        t=QInputDialog().getText(self,  "Xulpymoney",  self.tr("Change name"))
        if t[1]==True:
            self.concepts.selected.name=t[0]
            self.concepts.selected.save()
            self.mem.con.commit()
            self.mem.conceptos.order_by_name()
            self.regenerate_list()
            self.tblConcepts_reload()

    @pyqtSlot()  
    def on_actionExpensesAdd_triggered(self):
        t=QInputDialog().getText(self,  "Xulpymoney",  self.tr("Add a new expense concept"))
        if t[1]==True:
            concepto=Concept(self.mem, t[0], self.mem.tiposoperaciones.find_by_id(1), True, None)
            concepto.save()
            self.mem.con.commit()
            self.mem.conceptos.append(concepto)
            self.mem.conceptos.order_by_name()
            self.regenerate_list()
            self.tblConcepts_reload()

    @pyqtSlot()  
    def on_actionIncomesAdd_triggered(self):
        t=QInputDialog().getText(self,  "Xulpymoney",  self.tr("Add a new income concept"))
        if t[1]==True:
            concepto=Concept(self.mem, t[0], self.mem.tiposoperaciones.find_by_id(2), True, None)
            concepto.save()
            self.mem.con.commit()
            self.mem.conceptos.append(concepto)
            self.mem.conceptos.order_by_name()
            self.regenerate_list()
            self.tblConcepts_reload()

    @pyqtSlot()  
    def on_actionConceptDelete_triggered(self):
        if self.concepts.selected.borrar():
            self.mem.con.commit()
            self.mem.conceptos.remove(self.concepts.selected)
            self.regenerate_list()
            self.tblConcepts.clearSelection()
            self.concepts.selected=None
            self.tblConcepts_reload()
        else:
            qmessagebox(self.tr("This concept can't be deleted"))

    def on_tblConcepts_customContextMenuRequested(self,  pos):
        if self.concepts.selected==None:
            self.actionChangeName.setEnabled(False)
            self.actionConceptDelete.setEnabled(False)
        else:
            self.actionChangeName.setEnabled(True)
            self.actionConceptDelete.setEnabled(True)
        
        menu=QMenu()
        menu.addAction(self.actionExpensesAdd)
        menu.addAction(self.actionIncomesAdd)
        menu.addAction(self.actionChangeName)
        menu.addAction(self.actionConceptDelete)
        menu.exec_(self.tblConcepts.mapToGlobal(pos))

    def on_tblConcepts_itemSelectionChanged(self):
        try:
            for i in self.tblConcepts.selectedItems():#itera por cada item no row.
                self.concepts.selected=self.concepts.arr[i.row()]
        except:
            self.concepts.selected=None        

    def tblConcepts_reload(self):
        self.tblConcepts.setRowCount(self.concepts.length())
        self.tblConcepts.applySettings()
        for i, c in enumerate(self.concepts.arr):
            self.tblConcepts.setItem(i, 0, QTableWidgetItem(c.name))
            self.tblConcepts.setItem(i, 1, QTableWidgetItem(c.tipooperacion.name))
