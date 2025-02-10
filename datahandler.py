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
            
        self.fieldnames = ['Time', 'Harmonic', 'Voltage', 'Frequency', 'Channel1(X)', 'Channel2(Y)', 'Temperature', 'Field']
        self.data = {  
            'Time': [],
            'Harmonic': [],
            'Voltage': [], 
            'Frequency': [], 
            'Channel1(X)': [], 
            'Channel2(Y)': [],
            'Temperature': [],
            'Field': []
        }
        
        
    def write_to_csv(self, info):
        
        with open(self.csv_file_path, mode='a', newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            csv_writer.writerow(info)
    
    
    def write_header(self):
        
        with open(self.csv_file_path, mode='a', newline='') as csv_file: # Commented out original csv_writer lines, throwing error b/c dictionary misuse
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(self.fieldnames)

    def append_data(self, time, harmonic, voltage, freq, channel1, channel2, temp, field):
        
        info = {
            "Time": time,
            "Harmonic": harmonic,
            "Voltage": voltage,
            "Frequency": freq,
            "Channel1(X)": float(channel1),
            "Channel2(Y)": float(channel2),
            'Temperature': temp,
            'Field': field

        }

        self.data['Time'].append(time)
        self.data['Harmonic'].append(harmonic)
        self.data['Voltage'].append(voltage)
        self.data['Frequency'].append(freq)
        self.data['Channel1(X)'].append(float(channel1))
        self.data['Channel2(Y)'].append(float(channel2))
        self.data['Temperature'].append(temp)
        self.data['Field'].append(field)
        self.write_to_csv(info)