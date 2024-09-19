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

current_time = datetime.datetime.now().strftime("%m-%d-%Y %I.%M%p")
csv_file_path = f"C:\\Users\laqm\Documents\CSV Data Outputs\{current_time}.csv"
fieldnames = ['Time', 'Voltage', 'Frequency', 'Channel1(X)', 'Channel2(Y)']  # Field names for csv output
    
# Collects data into CSV and displays datapoints as a plot
def data_collect(writer):
    
    timevalue = 0
    print(fieldnames)

    while True:  # Until program is stopped
        freq     = my_instrument.query_ascii_values('FREQ?')[0]
        voltage  = my_instrument.query_ascii_values('SLVL?')[0]
        channel1 = my_instrument.query_ascii_values("OUTP? 1")[0]
        channel2 = my_instrument.query_ascii_values("OUTP? 2")[0]

        values = [timevalue, voltage, freq, float(channel1), float(channel2)]
        print(values)

        writer.writerow(values)

        time.sleep(2)
        timevalue += 2
        timevalue = round(timevalue, 2)
        plot('Time', 'Channel1(X)')


def plot(xvar, yvar):  # NOTE: THIS IS CURRENTLY NOT WORKING
    
    data = pd.read_csv(csv_file_path, delimiter=',')
    plt.plot(data[xvar], data[yvar])
    plt.xlabel(xvar)
    plt.ylabel(yvar)
    plt.show()

# Initiates CSV file + Driver Code
with open(csv_file_path, mode='w', newline="") as csv_file:
    
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(fieldnames)

    my_instrument = pyvisa.ResourceManager().open_resource('GPIB0::8::INSTR')
    data_collect(writer)