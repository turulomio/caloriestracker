## @brief Package to manage postgresql connection functions with qt timeouts
## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

import datetime
from PyQt5.QtCore import QObject,  pyqtSignal,  QTimer
from .connection_pg import Connection

class ConnectionQt(QObject,Connection):
    inactivity_timeout=pyqtSignal()
    def __init__(self):
        Connection.__init__(self)
        QObject.__init__(self)
        self.restart_timeout()
        self.inactivity_timeout_minutes=30

    def _check_inactivity(self):
        if datetime.datetime.now()-self._lastuse>datetime.timedelta(minutes=self.inactivity_timeout_minutes):
            self.disconnect()
            self._timerlastuse.stop()
            self.inactivity_timeout.emit()
        print ("Remaining time {}".format(self._lastuse+datetime.timedelta(minutes=self.inactivity_timeout_minutes)-datetime.datetime.now()))

    def cursor(self):
        self.restart_timeout()#Datetime who saves the las use of connection
        return self._con.cursor()

    def restart_timeout(self):
        """Resets timeout, usefull in long process without database connections"""
        self._lastuse=datetime.datetime.now()

    def cursor_one_row(self, sql, arr=[]):
        """Returns only one row"""
        self.restart_timeout()
        return super().cursor_one_row(sql, arr)

    def cursor_one_column(self, sql, arr=[]):
        """Returns un array with the results of the column"""
        self.restart_timeout()
        return super().cursor_one_column(sql, arr)

    def cursor_one_field(self, sql, arr=[]):
        """Returns only one field"""
        self.restart_timeout()
        return super().cursor_one_field(sql, arr)

        
    def connect(self, connection_string=None):
        """Used in code to connect using last self.strcon"""
        super().connect(connection_string)
        self.restart_timeout()
        self._timerlastuse = QTimer()
        self._timerlastuse.timeout.connect(self._check_inactivity)
        self._timerlastuse.start(300000)

    def disconnect(self):
        self._active=False
        if self._timerlastuse.isActive()==True:
            self._timerlastuse.stop()
        self._con.close()

