## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

def qmessagebox(text, resource=None):
    m=QMessageBox()
    if resource==None:
        m.setWindowIcon(QIcon(resource))
    m.setIcon(QMessageBox.Information)
    m.setText(text)
    m.exec_()
