"""
Note: This file was created as a placeholder until we fix the PPMS connection and figure out why it randomly stops sending data to our program.
This file only collects SR830 data, and sets zero values for PPMS data (temperature and magnetic field).

Created on Monday February 10 2025
Creator: Sana Naik
Under supervision of: Professor Jak Chakalian, Tsung-Chi Wu
"""
import time
import datetime
from instrument import Instrument
from datahandler import DataHandler

current_time = datetime.datetime.now().strftime("%m-%d-%Y %I.%M%p")

# ------------------------ SET UP HERE ------------------------ #
# Set file path name:
name = 'tcwu-#6_MR_80K-130K_3w_37.37Hz_1sttry' # default: nothing
file_path = f"C:\\Users\\ppms\\Documents\\CSV Data Outputs\\{name}{current_time}.csv"

# Set harmonic number:
harm_num_1 = 3 # for sr830 8, default: 1
harm_num_2 = 3  # for sr830 9, default: 1

# Set frequency in Hz:
freq1 = 37.37  # for sr830 8
freq2 = 37.37  # for sr830 9
# ------------------------ SET UP END ------------------------ #

# Init
data_handler = DataHandler(file_path = file_path)
instrument_1 = Instrument(None, data_handler)
instrument_2 = Instrument(None, data_handler, 'GPIB0::9::INSTR')
data_handler.write_header()
time_value = 0

try:
    instrument_1.set_harmonic(harm_num_1)
    instrument_2.set_harmonic(harm_num_2)
except:
    print("Error setting harmonic number. Please enter 1, 2, or 3 for harmonic number.")

try:
    instrument_1.set_frequency(freq1)
    instrument_2.set_frequency(freq2)
except:
    print("Error setting frequency. Please set a valid frequency value.")

# Immediately starts collecting data.
try:
    while True:
        # First lock-in
        harm1 = instrument_1.get_harmonic()
        voltage1 = instrument_1.get_voltage()
        freq1 = instrument_1.get_frequency()
        channel11 = instrument_1.get_channel1()
        channel21 = instrument_1.get_channel2()

        # Second lock-in
        harm2 = instrument_2.get_harmonic()
        voltage2 = instrument_2.get_voltage()
        freq2 = instrument_2.get_frequency()
        channel12 = instrument_2.get_channel1()
        channel22 = instrument_2.get_channel2()

        data_handler.append_data(time_value, harm1, voltage1, freq1, channel11, channel21, harm2, voltage2, freq2, channel12, channel22, 0, 0)
                
        time_value += 0.5
        time_value = round(time_value, 1)
        time.sleep(0.5)

except Exception as e:
    print(f"Error {e}")
