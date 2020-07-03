## @brief myCharts class
## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from PyQt5.QtChart import QChart,  QLineSeries, QChartView, QValueAxis, QDateTimeAxis,  QPieSeries, QScatterSeries, QCandlestickSeries,  QCandlestickSet
from PyQt5.QtCore import Qt, pyqtSlot, QObject, QPoint, pyqtSignal, QSize, QMutex
from PyQt5.QtGui import QPainter, QFont, QIcon, QColor, QImage, QClipboard
from PyQt5.QtWidgets import QWidget, QAction, QMenu, QFileDialog, QProgressDialog, QApplication, QDialog, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from .myqtablewidget import mqtw
from .. objects.percentage import Percentage
from .. casts import object2value
from .. datetime_functions import epochms2dtaware, dtaware2epochms, dtnaive2string
from collections import OrderedDict
from datetime import timedelta, datetime
from logging import error

class VCCommons(QChartView):
    displayed=pyqtSignal()
    def __init__(self):
        QChartView.__init__(self)

        self._title=None
        self._titleFontSize=14
        self._animations=True
        self._progressDialogEnabled=False
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.actionSave=QAction(self.tr("Save as image"))
        self.actionSave.setIcon(QIcon(":/reusingcode/save.png"))
        self.actionSave.triggered.connect(self.on_actionSave_triggered)
        
        self.actionCopyToClipboard=QAction(self.tr("Copy image"))
        self.actionCopyToClipboard.setIcon(QIcon(":/reusingcode/clipboard_copy.png"))
        self.actionCopyToClipboard.triggered.connect(self.on_actionCopyToClipboard_triggered)
        
    @pyqtSlot()
    def on_actionSave_triggered(self):
        filename="{} Chart.png".format(dtnaive2string(datetime.now(), "%Y%m%d %H%M"))    
        filename = QFileDialog.getSaveFileName(self, self.tr("Save File"), filename, self.tr("PNG Image (*.png)"))[0]
        if filename:
            self.save(filename)
        
    @pyqtSlot()
    def on_actionCopyToClipboard_triggered(self):
        self.copyImageToClipboard()

    ## Sets the title of the chart. If it's None, none title is shown.
    def setTitle(self, title):
        self._title=title

    ## Returns the title of the chart
    def title(self):
        return self._title
        
    ## Sets if a progress bar must be shown loading the graph.
    def setProgressDialogEnabled(self, show):
        self._progressDialogEnabled=show

    ## Returns if a progress bar must be shown loading the graph.
    def progressDialogEnabled(self):
        return self._progressDialogEnabled
        
    ##Set progress dialog attributes
    ## Only will be shown if self.progressDialogEnabled()==True (By default)
    ## if None leaves default
    ## @param title string
    ## @param text string
    ## @param qicon Qicon object
    ## @param min integer
    ## @param max integer
    def setProgressDialogAttributes(self, title, text, qicon, min=0, max=0):       
        self.progressdialog=QProgressDialog()
        self.progressdialog.setWindowIcon(qicon)
        self.progressdialog.setModal(True)        
        if title==None:
            self.progressdialog.setWindowTitle(self.tr("Creating chart"))
        else:
            self.progressdialog.setWindowTitle(title)
        if text==None:
            self.progressdialog.setLabelText(self.tr("Creating chart"))
        else:
            self.progressdialog.setLabelText(text)
        self.progressdialog.setMinimum(min)
        self.progressdialog.setMaximum(max)
        
    ## Sets the title font size. 14 by default.
    def setTitleFontSize(self, titleFontSize):
        self._titleFontSize=titleFontSize
        
    ## Function to use in display that sets the title
    ## @param size Integer with the font size
    def _display_set_title(self):
        font=QFont()
        font.setBold(True)
        font.setPointSize(self._titleFontSize)
        self.chart().setTitleFont(font)
        self.chart().setTitle(self._title)
        

    ##Updates progress dialog and set new number
    def setProgressDialogNumber(self, number):
        if self.progressDialogEnabled()==True:
            self.progressdialog.forceShow()      
            self.progressdialog.setValue(number)
            self.progressdialog.update()
            QApplication.processEvents()

    ## Save view to a file to generate an image file
    def save(self, savefile):
        img=QImage(self.size(), QImage.Format_ARGB32)
        painter=QPainter(img)
        painter.setRenderHint(QPainter.Antialiasing)
        self.render(painter)
        painter.end()
        img.save(savefile, quality=100)
        
    def copyImageToClipboard(self):
        img=QImage(self.size(), QImage.Format_ARGB32)
        painter=QPainter(img)
        painter.setRenderHint(QPainter.Antialiasing)
        self.render(painter)
        painter.end()
        QApplication.clipboard().setImage(img, QClipboard.Clipboard)

    ## Sets if the chart must show animations
    def setAnimations(self, boolean):
        self._animations=boolean
        
    ## Used to represent values in charts, using predefined formats set with setXFormat
    ## Value willbe epochms for datetimes
    ## @param value
    ## @param  format 
    def value2formated_string(self, value, format, decimals=2):
        if value=="---" or value is None:# Valores nulos
            return "---"
        
        if format=="date":
            return str(epochms2dtaware(value).date())
        elif format=="time":
            time=epochms2dtaware(value).time()
            return "{}:{}".format(time.hour, time.minute)
        elif format=="datetime":
            return str(epochms2dtaware(value))
        elif format=="int":
            return str(value)
        elif format=="float":
            return str(round(value, decimals))
        elif format=="EUR":
            return "{} €".format(round(value, decimals))
        else:
            error("{} is not a valid format in value2formated_string".format(format))

