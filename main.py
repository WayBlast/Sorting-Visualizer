from matplotlib.backends.backend_qt5agg import FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, QTimer, Qt
from matplotlib.figure import Figure
import random



NO_ELEMENTS = 25
MAX_VALUE = NO_ELEMENTS

PRIMARY_COLOR = "deepskyblue"
SECONDARY_COLOR = "yellowgreen"
TERTIARY_COLOR = "darkorange"
QUARTERNARY_COLOR = "yellow"
FINISH_COLOR = "green"

BUBBLE_DESCRIPTION = "Bubble Sort is a simple comparison-based sorting algorithm that repeatedly compares adjacent elements and swaps them if they are in the wrong order. After each pass, the largest unsorted element “bubbles” to its correct position at the end of the array.<br><br><b>Time Complexity:</b> Best: O(n), Average: O(n<sup>2</sup>), Worst: O(n<sup>2</sup>)<br><b>Space Complexity:</b> O(1) &nbsp;&nbsp; <b>Stable:</b> Yes &nbsp;&nbsp; <b>In-Place:</b> Yes"
INSERTION_DESCRIPTION = "Insertion Sort is a simple comparison-based sorting algorithm that builds the sorted array one element at a time by inserting each new element into its correct position within the already sorted portion. It shifts larger elements to the right to make space for the current key.<br><br><b>Time Complexity:</b> Best: O(n), Average: O(n<sup>2</sup>), Worst: O(n<sup>2</sup>)<br><b>Space Complexity:</b> O(1) &nbsp;&nbsp; <b>Stable:</b> Yes &nbsp;&nbsp; <b>In-Place:</b> Yes"

