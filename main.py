
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, QTimer, Qt
from matplotlib.figure import Figure
from algorithms.bubblesort import BubbleSort
from algorithms.insertionsort import InsertionSort
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
    
    

        

