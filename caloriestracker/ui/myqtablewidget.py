## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from PyQt5.QtCore import Qt,  pyqtSlot, QObject,  pyqtSignal
from PyQt5.QtGui import QKeySequence, QColor, QIcon, QBrush, QFont
from PyQt5.QtWidgets import QApplication, QHeaderView, QTableWidget, QFileDialog,  QTableWidgetItem, QWidget, QCheckBox, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QAction, QMenu, QToolButton, QAbstractItemView
from .. call_by_name import call_by_name
from .. datetime_functions import dtaware2string, dtaware_changes_tz, time2string
from .. libmanagers import ManagerSelectionMode
from .. casts import lor_remove_columns
from officegenerator import ODS_Write
from logging import info, debug, error
from datetime import datetime, date,  timedelta


## By default setselectionmode is object
## This widget uses the next qt resources for icons, you must set this resources in your app
## - :/reusingcode/button_cancel.png
## - :/reusingcode/libreoffice_calc.png
## - :/reusingcode/search.png
## - :/reusingcode/sort_down.png
## - :/reusingcode/sort_up.png

class mqtw(QWidget):
    setDataFinished=pyqtSignal()
    tableSelectionChanged=pyqtSignal()
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent=parent
        self.lay=QVBoxLayout()
        self.laySearch=QHBoxLayout()
        self.lbl=QLabel()

        self.table=QTableWidget()
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.verticalScrollBar().valueChanged.connect(self.on_table_verticalscrollbar_value_changed)
        self.table.horizontalHeader().sectionClicked.connect(self.on_table_horizontalHeader_sectionClicked)
        self.table.itemSelectionChanged.connect(self.on_itemSelectionChanged)
        self.table.verticalHeader().hide()
        self.setSelectionMode(QAbstractItemView.SelectRows, QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

        self.lbl.setText(self.tr("Add a string to filter rows"))
        self.txtSearch=QLineEdit()
        self.txtSearch.textChanged.connect(self.on_txt_textChanged)
        self.cmdCloseSearch=QToolButton()
        self.cmdCloseSearch.setIcon(QIcon(":/reusingcode/button_cancel.png"))
        self.showSearchOptions(False)
        self.cmdCloseSearch.released.connect(self.on_cmdCloseSearch_released)
        self.laySearch.addWidget(self.lbl)
        self.laySearch.addWidget(self.txtSearch)
        self.laySearch.addWidget(self.cmdCloseSearch)
        self.lay.addWidget(self.table)
        self.table.verticalScrollBar().valueChanged.connect(self.on_table_verticalscrollbar_value_changed)
        self.lay.addLayout(self.laySearch)
        self.setLayout(self.lay)
        
        self.actionExport=QAction(self.tr("Export to Libreoffice Calc"))
        self.actionExport.setIcon(QIcon(":/reusingcode/libreoffice_calc.png"))
        self.actionExport.triggered.connect(self.on_actionExport_triggered)
        
        self.actionSizeMinimum=QAction(self.tr("Minimum column size"))
        self.actionSizeMinimum.triggered.connect(self.on_actionSizeMinimum_triggered)
        self.actionSizeNeeded=QAction(self.tr("Needed column size"))
        self.actionSizeNeeded.triggered.connect(self.on_actionSizeNeeded_triggered)
        
        self.actionSearch=QAction(self.tr("Search in table"))
        self.actionSearch.setIcon(QIcon(":/reusingcode/search.png"))
        self.actionSearch.triggered.connect(self.on_actionSearch_triggered)
        self.actionSearch.setShortcut(Qt.CTRL + Qt.Key_F)
        
        self._last_height=None
        self._none_at_top=True
        self._sort_action_reverse=None#Needed for first setData
        self._ordering_enabled=False
        self.selected=None #Must be initializated
        self.selected_items=None
        self.auxiliar=None #Auxiliar value, sometimes I need to pass some value between mqtw and myqtw_additional (For example, active), this attribute helps to do it
        
    ## Sets if ordering must be enabled
    ## In mqtw id False by default. In mqtwManager and mqtwObjects is True by default
    ## @param boolean Booleano to set if ordering is enabled
    def setOrderingEnabled(self, boolean):
        self._ordering_enabled=boolean

    @pyqtSlot()
    ## This is for mqtw only object
    def on_itemSelectionChanged(self):        
        self.selected_items=None
        self.selected=None
        if hasattr(self, "data"):#Data is set
            if self.table.selectionBehavior()==QAbstractItemView.SelectRows and self.table.selectionMode()==QAbstractItemView.SingleSelection:
                # In this case returns a list with all items of the row
                self.selected_items=[]
                self.selected=[]
                for i in self.table.selectedItems():
                    if i.row()>=len(self.data):## Se pulsa un row fuera del data, por ejemplo un total
                        self.selected_items==None
                        self.selected==None
                        break
                    self.selected_items.append(i)
                    self.selected.append(self.itemData(i))
            elif self.table.selectionBehavior()==QAbstractItemView.SelectRows and self.table.selectionMode()==QAbstractItemView.MultiSelection:
                # In this case returns a list or rows
                error("This method fails if there is a wdgBool due to selecteditems only shows QTableWidgetItem")
                self.selected_items=[]
                self.selected=[]
                lastrow=[]
                lastrowitems=[]
                for i in self.table.selectedItems():
                    if i.row()>=len(self.data):## Se pulsa un row fuera del data, por ejemplo un total
                        self.selected_items==None
                        self.selected==None
                        break
                    lastrowitems.append(i)
                    lastrow.append(self.itemData(i))
                    if len(lastrow)==self.lengthRow():#Create a new row if len lastrow == leng. Minus 1 because it adds the last
                        self.selected.append(lastrow)
                        self.selected_items.append(lastrowitems)
                        lastrow=[]
                        lastrowitems=[]
            elif self.table.selectionBehavior()==QAbstractItemView.SelectItems and self.table.selectionMode()==QAbstractItemView.SingleSelection:
                # Returns the item selected
                for i in self.table.selectedItems():
                    if i.row()>=len(self.data):## Se pulsa un row fuera del data, por ejemplo un total
                        self.selected_items==None
                        self.selected==None
                        break
                    self.selected_items=i
                    self.selected=self.itemData(i)
            debug("{} data selection: {}".format(self.__class__.__name__,  self.selected))
            self.tableSelectionChanged.emit()
        else:
            debug("ItemSectionChanged without self.setData")

    ## You can obtain data value from an item
    def itemData(self,item):
        return self.data[item.row()][item.column()]

    def on_generic_customContextMenuRequested(self, pos):
        self.qmenu().exec_(self.table.mapToGlobal(pos))
        
    def setGenericContextMenu(self):
        self.table.customContextMenuRequested.connect(self.on_generic_customContextMenuRequested)
        
    ## Strikes out all qtablewidgetitem in a row
    ## @param row int Row index
    def setRowStrikeOut(self, row):
        for i in range(self.table.horizontalHeader().count()):
            qtwiSetStrikeOut(self.table.item(row, i))

    ## @param selectionBehavior are tags from Qt QAbstractItemView (SelectRows, SelectItems...)
    ## @param selectionMode are tags from Qt QAbstractItemView (SingleSelection, MultiSelection)
    def setSelectionMode(self, selectionBehavior, selectionMode):
        self.table.setSelectionBehavior(selectionBehavior)
        self.table.setSelectionMode(selectionMode)

    def setVerticalHeaderHeight(self, height):
        """height, if null default.
        Must be after settings"""
        if height==None:
            self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self._last_height=None
        else:
            self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.table.verticalHeader().setDefaultSectionSize(height) 
            self._last_height=height

    def sectionResized(self, logicalIndex, oldSize, newSize):
        self.table.horizontalHeader().setStretchLastSection(False)
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            for i in range(self.table.columnCount()):
                self.table.setColumnWidth(i, newSize)
            self._settings.setValue("{}/{}_horizontalheader_state".format(self._settingsSection, self._settingsObject), self.table.horizontalHeader().saveState() )
            debug("Saved {}/{}_horizontalheader_state to equal sizes".format(self._settingsSection, self._settingsObject))
            self._settings.sync()
        elif modifiers == Qt.ControlModifier:
            self.on_actionSizeMinimum_triggered()
        else:
            self._settings.setValue("{}/{}_horizontalheader_state".format(self._settingsSection, self._settingsObject), self.table.horizontalHeader().saveState() )
            debug("Saved {}/{}_horizontalheader_state manually".format(self._settingsSection, self._settingsObject))
            self._settings.sync()

    @pyqtSlot(int)
    def on_table_verticalscrollbar_value_changed(self, value):
        if value % 3 ==1:
            self.on_actionSizeNeeded_triggered()

    def setSettings(self, settings, settingsSection,  objectname):
        self._settings=settings #Made private due it had the same name of the method
        #For all myQTableWidget in settings app
        self.setVerticalHeaderHeight(int(self._settings.value("myQTableWidget/rowheight", 24)))
        self._settingsSection=settingsSection
        self._settingsObject=objectname
        self.setObjectName(self._settingsObject)
        
    def settings(self):
        return self._settings

    def clear(self):
        """Clear table"""
        self.table.setRowCount(0)
        self.table.clearContents()
    
    ## Resizes columns if column width is less than table hin
    def wheelEvent(self, event):
        self.on_actionSizeNeeded_triggered()
        event.accept()

    @pyqtSlot()
    def keyPressEvent(self, event):
        if  event.matches(QKeySequence.ZoomIn) and self._last_height!=None:
            height=int(self._settings.value("myQTableWidget/rowheight", 24))
            self._settings.setValue("myQTableWidget/rowheight", height+1)
            info("Setting myQTableWidget/rowheight set to {}".format(self._settings.value("myQTableWidget/rowheight", 24)))
            self.table.setVerticalHeaderHeight(int(self._settings.value("myQTableWidget/rowheight", 24)))
        elif  event.matches(QKeySequence.ZoomOut) and self._last_height!=None:
            height=int(self._settings.value("myQTableWidget/rowheight", 24))
            self._settings.setValue("myQTableWidget/rowheight", height-1)
            ("Setting myQTableWidget/rowheight set to {}".format(self._settings.value("myQTableWidget/rowheight", 24)))
            self.table.setVerticalHeaderHeight(int(self._settings.value("myQTableWidget/rowheight", 24)))
        elif event.matches(QKeySequence.Print):
            filename = QFileDialog.getSaveFileName(self, self.tr("Save File"), "table.ods", self.tr("Libreoffice calc (*.ods)"))[0]
            if filename:
                ods=ODS_Write(filename)
                self.officegeneratorModel( "My table").ods_sheet(ods)
                ods.save()

    ## Used to order using clicks in headers
    def on_table_horizontalHeader_sectionClicked(self, index):
        if hasattr(self, "data")==True and self._ordering_enabled==True:
            self.actionListOrderBy[index].triggered.emit()

    ## Used to order table progamatically
    def setOrderBy(self, index, reverse):
        if self._ordering_enabled==True:
            action=self.actionListOrderBy[index]
            if reverse==True:#Sort is made with action text, so I have to emulate. Text is changed from droawOrder By. It's how I will find in menu
                action.setText(action.text() + " (desc)")
            else: #No encontrado
                action.setText(action.text().replace(self.tr(" (desc)"),""))
            action.triggered.emit()
            
    ## When data is loaded, usually it's from an ordered manager of an ordered sql, to avoid displaying and ordering data twice, you can only draw Order by in widget
    def drawOrderBy(self, index, reverse):
        if self._ordering_enabled==True:
            action=self.actionListOrderBy[index]
            # Sets if its reverse or not and renames action
            if reverse==True:
                action.setText(action.text().replace(self.tr(" (desc)"),""))
                action.setIcon(QIcon(":/reusingcode/sort_up.png"))
                self.table.horizontalHeaderItem(index).setIcon(QIcon(":reusingcode/sort_down.png"))
            else: #No encontrado
                action.setText(action.text() + " (desc)")
                action.setIcon(QIcon(":/reusingcode/sort_down.png"))
                self.table.horizontalHeaderItem(index).setIcon(QIcon(":reusingcode/sort_up.png"))

            # Remover others (desc), to the rest of actions
            for i, other_action in enumerate(self.actionListOrderBy):
                if i!=index:# Different to selected action index
                    other_action.setText(other_action.text().replace(self.tr(" (desc)"),""))

    ## Order data columns. None values are set at the beginning
    def on_orderby_action_triggered(self):
        action=QObject.sender(self)#Busca el objeto que ha hecho la signal en el slot en el que está conectado
        self._sort_action_index=self.hh.index(action.text().replace(" (desc)",""))#Search the position in the headers of the action Text
        if action.text().find(self.tr(" (desc)"))>0:
            self._sort_action_reverse=True
        else: #No encontrado
            self._sort_action_reverse=False
        output="Order {}/{} by '{}'".format(self._settingsSection, self._settingsObject, self.actionListOrderBy[self._sort_action_index].text())#Must be set before changing direction        # -----------------------------------------------------------------------------
        start=datetime.now()
        nonull=[]
        null=[]
        for row in self.data:
            if row[self._sort_action_index] is None:
                null.append(row)
            else:
                nonull.append(row)
        try:
            nonull=sorted(nonull, key=lambda c: c[self._sort_action_index],  reverse=self._sort_action_reverse)
        except:
            debug("I couldn't order column due to there are different types on it.")
        if self._none_at_top==True:#Set None at top of the list
            if self._sort_action_reverse==False:# Desc must put None on the other side
                self.data=null+nonull
            else:
                self.data=nonull+null
        else:
            if self._sort_action_reverse==False:
                self.data=nonull+null
            else:
                self.data=null+nonull
        debug("{} took {}".format(output, datetime.now()-start))
        self.update()
        self.drawOrderBy(self._sort_action_index, self._sort_action_reverse)

    def update(self):
        self.setData(self.hh, self.hv, self.data, self.data_decimals, self.data_zonename)

    def applySettings(self):
        """settings must be defined before"""
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().sectionResized.connect(self.sectionResized)
        self.table.horizontalHeader().setStretchLastSection(False)
        state=self._settings.value("{}/{}_horizontalheader_state".format(self._settingsSection, self._settingsObject))
        if state:
            self.table.horizontalHeader().restoreState(state)
        
    ## Adds a horizontal header array , a vertical header array and a data array
    ##
    ## Automatically set alignment
    ## @param decimals int or list with the columns decimals
    def setData(self, header_horizontal, header_vertical, data, decimals=2, zonename='UTC'):
        ## Affeter selection an action of the OrderByAction list, returns its information, to be used in several classes

        start=datetime.now()
        if decimals.__class__.__name__=="int":
            decimals=[decimals]*len(header_horizontal)
        self.data_decimals=decimals
        self.data_zonename=zonename

        # Creates order actions here after creating data
        if hasattr(self,"actionListOrderBy")==False and self._ordering_enabled==True:
            self.actionListOrderBy=[]
            for header in header_horizontal:
                action=QAction("{}".format(header))
                self.actionListOrderBy.append(action)
                action.triggered.connect(self.on_orderby_action_triggered)
                action.setIcon(QIcon(":/reusingcode/sort_up.png"))

        # Headers
        self.hh=header_horizontal
        self.hv=header_vertical
        self.data=data

        self.table.setColumnCount(len(self.hh))
        if self.hh is not None:
            for i in range(len(self.hh)):
                self.table.setHorizontalHeaderItem(i, QTableWidgetItem(self.hh[i]))
        if self.hv is not None:
            self.table.verticalHeader().show()
            self.table.setRowCount(len(self.data))# To do not lose data
            for i in range(len(self.hv)):
                self.table.setVerticalHeaderItem(i, QTableWidgetItem(self.hv[i]))

        # Data
        self.applySettings()
        self.table.clearContents()
        self.table.setRowCount(len(self.data))
        for row in range(len(self.data)):
            for column in range(len(self.hh)):
                wdg=self.object2qtablewidgetitem(self.data[row][column], decimals[column], zonename)
                if wdg.__class__.__name__=="QWidget":#wdgBool
                    self.table.setCellWidget(row, column, wdg)
                else:#qtablewidgetitem
                    self.table.setItem(row, column, wdg)
        self.setDataFinished.emit()
        debug("Set data to {}/{} took {}".format(self._settingsSection, self._settingsObject, datetime.now()-start))

    def print(self, hh, hv, data):
        print(hh)
        for i, row in enumerate(data):
            print (hv[i] , row)
            
        print ("Len hh:", len(hh))
        print ("Len hv:", len(hv))
        print ("Len data:", len(data[0]), "x", len(data))
            
    ## If true None values are set at the top of the list after sorting. If not at the bottom of the list
    def setNoneAtTop(self,boolean):
        self._none_at_top=boolean

    ## Converts a objecct class to a qtablewidgetitem
    def object2qtablewidgetitem(self, o, decimals=2, zonename="UTC"):
        if o.__class__.__name__ in ["int"]:
            return qright(o)
        elif o.__class__.__name__ in ["datetime"]:
            return qdatetime(o,zonename)
        elif o.__class__.__name__ in ["date"]:
            return qdate(o)
        elif o.__class__.__name__ in ["time"]:
            return qtime(o)
        elif o.__class__.__name__ in ["float","Decimal"]:
            return qnumber(o,decimals)
        elif o.__class__.__name__ in ["Percentage",]:
            return qpercentage(o, decimals)
        elif o.__class__.__name__ in ["Money","Currency"]:
            return qcurrency(o, decimals)
        elif o.__class__.__name__ in ["bool", ]:
            return wdgBool(o)
        elif o is None:
            return qnone()
        elif o=="":
            return qempty()
        elif o=="#crossedout":
            return qcrossedout()
        else:            
            return qleft(o)

    ## Adds a row in a table, with values
    ## @param row integer with the row to add
    def addRow(self, row, value_list, decimals=2, zonename="UTC"):
        for column, value in enumerate(value_list):
            wdg=self.object2qtablewidgetitem(value, decimals, zonename)
            if wdg.__class__.__name__=="QWidget":# For example wdgBool
                    self.table.setCellWidget(row, column, wdg)
            else:#QTablewidgetitem
                self.table.setItem(row, column, wdg) 

    ## Returns a list of strings with the horizontal headers
    def listHorizontalHeaders(self):
        if self.hh is None:
            return None
        header=[]
        for i in range(self.table.horizontalHeader().count()):
            header.append(self.table.horizontalHeaderItem(i).text())
        return header

    ## Returns a list of strings with the horizontal headers
    def listVerticalHeaders(self):
        if self.hv is None:
            return None
        header=[]
        for i in range(self.table.verticalHeader().count()):
            if self.table.verticalHeaderItem(i) is not None:
                header.append(self.table.verticalHeaderItem(i).text())
        return header

    ## Returns a lisf of rows with the text of the 
    def listText(self):
        data=[]
        for i in range(self.table.rowCount()):
            row=[]
            for column in range(self.table.columnCount()):
                data.append(self.table.item(row,column).text())
        return data

    def on_cmdCloseSearch_released(self):
        self.txtSearch.setText("")
        self.showSearchOptions(False)
        
    def showSearchOptions(self, boolean):
        if boolean==True:
            self.lbl.show()
            self.txtSearch.show()
            self.cmdCloseSearch.show()
        else:
            self.lbl.hide()
            self.txtSearch.hide()
            self.cmdCloseSearch.hide()
            
    def showSearchCloseButton(self, boolean):
        if boolean==True:
            self.cmdCloseSearch.show()
        else:
            self.cmdCloseSearch.hide()

    def on_actionExport_triggered(self):
        filename = QFileDialog.getSaveFileName(self, self.tr("Save File"), "table.ods", self.tr("Libreoffice calc (*.ods)"))[0]
        if filename:
            ods=ODS_Write(filename)
            self.officegeneratorModel("My table").ods_sheet(ods)
            ods.save()

    def on_actionSizeMinimum_triggered(self):
        self.table.resizeRowsToContents()
        self.table.resizeColumnsToContents()
        self._settings.setValue("{}/{}_horizontalheader_state".format(self._settingsSection, self._settingsObject), self.table.horizontalHeader().saveState() )
        self._settings.sync()
        debug("Saved {}/{}_horizontalheader_state to minimum".format(self._settingsSection, self._settingsObject))

    def on_actionSizeNeeded_triggered(self):
        for i in range(self.table.columnCount()):
            if self.table.sizeHintForColumn(i)>self.table.columnWidth(i):
                self.table.setColumnWidth(i, self.table.sizeHintForColumn(i))
        self._settings.setValue("{}/{}_horizontalheader_state".format(self._settingsSection, self._settingsObject), self.table.horizontalHeader().saveState() )
        self._settings.sync()
        debug("Saved {}/{}_horizontalheader_state to needed".format(self._settingsSection, self._settingsObject))

    def on_actionSearch_triggered(self):
        self.lbl.show()
        self.txtSearch.show()
        self.cmdCloseSearch.show()
        self.txtSearch.setFocus()

    ## Returns a qmenu to be used in other qmenus
    def qmenu(self, title="Table options"):
        menu=QMenu(self.parent)
        menu.setTitle(self.tr(title))
        menu.addAction(self.actionExport)
        menu.addSeparator()
        menu.addAction(self.actionSearch)
        menu.addSeparator()
        if hasattr(self,"actionListOrderBy")==True and self._ordering_enabled==True:
            order=QMenu(menu)
            order.setTitle(self.tr("Order by"))
            for action in self.actionListOrderBy:
                order.addAction(action)
            menu.addMenu(order)
        size=QMenu(menu)
        size.setTitle(self.tr("Columns size"))
        size.addAction(self.actionSizeMinimum)
        size.addAction(self.actionSizeNeeded)
        menu.addMenu(size)
        return menu

    def on_txt_textChanged(self, text):
        for row in range(self.table.rowCount()):
            found=False
            for column in range(self.table.columnCount()):
                item=self.table.item(row,column)
                if item is not None and item.text().lower().find(text.lower())>=0:
                    found=True
                    break
            if found==False:
                self.table.hideRow(row)
            else:
                self.table.showRow(row)

    def officegeneratorModel(self, title="sheet"):
        def pixel2cm(pixels):
            #Converts size in pixels to cm
            PixelWidthDimension = self.logicalDpiX()# width dots per inch
            inch = pixels/PixelWidthDimension
            cm= inch*2.54*(1+0.05)
            return cm
        # # # # # # # # # #
        widths=[]
        vwidth=pixel2cm(self.table.verticalHeader().width())
        for i in range(self.table.columnCount()):
            widths.append(pixel2cm(self.table.columnWidth(i)))

        from officegenerator.standard_sheets import Model
        m=Model()
        m.setTitle(title)
        m.setHorizontalHeaders(self.listHorizontalHeaders(), widths)
        m.setVerticalHeaders(self.listVerticalHeaders(),vwidth)
        if len(self.data)>0 and self.__class__==mqtwObjects: #Need to remove last column (object column)
            data=lor_remove_columns(self.data, [len(self.data[0])-1, ])
        else:
            data=self.data
        m.setData(data)
        return m

    ## Returns the length of self.data. Additional functions doesn't affect this result
    ## If we are using a mqtwObjects, self.data has the same length as self.objects(), so it's fine
    def length(self):
        return len(self.data)
        
    ## REturns the len of a row using len of hh. If not uses len of self.data[0], if no returns 0
    def lengthRow(self):
        if self.hh is not None:
            return len(self.hh)
        elif self.length()>0:
            return len (self.data[0])
        else:
            return 0



## Uses data, but the last column of data it's the object of the row
## It's not a manager, but it's similar
## Used when Table is too complex for mqtwManager
##
## Selection is managed by self.mqtw.selected, not by self.manager, it's a data mqtw

class mqtwObjects(mqtw):
    def __init__(self, parent):
        mqtw.__init__(self, parent)
        self._ordering_enabled=True
        
    ## Return the last index of a row, where the object is
    def objectColumnIndex(self):
        return len(self.hh)
        
    ## @param row integer
    def object(self, row):
        if row<self.length(): #Additional methods can add rows programatically
            return self.data[row][self.objectColumnIndex()]
        return None

    ## Returns a list of objects in self.data. Usefull to set additional data
    def objects(self):
        r=[]
        for i in range(len(self.data)):
            r.append(self.object(i))
        return r

    @pyqtSlot()
    def on_itemSelectionChanged(self):
        self.selected_items=None
        self.selected=None
        if hasattr(self, "data"):#Data is set
            if self.table.selectionBehavior()==QAbstractItemView.SelectRows and self.table.selectionMode()==QAbstractItemView.SingleSelection:
                # In this case returns selected the object, selected_items a list of items. If there isn't selection returns [] and None
                self.selected_items=[]
                self.selected=None
                for i in self.table.selectedItems():
                    self.selected_items.append(i)
                    if i.column()==0:
                        self.selected=self.object(i.row())
            elif self.table.selectionBehavior()==QAbstractItemView.SelectRows and self.table.selectionMode()==QAbstractItemView.MultiSelection:
                # In this case returns a list or rows for items and a list of objects for values
                error("selected_items fails if there is a wdgBool due to selecteditems only shows QTableWidgetItem")
                self.selected_items=[]
                self.selected=[]
                lastrow=[]
                lastrowitems=[]
                for i in self.table.selectedItems():
                    lastrowitems.append(i)
                    if len(lastrow)==self.lengthRow():#Create a new row if len lastrow == leng. Minus 1 because it adds the last
                        self.selected_items.append(lastrowitems)
                        lastrowitems=[]
                    if i.column()==0:
                        self.selected.append(self.object(i.row()))
            elif self.table.selectionBehavior()==QAbstractItemView.SelectItems and self.table.selectionMode()==QAbstractItemView.SingleSelection:
                # Returns the item selected and the value of the item
                self.selected_items=None
                self.selected=None
                for i in self.table.selectedItems():
                    self.selected_items=i
                    self.selected=self.itemData(i)
            debug("{} data objects selection: {}".format(self.__class__.__name__,  self.selected))
            self.tableSelectionChanged.emit()
        else:
            debug("ItemSectionChanged without self.setData")

    ## Adds a horizontal header array , a vertical header array and a data array
    ##
    ## Automatically set alignment
    ## @param header_horizontal List
    ## @param header_vertical List
    ## @param data lor
    ## @param decimals
    ## @param zonename
    ## @param additional Function without it's call, to add additional table information like Total Rows or icons. Additional method has only one parameter, mqtw
    def setDataWithObjects(self, header_horizontal, header_vertical, data, decimals=2, zonename='UTC', additional=None):
        self.additional=additional
        self.data=data

        # Sets data
        self.setData(header_horizontal, header_vertical, data, decimals, zonename)

        if additional is not None:
            self.additional(self)

    def update(self):
        self.setDataWithObjects(self.hh, self.hv, self.data, self.data_decimals, self.data_zonename, additional=self.additional)

class mqtwManager(mqtw):
    def __init__(self, parent):
        mqtw.__init__(self, parent)
        self._ordering_enabled=True

    def on_itemSelectionChanged(self):
        self.manager.cleanSelection()
        for i in self.table.selectedItems():#itera por cada item no row.
            if i.column()==0:
                if self.manager.selectionMode()==ManagerSelectionMode.Object:
                    self.manager.selected=self.manager.object(i.row())
                elif self.manager.selectionMode()==ManagerSelectionMode.List:
                    self.manager.selected.append(self.manager.object(i.row()))
        debug("{} manager selection: {}".format(self.manager.__class__.__name__,  self.manager.selected))
        self.tableSelectionChanged.emit()

    ## @param header_horizontal List
    ## @param header_vertical List
    ## @param manager ObjectManager
    ## @param manager_attributes
    ## @param decimals
    ## @param zonename
    ## @param additional Function without it's call, to add additional table information like Total Rows or icons. Additional method has only one parameter, mqtw
    def setDataFromManager(self, header_horizontal, header_vertical, manager, manager_attributes, decimals=2, zonename='UTC', additional=None):
        self.manager_attributes=manager_attributes
        self.manager=manager
        self.additional=additional

        #Sets manager selection mode and table
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        if self.manager.selectionMode()==ManagerSelectionMode.Object:
            self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        else:
            self.table.setSelectionMode(QAbstractItemView.MultiSelection)

        # Sets data
        data=[]
        for o in manager.arr:
            row=[]
            for attribute in self.manager_attributes:
                row.append(call_by_name(o,attribute))
            data.append(row)
        self.setData(header_horizontal, header_vertical, data, decimals, zonename)

        if additional is not None:
            self.additional(self)

    ## Order data columns. None values are set at the beginning
    def on_orderby_action_triggered(self):
        action=QObject.sender(self)#Busca el objeto que ha hecho la signal en el slot en el que está conectado 
        self._sort_action_index=self.hh.index(action.text().replace(" (desc)",""))#Search the position in the headers of the action Text
        if action.text().find(self.tr(" (desc)"))>0:
            self._sort_action_reverse=True
        else: #No encontrado
            self._sort_action_reverse=False
        output="Order {}/{} by '{}'".format(self._settingsSection, self._settingsObject, self.actionListOrderBy[self._sort_action_index].text())#Must be set before changing direction
        start=datetime.now()
        self.manager.order_with_none(self.manager_attributes[self._sort_action_index], reverse=self._sort_action_reverse, none_at_top=self._none_at_top)
        debug("{} took {}".format(output, datetime.now()-start))
        self.update()        
        self.drawOrderBy(self._sort_action_index, self._sort_action_reverse)

    def update(self):
        self.setDataFromManager(self.hh, self.hv, self.manager, self.manager_attributes, self.data_decimals, self.data_zonename, additional=self.additional)


## @return qtablewidgetitem
def qbool(bool):
    """Prints bool and check. Is read only and enabled"""
    a=QTableWidgetItem()
    a.setFlags( Qt.ItemIsSelectable |  Qt.ItemIsEnabled )#Set no editable
    if bool:
        a.setCheckState(Qt.Checked);
        a.setText(QApplication.translate("Core","True"))
    else:
        a.setCheckState(Qt.Unchecked);
        a.setText(QApplication.translate("Core","False"))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
    return a

## Center checkbox
## You must use with table.setCellWidget(0,0,wdgBool)
## Is disabled to be readonly
## @return qwidget
def wdgBool(bool):
    pWidget = QWidget()
    pCheckBox = QCheckBox();
    pCheckBox.setAttribute(Qt.WA_TransparentForMouseEvents);
    pCheckBox.setFocusPolicy(Qt.NoFocus)
    if bool:
        pCheckBox.setCheckState(Qt.Checked);
    else:
        pCheckBox.setCheckState(Qt.Unchecked);
    pLayout = QHBoxLayout(pWidget);
    pLayout.addWidget(pCheckBox);
    pLayout.setAlignment(Qt.AlignCenter);
    pLayout.setContentsMargins(0,0,0,0);
    pWidget.setLayout(pLayout)
    return pWidget

## Returns a QTableWidgetItem representing an empty value
def qnone():
    return qcenter("- - -")

## Returns a QTableWidgetItem representing an empty value
def qempty():
    return qleft("")

def qcenter(string):
    if string==None:
        return qnone()
    a=QTableWidgetItem(str(string))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignCenter)
    return a
    
