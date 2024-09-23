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

# Prepare CSV file path
current_time = datetime.datetime.now().strftime("%m-%d-%Y %I.%M%p")
csv_file_path = f"C:\\Users\\laqm\\Documents\\CSV Data Outputs\\{current_time}.csv"
fieldnames = ['Time', 'Voltage', 'Frequency', 'Channel1(X)', 'Channel2(Y)']

# Collects data into CSV and displays datapoints as a plot
def data_collect():
    timevalue = 0

    # Write header to CSV file
    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    while True:
        # Query instrument data
        freq = my_instrument.query_ascii_values('FREQ?')[0]
        voltage = my_instrument.query_ascii_values('SLVL?')[0]
        channel1 = my_instrument.query_ascii_values("OUTP? 1")[0]
        channel2 = my_instrument.query_ascii_values("OUTP? 2")[0]

        # Prepare data for CSV
        info = {
            "Time": timevalue,
            "Voltage": voltage,
            "Frequency": freq,
            "Channel1(X)": float(channel1),
            "Channel2(Y)": float(channel2)
        }

        # Append data to CSV file
        with open(csv_file_path, mode='a', newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writerow(info)

        print(list(info.values()))  # Print data points
        time.sleep(2)
        timevalue += 2
        plot('Time', 'Channel1(X)')

def plot(xvar, yvar):  
    data = pd.read_csv(csv_file_path)
    plt.plot(data[xvar], data[yvar])
    plt.xlabel(xvar)
    plt.ylabel(yvar)
    plt.show()

# Driver Code
my_instrument = pyvisa.ResourceManager().open_resource('GPIB0::8::INSTR')
data_collect()