"""
Created on Thu Jan 26 15:55:22 2023
THIS HAS NO LAKESHORE TEMPERATURE CONTROLLER OR KEITHLEY FUNCTIONALITY
@author: laqm
Current contributor: Sana Naik
Past contributor: Keanu Shah
Under supervision of: Professor Jak Chakalian, Tsung-Chi Wu
"""

import pyvisa
import csv
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import datetime
import threading
import tkinter as tk

# Define constants
current_time = datetime.datetime.now().strftime("%m-%d-%Y %I.%M%p")
csv_file_path = f"C:\\Users\\laqm\\Documents\\CSV Data Outputs\\{current_time}.csv"
fieldnames = ['Time', 'Voltage', 'Frequency', 'Channel1(X)', 'Channel2(Y)']
my_instrument = pyvisa.ResourceManager().open_resource('GPIB0::8::INSTR')
plot_type = "line_graph"

# Collects data into CSV and plots
running = False
data = {  # dictionary to store datapoints
    'Time': [],
    'Voltage': [],
    'Frequency': [],
    'Channel1(X)': [],
    'Channel2(Y)': []
}

def run():
    global running
    running = True
    
    timevalue = 0

    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    while running:
        freq = my_instrument.query_ascii_values('FREQ?')[0]
        voltage = my_instrument.query_ascii_values('SLVL?')[0]
        channel1 = my_instrument.query_ascii_values("OUTP? 1")[0]
        channel2 = my_instrument.query_ascii_values("OUTP? 2")[0]

        info = {
            "Time": timevalue,
            "Voltage": voltage,
            "Frequency": freq,
            "Channel1(X)": float(channel1),
            "Channel2(Y)": float(channel2)
        }

        # Append data for plotting
        data['Time'].append(timevalue)
        data['Voltage'].append(voltage)
        data['Frequency'].append(freq)
        data['Channel1(X)'].append(float(channel1))
        data['Channel2(Y)'].append(float(channel2))

        with open(csv_file_path, mode='a', newline="") as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writerow(info)

        # GUI update
        if plot_type == "line_graph":
            ax.plot(data['Time'], data['Channel1(X)'], color = "blue")
        elif plot_type == "scatter_plot":
            ax.scatter(data['Time'], data['Channel1(X)'], color = "blue")
        canvas.draw()
        
        root.after(0, update_output_text, timevalue, voltage, freq, channel1, channel2)
            
        time.sleep(2)
        timevalue += 2

def update_output_text(timevalue, voltage, freq, channel1, channel2):
    text = output_text.cget("text") + f"\n{timevalue}, {voltage}, {freq}, {float(channel1)}, {float(channel2)}"
    output_text.configure(text=text)
    
def change_plot():
    global plot_type
    if plot_type == "line_graph":
        plot_type = "scatter_plot"
        plot_btn.configure(text = "Line Graph")
    elif plot_type == "scatter_plot":
        plot_type = "line_graph"
        plot_btn.configure(text = "Scatter Plot")

def start_run():
    threading.Thread(target=run, daemon=True).start()

def name_btn_clicked():
    global csv_file_path
    current_time = datetime.datetime.now().strftime("%m-%d-%Y %I.%M%p")
    csv_file_path = f"C:\\Users\\laqm\\Documents\\CSV Data Outputs\\{name_entry.get()}{current_time}.csv"
    filepath_text.configure(text=csv_file_path)

def stop():
    global running
    running = False
    
# Snap mouse to nearest data point in plot
def on_mouse_move(event):
    if event.inaxes is not None:
        mouse_x = event.xdata
        mouse_y = event.ydata
        
        # Calculate the distance from each data point
        distances = np.sqrt((np.array(data['Channel1(X)']) - mouse_y) ** 2 + (np.array(data['Time']) - mouse_x) ** 2)
        nearest_index = np.argmin(distances)  # index of the nearest point
        
        # Clear graph and redraw
        ax.clear()
        if plot_type == "line_graph":
            ax.plot(data['Time'], data['Channel1(X)'])
        elif plot_type == "scatter_plot":
            ax.scatter(data['Time'], data['Channel1(X)'])
        
        # Highlight the nearest point
        ax.plot(data['Time'][nearest_index], data['Channel1(X)'][nearest_index], 'ro')
        ax.annotate(f'({data["Time"][nearest_index]}, {data["Channel1(X)"][nearest_index]})',
                    (data['Time'][nearest_index], data['Channel1(X)'][nearest_index]),
                    textcoords="offset points", 
                    xytext=(0,10), 
                    ha='center', fontsize=8, color='red')
        
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Channel1(X)')
        ax.set_title('Channel1(X) vs. Time')
        
        canvas.draw()

# Driver code for GUI
root = tk.Tk()
root.title("LAQM Lock-In Amplifier Data Visualizer")
root.geometry('1600x900')

# Name frame
name_frame = tk.Frame(root, padx=20, pady=20)  
name_frame.pack()

name_text = tk.Label(name_frame, text="Enter your name (this will go in the CSV file name)")
name_text.pack()

name_entry = tk.Entry(name_frame, width=10)
name_entry.pack()

name_btn = tk.Button(name_frame, text="Enter", command=name_btn_clicked)
name_btn.pack(pady=5)

filepath_text = tk.Label(name_frame, text=csv_file_path)
filepath_text.pack()

# Start frame
start_frame = tk.Frame(root, padx=20, pady=20)
start_frame.pack()

start_text = tk.Label(start_frame, text="Begin Program?")
start_text.pack()

start_btn = tk.Button(start_frame, text="Start", command=start_run)
start_btn.pack(side="left", padx=5)

stop_btn = tk.Button(start_frame, text="Stop", command=stop)
stop_btn.pack(side="left", padx=5)

# Output frame
output_frame = tk.Frame(root, padx=10, pady=20)
output_frame.pack()

# Left frame
left_frame = tk.Frame(output_frame, padx=10, pady=20)
left_frame.pack(side="left")

output_title = tk.Label(left_frame, text="Output Data:")
output_title.config(font=16)
output_title.pack()

output_text = tk.Label(left_frame, text="")
output_text.pack()

# Right frame
right_frame = tk.Frame(output_frame, padx=10, pady=20)
right_frame.pack(side="right")

# Plotting stuff
plot_title = tk.Label(right_frame, text="Live Data Plot")
plot_title.config(font=(16))
plot_title.pack()

# Matplotlib figure and axis
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack()

# Navigation toolbar
toolbar_frame = tk.Frame(right_frame)
toolbar_frame.pack(fill=tk.X)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()

# Set up plot axes + title
ax.plot(data['Time'], data['Channel1(X)'])
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Channel1(X)')
ax.set_title('Channel1(X) vs. Time')

# Scatter plot and line graph options
plot_btn = tk.Button(toolbar_frame, text = "Scatter Plot", command = change_plot)
plot_btn.pack()

# Cursor snap to data point
fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

canvas._tkcanvas.pack(fill=tk.BOTH, expand=True)

root.mainloop()
