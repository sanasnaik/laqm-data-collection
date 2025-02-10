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
name = '' # default: nothing
file_path = f"C:\\Users\\ppms\\Documents\\CSV Data Outputs\\{name}{current_time}.csv"

# Set harmonic number:
harm_num = 1  # default: 1
# ------------------------ SET UP END ------------------------ #

#  Initialize
#  Start the server.
with mpv.Server():
    #  Start the client
    with mpv.Client(socket_timeout = None) as client:

        # Init
        data_handler = DataHandler(file_path = file_path)
        instrument = Instrument(client, data_handler)
        data_handler.write_header()
        time_value = 0
        try:
            instrument.set_harmonic(harm_num)
        except:
            print("Error: enter 1, 2, or 3 for harmonic number.")

        # Immediately starts collecting data.
        while True:
            harm = instrument.get_harmonic()
            voltage = instrument.get_voltage()
            freq = instrument.get_frequency()
            channel1 = instrument.get_channel1()
            channel2 = instrument.get_channel2()
            temp, _ = instrument.client.get_temperature()
            field, _ = instrument.client.get_field()
            instrument.autosens_thread()

            data_handler.append_data(time_value, harm, voltage, freq, channel1, channel2, temp, field)

            time_value += 0.3
            time_value = round(time_value, 1)
            time.sleep(0.3)
