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
        
    ## Override this to change manager
    def setWidgetType(self):
        self.widget=wdgManagerSelector(self)
        
    def setManagers(self, mem, section,  objectname, manager, selected, *initparams):
        self.mem=mem
        self.section=section
        self.objectname=objectname
        self.widget.setManagers(mem, section, objectname, manager, selected, *initparams)
        self.resize(self.mem.settings.value("{}/{}_dialog_size".format(self.section, self.objectname), QSize(800, 600)))

    def exec_(self):
        QDialog.exec_(self)
        self.mem.settings.setValue("{}/{}_dialog_size".format(self.section, self.objectname), self.size())
        debug("Selected objects: {}".format(str(self.widget.selected.arr)))

    def setLabel(self, s):
        self.lbl.setText(s)

## Managers must use the same objects in arrays (same address)
## They are considered as objects, and it's representation is from __repr__ method
class wdgManagerSelector(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.tbl=myQTableWidget(self)
        self.tblSelected=myQTableWidget(self)
        
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
        
        self.lay=QHBoxLayout(self)
        self.lay.addWidget(self.tbl)
        self.lay.addLayout(self.laybuttons)
        self.lay.addWidget(self.tblSelected)
        
        self.setObjectName("wdgManagerSelector")


    ## Hides Up and Down button
    def hideUpDown(self):
        self.cmdDown.hide()
        self.cmdUp.hide()
        
    def setManagers(self, mem, section,  objectname, manager, selected, *initparams):
        self.mem=mem
        self.section=section
        self.objectname=objectname
        self.tbl.settings(self.mem, self.section, "{}_tbl".format(self.objectname))
        self.tblSelected.settings(self.mem, self.section, "{}_tblSelected".format(self.objectname))
        
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
        self.tblSelected.setColumnCount(1)
        self.tblSelected.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Object")))
        self.tblSelected.applySettings() 
        self.tblSelected.setRowCount(self.selected.length())
        for i, o in enumerate(self.selected.arr):
            self.tblSelected.setItem(i, 0, QTableWidgetItem(str(o)))
        
    def _load_tbl(self):  
        self.tbl.setColumnCount(1)
        self.tbl.setHorizontalHeaderItem(0, QTableWidgetItem(self.tr("Object")))
        self.tbl.applySettings()
        self.tbl.setRowCount(self.manager.length())
        for i, o in enumerate(self.manager.arr):
                self.tbl.setItem(i, 0, QTableWidgetItem(str(o)))

    def on_cmdLeft_released(self):
        for i in self.tblSelected.selectedItems():
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
        for i in self.tbl.selectedItems():
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
        for i in self.tblSelected.selectedItems():
            pos=i.row()
        tmp=self.selected.arr[pos]
        self.selected.arr[pos]=self.selected.arr[pos-1]
        self.selected.arr[pos-1]=tmp
        self._load_tbl()
        self._load_tblSelected()             
        
    def on_cmdDown_released(self):
        pos=None
        for i in self.tblSelected.selectedItems():
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
        
        
## Shows selected objects in a QComboBox. You can press a button to open frmManagerSelector
class cmbManagerSelector(QWidget):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=None)
        self.combo=QComboBox(self)
        self.cmd=QToolButton(self)
        self.cmd.setToolTip(self.tr("Press to open a manager selector"))
        
        lay = QHBoxLayout(self)
        lay.addWidget(self.combo)
        lay.addWidget(self.cmd)
        
        self.frm=frmManagerSelector(self)
        
        self.cmd.released.connect(self.on_cmd_released)
        self.setIcons()
        
    def on_cmd_released(self):
        self.frm.exec_()
        self.combo.clear()
        for o in self.frm.widget.selected.arr:
            self.combo.addItem(str(o))
            
    ## Set widget icons from resources strings
    def setIcons(self, rsButton=":search"):
        if rsButton is not None:
            self.cmd.setIcon(QIcon(rsButton))
        

    def setManagers(self, mem, section, objectname, manager, selected,  *initparams):
        self.mem=mem
        self.frm.setManagers(mem, section, objectname, manager, selected, *initparams)
        if selected!=None:
            for o in selected.arr:
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
    w.frm.widget.hideUpDown()
    w.setManagers(mem,"frmSelectorExample", "frmSelector", manager, selected)
    w.move(300, 300)
    w.setWindowTitle('frmSelector example')
    w.show()
    
    app.exec()
