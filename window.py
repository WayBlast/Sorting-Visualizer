from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
import sortingAnim
import json
import os

NO_ELEMENTS = 25
MAX_VALUE = NO_ELEMENTS

class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        base_dir = os.path.dirname(os.path.abspath(__file__))
        strings_file_path = os.path.join(base_dir, "config", "strings.json")

        with open(strings_file_path, "r", encoding="utf-8") as f:
            self.strings = json.load(f)
    
        title = self.strings['appTitle']
        self.setWindowTitle(title)
        self.setFixedSize(500,600)
        self._createActions()
        self._createMenuBar()
        self._connectActions()

        self.no_values = MAX_VALUE

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.ax = self.canvas.figure.subplots()

        
        self.animation = sortingAnim.SortingAnimation(self.canvas, self.ax, "Bubble Sort", self.no_values)
        self.animation.generateData()
        self.animation.draw()     
        
        # Buttons
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

        # Connect animation button to animation object - not optimal but it works :/
        self.animation.setButton(self.animation_button)

        # Center
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout_buttons = QHBoxLayout()
        layout.addWidget(self.canvas)
        
        # Sort Label
        self.sort_title = QLabel("Bubble Sort", self)
        self.sort_title.setAlignment(Qt.AlignCenter)
        font = QFont('Arial', 14)
        font.setBold(True)
        self.sort_title.setFont(font)

        # Sort Description
        self.description = QLabel(self.strings['description']['bubbleSort'], self)
        self.description.setAlignment(Qt.AlignCenter)
        self.description.setWordWrap(True)
        font_desc = QFont('Arial', 10)
        self.description.setFont(font_desc)

        # Underline
        underline = QFrame()
        underline.setFrameShape(QFrame.HLine)
        underline.setFrameShadow(QFrame.Raised)  
        underline.setLineWidth(2) 

        # Overline
        overline = QFrame()
        overline.setFrameShape(QFrame.HLine)
        overline.setFrameShadow(QFrame.Raised)  
        overline.setLineWidth(2) 

        # Connect all widgets
        layout.addWidget(overline)
        layout.addWidget(self.sort_title)
        layout.addWidget(self.description)
        layout.addWidget(underline)
        layout.addLayout(layout_buttons)
        layout_buttons.addWidget(self.animation_button)
        layout_buttons.addWidget(self.shuffle_button)

    
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
                lambda _=False, x=n: self.animation.set_number(x)
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
        self.animation.change_sort(sort)
        self.sort_title.setText(sort)
        match sort:
            case "Bubble Sort":
                self.description.setText(self.strings['description']['bubbleSort'])
            case "Insertion Sort":
                self.description.setText(self.strings['description']['insertionSort'])

    def handle_shuffle(self):
        self.animation_button.blockSignals(True)
        self.animation_button.setChecked(False)
        self.animation_button.setText("Run")
        self.animation_button.blockSignals(False)

        self.animation.handle_shuffle()


    def handle_toggled(self, checked: bool):
        self.animation.handleToggle(checked)

        if checked:
            self.animation_button.setText("Stop")
        else:
            self.animation_button.setText("Run")

    def closeEvent(self, event):
        super().closeEvent(event)      
