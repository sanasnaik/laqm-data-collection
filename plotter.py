# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 14:41:30 2024

@author: laqm
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Plotter:
    def __init__(self, canvas, ax, data_handler):
        
        self.canvas = canvas
        self.ax = ax
        self.autoscale = True
        self.plot_type = "line_graph"
        self.data_handler = data_handler
        
        self.x_option = 'Time'
        self.y_option = 'Channel1(X)'
    
    
    #  Occurs every two seconds
    def update_plot(self, data, x_option, y_option):
        
        self.ax.autoscale(self.autoscale)
            
        if self.plot_type == "line_graph":
            self.ax.plot(data[x_option], data[y_option], color="blue")
            
        elif self.plot_type == "scatter_plot":
            self.ax.scatter(data[x_option], data[y_option], color="blue")
            
        self.ax.set_xlabel(x_option)
        self.ax.set_ylabel(y_option)
        
        self.x_option = x_option
        self.y_option = y_option
        
        self.ax.set_title(f'{y_option} vs. {x_option}')
        self.canvas.draw()
        
        
    #  highlights and annotates the nearest data point
    def on_mouse_move(self, event):
        if event.inaxes is not None:
            mouse_x = event.xdata
            mouse_y = event.ydata
    
            #  calculate the distance from each data point
            distances = np.sqrt((np.array(self.data_handler.data[self.x_option]) - mouse_x) ** 2 +
                                (np.array(self.data_handler.data[self.y_option]) - mouse_y) ** 2)
            nearest_index = np.argmin(distances)  # index of the nearest point
    
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
    
            # Replot the graph
            self.ax.clear()
            
            if not self.autoscale:
                self.ax.set_xlim(xlim)
                self.ax.set_ylim(ylim)
    
            self.ax.autoscale(self.autoscale)
            
            if self.plot_type == "line_graph":
                self.ax.plot(self.data_handler.data[self.x_option], self.data_handler.data[self.y_option], color="blue")
            elif self.plot_type == "scatter_plot":
                self.ax.scatter(self.data_handler.data[self.x_option], self.data_handler.data[self.y_option], color="blue")
    
            #  highlight the nearest point
            self.ax.plot(self.data_handler.data[self.x_option][nearest_index],
                         self.data_handler.data[self.y_option][nearest_index], 'ro')
            self.ax.annotate(f'({self.data_handler.data[self.x_option][nearest_index]}, '
                             f'{self.data_handler.data[self.y_option][nearest_index]})',
                             (self.data_handler.data[self.x_option][nearest_index],
                              self.data_handler.data[self.y_option][nearest_index]),
                             textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8, color='red')
    
            self.ax.set_xlabel(self.x_option)
            self.ax.set_ylabel(self.y_option)
            self.ax.set_title(f'{self.y_option} vs. {self.x_option}')
    
            self.canvas.draw()


    def toggle_autoscale(self):
        self.autoscale = not self.autoscale