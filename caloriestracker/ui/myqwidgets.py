## THIS IS FILE IS FROM https://github.com/turulomio/reusingcode IF YOU NEED TO UPDATE IT PLEASE MAKE A PULL REQUEST IN THAT PROJECT
## DO NOT UPDATE IT IN YOUR CODE IT WILL BE REPLACED USING FUNCTION IN README

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QApplication
from os import path, remove

def qmessagebox(text, resource=None):
    m=QMessageBox()
    if resource==None:
        m.setWindowIcon(QIcon(resource))
    m.setIcon(QMessageBox.Information)
    m.setText(text)
    m.exec_()



## Asks a a question to delete a file
## Returns True or False if file has been deleted
def question_delete_file(filename):
    reply = QMessageBox.question(
                    None, 
                    QApplication.translate("Core", 'File deletion question'), 
                    QApplication.translate("Core", "Do you want to delete this file:\n'{}'?").format(filename), 
                    QMessageBox.Yes, 
                    QMessageBox.No
                )
    if reply==QMessageBox.Yes:
        remove(filename)
        if path.exists(filename)==False:
            return True
    return False