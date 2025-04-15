"""
Note: This file is created to test the PPMS connection. Currently the program stops randomly in the middle of running.
We have an email thread with Quantum Designs discussing why this could be happening.
This file can be used to create PPMS "QdMultiVu" logs to hopefully help diagnose this issue.

Creator: Sana Naik
Under supervision of: Professor Jak Chakalian, Tsung-Chi Wu
"""
import time
import MultiPyVu as mpv

#  Initialize
#  Start the server.
with mpv.Server():
    
    #  Start the client
    with mpv.Client(socket_timeout = 5000) as client:
        print('Time, Harmonic, Voltage, Frequency, Channel1(X), Channel2(Y), Temperature, Field')
        time_value = 0

        # Immediately starts collecting data.
        while True:
            temp, _ = client.get_temperature()
            field, _ = client.get_field()

            print(time_value, 0, 0, 0, 0, 0, temp, field)

            time_value += 0.3
            time_value = round(time_value, 1)
            time.sleep(0.3)