def qcrossedout():
    a=qempty()
    brush = QBrush(QColor(0, 0, 0))
    brush.setStyle(Qt.BDiagPattern)
    a.setBackground(brush)
    return a

## Currency object from reusingcode
def qcurrency(currency, decimals=2):
    if currency is None or currency.amount is None:
        return qnone()
    a=QTableWidgetItem(currency.string(decimals))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    if currency.amount==None:
        a.setForeground(QColor(0, 0, 255))
    elif currency.amount<0:
        a.setForeground(QColor(255, 0, 0))
    return a

def qleft(string):
    if string==None:
        return qnone()
    a=QTableWidgetItem(str(string))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignLeft)
    return a

def qright(string):
    if string==None:
        return qnone()
    a=QTableWidgetItem(str(string))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    return a

## Creates a QTableWidgetItem with the date
def qdate(date):
    if date==None:
        return qnone()
    return qright(date)

## dt es un datetime con timezone, que se mostrara con la zone pasado como parametro
## Convierte un datetime a string, teniendo en cuenta los microsehgundos, para ello se convierte a datetime local
def qdatetime(dt, tz_name):
    newdt=dtaware_changes_tz(dt, tz_name)
    if newdt==None:
        return qnone()
    a=QTableWidgetItem(dtaware2string(newdt, "%Y-%m-%d %H:%M:%S"))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    return a


