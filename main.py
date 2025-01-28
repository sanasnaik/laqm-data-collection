"""
Created on Thu Jan 26 15:55:22 2023
THIS HAS NO LAKESHORE TEMPERATURE CONTROLLER OR KEITHLEY FUNCTIONALITY
@author: laqm
Current contributor: Sana Naik
Past contributor: Keanu Shah
Under supervision of: Professor Jak Chakalian, Tsung-Chi Wu
"""
import tkinter as tk
import time
import MultiPyVu as mpv
import sys

#  Separate clases to keep code modular!
from instrument import Instrument
from datahandler import DataHandler
from gui import GUI
from plotter import Plotter

#  Initialize
#  Start the server.
with mpv.Server():
    #  Start the client
    with mpv.Client(socket_timeout=None) as client:
        
        data_handler = DataHandler()
        instrument = Instrument(client, data_handler)
        plotter = Plotter(None, None, None)
        root = tk.Tk()
        gui = GUI(root, instrument, data_handler, plotter, client)

        root.mainloop()
        sys.exit()