# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 14:41:53 2024

@author: laqm
"""

import csv
import datetime

class DataHandler:
    
    def __init__(self, file_path=None):
        self.current_time = datetime.datetime.now().strftime("%m-%d-%Y %I.%M%p")
        
        if file_path:
            self.csv_file_path = file_path
        else:
            self.csv_file_path = f"C:\\Users\\ppms\\Documents\\CSV Data Outputs\\{self.current_time}.csv"
            
        self.fieldnames = ['Time', 'Harmonic_1', 'Harmonic_2', 'Voltage_1', 'Voltage_2', 'Frequency_1', 'Frequency_2', 'Channel1(X)_1', 'Channel1(X)_2', 'Channel2(Y)_1', 'Channel2(Y)_2', 'Temperature', 'Field']
        # self.data = {  
        #     'Time': [],
        #     'Harmonic1': [],
        #     'Voltage1': [], 
        #     'Frequency1': [], 
        #     'Channel1(X)1': [], 
        #     'Channel2(Y)1': [],
        #     'Harmonic2': [],
        #     'Voltage2': [], 
        #     'Frequency2': [], 
        #     'Channel1(X)2': [], 
        #     'Channel2(Y)2': [],
        #     'Temperature': [],
        #     'Field': []
        # }
        
        
    def write_to_csv(self, info):
        
        with open(self.csv_file_path, mode='a', newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            csv_writer.writerow(info)
    
    
    def write_header(self):
        
        with open(self.csv_file_path, mode='a', newline='') as csv_file: # Commented out original csv_writer lines, throwing error b/c dictionary misuse
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(self.fieldnames)

    def append_data(self, time, harmonic1, voltage1, freq1, channel11, channel21, harmonic2, voltage2, freq2, channel12, channel22, temp, field):
        
        info = {
            "Time": time,
            "Harmonic_1": harmonic1,
            "Harmonic_2": harmonic2,
            "Voltage_1": voltage1,
            "Voltage_2": voltage2,
            "Frequency_1": freq1,
            "Frequency_2": freq2,
            "Channel1(X)_1": float(channel11),
            "Channel1(X)_2": float(channel12),
            "Channel2(Y)_1": float(channel21),
            "Channel2(Y)_2": float(channel22),
            'Temperature': temp,
            'Field': field

        }

        # self.data['Time'].append(time)
        # self.data['Harmonic1'].append(harmonic1)
        # self.data['Voltage1'].append(voltage1)
        # self.data['Frequency1'].append(freq1)
        # self.data['Channel1(X)1'].append(float(channel11))
        # self.data['Channel2(Y)1'].append(float(channel21))
        # self.data['Harmonic2'].append(harmonic2)
        # self.data['Voltage2'].append(voltage2)
        # self.data['Frequency2'].append(freq2)
        # self.data['Channel1(X)2'].append(float(channel12))
        # self.data['Channel2(Y)2'].append(float(channel22))
        # self.data['Temperature'].append(temp)
        # self.data['Field'].append(field)
        self.write_to_csv(info)