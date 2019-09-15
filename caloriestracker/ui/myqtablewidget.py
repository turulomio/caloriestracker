from PyQt5.QtCore import Qt,  pyqtSlot
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QHeaderView, QTableWidget, QFileDialog,  QTableWidgetItem
from .qtablewidgetitems import qright, qleft
from officegenerator import ODS_Write, Currency, Percentage,  Coord
import datetime
import logging
from decimal import Decimal

class myQTableWidget(QTableWidget):
    def __init__(self, parent):
        QTableWidget.__init__(self, parent)
        self.parent=parent
        self.mem=None
        self.sectionname=None
        self._save_settings=True
        self.setAlternatingRowColors(True)
        self.saved_printed=False#To avoid printing a lot of times
        self._last_height=None
        
        
    def setVerticalHeaderHeight(self, height):
        """height, if null default.
        Must be after settings"""
        if height==None:
            self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self._last_height=None
        else:
            self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
            self.verticalHeader().setDefaultSectionSize(height) 
            self._last_height=height

    def setSaveSettings(self, state):
        """Used when i don't want my columns with being saved"""
        self._save_settings=state

    def sectionResized(self, logicalIndex, oldSize, newSize):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            for i in range(self.columnCount()):
                self.setColumnWidth(i, newSize)
        elif modifiers == Qt.ControlModifier:
            self.resizeRowsToContents()
            self.resizeColumnsToContents()
        self.save()
            
            
    def save(self):
        if self._save_settings==True:
            self.mem.settings.setValue("{}/{}_horizontalheader_state".format(self.sectionname, self.objectName()), self.horizontalHeader().saveState() )
            if self.saved_printed==False: 
                print("Saved {}/{}_horizontalheader_state".format(self.sectionname, self.objectName()))
                self.saved_printed=True
        
    def settings(self, mem, sectionname,  objectname=None):
        """objectname used for dinamic tables"""
        self.mem=mem
        self.setVerticalHeaderHeight(int(self.mem.settings.value("myQTableWidget/rowheight", 24)))
        self.sectionname=sectionname
        if objectname!=None:
            self.setObjectName(objectname)

    def applySettings(self):
        """settings must be defined before"""
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.horizontalHeader().sectionResized.connect(self.sectionResized)
        state=self.mem.settings.value("{}/{}_horizontalheader_state".format(self.sectionname, self.objectName()))
        if state:
            self.horizontalHeader().restoreState(state)
        

    def clear(self):
        """Clear table"""
        self.setRowCount(0)
        self.clearContents()

    def verticalScrollbarAction(self,  action):
        """Resizes columns if column width is less than table hint"""
        for i in range(self.columnCount()):
            if self.sizeHintForColumn(i)>self.columnWidth(i):
                self.setColumnWidth(i, self.sizeHintForColumn(i))

    @pyqtSlot()
    def keyPressEvent(self, event):
        if  event.matches(QKeySequence.ZoomIn) and self._last_height!=None:
            height=int(self.mem.settings.value("myQTableWidget/rowheight", 24))
            self.mem.settings.setValue("myQTableWidget/rowheight", height+1)
            logging.info("Setting myQTableWidget/rowheight set to {}".format(self.mem.settings.value("myQTableWidget/rowheight", 24)))
            self.setVerticalHeaderHeight(int(self.mem.settings.value("myQTableWidget/rowheight", 24)))
        elif  event.matches(QKeySequence.ZoomOut) and self._last_height!=None:
            height=int(self.mem.settings.value("myQTableWidget/rowheight", 24))
            self.mem.settings.setValue("myQTableWidget/rowheight", height-1)
            ("Setting myQTableWidget/rowheight set to {}".format(self.mem.settings.value("myQTableWidget/rowheight", 24)))
            self.setVerticalHeaderHeight(int(self.mem.settings.value("myQTableWidget/rowheight", 24)))
        elif event.matches(QKeySequence.Print):
            filename = QFileDialog.getSaveFileName(self, self.tr("Save File"), "table.ods", self.tr("Libreoffice calc (*.ods)"))[0]
            if filename:
                Table2ODS(self.mem,filename, self, "My table")

    ## Adds a horizontal header array , a vertical header array and a data array
    ##
    ## Automatically set alignment
    def setData(self, header_horizontal, header_vertical, data):
        self.data_header_horizontal=header_horizontal
        self.data_header_vertical=header_vertical
        self.data=data
        self.setColumnCount(len(self.data_header_horizontal))
        for i in range(len(self.data)):
            self.setHorizontalHeaderItem(i, QTableWidgetItem(self.data_header_horizontal[i]))
        #DATA  
        self.applySettings()
        self.clearContents()
        
        self.setRowCount(self.length()+1)
        
        self.applySettings()
        self.setRowCount(self.length())        
        for row in len(self.data):
            for column in len(self.data_header_horizontal) :
                self.setitem(row, column, self.object2qtablewidgetitem(self.data[row][column]))
                    
    ## Converts a objecct class to a qtablewidgetitem
    def object2qtablewidgetitem(self, o):
        if o.__class__ in [int,  float, Decimal]:
            return qright(o)
        else:
            return qleft(o)
    ## Converts self.data to an other list with officegenerator objects
    def data2officegeneratordata(self, arr):
        r=[]
        for i,  row in enumerate(self.arr):
            for j,  column in enumerate(row):
                r.append(self.data[row][column])
            
            
