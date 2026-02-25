
import sys
from PyQt5.QtWidgets import *
import window

if __name__ =="__main__":
    qapp = QApplication.instance()
    if not qapp:
        qapp = QApplication(sys.argv)

    app = window.ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()
    
    

        

