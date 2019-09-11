from PyQt5.QtCore import  Qt,  pyqtSlot,  QObject
from PyQt5.QtGui import QPainter, QFont,  QColor, QIcon
from PyQt5.QtWidgets import QAction, QMenu, QFileDialog, QProgressDialog, QApplication
from xulpymoney.libxulpymoney import    Percentage
from xulpymoney.libxulpymoneyfunctions import epochms2dtaware, dtaware2epochms, dtnaive2string
from xulpymoney.libxulpymoneytypes import  eOHCLDuration, eDtStrings
import datetime
from PyQt5.QtChart import QChart,  QLineSeries, QChartView, QValueAxis, QDateTimeAxis,  QPieSeries, QCandlestickSeries,  QCandlestickSet,  QScatterSeries

class VCCommons(QChartView):
    def __init__(self):
        QChartView.__init__(self)

        self._title=None
        self._titleFontSize=14
        self._progressDialogEnabled=False
        self.actionSave=QAction(self.tr("Save as image"))
        self.actionSave.setIcon(QIcon(":/xulpymoney/save.png"))
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_customContextMenuRequested)
        self.actionSave.triggered.connect(self.on_actionSave_triggered)

    def on_customContextMenuRequested(self, pos):
        menu=QMenu()
        menu.addAction(self.actionSave)
        menu.exec_(self.mapToGlobal(pos))
        
    @pyqtSlot()
    def on_actionSave_triggered(self):
        filename="{} Chart.png".format(dtnaive2string(datetime.datetime.now(), type=eDtStrings.Filename))    
        filename = QFileDialog.getSaveFileName(self, self.tr("Save File"), filename, self.tr("PNG Image (*.png)"))[0]
        if filename:
            self.save(filename)

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
    ## @param qicon Qicon object
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
        pixmap=self.grab()
        pixmap.save(savefile, quality=100)

class VCTemporalSeries(VCCommons):
    def __init__(self):
        VCCommons.__init__(self)
        self.__chart=QChart() #After setChart you must call it with chart()
        self._allowHideSeries=True

        #Axis cration
        self.axisX=QDateTimeAxis()
        self.axisX.setTickCount(15);
        self.axisX.setFormat("yyyy-MM");
        self.maxx=None
        self.maxy=None
        self.minx=None
        self.miny=None
        
        self.axisY = QValueAxis()
        self.axisY.setLabelFormat("%i")

        self.setRenderHint(QPainter.Antialiasing);
        
        self.series=[]
        self.__ohclduration=eOHCLDuration.Day

    def setAxisFormat(self, axis,  min, max, type, zone=None):
        """
            type=0 #Value
            type=1 # Datetime
            
            if zone=None remains in UTC, zone is a zone object.
        """
        if type==0:
            if max-min<=0.01:
                axis.setLabelFormat("%.4f")
            elif max-min<=100:
                axis.setLabelFormat("%.2f")
            else:
                axis.setLabelFormat("%i")
        elif type==1:
            max=epochms2dtaware(max)#UTC aware
            min=epochms2dtaware(min)
            if max-min<datetime.timedelta(days=1):
                axis.setFormat("hh:mm")
            else:
                axis.setFormat("yyyy-MM-dd")

    def setOHCLDuration(self, ohclduration):
        self.__ohclduration=ohclduration


    def setAllowHideSeries(self, boolean):
        self._allowHideSeries=boolean

        
    def appendTemporalSeries(self, name,  currency=None):
        """
            currency is a Currency object
        """
        self.currency=currency
        ls=QLineSeries()
        ls.setName(name)
        self.series.append(ls)
        return ls        

    def appendTemporalSeriesData(self, ls, x, y):
        """
            x is a datetime zone aware
        """
        x=dtaware2epochms(x)
        ls.append(x, y)
        
        if self.maxy==None:#Gives first maxy and miny
            self.maxy=y
            self.miny=y
            self.maxx=x
            self.minx=x
            
        if y>self.maxy:
            self.maxy=y
        if y<self.miny:
            self.miny=y
        if x>self.maxx:
            self.maxx=x
        if x<self.minx:
            self.minx=x
        
    def appendCandlestickSeries(self, name, currency):
        self.currency=currency
        ls=QCandlestickSeries()
        ls.setName(name)
        ls.setIncreasingColor(QColor(Qt.green));
        ls.setDecreasingColor(QColor(Qt.red));
        self.series.append(ls)
        return ls
        
    def appendCandlestickSeriesData(self, ls, ohcl):
        x=dtaware2epochms(ohcl.datetime())
        ls.append(QCandlestickSet(ohcl.open, ohcl.high, ohcl.low, ohcl.close, x ))
        if self.maxy==None:
            self.maxy=ohcl.high
            self.miny=ohcl.low
            self.maxx=x
            self.minx=x
        if ohcl.high>self.maxy:
            self.maxy=ohcl.high
        if ohcl.low<self.miny:
            self.miny=ohcl.low     
        if x>self.maxx:
            self.maxx=x
        if x<self.minx:
            self.minx=x
            
    def appendScatterSeries(self, name,  currency=None):
        """
            currency is a Currency object
        """
        self.currency=currency
        ls=QScatterSeries()
        ls.setName(name)
        self.series.append(ls)
        return ls

    def appendScatterSeriesData(self, ls, x, y):
        self.appendTemporalSeriesData(ls, x, y)
        
    def mouseMoveEvent(self, event):
        """
            event is a QMouseEvent
        """
        pass

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
        if self.__chart!=None:
            del self.__chart
        self.__chart=QChart()
        self.setChart(self.__chart)
        self.chart().setAnimationOptions(QChart.AllAnimations);
        self.chart().layout().setContentsMargins(0,0,0,0)
        self._display_set_title()

        self.setAxisFormat(self.axisX, self.minx, self.maxx, 1)
        self.setAxisFormat(self.axisY, self.miny, self.maxy, 0)
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

class VCPie(VCCommons):
    def __init__(self):
        VCCommons.__init__(self)
        self.setRenderHint(QPainter.Antialiasing)
        self.clear()

    def setCurrency(self, currency):
        """
            currency is a Currency Object
        """
        self.currency=currency

    def appendData(self, name, value,  exploded=False):
        slice=self.serie.append(name, value)
        slice.setExploded(exploded)
        slice.setLabelVisible()
        
    def display(self):
        self.setChart(self.__chart)
        self._display_set_title()
        tooltip=""
        c=self.currency.string
        for slice in self.serie.slices():
            tooltip=tooltip+"{}: {} ({})\n".format(slice.label(), c(slice.value()), Percentage(slice.percentage(), 1)).upper()
            slice.setLabel("{}: {}".format(slice.label(), Percentage(slice.percentage(), 1)).upper())
            if slice.percentage()<0.005:
                slice.setLabelVisible(False)
        tooltip=tooltip+"*** Total: {} ***".format(c(self.serie.sum())).upper()
        self.chart().addSeries(self.serie)
        
        self.setToolTip(tooltip)
        self.repaint()
        
    def clear(self, animations=True):
        self.__chart=QChart()
        self.setChart(self.__chart)
        self.chart().legend().hide()
        self.chart().layout().setContentsMargins(0,0,0,0);
        if animations==True:
            self.chart().setAnimationOptions(QChart.AllAnimations);
        else:
            self.chart().setAnimationOptions(QChart.NoAnimation)
        self.serie=QPieSeries()
        self.serie.setPieStartAngle(90)
        self.serie.setPieEndAngle(450)

