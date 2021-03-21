from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QLabel, QComboBox, QDialog, QDialogButtonBox, QWidget, QTableWidgetItem, QVBoxLayout, QToolButton, QHBoxLayout
from logging import debug
from .myqtablewidget import mqtw
from .. call_by_name import call_by_name

class frmManagerSelector(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=None)
        self.bb=QDialogButtonBox(self)
        self.setWidgetType()
        
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        
        self.lbl=QLabel()
        self.lbl.setText(self.tr("Manager selector"))
        self.lbl.setFont(font)
        self.lbl.setAlignment(Qt.AlignCenter)
        
        lay = QVBoxLayout(self)
        lay.addWidget(self.lbl)
        lay.addWidget(self.widget)
        lay.addWidget(self.bb)
        self._resourcesIconRoot="reusing"
        
    ## Override this to change manager
    def setWidgetType(self):
        self.widget=wdgManagerSelector(self)
        
    ## Both managers must have setConstructorParameters
    def setManagers(self, settings, settingsSection,  settingsObject, manager, selected):
        self._settings=settings
        self._settingsSection=settingsSection
        self._settingsObject=settingsObject
        self.widget.setManagers(self._settings, self._settingsSection, self._settingsObject, manager, selected)
        self.resize(self._settings.value("{}/{}_dialog_size".format(self._settingsSection, self._settingsObject), QSize(800, 600)))

    def exec_(self):
        QDialog.exec_(self)
        self._settings.setValue("{}/{}_dialog_size".format(self._settingsSection, self._settingsObject), self.size())
        debug("Selected objects: {}".format(str(self.widget.selected.arr)))

    def setLabel(self, s):
        self.lbl.setText(s)

