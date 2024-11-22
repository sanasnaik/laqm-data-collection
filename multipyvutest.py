# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 13:04:44 2024
Sana Naik
@author: laqm
"""

#!/usr/bin/env python3
'''
Run this first to make sure that the PPMS is properly connected
'''

import time
import MultiPyVu as mpv

# Start the server.
with mpv.Server():
    # Start the client
    with mpv.Client() as client:

        # A basic loop that demonstrates communication between
        # client/server
        for t in range(5):
            # Polls MultiVu for the temperature, field, and their
            # respective states
            t, t_status = client.get_temperature()
            f, f_status = client.get_field()

            # Relay the information from MultiVu
            message = f'The temperature is {t}, status is {t_status}; '
            message += f'the field is {f}, status is {f_status}. '
            print(message)

            # collect data at roughly 2s intervals
            time.sleep(2)

# Idea 1: button starts the mpv.Server and mpv.Client at the same time as it
# starts the lock-in amplifier collecting data?

# Idea 2: the function to collect data will contain both the lock in data
# collection command and the ppms data collection command directly after
# each other, so they execute at almost the same time.