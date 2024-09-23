"""
Created on Thu Jan 26 15:55:22 2023
THIS HAS NO LAKESHORE TEMPERATURE CONTROLLER OR KEITHLEY FUNCTIONALITY
@author: laqm
Current contributor: Sana Naik
Past contributor: Keanu Shah
Under supervision of: Professor Jak Chakalian, Tsung-Chi Wu
"""

import pyvisa
import csv
import time
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from tkinter import *

# Define constants
current_time = datetime.datetime.now().strftime("%m-%d-%Y %I.%M%p")
csv_file_path = f"C:\\Users\\laqm\\Documents\\CSV Data Outputs\\{current_time}.csv"
fieldnames = ['Time', 'Voltage', 'Frequency', 'Channel1(X)', 'Channel2(Y)']
my_instrument = pyvisa.ResourceManager().open_resource('GPIB0::8::INSTR')

# Collects data into CSV and plots
def run():
    timevalue = 0

    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    while True:
        freq = my_instrument.query_ascii_values('FREQ?')[0]
        voltage = my_instrument.query_ascii_values('SLVL?')[0]
        channel1 = my_instrument.query_ascii_values("OUTP? 1")[0]
        channel2 = my_instrument.query_ascii_values("OUTP? 2")[0]

        info = {
            "Time": timevalue,
            "Voltage": voltage,
            "Frequency": freq,
            "Channel1(X)": float(channel1),
            "Channel2(Y)": float(channel2)
        }

        with open(csv_file_path, mode='a', newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writerow(info)

        text = output_text.cget("text") + f"\n{timevalue}, {voltage}, {freq}, {float(channel1)}, {float(channel2)}"
        output_text.configure(text = text)
        time.sleep(2)
        timevalue += 2
        plot('Time', 'Channel1(X)')

def plot(xvar, yvar):  
    data = pd.read_csv(csv_file_path)
    plt.plot(data[xvar], data[yvar])
    plt.xlabel(xvar)
    plt.ylabel(yvar)
    plt.show()
    
def name_btn_clicked():
    current_time = datetime.datetime.now().strftime("%m-%d-%Y %I.%M%p")
    csv_file_path = f"C:\\Users\\laqm\\Documents\\CSV Data Outputs\\{name_entry.get()} {current_time}.csv"
    filepath_text.configure(text = csv_file_path)
    
# Driver code for GUI
root = Tk()

root.title("LAQM Lock-In Amplifier Data Visualizer")
root.geometry('960x540')

name_text = Label(root, text = "Enter your name (this will go in the CSV file name)")
name_text.grid(column = 0, row = 0)

name_entry = Entry(root, width = 10)
name_entry.grid(column = 1, row = 0)

name_btn = Button(root, text = "Enter", command = name_btn_clicked)
name_btn.grid(column = 2, row = 0)

start_text = Label(root, text = "Begin Program?")
start_text.grid(column = 0, row = 1)

start_btn = Button(root, text = "Start", command = run)
start_btn.grid(column = 1, row = 1)

filepath_text = Label(root, text = csv_file_path)
filepath_text.grid(column = 3, row = 1)

output_text = Label(root, text = "Output values:")
output_text.grid(column = 0, row = 2)

root.mainloop()