def qnumber(n, digits=2):
    if n==None:
        return qnone()
    n=round(n, digits)
    a=qright(n)
    if n<0:
        a.setForeground(QColor(255, 0, 0))
    return a

## Colorizes a number comparing it with a limit
def qnumber_limited(n, limit, digits=2, reverse=False):
    if n==None:
        return qnone()
    a=qnumber(n, 2)
    if reverse==True:
        color_above=QColor(148, 255, 148)
        color_under=QColor(255, 148, 148)
    else:        
        color_under=QColor(148, 255, 148)
        color_above=QColor(255, 148, 148)
    if n>=limit:
        a.setBackground(color_above)
    else:
        a.setBackground(color_under)
    return a

## Shows the time of a datetime
## See function time2string of datetime_functions to see formats
## @param ti must be a time object
## @param format
def qtime(ti, format="HH:MM:SS"):
    if ti==None:
        return qnone()
    item=qright(time2string(ti, format))
    if format=="Xulpymoney":
        if ti.microsecond==5:
            item.setBackground(QColor(255, 255, 148))
        elif ti.microsecond==4:
            item.setBackground(QColor(148, 148, 148))
    return item

def qpercentage(percentage, decimals=2):
    if percentage is None:
        return qnone()
    a=QTableWidgetItem(percentage.string(decimals))
    a.setTextAlignment(Qt.AlignVCenter|Qt.AlignRight)
    if percentage.value==None:
        a.setForeground(QColor(0, 0, 255))
    elif percentage.value<0:
        a.setForeground(QColor(255, 0, 0))
    return a
    
