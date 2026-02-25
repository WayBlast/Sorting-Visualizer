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
from algorithms.bubblesort import BubbleSort
from algorithms.insertionsort import InsertionSort
import json
import os


class SortingAnimation():
    def __init__(self, canvas, ax, sort, no_values):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        style_file_path = os.path.join(base_dir, "config", "style.json")

        with open(style_file_path, "r", encoding="utf-8") as f:
            self.colors = json.load(f)
    
        self.primary_color = self.colors["themes"]["default"]["primaryColor"]
        self.secondary_color = self.colors["themes"]["default"]["secondaryColor"]
        self.tertiary_color = self.colors["themes"]["default"]["tertiaryColor"]
        self.quarternary_color = self.colors["themes"]["default"]["quarternaryColor"]
        self.finish_color = self.colors["themes"]["default"]["finishColor"]
        
        self.canvas = canvas
        self.ax = ax
        self.sort = sort
        self.no_values = no_values

    def draw(self):
        
        match self.sort:
            case 'Bubble Sort':
                func = self.callback_animation_bubble
            case 'Insertion Sort':
                func = self.callback_animation_insertion
            case _:
                raise Exception("Sorting Algorithm not defined")

        self.anim = animation.FuncAnimation(
            self.canvas.figure,
            func,
            frames=self.generator,
            interval=1,
            blit=False,
            cache_frame_data=False
        )

        self._anim_bootstrapped = False
        if hasattr(self.anim, "_first_draw_id"):
            self.canvas.mpl_disconnect(self.anim._first_draw_id)

        self.anim.event_source.stop()
        self.anim_running = False

    def callback_animation_bubble(self, frame):
        
        i, j, values, edge  = frame
        if edge == -1:
            if self.finish_index[0] == 0:
                self.anim.event_source.interval = 80
                self.barcollection[self.finish_index[0]].set_color(self.finish_color)

            if self.finish_index[0] == len(self.barcollection):
                self.animation_button.blockSignals(True)
                self.animation_button.setChecked(False)
                self.animation_button.setText("Run")
                self.animation_button.blockSignals(False)

                self.anim.event_source.stop()
            else:    
                self.barcollection[self.finish_index[0]].set_color(self.finish_color)
                self.finish_index[0] += 1 
        else: 
            self.last[0].set_color(self.primary_color)
            self.last[1].set_color(self.primary_color)

            if edge == 1:
                
                self.barcollection[self.barrier[0]].set_color(self.secondary_color)
                self.barrier[0] -= 1
            
            self.barcollection[i].set_color(self.tertiary_color)
            self.barcollection[j].set_color(self.quarternary_color)

            self.barcollection[i].set_height(values[i])
            self.barcollection[j].set_height(values[j])
            self.last[0] = self.barcollection[i]
            self.last[1] = self.barcollection[j]


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
                self.barcollection[self.finish_index[0]].set_color(self.finish_color)
                self.finish_index[0] += 1 
        else:
            for idx in self.last:  
                self.barcollection[idx].set_color(
                self.secondary_color if idx <= self.barrier[0] else self.primary_color
                )
                self.barcollection[idx].set_height(values[idx])
            
            
            if i >= 0 and j >= 0:
                self.barcollection[i].set_height(values[i])
                self.barcollection[i].set_color(self.tertiary_color)
                self.barcollection[j].set_height(values[j])

            if edge == 1 and self.barrier[0] != len(self.barcollection) :
                self.barrier[0] += 1
            
            # Performance killer
            for bar in range(0, self.barrier[0]):
                self.barcollection[bar].set_color(self.secondary_color)
            if i >= 0 and j >= 0:
                self.barcollection[i].set_color(self.tertiary_color)
                self.barcollection[j].set_color(self.quarternary_color)

                self.last[0] = i
                self.last[1] = j

    def setSort(self, sort):
        self.sort = sort


    def set_number(self, n: int):
        self.no_values = n
        self.handle_shuffle()

    def handle_shuffle(self):
        self.anim.event_source.stop()
        self._anim_bootstrapped = False
        
        self.generateData()
        self.draw()

        self.canvas.draw()

    def handleToggle(self, checked):
        if checked:
            if not self._anim_bootstrapped:
                self._anim_bootstrapped = True
                self.anim._start()  
            else:
                self.anim.event_source.start()
        else:
            self.anim.event_source.stop()

    def generateData(self):
        self.values = random.sample(range(1, self.no_values+1), self.no_values)
        
        self.ax.clear()
        self.ax.set_ylim(0,self.no_values+1)
        self.barcollection = self.ax.bar(range(len(self.values)), 
                                         self.values,
                                         width=0.7,
                                         edgecolor='none',
                                         linewidth=0,
                                         color=self.primary_color)
    
        match self.sort:
            case 'Bubble Sort':
                self.algo = BubbleSort(self.values)
                self.generator = self.algo.generator()
                self.last = [self.barcollection[0],self.barcollection[1]]
                self.barrier = [len(self.values)-1]
                self.finish_index = [0]
            case 'Insertion Sort':
                self.algo = InsertionSort(self.values)
                self.generator = self.algo.generator()
                self.barrier = [0] 
                self.last = [0,1]
                self.finish_index = [0]

    def setButton(self, animation_button):
        self.animation_button = animation_button
    
    def change_sort(self, sort: str):
        self.sort = sort
        self.handle_shuffle()

        self.animation_button.blockSignals(True)
        self.animation_button.setChecked(False)
        self.animation_button.setText("Run")
        self.animation_button.blockSignals(False)


    