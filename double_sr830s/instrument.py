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
        self.instrument = self.rm.open_resource(id)
        self.sens = 0
        self.pymeasure_instrument = SR830(id)
        self.sensitivity_list = [1, 2*10^-9]
        self.autosens_thread_running = False
        self.autosens_lock = threading.Lock()

    #  Gets the amplitude of the sine output in volts
    def get_voltage(self):
        return self.instrument.query_ascii_values('SLVL?')[0]
    
    #  Gets the frequency 
    def get_frequency(self):
        return self.instrument.query_ascii_values('FREQ?')[0]
    
    def get_channel1(self):
        return self.instrument.query_ascii_values("OUTP? 1")[0]
    
    def get_channel2(self):
        return self.instrument.query_ascii_values("OUTP? 2")[0]
    
    def get_harmonic(self):
        return self.instrument.query_ascii_values("HARM?")[0]
    
    def set_harmonic(self, harmonic_num):
        self.pymeasure_instrument.harmonic = harmonic_num

    #  Auto adjusts sensitivity
    def autosens(self):
        with self.autosens_lock:
            self.autosens_thread_running = True
        
        if self.pymeasure_instrument.is_out_of_range():
            self.pymeasure_instrument.quick_range()

        # change sensitivity so that it increases senstivity when it is "0"
        elif int(self.pymeasure_instrument.ask("SENS?")) > 0:
            while self.get_voltage() == 0 or self.get_channel1() == 0 or self.get_channel2() == 0:
                self.pymeasure_instrument.write('LIAE 2,1')
                self.pymeasure_instrument.write("SENS%d" % (int(self.pymeasure_instrument.ask("SENS?")) - 1))
                # time.sleep(5.0 * self.pymeasure_instrument.time_constant)
                self.pymeasure_instrument.write("*CLS")
                # Set the range as low as possible
                newsensitivity = 1.15 * abs(self.pymeasure_instrument.magnitude)
                if self.pymeasure_instrument.input_config in ('I (1 MOhm)', 'I (100 MOhm)'):
                    newsensitivity = newsensitivity * 1e6
                self.sens = newsensitivity
                
        with self.autosens_lock:
            self.autosens_thread_running = False
        
