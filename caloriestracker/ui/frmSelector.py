from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QLabel, QComboBox, QDialog, QDialogButtonBox, QWidget, QTableWidgetItem, QVBoxLayout, QToolButton, QHBoxLayout
from logging import debug
from .myqtablewidget import myQTableWidget
#from .. myqwidgets import qmessagebox

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
        
    def setManagers(self, settings, settingsSection,  settingsObject, manager, selected, *initparams):
        self.settings=settings
        self.settingsSection=settingsSection
        self.settingsObject=settingsObject
        self.widget.setManagers(settings, settingsSection, settingsObject, manager, selected, *initparams)
        self.resize(self.settings.value("{}/{}_dialog_size".format(self.settingsSection, self.settingsObject), QSize(800, 600)))

    def exec_(self):
        QDialog.exec_(self)
        self.settings.setValue("{}/{}_dialog_size".format(self.settingsSection, self.settingsObject), self.size())
        debug("Selected objects: {}".format(str(self.widget.selected.arr)))

    def setLabel(self, s):
        self.lbl.setText(s)

## Managers must use the same objects in arrays (same address)
## They are considered as objects, and it's representation is from __repr__ method
class wdgManagerSelector(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.mqtw=myQTableWidget(self)
        self.mqtw.showSearchOptions(True)
        self.mqtw.showSearchCloseButton(False)
        self.mqtwSelected=myQTableWidget(self)
        self.mqtwSelected.showSearchOptions(True)
        self.mqtwSelected.showSearchCloseButton(False)
        
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

    ## Hides Up and Down button
    def showUpDown(self):
        self.cmdDown.show()
        self.cmdUp.show()
        
    ## By default is True. Show Icons y tables and combobox 
    def showObjectIcons(self, boolean):
        self._showObjectIcons=boolean
        
    def setManagers(self, settings, settingsSection,  settingsObject, manager, selected, *initparams):
        self.settings=settings
        self.settingsSection=settingsSection
        self.settingsObject=settingsObject
        self.mqtw.settings(self.settings, self.settingsSection, "{}_tbl".format(self.settingsObject))
        self.mqtwSelected.settings(self.settings, self.settingsSection, "{}_tblSelected".format(self.settingsObject))
        
        self.manager=manager.clone(*initparams)#Clone manager to delete safely objects

        #removes selected objects from manager
        if selected is None:
            self.selected=manager.__class__(*initparams)
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
        for i, o in enumerate(self.selected.arr):
            self.mqtwSelected.table.setItem(i, 0, QTableWidgetItem(str(o)))
            if self._showObjectIcons==True:
                self.mqtwSelected.table.item(i, 0).setIcon(o.qicon())
        
    def _load_tbl(self):  
        self.mqtw.table.setColumnCount(1)
        self.mqtw.table.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Object")))
        self.mqtw.applySettings()
        self.mqtw.table.setRowCount(self.manager.length())
        for i, o in enumerate(self.manager.arr):
            self.mqtw.table.setItem(i, 0, QTableWidgetItem(str(o)))
            if self._showObjectIcons==True:
                self.mqtw.table.item(i, 0).setIcon(o.qicon())

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
        
    def on_tbl_cellDoubleClicked(self, row, column):
        self.on_cmdRight_released()
        
    def on_tblSelected_cellDoubleClicked(self, row, column):
        self.on_cmdLeft_released()
        

## This code use the following path to set Icons in qrc qt files
## - ":/reusingcode/search.png"
## Shows selected objects in a QComboBox. You can press a button to open frmManagerSelector
class cmbManagerSelector(QWidget):
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
                self.combo.addItem(o.qicon(), str(o))
            else:
                self.combo.addItem(str(o))

    def setManagers(self, settings, settingsSection, settingsObject, manager, selected,  *initparams):
        self.settings=settings
        self.frm.setManagers(settings, settingsSection, settingsObject, manager, selected, *initparams)
        if selected!=None:
            for o in selected.arr:
                if self._showObjectIcons==True:
                    self.combo.addItem(o.qicon(), str(o))
                else:
                    self.combo.addItem(str(o))

    ## Returns the selected manager
    def selected(self):
        return self.frm.widget.selected

if __name__ == '__main__':
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
            return QIcon(":/prueba.svg")
    
    class PruebaManager(ObjectManager_With_IdName):
        def __init__(self):
            ObjectManager_With_IdName.__init__(self)
            
    d={'one':1, 'two':2, 'three':3, 'four':4}
    manager=PruebaManager()
    for k, v in d.items():
        manager.append(Prueba(v, k))
        
    selected=PruebaManager()
    selected.append(manager.arr[3])
    
    mem=Mem()
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])

    w = cmbManagerSelector()
    #w.frm.widget.hideUpDown()
    w.setManagers(mem.settings,"frmSelectorExample", "frmSelector", manager, selected)
    w.move(300, 300)
    w.setWindowTitle('frmSelector example')
    w.show()
    
    app.exec()