class VCTemporalSeriesAlone(VCCommons):
    def __init__(self):
        VCCommons.__init__(self)
        self.clear()
        self.popuplock=QMutex()
        self._x_format="date"
        self._x_timezone="UTC"
        self._x_decimals=0#Needed in popup
        self._x_tickcount=8
        self._x_title=""
        self._y_format="float"
        self._y_decimals=2
        self._y_title=""

    ## To clean pie, removes serie and everithing is like create an empty pie
    def clear(self):
        self._chart=QChart()
        self.setChart(self._chart)
        self.setRenderHint(QPainter.Antialiasing)
        self._allowHideSeries=True

        self.axisX=QDateTimeAxis()
        self.maxx=None
        self.minx=None

        self.axisY = QValueAxis()
        self.maxy=None
        self.miny=None
        
        self.series=[]
        self.chart().legend().hide()
        self.popup=MyPopup(self)

    def appendCandlestickSeries(self, name):
        ls=QCandlestickSeries()
        ls.setName(name)
        ls.setIncreasingColor(QColor(Qt.green));
        ls.setDecreasingColor(QColor(Qt.red));
        self.series.append(ls)
        return ls

    def appendCandlestickSeriesData(self, ls, dtaware, ope, hig, clo, low):
        x=dtaware2epochms(dtaware)
        ls.append(QCandlestickSet(float(ope), float(hig), float(clo), float(low), x ))
        if self.maxy==None:
            self.maxy=float(hig)
            self.miny=float(low)
            self.maxx=x
            self.minx=x
        if hig>self.maxy:
            self.maxy=float(hig)
        if low<self.miny:
            self.miny=float(low)
        if x>self.maxx:
            self.maxx=x
        if x<self.minx:
            self.minx=x

    ## Used to draw poinnts in a temporal series
    def appendScatterSeries(self, name):
        ls=QScatterSeries()
        ls.setName(name)
        self.series.append(ls)
        return ls

    def appendScatterSeriesData(self, ls, x, y):
        self.appendTemporalSeriesData(ls, x, y)


    ## @param stringtype is one of the types in casts.value2object. Can be auto too to auto select best datetime format
    def setXFormat(self, stringtype, title="",  zone_name="UTC", tickcount=8):
        self._x_format=stringtype
        self._x_zone_name=zone_name
        self._x_tickcount=tickcount
        self._x_title=title
        
        
        
    def _applyXFormat(self):
        self.axisX.setTickCount(8)
        self.axisX.setTitleText(self._x_title)
        if self._x_format=="time":
            self.axisX.setFormat("hh:mm")
        else:
            self.axisX.setFormat("yyyy-MM-dd")
        

    def setYFormat(self, stringtype,   title="", decimals=2):
        self._y_format=stringtype
        self._y_decimals=decimals
        self._y_title=title

    def _applyYFormat(self):
        self.axisY.setTitleText(self._y_title)
        if self._y_format=="int":
            self.axisY.setLabelFormat("%i")
        elif self._y_format in ["float", "Decimal"]:
            self.axisY.setLabelFormat("%.{}f".format(self._y_decimals))

    def setAllowHideSeries(self, boolean):
        self._allowHideSeries=boolean

        
    def appendTemporalSeries(self, name):
        ls=QLineSeries()
        ls.setName(name)
        self.series.append(ls)
        return ls        

    def appendTemporalSeriesData(self, ls, x, y):
        """
            x is a datetime zone aware
        """
        x=dtaware2epochms(x)
        y=float(y)
        ls.append(x, y)
        
        if self.maxy==None:#Gives first maxy and miny
            self.maxy=y*1.01
            self.miny=y*0.99
            self.maxx=x*1.01
            self.minx=x*0.99
            
        if y>self.maxy:
            self.maxy=y
        if y<self.miny:
            self.miny=y
        if x>self.maxx:
            self.maxx=x
        if x<self.minx:
            self.minx=x

    def mouseMoveEvent(self, event):     
        ##Sets the place of the popup in the windows to avoid getout of the screen
        ##frmshow can be a frmShowCasilla or a frmShowFicha
        def placePopUp():
            resultado=QPoint(event.x()+15, event.y()+15)
            if event.x()>self.width()-self.popup.width()-15:
                resultado.setX(event.x()-self.popup.width()-15)
            if event.y()>self.height()-self.popup.height()-15:
                resultado.setY(event.y()-self.popup.height()-15)
            return resultado

        # ---------------------------------------
        
        if self.popuplock.tryLock()==False:
            event.reject()
            return
        QChartView.mouseMoveEvent(self, event)
        xVal = self.chart().mapToValue(event.pos()).x()
        yVal = self.chart().mapToValue(event.pos()).y()

        maxX = self.axisX.max().toMSecsSinceEpoch()
        minX = self.axisX.min().toMSecsSinceEpoch()
        maxY = self.axisY.max()
        minY = self.axisY.min()
        if xVal <= maxX and  xVal >= minX and yVal <= maxY and yVal >= minY:
            self.popup.move(self.mapToGlobal(placePopUp()))
            self.popup.refresh(self, xVal, yVal)
        self.popuplock.unlock()

    ## Return the value of the serie in x
    def series_value(self, serie, x):
        if serie.__class__.__name__=="QLineSeries":
            for point in serie.pointsVector():
                if point.x()>=x:
                    return point.y()
        elif serie.__class__.__name__=="QCandlestickSeries":
            for qohcl in serie.sets():
                if qohcl.timestamp()>=x:
                    return qohcl.close

    ## Returns values from QSeries objects in an ordereddict d[x]=y, key is a dtaware
    def series_dictionary(self, serie):
        d=OrderedDict()
        if serie.__class__.__name__=="QLineSeries":
            for point in serie.pointsVector():
                d[epochms2dtaware(point.x())]=point.y()
        elif serie.__class__.__name__=="QCandlestickSeries":
            for qohcl in serie.sets():
                d[epochms2dtaware(qohcl.timestamp())]=qohcl.close
        return d

    @pyqtSlot()
    def on_marker_clicked(self):
        marker=QObject.sender(self)#Busca el objeto que ha hecho la signal en el slot en el que está conectado, ya que estaban conectados varios objetos a una misma señal
        marker.series().setVisible(not marker.series().isVisible())
        marker.setVisible(True)
        if marker.series().isVisible():
            alpha = 1
        else:
            alpha=0.5

        lbrush=marker.labelBrush()
        color=lbrush.color()
        color.setAlphaF(alpha)
        lbrush.setColor(color)
        marker.setLabelBrush(lbrush)

        brush=marker.brush()
        color=brush.color()
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setBrush(brush)
        
        pen=marker.pen()
        color=pen.color()
        color.setAlphaF(alpha)
        pen.setColor(color)
        marker.setPen(pen)



    ## Used to display chart. You cannot use it twice. close the view widget and create another one
    def display(self):
        if self._chart!=None:
            del self._chart
        self._chart=QChart()
        self.setChart(self._chart)
        if self._animations==True:
            self.chart().setAnimationOptions(QChart.AllAnimations)
        else:
            self.chart().setAnimationOptions(QChart.NoAnimation)
        self.chart().layout().setContentsMargins(0,0,0,0)
        self._display_set_title()

        self._applyXFormat()
        self._applyYFormat()
        self.chart().addAxis(self.axisY, Qt.AlignLeft)
        self.chart().addAxis(self.axisX, Qt.AlignBottom)

        for s in self.series:
            self.chart().addSeries(s)
            s.attachAxis(self.axisX)
            s.attachAxis(self.axisY)
        self.axisY.setRange(self.miny, self.maxy)

        #Legend positions
        if len(self.chart().legend().markers())>6:
            self.chart().legend().setAlignment(Qt.AlignLeft)
        else:
            self.chart().legend().setAlignment(Qt.AlignTop)

        if self._allowHideSeries==True:
            for marker in self.chart().legend().markers():
                try:
                    marker.clicked.disconnect()
                except:
                    pass
                marker.clicked.connect(self.on_marker_clicked)
        self.repaint()

    ## Returns a qmenu to be used in other qmenus
    def qmenu(self, title="Chart options"):
        menu=QMenu(self)
        menu.setTitle(self.tr(title))
        menu.addAction(self.actionCopyToClipboard)
        menu.addSeparator()
        menu.addAction(self.actionSave)
        return menu

    ## If you use VCPieAlone you can add a context menu setting boolean to True
    def setCustomContextMenu(self, boolean):
        self.customContextMenuRequested.connect(self.on_customContextMenuRequested)

    def on_customContextMenuRequested(self, pos):
        self.qmenu().exec_(self.mapToGlobal(pos))



