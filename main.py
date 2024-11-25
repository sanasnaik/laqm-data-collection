"""
Created on Thu Jan 26 15:55:22 2023
THIS HAS NO LAKESHORE TEMPERATURE CONTROLLER OR KEITHLEY FUNCTIONALITY
@author: laqm
Current contributor: Sana Naik
Past contributor: Keanu Shah
Under supervision of: Professor Jak Chakalian, Tsung-Chi Wu
"""
import tkinter as tk

#  Separate clases to keep code modular!
from instrument import Instrument
from datahandler import DataHandler
from gui import GUI
from plotter import Plotter

#  Initialize
instrument = Instrument()
data_handler = DataHandler()
plotter = Plotter(None, None, None)
root = tk.Tk()
gui = GUI(root, instrument, data_handler, plotter)

root.mainloop()

