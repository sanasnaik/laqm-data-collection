# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 14:42:07 2024
@author: laqm
"""

import pyvisa

class Instrument:
    def __init__(self, resource_address='GPIB0::8::INSTR'):
        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(resource_address)
    
    def get_voltage(self):
        return self.instrument.query_ascii_values('SLVL?')[0]
    
    def get_frequency(self):
        return self.instrument.query_ascii_values('FREQ?')[0]
    
    def get_channel1(self):
        return self.instrument.query_ascii_values("OUTP? 1")[0]
    
    def get_channel2(self):
        return self.instrument.query_ascii_values("OUTP? 2")[0]
