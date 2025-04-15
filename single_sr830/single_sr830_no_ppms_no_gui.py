"""
Note: This file was created as a placeholder until we fix the PPMS connection and figure out why it randomly stops sending data to our program.
This file only collects SR830 data, and sets zero values for PPMS data (temperature and magnetic field).

Creator: Sana Naik
Under supervision of: Professor Jak Chakalian, Tsung-Chi Wu
"""
import time
import MultiPyVu as mpv
import datetime
from instrument import Instrument
from datahandler import DataHandler

current_time = datetime.datetime.now().strftime("%m-%d-%Y %I.%M%p")

# ------------------------ SET UP HERE ------------------------ #
# Set file path name:
name = 'Sana_Test' # default: nothing
file_path = f"C:\\Users\\ppms\\Documents\\CSV Data Outputs\\{name}{current_time}.csv"

# Set harmonic number:
harm_num = 1  # for sr830 8, default: 1

# Set frequency in Hz:
freq = 137.77  # for sr830 8
# ------------------------ SET UP END ------------------------ #

# Init
data_handler = DataHandler(file_path = file_path)
instrument = Instrument(None, data_handler)
data_handler.write_header()
time_value = 0

try:
    instrument.set_harmonic(harm_num)
except:
    print("Error setting harmonic number. Please enter 1, 2, or 3 for harmonic number.")

try:
    instrument.set_frequency(freq)
except:
    print("Error setting frequency. Please set a valid frequency value.")

# Immediately starts collecting data.
try:
    while True:
        harm1 = instrument.get_harmonic()
        voltage1 = instrument.get_voltage()
        freq1 = instrument.get_frequency()
        channel11 = instrument.get_channel1()
        channel21 = instrument.get_channel2()

        data_handler.append_data(time_value, harm1, voltage1, freq1, channel11, channel21, 0, 0)
                
        time_value += 0.5
        time_value = round(time_value, 1)
        time.sleep(0.5)

except Exception as e:
    print(f"Error {e}")
