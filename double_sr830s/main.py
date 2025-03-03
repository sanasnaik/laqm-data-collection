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
    with mpv.Client() as client:

        data_handler = DataHandler()
        instrument_1 = Instrument(client, data_handler)
        instrument_2 = Instrument(client, data_handler, 'GPIB0::9::INSTR')
        plotter = Plotter(None, None, None)  # unused
        root = tk.Tk()
        gui = GUI(root, instrument_1, instrument_2, data_handler, plotter, client)

        root.mainloop()
        sys.exit()