## Managers must use the same objects in arrays (same address)
## They are considered as objects, and it's representation is from __repr__ method
class wdgManagerSelector(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.mqtw=mqtw(self)
        self.mqtw.showSearchOptions(True)
        self.mqtw.showSearchCloseButton(False)
        self.mqtw.setGenericContextMenu()
        self.mqtw.setOrderingEnabled(True)
        self.mqtw.table.cellDoubleClicked.connect(self.on_mqtw_cellDoubleClicked)
        
        self.mqtwSelected=mqtw(self)
        self.mqtwSelected.showSearchOptions(True)
        self.mqtwSelected.showSearchCloseButton(False)
        self.mqtwSelected.setGenericContextMenu()
        self.mqtwSelected.setOrderingEnabled(True)
        self.mqtwSelected.table.cellDoubleClicked.connect(self.on_mqtwSelected_cellDoubleClicked)
        
        self.laybuttons = QVBoxLayout()
        self.cmdLeft=QToolButton(self)
        self.cmdLeft.setText("<")
        self.cmdLeftAll=QToolButton(self)
        self.cmdLeftAll.setText("<<")
        self.cmdRight=QToolButton(self)
        self.cmdRight.setText(">")
        self.cmdRightAll=QToolButton(self)
        self.cmdRightAll.setText(">>")
        self.cmdDown=QToolButton(self)
        self.cmdUp=QToolButton(self)
        self.laybuttons.addWidget(self.cmdUp)
        self.laybuttons.addWidget(self.cmdRightAll)
        self.laybuttons.addWidget(self.cmdRight)
        self.laybuttons.addWidget(self.cmdLeft)
        self.laybuttons.addWidget(self.cmdLeftAll)
        self.laybuttons.addWidget(self.cmdDown)
        self.laybuttons.setAlignment(Qt.AlignVCenter)
        
        self.cmdDown.hide()
        self.cmdUp.hide()
        
        self.lay=QHBoxLayout(self)
        self.lay.addWidget(self.mqtw)
        self.lay.addLayout(self.laybuttons)
        self.lay.addWidget(self.mqtwSelected)        
        self._showObjectIcons=True
        self._showObjectCallingByName="name"
        
    ## Objects are showed in tables using call_by_name method
    ## @param string_or_tuple parameter to call mehtod using call_by_name module
    def setShowObjectCallingByName(self, string_or_tuple):
        self._showObjectCallingByName=string_or_tuple

    ## Hides Up and Down button
    def showUpDown(self):
        self.cmdDown.show()
        self.cmdUp.show()
        
    ## By default is True. Show Icons y tables and combobox 
    def showObjectIcons(self, boolean):
        self._showObjectIcons=boolean

    ## manager needs to have add setConstructorParameters to generate emptyManager
    def setManagers(self, settings, settingsSection,  settingsObject, manager, selected):
        self._settings=settings
        self._settingsSection=settingsSection
        self._settingsObject=settingsObject
        self.mqtw.setSettings(self._settings, self._settingsSection, "{}_tbl".format(self._settingsObject))
        self.mqtwSelected.setSettings(self._settings, self._settingsSection, "{}_tblSelected".format(self._settingsObject))

        self.manager=manager.clone()#Clone manager to delete safely objects

        #removes selected objects from manager
        if selected is None:
            self.selected=self.manager.emptyManager()
        else:
            self.selected=selected
            for o in self.selected.arr:
                self.manager.remove(o)

        self._load_tbl()
        self._load_tblSelected()
        self.cmdDown.released.connect(self.on_cmdDown_released)
        self.cmdUp.released.connect(self.on_cmdUp_released)
        self.cmdLeft.released.connect(self.on_cmdLeft_released)
        self.cmdRight.released.connect(self.on_cmdRight_released)
        self.cmdLeftAll.released.connect(self.on_cmdLeftAll_released)
        self.cmdRightAll.released.connect(self.on_cmdRightAll_released)

    def _load_tblSelected(self):       
        self.mqtwSelected.table.setColumnCount(1)
        self.mqtwSelected.table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Object")))
        self.mqtwSelected.applySettings() 
        self.mqtwSelected.table.setRowCount(self.selected.length())
        self.selected.arr=sorted(self.selected.arr, key=lambda o: str(call_by_name(o, self._showObjectCallingByName)),  reverse=False)  
        for i, o in enumerate(self.selected.arr):
            self.mqtwSelected.table.setItem(i, 0, QTableWidgetItem(str(call_by_name(o, self._showObjectCallingByName))))
            if self._showObjectIcons==True:
                self.mqtwSelected.table.item(i, 0).setIcon(o.qicon())
            self.mqtwSelected.table.showRow(i)
        self.mqtwSelected.on_txt_textChanged(self.mqtwSelected.txtSearch.text())
        
    def _load_tbl(self):  
        self.mqtw.table.setColumnCount(1)
        self.mqtw.table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Object")))
        self.mqtw.applySettings()
        self.mqtw.table.setRowCount(self.manager.length())
        self.manager.arr=sorted(self.manager.arr, key=lambda o: str(call_by_name(o, self._showObjectCallingByName)),  reverse=False)  
        for i, o in enumerate(self.manager.arr):
            self.mqtw.table.setItem(i, 0, QTableWidgetItem(str(call_by_name(o, self._showObjectCallingByName))))
            if self._showObjectIcons==True:
                self.mqtw.table.item(i, 0).setIcon(o.qicon())
            self.mqtw.table.showRow(i)
        self.mqtw.on_txt_textChanged(self.mqtw.txtSearch.text())

    def on_cmdLeft_released(self):
        for i in self.mqtwSelected.table.selectedItems():
            selected=self.selected.arr[i.row()]
            self.manager.append(selected)       
            self.selected.remove(selected) 
        self._load_tbl()
        self._load_tblSelected()

    def on_cmdLeftAll_released(self):
        for o in self.selected.arr:
            self.manager.append(o)      
        self.selected.clean()
        self._load_tbl()
        self._load_tblSelected()

    def on_cmdRightAll_released(self):
        for o in self.manager.arr:
            self.selected.append(o)       
        self.manager.clean()
        self._load_tbl()
        self._load_tblSelected()
        
    def on_cmdRight_released(self):
        for i in self.mqtw.table.selectedItems():
            selected=self.manager.arr[i.row()]
            self.selected.append(selected)
            self.manager.remove(selected)
        self._load_tbl()
        self._load_tblSelected()   
        
        
    def on_cmd_released(self):
        print("Selected",  self.selected.arr)
        self.done(0)
        
    def on_cmdUp_released(self):
        pos=None
        for i in self.mqtwSelected.table.selectedItems():
            pos=i.row()
        tmp=self.selected.arr[pos]
        self.selected.arr[pos]=self.selected.arr[pos-1]
        self.selected.arr[pos-1]=tmp
        self._load_tbl()
        self._load_tblSelected()             
        
    def on_cmdDown_released(self):
        pos=None
        for i in self.mqtwSelected.table.selectedItems():
            pos=i.row()
        tmp=self.selected.arr[pos+1]
        self.selected.arr[pos+1]=self.selected.arr[pos]
        self.selected.arr[pos]=tmp
        self._load_tbl()
        self._load_tblSelected()        
        
    def on_mqtw_cellDoubleClicked(self, row, column):
        self.on_cmdRight_released()
        
    def on_mqtwSelected_cellDoubleClicked(self, row, column):
        self.on_cmdLeft_released()
        

## This code use the following path to set Icons in qrc qt files
## - ":/reusingcode/search.png"
## Shows selected objects in a QComboBox. You can press a button to open frmManagerSelector
class cmbManagerSelector(QWidget):
    comboSelectionChanged=pyqtSignal()
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=None)
        self.combo=QComboBox(self)
        self.cmd=QToolButton(self)
        self.cmd.setIcon(QIcon(":/reusingcode/search.png"))
        self.cmd.setToolTip(self.tr("Press to open a manager selector"))
        
        lay = QHBoxLayout(self)
        lay.addWidget(self.combo)
        lay.addWidget(self.cmd)
        
        self.frm=frmManagerSelector(self)
        
        self.cmd.released.connect(self.on_cmd_released)
        self._showObjectIcons=True
        
    ## By default is True. Show Icons y tables and combobox 
    def showObjectIcons(self, boolean):
        self._showObjectIcons=boolean

    def on_cmd_released(self):
        self.frm.exec_()
        self.combo.clear()
        for o in self.frm.widget.selected.arr:
            if self._showObjectIcons==True:
                self.combo.addItem(o.qicon(), call_by_name(o, self.frm.widget._showObjectCallingByName))
            else:
                self.combo.addItem(call_by_name(o, self.frm.widget._showObjectCallingByName))
        self.comboSelectionChanged.emit()

    def setManagers(self, settings, settingsSection, settingsObject, manager, selected):
        self._settings=settings
        self.frm.setManagers(settings, settingsSection, settingsObject, manager, selected)
        if selected!=None:
            for o in selected.arr:
                if self._showObjectIcons==True:
                    self.combo.addItem(o.qicon(), call_by_name(o, self.frm.widget._showObjectCallingByName))
                else:
                    self.combo.addItem(call_by_name(o, self.frm.widget._showObjectCallingByName))

    ## Returns the selected manager
    def selected(self):
        return self.frm.widget.selected

def example():
    from libmanagers import ObjectManager_With_IdName
    from PyQt5.QtCore import QSettings
    class Mem:
        def __init__(self):
            self.settings=QSettings()
            
    class Prueba:
        def __init__(self, id=None, name=None):
            self.id=id
            self.name=name
            
        def qicon(self):
            return QIcon(":/xulpymoney/xulpymoney.png")
    
    class PruebaManager(ObjectManager_With_IdName):
        def __init__(self):
            ObjectManager_With_IdName.__init__(self)
            
    d={'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'ten':10, 'eleven':11}
    manager=PruebaManager()
    manager.setConstructorParameters()
    for k, v in d.items():
        manager.append(Prueba(v, k))
        
    selected=PruebaManager()
    selected.setConstructorParameters()
    selected.append(manager.arr[3])
    
    mem=Mem()
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    from importlib import import_module
    import_module("xulpymoney.images.xulpymoney_rc")

    w = cmbManagerSelector()
    #w.frm.widget.hideUpDown()
    w.setManagers(mem.settings,"frmSelectorExample", "frmSelector", manager, selected)
    w.move(300, 300)
    w.setWindowTitle('frmSelector example')
    w.show()
    
    app.exec()