## Sets font to bold
## @param qtwi QTableWidgetItem
def qtwiSetBold(qtwi):
    font=QFont()
    font.setBold(True)
    qtwi.setFont(font)
    
## Text is set to strike out
## @param qtwi QTableWidgetItem
def qtwiSetStrikeOut(qtwi):
    font=QFont()
    font.setStrikeOut(True)
    qtwi.setFont(font)

def example():
    from libmanagers import ObjectManager_With_IdName_Selectable
    from PyQt5.QtCore import QSettings
    from base64 import b64encode

    class Mem:
        def __init__(self):
            self.settings=QSettings()
            self.name="namemem"
        def age(self, integer):
            return integer

    class Prueba:
        def __init__(self, id=None, name=None, date=None, datetime=None):
            self.id=id
            self.name=name
            self.date=date
            self.datetime=datetime
            self.pruebita=Mem()

    class PruebaManager(ObjectManager_With_IdName_Selectable):
        def __init__(self):
            ObjectManager_With_IdName_Selectable.__init__(self)

        def prueba(self, wdg):
            pass

    def __additional_with_objects(wdg):
        wdg.table.setRowCount(len(wdg.data)+1)
        wdg.table.setItem(len(wdg.data), 0 , qnone())
        for i, o in enumerate(wdg.objects()):
            if o.id==5:
                wdg.table.item(i , 0).setIcon(QIcon(":/reusingcode/search.png"))
            if o.id==6:
                qtwiSetBold(wdg.table.item(i, 0))
            if o.id==7:
                qtwiSetStrikeOut(wdg.table.item(i, 0))
            if o.id==8:
                wdg.setRowStrikeOut(i)

    def __on_mqtw_manager_customContextMenuRequested(pos):
        menu=QMenu()
        menu.addMenu(mqtw_manager.qmenu())
        menu.addSeparator()
        menu.addMenu(mqtw_manager.qmenu())
        menu.exec_(mqtw_manager.table.mapToGlobal(pos))

    manager_manager=PruebaManager()
    for i in range(100):
        manager_manager.append(Prueba(i, b64encode(bytes(str(i).encode('UTF-8'))).decode('UTF-8'), date.today()-timedelta(days=i), datetime.now()+timedelta(seconds=3758*i)))

    manager_data=PruebaManager()
    manager_data.append(Prueba(None,"Con None",date.today(),datetime.now()))
    manager_data.append(Prueba(None, "", None, None))
    manager_data.append(Prueba(None, None, None, None))
    manager_data.append(Prueba(None, "#crossedout", None, None))
    manager_data.append(Prueba(None, False, None, None))
    manager_data.append(Prueba(None, True, None, None))

    data=[]
    for o in manager_data.arr:
        data.append([o.id, o.name,  o.date,  o.datetime,  o.pruebita.name, o.pruebita.age(1)])
        
    data_object=[]
    for o in manager_manager.arr[0:10]:
        data_object.append([o.id, o.name,  o.date,  o.datetime,  o.pruebita.name, o.datetime.time(), o])

    mem=Mem()
    app = QApplication([])
    from importlib import import_module
    import_module("xulpymoney.images.xulpymoney_rc")
    w=QWidget()
    w.showMaximized()
    hv=None

    lay=QHBoxLayout(w)
    
    #mqtw
    mqtw_data = mqtw(w)
    mqtw_data.setSelectionMode(QAbstractItemView.SelectRows, QAbstractItemView.MultiSelection)
    mqtw_data.setGenericContextMenu()
    hv=["Johnny be good"]*len(data)
    mqtw_data.setSettings(mem.settings, "myqtablewidget", "mqtw")
    hh=["mqtw", "Name", "Date", "Last update","Mem.name", "Age"]
    mqtw_data.setData(hh, hv, data )
    
    #mqtw with object
    mqtw_data_with_object = mqtwObjects(w)
    mqtw_data_with_object.setSelectionMode(QAbstractItemView.SelectRows, QAbstractItemView.MultiSelection)
    mqtw_data_with_object.setGenericContextMenu()
    hv=["Johnny be good"]*len(data_object)
    mqtw_data_with_object.setSettings(mem.settings, "myqtablewidget", "mqtwObjects")
    hh=["mqtwObjects", "Name", "Date", "Last update","Mem.name", "Time"]
    mqtw_data_with_object.setDataWithObjects(hh, hv, data_object, additional=__additional_with_objects )
    mqtw_data_with_object.drawOrderBy(2,  True)

    #mqtwManager
    mqtw_manager = mqtwManager(w)    
    manager_manager.setSelectionMode(ManagerSelectionMode.List)
    mqtw_manager.table.customContextMenuRequested.connect(__on_mqtw_manager_customContextMenuRequested)
    mqtw_manager.setSettings(mem.settings, "myqtablewidget", "mqtwManager")
    hh=["Id", "Name", "Date", "Last update","Mem.name", "Age"]

    mqtw_manager.setDataFromManager(hh, None, manager_manager, ["id", "name", "date", "datetime", "pruebita.name", ("pruebita.age", [1, ])], additional=manager_manager.prueba)
    mqtw_manager.setOrderBy(2,  True)

    lay.addWidget(mqtw_data)
    lay.addWidget(mqtw_data_with_object)
    lay.addWidget(mqtw_manager)
    w.setWindowTitle('myQTableWidget example')
    w.resize(1400, 600)
    w.show()

    app.exec()
