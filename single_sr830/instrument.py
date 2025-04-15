# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 14:42:07 2024
@author: laqm
"""

import pyvisa
import time
import MultiPyVu as mpv
from pymeasure.instruments.srs import SR830
import threading

class Instrument:
    def __init__(self, client, data_handler, id = 'GPIB0::8::INSTR'):
        self.rm = pyvisa.ResourceManager()
        self.client = client
        self.data_handler = data_handler
        self.instrument = self.rm.open_resource(id, timeout=5000)
        self.sens = 0
        self.pymeasure_instrument = SR830(id)
        self.autosens_thread = threading.Thread(target = self.autosens, daemon = True)
        self.running = True
        self.autosens_thread.start()

    #  Gets the amplitude of the sine output in volts
    def get_voltage(self):
        try:
            return self.instrument.query_ascii_values('SLVL?')[0]
        except Exception as e:
            return f"Error getting voltage: {e}"

    # Gets the frequency
    def get_frequency(self):
        try:
            return self.instrument.query_ascii_values('FREQ?')[0]
        except Exception as e:
            return f"Error getting frequency: {e}"

    def set_frequency(self, freq):
        try:
            self.pymeasure_instrument.frequency = freq
        except Exception as e:
            print(f"Error setting frequency: {e}")      

    def get_channel1(self):
        try:
            return self.instrument.query_ascii_values("OUTP? 1")[0]
        except Exception as e:
            return f"Error getting channel 1: {e}"

    def get_channel2(self):
        try:
            return self.instrument.query_ascii_values("OUTP? 2")[0]
        except Exception as e:
            return f"Error getting channel 2: {e}"

    def get_harmonic(self):
        try:
            return self.instrument.query_ascii_values("HARM?")[0]
        except Exception as e:
            return f"Error getting harmonic: {e}"

    def set_harmonic(self, harmonic_num):
        try:
            self.pymeasure_instrument.harmonic = harmonic_num
        except Exception as e:
            return f"Error setting harmonic: {e}"

    #  Auto adjusts sensitivity
    def autosens(self):
        """ Continuously runs autosens every 1 second in the background """
        while self.running:
            try:
                if int(self.pymeasure_instrument.ask("LIAS?2").strip()) == 1:
                        self.pymeasure_instrument.quick_range()

                elif int(self.pymeasure_instrument.ask("SENS?").strip()) > 0:
                    retries = 0
                    while self.get_voltage() == 0 or self.get_channel1() == 0 or self.get_channel2() == 0 and retries < 10:
                        self.pymeasure_instrument.write('LIAE 2,1')
                        self.pymeasure_instrument.write("SENS%d" % (int(self.pymeasure_instrument.ask("SENS?")) - 1))
                        # time.sleep(5.0 * self.pymeasure_instrument.time_constant)
                        self.pymeasure_instrument.write("*CLS")
                        # Set the range as low as possible
                        newsensitivity = 1.15 * abs(self.pymeasure_instrument.magnitude)
                        if self.pymeasure_instrument.input_config in ('I (1 MOhm)', 'I (100 MOhm)'):
                            newsensitivity = newsensitivity * 1e6
                        self.sens = newsensitivity
                        retries += 1
            except Exception as e:
                print(f"Error: {e}")

            time.sleep(1)

    def stop(self):
        self.running = False
    