# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 14:42:07 2024
@author: laqm
"""

import pyvisa
import MultiPyVu as mpv
from pymeasure.instruments.srs import SR830

class Instrument:
    def __init__(self, client):
        self.rm = pyvisa.ResourceManager()
        self.client = client
        self.instrument = self.rm.open_resource('GPIB0::8::INSTR')
        self.pymeasure_instrument = SR830('GPIB0::8::INSTR')

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

    #  Auto adjusts sensitivity (fix this)
    def autosens(self):
        if self.pymeasure_instrument.is_out_of_range():
            print("oor")
            self.pymeasure_instrument.quick_range()