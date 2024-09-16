"""
Created on Thu Jan 26 15:55:22 2023
THIS HAS NO LAKESHORE TEMPERATURE CONTROLLER FUNCTIONALITY BEWARE
@author: laqm
"""

import pyvisa
import csv
import time
import logging as log
import pandas as pd
import matplotlib.pyplot as plt
import datetime

rm = pyvisa.ResourceManager()
current_time = datetime.datetime.now().strftime("%m-%d-%Y %I.%M%p")

def select_instrument():
    if 'GPIB0::16::INSTR' in rm.list_resources():
        return rm.open_resource('GPIB0::16::INSTR'), 'Keithley'
    else:
        return rm.open_resource('GPIB0::8::INSTR'), 'Lock-In Amplifier'

my_instrument, instrument_type = select_instrument()

sensitivityold = { 0: "2 nV/fA",	13: "50 uV/pA",
                1: "5 nV/fA",		14: "100 uV/pA",
                2: "10 nV/fA",	    15: "200 uV/p                                                                                                                                    ",
                3: "20 nV/fA",	    16: "500 uV/pA",
                4: "50 nV/fA",	    17: "1 mV/nA",
                5: "100 nV/fA",	    18: "2 mV/nA",
                6: "200 nV/fA",	    19: "5 mV/nA",
                7: "500 nV/fA",	    20: "10 mV/nA",
                8: "1 uV/pA",		21: "20 mV/nA",
                9: "2 uV/pA",		22: "50 mV/nA",
                10: "5 uV/pA",		23: "100 mV/nA",
                11: "10 uV/pA",	    24: "200 mV/nA",
                12: "20 uV/pA",	    25: "500 mV/nA",
                26: "1 V/uA" }

def autosensitivity(channel1x):
    
    newvalue = 10 * channel1x
    sensitivity = [2e-9, 5e-9, 1e-8, 2e-8, 5e-8, 1e-7, 
                   2e-7, 5e-7, 1e-6, 2e-6, 5e-6, 1e-5, 
                   2e-5, 5e-5, 1e-4, 2e-4, 5e-4, 1e-3, 
                   2e-3, 5e-3, 1e-2, 2e-2, 5e-2, 1e-1, 
                   2e-1, 5e-1]
    
    xmax = [newvalue - x if newvalue - x >= 0 else 500 for x in sensitivity]
    return xmax.index(min(xmax))

# Create initial CSV file
def create_file():
    
    with open(f"CSV Data Outputs/{current_time}.csv", mode='w', newline="") as csv_file:
        
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Time', 'Voltage', 'Frequency', 'Channel1(X)', 'Channel2(Y)', 'Sensitivity', 'Temperature', 
                         'PID', 'Ramprate', 'Setpoint'])

def data_collect():
    
    if instrument_type == 'Lock-In Amplifier':
        collect_lockin_data()
        
    elif instrument_type == 'Keithley':
        collect_keithley_data()

def collect_lockin_data():
    
    count, voltageincrement, timevalue = 0, 0.1, 0
    fieldnames = ['Time', 'Voltage', 'Frequency', 'Channel1(X)', 'Channel2(Y)']

    with open(f"CSV Data Outputs/{current_time}.csv", mode='w') as csv_file:
        
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    while count < 172800:
        
        channel1 = float(my_instrument.query_ascii_values("OUTP? 1")[0])
        freq = my_instrument.query_ascii_values('FREQ?')[0]
        voltage = my_instrument.query_ascii_values('SLVL?')[0]
        channel2 = float(my_instrument.query_ascii_values("OUTP? 2")[0])

        values = [timevalue, voltage, freq, channel1, channel2]
        print(values)

        with open(f"CSV Data Outputs/{current_time}.csv", mode='a', newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            info = {
                "Time": timevalue,
                "Voltage": voltage,
                "Frequency": freq,
                "Channel1(X)": channel1,
                "Channel2(Y)": channel2
            }
            csv_writer.writerow(info)

        count += 2
        time.sleep(2)
        timevalue += 2
        timevalue = round(timevalue, 2)
        voltageincrement += 0.3
        plot('Time', 'Channel1(X)')  # Plotting Time vs Channel1(X)

def collect_keithley_data():
    
    timevalue = 0
    x = 0

    my_instrument.write('*RST')
    my_instrument.write("TRAC:CLE")
    my_instrument.write('SYST:COMM:SER:SEND "REN"')
    my_instrument.write('SYST:COMM:SER:SEND "VOLT:RANG 0.01"')
    my_instrument.write('SYST:COMM:SER:SEND "VOLT:NPLC 1"')
    my_instrument.write('*RST')
    my_instrument.write('SOUR:DELT:HIGH 1e-6')
    my_instrument.write('SOUR:DELT:COUN 1')
    my_instrument.write('SOUR:CURR:RANGE:AUTO 1')
    my_instrument.write('TRAC:POIN 1')
    my_instrument.write('SOUR:DELT:ARM')

    fieldnames = ["Time", "Temperature", "Voltage", "PID", "RampRate", "Setpoint"]

    with open(f"CSV Data Outputs/{current_time}.csv", mode='w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    while x < 600000:
        time1 = time.time()
        my_instrument.write('INIT:IMM')
        log.info('Delta measurements have started')

        temp = my_instrument.query('TRAC:DATA?').replace('+', '').split(',')[0]
        values = [round(timevalue + (time.time() - time1), 2), temp]

        with open(f"CSV Data Outputs/{current_time}.csv", mode='a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            info = {
                "Time": values[0],
                "Temperature": values[1]
            }
            csv_writer.writerow(info)

        x += 0.1
        time.sleep(1)
        timevalue += 1
        timevalue = round(timevalue, 2)

    my_instrument.write('*RST')
    my_instrument.write("TRAC:CLE")

# Read data from the CSV file
def read_file():
    with open(f"CSV Data Outputs/{current_time}.csv", newline="") as csv_file:
        reader = csv.reader(csv_file)
        for item in reader:
            print(item)

# Plotting function
def plot(xvar, yvar):
    data = pd.read_csv(f"CSV Data Outputs/{current_time}.csv")
    plt.plot(data[xvar], data[yvar])
    plt.show()

# Driver Code
if instrument_type == 'Lock-In Amplifier':
    create_file()
    data_collect()
    read_file()