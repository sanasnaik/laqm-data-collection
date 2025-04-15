"""
Note: run this code file on its own for long-term collection. 
Tkinter ends up freezing with too many threads running at once.

Created on Monday February 10 2025
Creator: Sana Naik
Under supervision of: Professor Jak Chakalian, Tsung-Chi Wu
"""
import time
import MultiPyVu as mpv
import datetime

#  Separate clases to keep code modular!
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
temp = 0
field = 0

try:
    instrument.set_harmonic(harm_num)
except:
    print("Error: enter 1, 2, or 3 for harmonic number.")

instrument.set_frequency(freq)

# Immediately starts collecting data.
try:
    while True:
        harm1 = instrument.get_harmonic()
        voltage1 = instrument.get_voltage()
        freq1 = instrument.get_frequency()
        channel11 = instrument.get_channel1()
        channel21 = instrument.get_channel2()

        data_handler.append_data(time_value, harm1, voltage1, freq1, channel11, channel21, temp, field)
                
        time_value += 0.5
        time_value = round(time_value, 1)
        time.sleep(0.5)

except Exception as e:
    print(f"Error {e}")
