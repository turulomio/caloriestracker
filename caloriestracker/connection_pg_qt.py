## @brief Package to manage postgresql connection functions with qt timeouts
## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from datetime import datetime,  timedelta
from PyQt5.QtCore import QObject,  pyqtSignal,  QTimer
from .connection_pg import Connection
from logging import debug

class ConnectionQt(QObject,Connection):
    inactivity_timeout=pyqtSignal()
    def __init__(self):
        Connection.__init__(self)
        QObject.__init__(self)
        self._timerlastuse = QTimer()
        self._timerlastuse.timeout.connect(self._check_inactivity)
        self._inactivity_timeout_seconds=30*60

    def _check_inactivity(self):
        if datetime.now()-self._lastuse>timedelta(seconds=self._inactivity_timeout_seconds):
            self.disconnect()
            debug("Disconnected due to inactivity")
            self.inactivity_timeout.emit()
        else:
            self._timerlastuse.start(self._inactivity_timeout_seconds*1000/5)
            debug("Connection remaining time: {}".format(self._lastuse+timedelta(seconds=self._inactivity_timeout_seconds)-datetime.now()))

    ## Returns the number of seconds of the timeout
    def connectionTimeout(self):
        return self._inactivity_timeout_seconds

    ## @param seconds int with the number of connection timeout limit
    def setConnectionTimeout(self, seconds):
        self._inactivity_timeout_seconds=seconds

    def cursor(self):
        self._lastuse=datetime.now()
        return self._con.cursor()

    def cursor_one_row(self, sql, arr=[]):
        self._lastuse=datetime.now()
        return super().cursor_one_row(sql, arr)

    def execute(self, sql, arr=[]):
        self._lastuse=datetime.now()
        return super().execute(sql, arr)

    def cursor_one_column(self, sql, arr=[]):
        self._lastuse=datetime.now()
        return super().cursor_one_column(sql, arr)

    def cursor_one_field(self, sql, arr=[]):
        self._lastuse=datetime.now()
        return super().cursor_one_field(sql, arr)

    ## Used in code to connect using last self.strcon
    def connect(self, connection_string=None):
        super().connect(connection_string)
        self._lastuse=datetime.now()
        self._check_inactivity()

    def disconnect(self):
        if self.is_active()==True:
            if self._timerlastuse and self._timerlastuse.isActive()==True:
                self._timerlastuse.stop()
            Connection.disconnect(self)