## Yo must:
## 1. Create widget
## 1. Append data
## 1. Display

## If you use clear, you must append data and display again

class VCTemporalSeries(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent=parent
        
        self.lay=QHBoxLayout()
        
        self.layTable=QVBoxLayout()
        
        self.ts=VCTemporalSeriesAlone()
        self.table=mqtw(self)
        self.table.setGenericContextMenu()
        self.table.hide()

        self.lay.addWidget(self.ts)
        self.layTable.addWidget(self.table)
        self.lay.addLayout(self.layTable)
        self.setLayout(self.lay)

        self.actionShowData=QAction(self.tr("Show chart data"))
        self.actionShowData.setIcon(QIcon(":/reusingcode/database.png"))
        self.actionShowData.triggered.connect(self.on_actionShowData_triggered)

        self.ts.customContextMenuRequested.connect(self.on_customContextMenuRequested)

    ## Returns if the Widget hasn't series loaded
    def isEmpty(self):
        if len(self.ts.series)==0:
            return True
        return False

    def setSettings(self, settings, settingsSection,  settingsObject):
        self._settings=settings
        self._settingsSection=settingsSection
        self._settingsObject=settingsObject
        self.setObjectName(self._settingsObject)
        self.table.setSettings(self._settings, self._settingsSection, self._settingsObject+"_mqtw")

    def settings(self):
        return self._settings

    def on_actionShowData_triggered(self):
        if self.actionShowData.text()==self.tr("Show chart data"):
            self.table.setMinimumSize(QSize(self.width()*3/8, self.height()*3/8))
            self.table.show()
            self.actionShowData.setText(self.tr("Hide chart data"))
        else:
            self.table.hide()
            self.actionShowData.setText(self.tr("Show chart data"))

    ## Returns a qmenu to be used in other qmenus
    def qmenu(self, title="Temporal serie chart options"):
        menu=QMenu(self)
        menu.setTitle(self.tr(title))
        menu.addAction(self.ts.actionCopyToClipboard)
        menu.addSeparator()
        menu.addAction(self.ts.actionSave)
        menu.addSeparator()
        menu.addAction(self.actionShowData)
        return menu

    def on_customContextMenuRequested(self, pos):
        self.qmenu().exec_(self.mapToGlobal(pos))

    ## Widget is restored to fabric, it's like instanciate a new one
    def clear(self):
        self.ts.clear()
        self.table.clear()

    def display(self):
        self.ts.display()
        hh=["Datetime"]
        #I create a dictionary con d[datetime]=(valor_serie0, valor_serie1)...
        unordered={}
        
        #Initiate dictionary
        for serie in self.ts.series:
            hh.append(serie.name())
            for dt, value in self.ts.series_dictionary(serie).items():
                unordered[dt]=[None]*len(self.ts.series)
        
        d= OrderedDict(sorted(unordered.items(), key=lambda t: t[0]))
                
        #Filling
        for i, serie in enumerate(self.ts.series):
            for dt, value in self.ts.series_dictionary(serie).items():
                d[dt][i]=value           

        data=[]
        for key, value in d.items():
            data.append((key, *value))
        self.table.setData(hh, None, data)
        self.table.drawOrderBy(0, False)
        self.table.on_actionSizeMinimum_triggered()
        self.table.settings().sync()
        

class VCTemporalSeriesWithTwoYAxisAlone(VCTemporalSeriesAlone):
    def __init__(self):
        VCTemporalSeriesAlone.__init__(self)
        self.series2=[]
        self._y2_format="Decimal"
        self._y2_decimals=2
        self._y2_title=""

    ## To clean pie, removes serie and everithing is like create an empty pie
    def clear(self):
        VCTemporalSeriesAlone.clear(self)

        self.axisY2 = QValueAxis()
        self.maxy2=None
        self.miny2=None
        self.series2=[]

        
    def appendTemporalSeriesAxis2(self, name):
        ls=QLineSeries()
        ls.setName(name)
        self.series2.append(ls)
        return ls


    def setY2Format(self, stringtype,   title="", decimals=2):
        self._y2_format=stringtype
        self._y2_decimals=decimals
        self._y2_title=title
        
    def appendTemporalSeriesDataAxis2(self, ls, x, y):
        x=dtaware2epochms(x)
        y=float(y)
        ls.append(x, y)

        if self.maxy2==None:#Gives first maxy and miny
            self.maxy2=y*1.01
            self.miny2=y*0.99
            self.maxx=x*1.01
            self.minx=x*0.99
            
        if y>self.maxy2:
            self.maxy2=y
        if y<self.miny2:
            self.miny2=y
        if x>self.maxx:
            self.maxx=x
        if x<self.minx:
            self.minx=x


    def _applyY2Format(self):
        self.axisY2.setTitleText(self._y2_title)
        if self._y2_format=="int":
            self.axisY2.setLabelFormat("%i")
        elif self._y2_format in ["float", "Decimal"]:
            self.axisY2.setLabelFormat("%.{}f".format(self._y2_decimals))

    ## Used to display chart. You cannot use it twice. close the view widget and create another one
    def display(self):
        if self._chart!=None:
            del self._chart
        self._chart=QChart()
        self.setChart(self._chart)
        if self._animations==True:
            self.chart().setAnimationOptions(QChart.AllAnimations);
        else:
            self.chart().setAnimationOptions(QChart.NoAnimation)
        self.chart().layout().setContentsMargins(0,0,0,0)
        self._display_set_title()

        self._applyXFormat()
        self._applyYFormat()
        self._applyY2Format()
        self.chart().addAxis(self.axisY, Qt.AlignLeft)
        self.chart().addAxis(self.axisX, Qt.AlignBottom)
        self.chart().addAxis(self.axisY2, Qt.AlignRight)

        for s in self.series:
            self.chart().addSeries(s)
            s.attachAxis(self.axisX)
            s.attachAxis(self.axisY)
        self.axisY.setRange(self.miny, self.maxy)

        for s in self.series2:
            self.chart().addSeries(s)
            s.attachAxis(self.axisX)
            s.attachAxis(self.axisY2)
        self.axisY2.setRange(self.miny2, self.maxy2)

        #Legend positions
        if len(self.chart().legend().markers())>6:
            self.chart().legend().setAlignment(Qt.AlignLeft)
        else:
            self.chart().legend().setAlignment(Qt.AlignTop)

        if self._allowHideSeries==True:
            for marker in self.chart().legend().markers():
                try:
                    marker.clicked.disconnect()
                except:
                    pass
                marker.clicked.connect(self.on_marker_clicked)
        self.repaint()

class VCTemporalSeriesWithTwoYAxis(VCTemporalSeries):
    def __init__(self,parent=None):
        VCTemporalSeries.__init__(self,parent)
        self.lay.removeWidget(self.ts)
        
        self.ts=VCTemporalSeriesWithTwoYAxisAlone()
        self.lay.addWidget(self.ts)

class VCScatterAlone(VCCommons):
    def __init__(self):
        VCCommons.__init__(self)
        self.clear()
        self.popuplock=QMutex()
        self._x_format="float"
        self._x_decimals=2
        self._x_title=""
        self._y_format="float"
        self._y_decimals=2
        self._y_title=""

    ## To clean pie, removes serie and everithing is like create an empty pie
    def clear(self):
        self._chart=QChart()
        self.setChart(self._chart)
        self.setRenderHint(QPainter.Antialiasing)
        self._allowHideSeries=True

        self.axisX=QValueAxis()
        self.maxx=None
        self.minx=None

        self.axisY = QValueAxis()
        self.maxy=None
        self.miny=None
        
        self.series=[]
        self.chart().legend().hide()
        self.popup=MyPopup(self)

    def appendScatterSeries(self, name, list_x, list_y):
        ls=QScatterSeries()
        ls.setName(name)
        self.series.append(ls)
        for i in range(len(list_x)):
            x=float(list_x[i])
            y=float(list_y[i])
            ls.append(x, y)
            
            if self.maxy==None:#Gives first maxy and miny
                self.maxy=y*1.01
                self.miny=y*0.99
                self.maxx=x*1.01
                self.minx=x*0.99
                
            if y>self.maxy:
                self.maxy=y
            if y<self.miny:
                self.miny=y
            if x>self.maxx:
                self.maxx=x
            if x<self.minx:
                self.minx=x
        

    def setXFormat(self, stringtype,   title="", decimals=2):
        self._x_format=stringtype
        self._x_decimals=decimals
        self._x_title=title
        
        
        
    def _applyXFormat(self):
#        self.axisX.setTickCount(8)
        self.axisX.setTitleText(self._x_title)
        if self._x_format=="int":
            self.axisX.setLabelFormat("%i")
        elif self._x_format in ["float", "Decimal"]:
            self.axisX.setLabelFormat("%.{}f".format(self._x_decimals))


    def setYFormat(self, stringtype,   title="", decimals=2):
        self._y_format=stringtype
        self._y_decimals=decimals
        self._y_title=title

    def _applyYFormat(self):
        self.axisY.setTitleText(self._y_title)
        if self._y_format=="int":
            self.axisY.setLabelFormat("%i")
        elif self._y_format in ["float", "Decimal"]:
            self.axisY.setLabelFormat("%.{}f".format(self._y_decimals))

    def setAllowHideSeries(self, boolean):
        self._allowHideSeries=boolean

    def mouseMoveEvent(self, event):     
        ##Sets the place of the popup in the windows to avoid getout of the screen
        ##frmshow can be a frmShowCasilla or a frmShowFicha
        def placePopUp():
            resultado=QPoint(event.x()+15, event.y()+15)
            if event.x()>self.width()-self.popup.width()-15:
                resultado.setX(event.x()-self.popup.width()-15)
            if event.y()>self.height()-self.popup.height()-15:
                resultado.setY(event.y()-self.popup.height()-15)
            return resultado

        # ---------------------------------------
        if self.popuplock.tryLock()==False:
            event.reject()
            return
        QChartView.mouseMoveEvent(self, event)
        xVal = self.chart().mapToValue(event.pos()).x()
        yVal = self.chart().mapToValue(event.pos()).y()

        maxX = self.axisX.max()
        minX = self.axisX.min()
        maxY = self.axisY.max()
        minY = self.axisY.min()
        if xVal <= maxX and  xVal >= minX and yVal <= maxY and yVal >= minY:
            self.popup.move(self.mapToGlobal(placePopUp()))
            self.popup.refresh(self, xVal, yVal)
        self.popuplock.unlock()

    @pyqtSlot()
    def on_marker_clicked(self):
        marker=QObject.sender(self)#Busca el objeto que ha hecho la signal en el slot en el que está conectado, ya que estaban conectados varios objetos a una misma señal
        marker.series().setVisible(not marker.series().isVisible())
        marker.setVisible(True)
        if marker.series().isVisible():
            alpha = 1
        else:
            alpha=0.5

        lbrush=marker.labelBrush()
        color=lbrush.color()
        color.setAlphaF(alpha)
        lbrush.setColor(color)
        marker.setLabelBrush(lbrush)

        brush=marker.brush()
        color=brush.color()
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setBrush(brush)
        
        pen=marker.pen()
        color=pen.color()
        color.setAlphaF(alpha)
        pen.setColor(color)
        marker.setPen(pen)



    ## Used to display chart. You cannot use it twice. close the view widget and create another one
    def display(self):
        if self._chart!=None:
            del self._chart
        self._chart=QChart()
        self.setChart(self._chart)
        if self._animations==True:
            self.chart().setAnimationOptions(QChart.AllAnimations);
        else:
            self.chart().setAnimationOptions(QChart.NoAnimation)
        self.chart().layout().setContentsMargins(0,0,0,0)
        self._display_set_title()

        self._applyXFormat()
        self._applyYFormat()
        self.chart().addAxis(self.axisY, Qt.AlignLeft);
        self.chart().addAxis(self.axisX, Qt.AlignBottom);

        for s in self.series:
            self.chart().addSeries(s)
            s.attachAxis(self.axisX)
            s.attachAxis(self.axisY)
        self.axisY.setRange(self.miny, self.maxy)

        #Legend positions
        if len(self.chart().legend().markers())>6:
            self.chart().legend().setAlignment(Qt.AlignLeft)
        else:
            self.chart().legend().setAlignment(Qt.AlignTop)

        if self._allowHideSeries==True:
            for marker in self.chart().legend().markers():
                try:
                    marker.clicked.disconnect()
                except:
                    pass
                marker.clicked.connect(self.on_marker_clicked)
        self.repaint()

    ## Returns a qmenu to be used in other qmenus
    def qmenu(self, title="Chart options"):
        menu=QMenu(self)
        menu.setTitle(self.tr(title))
        menu.addAction(self.actionCopyToClipboard)
        menu.addSeparator()
        menu.addAction(self.actionSave)
        return menu

    ## If you use VCPieAlone you can add a context menu setting boolean to True
    def setCustomContextMenu(self, boolean):
        self.customContextMenuRequested.connect(self.on_customContextMenuRequested)

    def on_customContextMenuRequested(self, pos):
        self.qmenu().exec_(self.mapToGlobal(pos))



## Yo must:
## 1. Create widget
## 1. Append data
## 1. Display

## If you use clear, you must append data and display again

class VCScatter(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent=parent
        
        self.lay=QHBoxLayout()
        
        self.layTable=QVBoxLayout()
        
        self.scatter=VCScatterAlone()
        self.table=mqtw(self)
        self.table.setGenericContextMenu()
        self.table.hide()

        self.lay.addWidget(self.scatter)
        self.layTable.addWidget(self.table)
        self.lay.addLayout(self.layTable)
        self.setLayout(self.lay)

        self.actionShowData=QAction(self.tr("Show chart data"))
        self.actionShowData.setIcon(QIcon(":/reusingcode/database.png"))
        self.actionShowData.triggered.connect(self.on_actionShowData_triggered)

        self.scatter.customContextMenuRequested.connect(self.on_customContextMenuRequested)

    ## Returns if the Widget hasn't series loaded
    def isEmpty(self):
        if len(self.scatter.series)==0:
            return True
        return False

    def setSettings(self, settings, settingsSection,  settingsObject):
        self._settings=settings
        self._settingsSection=settingsSection
        self._settingsObject=settingsObject
        self.setObjectName(self._settingsObject)
        self.table.setSettings(self._settings, self._settingsSection, self._settingsObject+"_mqtw")

    def settings(self):
        return self._settings

    def on_actionShowData_triggered(self):
        if self.actionShowData.text()==self.tr("Show chart data"):
            self.table.setMinimumSize(QSize(self.width()*3/8, self.height()*3/8))
            self.table.show()
            self.actionShowData.setText(self.tr("Hide chart data"))
        else:
            self.table.hide()
            self.actionShowData.setText(self.tr("Show chart data"))

    ## Returns a qmenu to be used in other qmenus
    def qmenu(self, title="Scatter chart options"):
        menu=QMenu(self)
        menu.setTitle(self.tr(title))
        menu.addAction(self.scatter.actionCopyToClipboard)
        menu.addSeparator()
        menu.addAction(self.scatter.actionSave)
        menu.addSeparator()
        menu.addAction(self.actionShowData)
        return menu

    def on_customContextMenuRequested(self, pos):
        self.qmenu().exec_(self.mapToGlobal(pos))

    ## Widget is restored to fabric, it's like instanciate a new one
    def clear(self):
        self.scatter.clear()
        self.table.clear()

    def display(self):
        self.scatter.display()
        return 
#        hh=["Datetime"]
#        #I create a dictionary con d[datetime]=(valor_serie0, valor_serie1)...
#        unordered={}
#        
#        #Initiate dictionary
#        for serie in self.scatter.series:
#            hh.append(serie.name())
#            for dt, value in self.scatter.series_dictionary(serie).items():
#                unordered[dt]=[None]*len(self.scatter.series)
#        
#        d= OrderedDict(sorted(unordered.items(), key=lambda t: t[0]))
#                
#        #Filling
#        for i, serie in enumerate(self.scatter.series):
#            for dt, value in self.scatter.series_dictionary(serie).items():
#                d[dt][i]=value           
#
#        data=[]
#        for key, value in d.items():
#            data.append((key, *value))
#        self.table.setData(hh, None, data)
#        self.table.drawOrderBy(0, False)
#        self.table.on_actionSizeMinimum_triggered()
#        self.table.settings().sync()

class VCPieAlone(VCCommons):
    def __init__(self):
        VCCommons.__init__(self)
        self.clear()
        
    ## If you use VCPieAlone you can add a context menu setting boolean to True
    def setCustomContextMenu(self, boolean):
        self.customContextMenuRequested.connect(self.on_customContextMenuRequested)

    def appendData(self, name, value,  exploded=False):
        self.data.append([name, value])
        slice=self.serie.append(name, object2value(value))#only float
        slice.setExploded(exploded)
        slice.setLabelVisible()
    
    ## To clean pie, removes serie and everithing is like create an empty pie
    def clear(self):
        self._chart=QChart()
        self.setChart(self._chart)
        self.setRenderHint(QPainter.Antialiasing)
        self.data=[]
        self.serie=QPieSeries()
        self.serie.setPieStartAngle(90)
        self.serie.setPieEndAngle(450)
        self.chart().legend().hide()
    
    ## To show pie
    def display(self):
        self.chart().layout().setContentsMargins(0,0,0,0);
        if self._animations==True:
            self.chart().setAnimationOptions(QChart.AllAnimations);
        else:
            self.chart().setAnimationOptions(QChart.NoAnimation)

        self._display_set_title()
        for slice in self.serie.slices():
            slice.setLabel("{}: {}".format(slice.label(), Percentage(slice.percentage(), 1)))
            if slice.percentage()<0.005:
                slice.setLabelVisible(False)
        self.chart().addSeries(self.serie)
        
        self.repaint()
        self.displayed.emit()
        
    def sum_values(self):
        if len(self.data)==0:
            return None
        cls=self.data[0][1].__class__.__name__
        if cls in ["int", "float", "Decimal"]:
            s=0
        elif cls in ["Currency",]:
            s=self.data[0][1].__class__(0, self.data[0][1].currency)
        elif cls in ["Money",]:
            s=self.data[0][1].__class__(self.data[0][1].mem, 0, self.data[0][1].currency)
        for row in self.data:
            s=s+row[1]
        return s



    ## Returns a qmenu to be used in other qmenus
    def qmenu(self, title="Pie chart options"):
        menu=QMenu(self)
        menu.setTitle(self.tr(title))
        menu.addAction(self.actionSave)
        return menu

    def on_customContextMenuRequested(self, pos):
        self.qmenu().exec_(self.mapToGlobal(pos))
        
class MyPopup(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent, Qt.ToolTip|Qt.WindowStaysOnTopHint)
        self.setAttribute( Qt.WA_ShowWithoutActivating)
        self.parent=parent
        
    def refresh(self, vc, xVal, yVal):
        self.vc=vc
        self.xVal=xVal
        self.yVal=yVal
        
        #Creating empy labels
        if hasattr(self, 'lblTitles')==False:
            self.lay = QVBoxLayout(self)
            self.lblPosition=QLabel()
            self.lblPosition.setAlignment(Qt.AlignCenter)
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.lblPosition.setFont(font)
            self.lay.addWidget(self.lblPosition)
            
            self.line = QFrame(self)
            self.line.setFrameShape(QFrame.HLine)
            self.line.setFrameShadow(QFrame.Sunken)
            self.lay.addWidget(self.line)
            
            self.lblTitles=[]
            self.lblValues=[]
            for serie in self.vc.series:
                title=QLabel()
                value=QLabel()
                self.lblTitles.append(title)
                self.lblValues.append(value)
                layh=QHBoxLayout()
                layh.addWidget(title)
                layh.addWidget(value)
                self.lay.addLayout(layh)
            self.setLayout(self.lay)
        
        modifiers = QApplication.keyboardModifiers()        
        
        if modifiers== Qt.ShiftModifier: #SHOW CCURRENT VALUE
            self.lblPosition.setText("{}, {}".format(self.parent.value2formated_string(xVal, self.parent._x_format, self.parent._x_decimals), self.parent.value2formated_string(yVal, self.parent._y_format, self.parent._y_decimals)))
            for i, serie in enumerate(self.vc.series):
                    self.lblValues[i].hide()
                    self.lblTitles[i].hide()
                    self.line.hide()
            self.show()

        elif modifiers== Qt.ControlModifier: #SHOW CURRENT VALUES OF SERIES
            self.lblPosition.setText("{}, {}".format(self.parent.value2formated_string(xVal, self.parent._x_format, self.parent._x_decimals), self.parent.value2formated_string(yVal, self.parent._y_format, self.parent._y_decimals)))
            for i, serie in enumerate(self.vc.series):
                if serie.isVisible():
                    self.lblValues[i].show()
                    self.lblTitles[i].show()
                    self.lblTitles[i].setText(serie.name())
                    try:
                        value=self.vc.series_value(serie, self.xVal)
                    except:
                        value="---"
                    self.lblValues[i].setText(self.parent.value2formated_string(value, self.parent._y_format, self.parent._y_decimals))
                    self.line.show()
                    self.show()
                else:
                    self.lblValues[i].hide()
                    self.lblTitles[i].hide()
            self.show()

        elif modifiers ==Qt.ShiftModifier|Qt.ControlModifier: #SHOW LAST VALUES OF SERIES
            self.lblPosition.setText(self.tr("Last value") )
            for i, serie in enumerate(self.vc.series):
                if serie.isVisible():
                    self.lblValues[i].show()
                    self.lblTitles[i].show()
                    self.lblTitles[i].setText(serie.name())
                    try:
                        value=serie.pointsVector()[len(serie.pointsVector())-1].y()
                    except:
                        value="---"
                    self.lblValues[i].setText(self.parent.value2formated_string(value, self.parent._y_format, self.parent._y_decimals))
                    self.line.show()
                    self.show()
                else:
                    self.lblValues[i].hide()
                    self.lblTitles[i].hide()
            self.show()
        
        else:
            self.hide()


    def mousePressEvent(self, event):
        self.hide()



## Yo must:
## 1. Create widget
## 1. Append data
## 1. Display

## If you use clear, you must append data and display again

class VCPie(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent=parent
        
        self.lay=QHBoxLayout()
        
        self.layTable=QVBoxLayout()
        
        self.lblTotal=QLabel(self)
        self.lblTotal.hide()        
        font = QFont()
        font.setBold(True)
        self.lblTotal.setFont(font)
        self.lblTotal.setAlignment(Qt.AlignCenter)

        self.pie=VCPieAlone()
        #piesizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #piesizePolicy.setHorizontalStretch(2)
        #self.pie.setSizePolicy(piesizePolicy)

        self.table=mqtw(self)
        self.table.hide()
        #tablesizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        #tablesizePolicy.setHorizontalStretch(1)
        #self.table.setSizePolicy(tablesizePolicy)

        self.lay.addWidget(self.pie)
        self.layTable.addWidget(self.table)
        self.layTable.addWidget(self.lblTotal)
        self.lay.addLayout(self.layTable)
        self.setLayout(self.lay)

        self.actionShowData=QAction(self.tr("Show chart data"))
        self.actionShowData.setIcon(QIcon(":/reusingcode/database.png"))
        self.actionShowData.triggered.connect(self.on_actionShowData_triggered)

        self.pie.customContextMenuRequested.connect(self.on_customContextMenuRequested)

    def setSettings(self, settings, settingsSection,  settingsObject):
        self._settings=settings
        self._settingsSection=settingsSection
        self._settingsObject=settingsObject
        self.setObjectName(self._settingsObject)
        self.table.setSettings(self._settings, self._settingsSection, self._settingsObject+"_mqtw")

    def settings(self):
        return self._settings

    def on_actionShowData_triggered(self):
        if self.actionShowData.text()==self.tr("Show chart data"):
            self.table.setMinimumSize(QSize(self.width()*3/8, self.height()*3/8))
            self.table.show()
            self.lblTotal.show()
            self.actionShowData.setText(self.tr("Hide chart data"))
        else:
            self.table.hide()
            self.lblTotal.hide()
            self.actionShowData.setText(self.tr("Show chart data"))

    ## Returns a qmenu to be used in other qmenus
    def qmenu(self, title="Pie chart options"):
        menu=QMenu(self)
        menu.setTitle(self.tr(title))
        menu.addAction(self.pie.actionCopyToClipboard)
        menu.addSeparator()
        menu.addAction(self.pie.actionSave)
        menu.addSeparator()
        menu.addAction(self.actionShowData)
        return menu

    def on_customContextMenuRequested(self, pos):
        self.qmenu().exec_(self.mapToGlobal(pos))

    ## Widget is restored to fabric, it's like instanciate a new one
    def clear(self):
        self.pie.clear()
        self.table.clear()
        self.lblTotal.setText("")

    def display(self):
        self.pie.display()
        data=[]
        for o in self.pie.data:
            data.append([o[0], o[1], Percentage(o[1],self.pie.sum_values())])
        self.table.setData([self.tr("Name"), self.tr("Value"), self.tr("Percentage")], None, data)
        self.table.setOrderBy(2, False)
        self.lblTotal.setText(self.tr("Total: {}").format(self.pie.sum_values()))
        self.table.on_actionSizeMinimum_triggered()
        self.table.settings().sync()

def example():
    d={'one':1, 'two':2, 'three':3, 'four':4}
    app = QApplication([])
    from importlib import import_module
    import_module("xulpymoney.images.xulpymoney_rc")
    w=QWidget()
    from PyQt5.QtCore import QSettings
    settings=QSettings()
    
    #Temporal series
    vcts=VCTemporalSeries()
    vcts.ts.setTitle("Example of VCTemporalSeries")
    vcts.setSettings(settings, "example", "vcts")
    vcts.ts.setXFormat("date", "Time")
    vcts.ts.setYFormat("EUR", "Money (€)" , decimals=2)
    sBasic=vcts.ts.appendTemporalSeries("Basic")
    for i in range(20):
        vcts.ts.appendTemporalSeriesData(sBasic, datetime.now()+timedelta(days=i),  i % 5)
    vcts.display()
    vcts.clear()
    sBasic=vcts.ts.appendTemporalSeries("Basic")
    for i in range(20):
        vcts.ts.appendTemporalSeriesData(sBasic, datetime.now()+timedelta(days=i),  i % 8)
    vcts.display()
    
    #Pie
    wdgvcpie=VCPie(w)
    wdgvcpie.pie.setTitle("Demo pie")
    wdgvcpie.setSettings(settings, "example", "vcpie")
    for k, v in d.items():
        wdgvcpie.pie.appendData(k, v)
    wdgvcpie.display()
    wdgvcpie.clear()
    for k, v in d.items():
        wdgvcpie.pie.appendData(k, v)
    wdgvcpie.display()
    
    
    #Scatter
    wdgscatter=VCScatter(w)
    wdgscatter.scatter.setTitle("Scatter chart")
    wdgscatter.setSettings(settings, "example", "scatter")
    wdgscatter.scatter.appendScatterSeries("Correlation", [1, 2, 3, 4, 5], [0, 2, 1, 3, 3])
    wdgscatter.display()
    print("SEGUNDO")
    wdgscatter.clear()
    wdgscatter.scatter.setTitle("Scatter chart")
    wdgscatter.setSettings(settings, "example", "scatter")
    wdgscatter.scatter.appendScatterSeries("Correlation", [1, 2, 3, 4, 5], [0, 2, 1, 3, 3])
    wdgscatter.display()
    

    #Temporal series two axis
    vcts2=VCTemporalSeriesWithTwoYAxis(w)
    vcts2.ts.setTitle("Example of VCTemporalSeries with two axis")
    vcts2.setSettings(settings, "example", "vcts2")
    vcts2.ts.setXFormat("time", "Time")
    vcts2.ts.setYFormat("EUR", "Money (€)" , decimals=2)
    vcts2.ts.setY2Format("EUR", "Money (€)" , decimals=2)
    sBasic=vcts2.ts.appendTemporalSeries("Basic")
    for i in range(20):
        vcts2.ts.appendTemporalSeriesData(sBasic, datetime.now()+timedelta(days=i),  i % 5)
    sBasic2=vcts2.ts.appendTemporalSeriesAxis2("Basic 2")
    for i in range(20):
        vcts2.ts.appendTemporalSeriesDataAxis2(sBasic2, datetime.now()+timedelta(days=i),  i % 8)
    vcts2.display()


    #Widget
    lay=QHBoxLayout(w)
    lay.addWidget(vcts)
    lay.addWidget(wdgvcpie)
    lay.addWidget(wdgscatter)
    lay.addWidget(vcts2)
    w.resize(1500, 450)
    w.move(300, 300)
    w.setWindowTitle('myqcharts example')
    w.show()
    


    app.exec()
