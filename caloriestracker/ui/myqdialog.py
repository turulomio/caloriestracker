## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout

class WidgetsDisplayMode:
    Vertical=0
    Horizonal=1

class MyNonModalQDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.parent=parent
        self._widgetsDisplayMode=WidgetsDisplayMode.Vertical

    def setSettings(self, settings, settingsSection, settingsObject, width=800, height=600):
        self.settings=settings
        self._settingsSection=settingsSection
        self._settingsObject=settingsObject
        self.resize(self.settings.value("{}/{}".format(self._settingsSection, self._settingsObject), QSize(width, height)))


    def setWidgetsDisplayMode(self, wdm):
        self._widgetsDisplayMode=wdm

    def widgetsDisplayMode(self):
        return self._widgetsDisplayMode

    ## @param *widgets List of Widgets
    def setWidgets(self, *widgets):
        if self.widgetsDisplayMode()==WidgetsDisplayMode.Vertical:
            self.layout = QVBoxLayout(self)
        elif self.widgetsDisplayMode()==WidgetsDisplayMode.Horizontal:
            self.layout = QHBoxLayout(self)
        for wdg in widgets:
            self.layout.addWidget(wdg)

    ## Manage close event to save dialog size
    def closeEvent(self, event):
        self._syncSettings()

    def _syncSettings(self):
        self.settings.setValue("{}/{}".format(self._settingsSection, self._settingsObject), self.size())
        self.settings.sync()

class MyModalQDialog(MyNonModalQDialog):
    def __init__(self, parent=None):
        MyNonModalQDialog.__init__(self, parent)

    def exec_(self):
        self._syncSettings()
        QDialog.exec_(self)
