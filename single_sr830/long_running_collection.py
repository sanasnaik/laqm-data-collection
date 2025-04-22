"""
No GUI

Created on Monday February 10 2025
Creator: Sana Naik
Under supervision of: Professor Jak Chakalian, Tsung-Chi Wu
"""
import time
import MultiPyVu as mpv
import datetime
import threading

#  Separate clases to keep code modular!
from instrument import Instrument
from datahandler import DataHandler

current_time = datetime.datetime.now().strftime("%m-%d-%Y %I.%M%p")

# ------------------------ SET UP HERE ------------------------ #
# Set file path name:
name = 'tcwu-EIODevice-Rload1MOhm-RT2' # default: nothing
file_path = f"C:\\Users\\ppms\\Documents\\CSV Data Outputs\\{name}{current_time}.csv"

# Set harmonic number:
harm_num = 1  # default: 1
# ------------------------ SET UP END ------------------------ #

#  Initialize
#  Start the server.
with mpv.Server():
    #  Start the client
    with mpv.Client(socket_timeout = 5000) as client:

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

            try:
                temp, _ = client.get_temperature()
            except Exception as e:
                print("Couldn't get temperature data")
            
            try:
                field, _ = client.get_field()
            except Exception as e:
                print("Couldn't get field data")

            with instrument.autosens_lock:
                if not instrument.autosens_thread_running:
                    # Start a new autosens thread if the previous one has finished
                    autosens_thread = threading.Thread(target = instrument.autosens, daemon = True)
                    autosens_thread.start()

            data_handler.append_data(time_value, harm, voltage, freq, channel1, channel2, temp, field)

            time_value += 0.3
            time_value = round(time_value, 1)
            time.sleep(0.3)
