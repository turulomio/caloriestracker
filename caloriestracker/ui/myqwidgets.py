## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QApplication, QInputDialog, QLineEdit, qApp
from decimal import Decimal
from os import path, remove

def qmessagebox(text, resource=":/reusingcode/qmessagebox"):
    m=QMessageBox()
    m.setWindowIcon(QIcon(resource))
    m.setIcon(QMessageBox.Information)
    m.setText(text)
    m.exec_()


def qinputbox_string(text, resource=":/reusingcode/qmessagebox"):
    m=QInputDialog()
    qApp.setWindowIcon(QIcon(resource)) #In windows m.setWindowIcon fails, so I need o set qApp window
    text,  ok_pressed=m.getText(None,  QApplication.translate("Reusing","Enter a string"), text , QLineEdit.Normal)
    if ok_pressed is True:
        return text
    else:
        return None

def qinputbox_decimal(text, resource=":/reusingcode/qmessagebox"):
    while True:
        m=QInputDialog()
        qApp.setWindowIcon(QIcon(resource)) #In windows m.setWindowIcon fails, so I need o set qApp window
        text,  ok_pressed=m.getText(None,  QApplication.translate("Reusing","Enter a number"), text , QLineEdit.Normal)
        if ok_pressed is True:
            try:
                return Decimal(text)
            except:
                pass
        else:
            return None

def qmessagebox_developing():
    qmessagebox(QApplication.translate("Reusing", "This part is being developed."))

## Asks a a question to delete a file
## Returns True or False if file has been deleted
def question_delete_file(filename):
    reply = QMessageBox.question(
                    None, 
                    QApplication.translate("Reusing", 'File deletion question'), 
                    QApplication.translate("Reusing", "Do you want to delete this file:\n'{}'?").format(filename), 
                    QMessageBox.Yes, 
                    QMessageBox.No
                )
    if reply==QMessageBox.Yes:
        remove(filename)
        if path.exists(filename)==False:
            return True
    return False
    
## Asks a a question 
## Returns True or False when the user clicks in yes or no button
def qmessagebox_question(text):
    reply = QMessageBox.question(
                    None, 
                    QApplication.translate("Reusing", 'Please answer this question'), 
                    text, 
                    QMessageBox.Yes, 
                    QMessageBox.No
                )
    if reply==QMessageBox.Yes:
            return True
    return False
