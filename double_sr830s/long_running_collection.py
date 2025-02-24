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
harm_num_1 = 1  # for sr830 8, default: 1
harm_num_2 = 1  # for sr830 9, default: 1
# ------------------------ SET UP END ------------------------ #

#  Initialize
#  Start the server.
with mpv.Server():
    #  Start the client
    with mpv.Client(socket_timeout = None) as client:

        # Init
        data_handler = DataHandler(file_path = file_path)
        instrument_1 = Instrument(client, data_handler)
        instrument_2 = Instrument(client, data_handler, 'GPIB0::9::INSTR')
        data_handler.write_header()
        time_value = 0
        try:
            instrument_1.set_harmonic(harm_num_1)
            instrument_2.set_harmonic(harm_num_2)
        except:
            print("Error: enter 1, 2, or 3 for harmonic number.")

        # Immediately starts collecting data.
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

            temp, _ = instrument_1.client.get_temperature()
            field, _ = instrument_1.client.get_field()

            data_handler.append_data(time_value, harm1, voltage1, freq1, channel11, channel21, harm2, voltage2, freq2, channel12, channel22, temp, field)

            if not instrument_1.autosens_thread_running:
                threading.Thread(target=instrument_1.autosens, daemon=True).start()
                time.sleep(0.5)  # Small delay prevents conflicts

            if not instrument_2.autosens_thread_running:
                threading.Thread(target=instrument_2.autosens, daemon=True).start()
                    
            time_value += 0.3
            time_value = round(time_value, 1)
            time.sleep(0.3)