class Table2ODS(ODS_Write):
    def __init__(self, mem, filename, table, title):
        ODS_Write.__init__(self, filename)
        self.mem=mem
        sheet=self.createSheet(title)
        #Array width
        widths=[]
        if not table.verticalHeader().isHidden():
            widths.append(table.verticalHeader().width()*0.90)
        for i in range(table.columnCount()):
            widths.append(table.columnWidth(i)*0.90)
        sheet.setColumnsWidth(widths)

        #firstcontentletter and firstcontentnumber
        if table.horizontalHeader().isHidden() and not table.verticalHeader().isHidden():
            coord=Coord("B1")
        elif not table.horizontalHeader().isHidden() and table.verticalHeader().isHidden():
            coord=Coord("A2")
        elif not table.horizontalHeader().isHidden() and not table.verticalHeader().isHidden():
            coord=Coord("B2")
        elif table.horizontalHeader().isHidden() and table.verticalHeader().isHidden():
            coord=Coord("A1")
        sheet.setSplitPosition(coord)
        #HH
        if not table.horizontalHeader().isHidden():
            for letter in range(table.columnCount()):
                sheet.add(Coord(coord.letter + "1").addColumn(letter), table.horizontalHeaderItem(letter).text(), "OrangeCenter")
        logging.debug("HH Done")
        #VH
        if not table.verticalHeader().isHidden():
            for number in range(table.rowCount()):
                try:#Caputuro cuando se numera sin items 1, 2, 3
                    sheet.add(Coord("A" + coord.number).addRow(number), table.verticalHeaderItem(number).text(), "YellowLeft")
                except:
                    pass
        logging.debug("VH Done")
        #Items
        for number in range(table.rowCount()):
            for letter in range(table.columnCount()):
                try:
                    o=self.itemtext2object(table.item(number, letter).text())
                    sheet.add(Coord(coord.string()).addColumn(letter).addRow(number),o, self.object2style(o))
                except:#Not a QTableWidgetItem or NOne
                    pass
        logging.debug("Items done")
        sheet.setCursorPosition(coord.letter+ str(table.rowCount()+2))
        self.save()

    def itemtext2object(self, t):
        """
            Convierte t en un Money, Percentage o lo deja como text
        """
        if t[-2:]==" %":
            try:
                number=Decimal(t.replace(" %", ""))
                return Percentage(number, 100)
            except:
                logging.info("Error converting percentage")
                pass
        elif t[-2:] in (" €"," $"):
           try:
                number=Decimal(t.replace(t[-2:], "").replace(".", "").replace(",", "."))
                return Currency(number, self.mem.currencies.find_by_symbol(t[-1:]).id)
           except:
                logging.info("Error converting Money")
        elif t.find(":")!=-1 and t.find("-")!=-1:
            try:
                return datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
            except:
                logging.info("Error convertir datetime {}".format(t))
        elif t.find("-")!=-1:
            try:
                return datetime.datetime.strptime(t, "%Y-%m-%d").date()
            except:
                logging.info("Error convertir date {}".format(t))
        elif t.find(".")!=-1:
            try:
                return Decimal(t)
            except:
                logging.info("Error convertir Decimal {}".format(t))
        else:
            try:
                return int(t)
            except:
                logging.info("Error convertir Integer {}".format(t))
        return t


    def object2style(self, o):
        """
            Define el style de un objeto
        """
        if o.__class__==Currency:
            return "WhiteEuro"
        elif o.__class__==Percentage:
            return "WhitePercentage"
        elif o.__class__==datetime.datetime:
            return "WhiteDatetime"
        elif o.__class__==datetime.date:
            return "WhiteDate"
        elif o.__class__==Decimal:
            return "WhiteDecimal6"
        elif o.__class__==int:
            return "WhiteInteger"
        else:
            return "WhiteLeft"
