"""
Created on Thu Jan 26 15:55:22 2023
THIS HAS NO LAKESHORE TEMPERATURE CONTROLLER FUNCTIONALITY BEWARE
@author: laqm
Current contributor: Sana Naik
Past contributor: Keanu Shah
Under supervision of: Professor Jak Chakalian, Tsung-Chi Wu
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

# Create initial CSV file
def create_file():
    
    with open(f"C:\\Users\laqm\Documents\CSV Data Outputs\{current_time}.csv", mode='w', newline="") as csv_file:
        
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Time', 'Voltage', 'Frequency', 'Channel1(X)', 'Channel2(Y)', 'Sensitivity', 'Temperature', 
                         'PID', 'Ramprate', 'Setpoint'])

def data_collect():
    
    if instrument_type == 'Lock-In Amplifier':
        collect_lockin_data()
        
    elif instrument_type == 'Keithley':
        collect_keithley_data()

def collect_lockin_data():
    
    voltageincrement, timevalue = 0.1, 0
    fieldnames = ['Time', 'Voltage', 'Frequency', 'Channel1(X)', 'Channel2(Y)']
    print(fieldnames)
    
    with open(f"C:\\Users\laqm\Documents\CSV Data Outputs\{current_time}.csv", mode='w') as csv_file:
        
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        
    while timevalue < 172800:  # 48hrs
    
        channel1 = float(my_instrument.query_ascii_values("OUTP? 1")[0])
        freq = my_instrument.query_ascii_values('FREQ?')[0]
        voltage = my_instrument.query_ascii_values('SLVL?')[0]
        channel2 = float(my_instrument.query_ascii_values("OUTP? 2")[0])
    
        values = [timevalue, voltage, freq, channel1, channel2]
        print(values)
    
        with open(f"C:\\Users\laqm\Documents\CSV Data Outputs\{current_time}.csv", mode='a', newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            info = {
                "Time": timevalue,
                "Voltage": voltage,
                "Frequency": freq,
                "Channel1(X)": channel1,
                "Channel2(Y)": channel2
            }
            csv_writer.writerow(info)
    
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

    with open(f"C:\\Users\laqm\Documents\CSV Data Outputs\{current_time}.csv", mode='w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    while x < 600000:
        time1 = time.time()
        my_instrument.write('INIT:IMM')
        log.info('Delta measurements have started')

        temp = my_instrument.query('TRAC:DATA?').replace('+', '').split(',')[0]
        values = [round(timevalue + (time.time() - time1), 2), temp]

        with open(f"C:\\Users\laqm\Documents\CSV Data Outputs\{current_time}.csv", mode='a') as csv_file:
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

def plot(xvar, yvar):
    data = pd.read_csv(f"C:\\Users\laqm\Documents\CSV Data Outputs\{current_time}.csv")
    plt.plot(data[xvar], data[yvar])
    plt.xlabel(xvar)
    plt.ylabel(yvar)
    plt.show()

# Driver Code
create_file()
data_collect()