class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "Sorting Visualizer"
        self.setWindowTitle(title)

        self._createActions()
        self._createMenuBar()
        self._connectActions()
        self.sort = "Bubble Sort"

        self.no_values = MAX_VALUE

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.ax = self.canvas.figure.subplots()

        self._generateData()   
        self._draw()     
        
        self.animation_button = QPushButton("Run", checkable=True)
        self.shuffle_button = QPushButton("Shuffle", checkable=False)
        self.animation_button.setChecked(False)

        font_btn = QFont("Arial", 13)
        font_btn.setBold(True)
        self.animation_button.setFont(font_btn)
        self.shuffle_button.setFont(font_btn)

        self.animation_button.toggled.connect(self.handle_toggled)
        self.shuffle_button.clicked.connect(self.handle_shuffle)
        central_widget = QWidget()

        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout_buttons = QHBoxLayout()
        layout.addWidget(self.canvas)
        
        self.sort_title = QLabel("Bubble Sort", self)
        self.sort_title.setAlignment(Qt.AlignCenter)
        font = QFont('Arial', 14)
        font.setBold(True)
        self.sort_title.setFont(font)

        self.description = QLabel(BUBBLE_DESCRIPTION, self)
        self.description.setAlignment(Qt.AlignCenter)
        self.description.setWordWrap(True)
        font_desc = QFont('Arial', 10)
        self.description.setFont(font_desc)

        underline = QFrame()
        underline.setFrameShape(QFrame.HLine)
        underline.setFrameShadow(QFrame.Raised)  
        underline.setLineWidth(2) 

        overline = QFrame()
        overline.setFrameShape(QFrame.HLine)
        overline.setFrameShadow(QFrame.Raised)  
        overline.setLineWidth(2) 

        layout.addWidget(overline)
        layout.addWidget(self.sort_title)
        layout.addWidget(self.description)
        layout.addWidget(underline)
        
        
        layout.addLayout(layout_buttons)
        layout_buttons.addWidget(self.animation_button)
        layout_buttons.addWidget(self.shuffle_button)

        self.anim_running = False
        self.anim.event_source.stop()
        self.animation_button.setChecked(False)

    def _draw(self):
        match self.sort:
            case 'Bubble Sort':
                self.anim = animation.FuncAnimation(
                    self.canvas.figure,
                    self.callback_animation_bubble,
                    frames=self.generator,
                    interval=1,
                    blit=False,
                    cache_frame_data=False
                )

                self._anim_bootstrapped = False
                if hasattr(self.anim, "_first_draw_id"):
                    self.canvas.mpl_disconnect(self.anim._first_draw_id)

                self.anim.event_source.stop()

            case 'Insertion Sort':
                
                self.anim = animation.FuncAnimation(
                    self.canvas.figure,
                    self.callback_animation_insertion,
                    frames=self.generator,
                    interval=1,
                    blit=False,
                    cache_frame_data=False
                )

                self._anim_bootstrapped = False
                if hasattr(self.anim, "_first_draw_id"):
                    self.canvas.mpl_disconnect(self.anim._first_draw_id)

                self.anim.event_source.stop()

            case _:
                pass

    def _generateData(self):
        self.values = random.sample(range(1, self.no_values+1), self.no_values)
        
        self.ax.clear()
        self.ax.set_ylim(0,self.no_values)
        self.barcollection = self.ax.bar(range(len(self.values)), 
                                         self.values,
                                         width=1.0,
                                         edgecolor='none',
                                         linewidth=0,
                                         color="deepskyblue")
    
        match self.sort:
            case 'Bubble Sort':
                self.generator = bubblesort(self.values)
                self.last = [self.barcollection[0],self.barcollection[1]]
                self.barrier = [len(self.values)-1]
                self.finish_index = [0]
            case 'Insertion Sort':
                self.generator = insertionsort(self.values)
                self.barrier = [0] 
                self.finish_index = [0]
        

    def _createMenuBar(self):
        menuBar = self.menuBar()
        settingsMenu = QMenu("&Settings", self)
        menuBar.addMenu(settingsMenu)

        algoSelectMenu = settingsMenu.addMenu("Algorithm...")
        algoSelectMenu.addAction(self.bubbleAction)
        algoSelectMenu.addAction(self.insertionAction)
        algoSelectMenu.addAction(self.selectionAction)

        numberMenu = settingsMenu.addMenu("Number...")

        for n in (10, 25, 50, 75, 99):
            numberMenu.addAction(
                str(n),
                lambda _=False, x=n: self.set_number_and_shuffle(x)
            )
        settingsMenu.addAction(self.speedAction)
        menuBar.addMenu(QMenu("&Help", self))

    def _connectActions(self):
        self.bubbleAction.triggered.connect(lambda checked = False: self.change_sort("Bubble Sort"))
        self.insertionAction.triggered.connect(lambda checked = False: self.change_sort("Insertion Sort"))

    def _createActions(self):
        self.numberAction = QAction(self)
        self.numberAction.setText("&Number")
        self.speedAction = QAction(self)
        self.speedAction.setText("&Speed")

        self.bubbleAction = QAction(self)
        self.bubbleAction.setText("&Bubble Sort")
        self.insertionAction = QAction(self)
        self.insertionAction.setText("&Insertion Sort")
        self.selectionAction = QAction(self)
        self.selectionAction.setText("&Selection Sort")

    def change_sort(self, sort: str):
        self.sort = sort
        self.handle_shuffle()
        self.sort_title.setText(sort)
        match sort:
            case "Bubble Sort":
                self.description.setText(BUBBLE_DESCRIPTION)
            case "Insertion Sort":
                self.description.setText(INSERTION_DESCRIPTION)

    def callback_animation_insertion(self, frame):
        values, i, j, edge = frame
        if edge == -1:
            if self.finish_index[0] == 0:
                self.anim.event_source.interval = 80

            if self.finish_index[0] == len(self.barcollection):
                self.animation_button.blockSignals(True)
                self.animation_button.setChecked(False)
                self.animation_button.setText("Run")
                self.animation_button.blockSignals(False)
                self.anim.event_source.stop()
            else:    
                self.barcollection[self.finish_index[0]].set_color(FINISH_COLOR)
                self.finish_index[0] += 1 

            
        else:
            for bar in range(len(self.barcollection)):
                self.barcollection[bar].set_height(values[bar])
                self.barcollection[bar].set_color("deepskyblue")

            if edge == 1 and self.barrier[0] != len(self.barcollection) :
                self.barrier[0] += 1
            
            for bar in range(0, self.barrier[0]):
                self.barcollection[bar].set_color(SECONDARY_COLOR)
            self.barcollection[i].set_color(TERTIARY_COLOR)
            self.barcollection[j].set_color(QUARTERNARY_COLOR)

    def callback_animation_bubble(self, frame):
        
        i, j, values, edge  = frame
        if edge == -1:
            if self.finish_index[0] == 0:
                self.anim.event_source.interval = 80
                self.barcollection[self.finish_index[0]].set_color(FINISH_COLOR)

            if self.finish_index[0] == len(self.barcollection):
                self.animation_button.blockSignals(True)
                self.animation_button.setChecked(False)
                self.animation_button.setText("Run")
                self.animation_button.blockSignals(False)
                self.anim.event_source.stop()
            else:    
                self.barcollection[self.finish_index[0]].set_color(FINISH_COLOR)
                self.finish_index[0] += 1 
        else: 
            self.last[0].set_color("deepskyblue")
            self.last[1].set_color("deepskyblue")

            if edge == 1:
                
                self.barcollection[self.barrier[0]].set_color(SECONDARY_COLOR)
                self.barrier[0] -= 1
            
            self.barcollection[i].set_color(TERTIARY_COLOR)
            self.barcollection[j].set_color(SECONDARY_COLOR)

            self.barcollection[i].set_height(values[i])
            self.barcollection[j].set_height(values[j])
            self.last[0] = self.barcollection[i]
            self.last[1] = self.barcollection[j]

    def set_number_and_shuffle(self, n: int):
        self.no_values = n
        self.handle_shuffle()

    def handle_shuffle(self):
        self.anim.event_source.stop()
        self._anim_bootstrapped = False

        self.animation_button.blockSignals(True)
        self.animation_button.setChecked(False)
        self.animation_button.setText("Run")
        self.animation_button.blockSignals(False)

        self._generateData()
        self._draw()

        self.canvas.draw()

    def handle_toggled(self, checked: bool):
        if checked:
            if not self._anim_bootstrapped:
                self._anim_bootstrapped = True
                self.anim._start()  
            else:
                self.anim.event_source.start()

            self.animation_button.setText("Stop")
        else:
            self.anim.event_source.stop()
            self.animation_button.setText("Run")

    def closeEvent(self, event):
        super().closeEvent(event)      

def bubblesort(values: list[int]):
    i = 0
    barrier = len(values) - 1
    
    while True:
        edge = 0
        if barrier == 0:
            while True:
                
                edge = -1
                yield (i,i+1,values, edge)

        if i == barrier:
            i = 0
            barrier -= 1
            edge = 1
            
        if values[i+1] < values[i]:
                
                temp = values[i+1]
                values[i+1] = values[i]
                values[i] = temp
        yield (i,i+1,values, edge)
        i+=1     

def insertionsort(values: list[int]):
    for j in range(1, len(values)):
        key = values[j]
        i = j-1

        while i >= 0 and values[i] > key:
            values[i+1] = values[i]
            i -= 1

            yield (values, i, j, 0)
        values[i+1] = key 
        yield (values, i, j, 1)
    while True:
        yield (values, i, j, -1)


if __name__ =="__main__":
    qapp = QApplication.instance()
    if not qapp:
        qapp = QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()
    
    

        

