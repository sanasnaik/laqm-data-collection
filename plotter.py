# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 14:41:30 2024

@author: laqm
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Plotter:
    def __init__(self, canvas, ax):
        self.canvas = canvas
        self.ax = ax
        self.autoscale = True
        self.plot_type = "line_graph"
    
    def update_plot(self, data, x_option, y_option):
        self.ax.clear()
        if self.autoscale:
            self.ax.autoscale(True)
        if self.plot_type == "line_graph":
            self.ax.plot(data[x_option], data[y_option], color="blue")
        elif self.plot_type == "scatter_plot":
            self.ax.scatter(data[x_option], data[y_option], color="blue")
        self.ax.set_xlabel(x_option)
        self.ax.set_ylabel(y_option)
        self.ax.set_title(f'{y_option} vs. {x_option}')
        self.canvas.draw()

    def change_plot(self):
        if self.plot_type == "line_graph":
            self.plot_type = "scatter_plot"
        elif self.plot_type == "scatter_plot":
            self.plot_type = "line_graph"