# -*- coding: utf-8 -*-
"""
GUI SETUP
Created on Mon Nov  4 16:03:00 2024
@author: laqm
Creator: Sana Naik
"""
import tkinter as tk
from tkinter import ttk
from instrument import Instrument
from datahandler import DataHandler
from plotter import Plotter
import threading
import time
import sys
import matplotlib.pyplot as plt
import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pyvisa
import MultiPyVu as mpv
from pymeasure.instruments.srs import SR830

class GUI:
    def __init__(self, root, instrument, data_handler, plotter, client):
        self.client = client
        self.root = root
        self.data_handler = data_handler
        self.instrument = instrument
        #self.data_handler.write_header()
        self.plotter = plotter
        self.data_collect_id = ''
        
        self.collecting = False
        self.time_value = 0
        self.x_option = tk.StringVar(value = "Time")
        self.y_option = tk.StringVar(value = "Channel1(X)")

        self.setup_gui()
    
    def setup_gui(self):
        self.root.title("LAQM Lock-In Amplifier Data Visualizer")
        self.root.geometry('1600x900')

        # Name frame
        self.name_frame = tk.Frame(self.root, padx=20, pady=20)
        self.name_frame.pack(pady=50)

        self.name_text = tk.Label(self.name_frame, text="Enter your name (this will go in the CSV file name)\n NOTE: Give file a unique name", font=16)
        self.name_text.pack()
        
        self.name_entry = tk.Entry(self.name_frame, width=10)
        self.name_entry.pack()
        
        self.name_btn = tk.Button(self.name_frame, text="Enter", command=self.name_btn_clicked)
        self.name_btn.pack(pady=5)

        self.filepath_text = tk.Label(self.name_frame, text=self.data_handler.csv_file_path)
        self.filepath_text.pack()

        self.close_text = tk.Label(self.name_frame, text="Do not click X. Click 'Close' to close window.", font = 10)
        self.close_text.pack()

        # Close button -- test
        self.close_btn = tk.Button(self.name_frame, text="Close", command=self.close, font=10)
        self.close_btn.pack()
        
        # Start frame
        self.start_frame = tk.Frame(self.root, padx=20, pady=20)
        self.start_frame.pack()
        
        self.start_text = tk.Label(self.start_frame, text="Begin Program?", font=20, justify="center")
        self.start_text.pack()
        
        self.start_btn = tk.Button(self.start_frame, text="Start", command=self.start_run, font=10)
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = tk.Button(self.start_frame, text="Stop", command=self.stop, font=10)
        self.stop_btn.pack(side="right", padx=5)

        self.harmonic_text = tk.Label(self.start_frame, text="Set Harmonic Number. Current: 1", font=20, justify="center")
        self.harmonic_text.pack()

        self.harmonic_entry = tk.Entry(self.start_frame, width=10)
        self.harmonic_entry.pack()

        self.harmonic_btn = tk.Button(self.start_frame, text="Enter", command=self.change_harmonic)
        self.harmonic_btn.pack(pady=5)

        # ----------------------- Output Frame ----------------------- #
        self.output_frame = tk.Frame(self.root, padx=10, pady=20)
        self.output_frame.pack()

        # Data frame
        self.left_frame = tk.Frame(self.output_frame, padx=10, pady=20)
        self.left_frame.pack(side="left", padx=0)
        
        self.output_title = tk.Label(self.left_frame, text="Output Data", font=16)
        self.output_title.pack()
        
        # Table of data
        self.tree = ttk.Treeview(self.left_frame, columns=("Time", "Harmonic", "Voltage", "Frequency", "Channel1(X)", "Channel2(Y)", "Temp", "Field"), show="headings")
        self.tree.heading("Time", text="Time (Seconds)")
        self.tree.heading("Harmonic", text="Harmonic Number")
        self.tree.heading("Voltage", text="Voltage")
        self.tree.heading("Frequency", text="Frequency")
        self.tree.heading("Channel1(X)", text="Channel1(X)")
        self.tree.heading("Channel2(Y)", text="Channel2(Y)")
        self.tree.heading("Temp", text="Temperature (K)")
        self.tree.heading("Field", text="Magnetic Field")
        
        self.tree.column("Time", width=100)
        self.tree.column("Harmonic", width=100)
        self.tree.column("Channel2(Y)", width=100)
        self.tree.column("Voltage", width=100)
        self.tree.column("Frequency", width=100)
        self.tree.column("Channel1(X)", width=100)
        self.tree.column("Channel2(Y)", width=100)
        self.tree.column("Temp", width=100)
        self.tree.column("Field", width=100)
        
        # Scrollbar
        self.vsb = ttk.Scrollbar(self.left_frame, command=self.tree.yview)
        self.vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.vsb.set)
        
        self.tree.pack()

        # ----------------------- Plotting stuff ----------------------- #
        # self.right_frame = tk.Frame(self.output_frame, padx=10, pady=20)
        # self.right_frame.pack(side="right")

        # # Dropdowns for selecting x and y axis fields
        # self.header_frame = tk.Frame(self.right_frame)
        # self.header_frame.pack()
        
        # self.x_drop = tk.OptionMenu(self.header_frame, self.x_option, *self.data_handler.fieldnames)
        # self.y_drop = tk.OptionMenu(self.header_frame, self.y_option, *self.data_handler.fieldnames)
        
        # self.x_drop.pack(side='right')
        # self.y_drop.pack(side='left')

        # # Plotting area
        # self.fig, self.ax = plt.subplots()
        # self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        # self.canvas.get_tk_widget().pack()
        
        # # Navigation toolbar
        # self.toolbar_frame = tk.Frame(self.right_frame)
        # self.toolbar_frame.pack(fill=tk.X)
        # self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        # self.toolbar.update()
        
        # self.plotter = Plotter(self.canvas, self.ax, self.data_handler)

        # # Set up plot axes + title
        # self.ax.plot(self.data_handler.data['Time'], self.data_handler.data['Channel1(X)'])
        # self.ax.set_xlabel('Time (seconds)')
        # self.ax.set_ylabel('Channel1(X)')
        # self.ax.set_title('Channel1(X) vs. Time')
        
        # # Scatter plot and line graph options
        # self.plot_btn = tk.Button(self.toolbar_frame, text = "Scatter Plot", command = self.change_plot)
        # self.plot_btn.pack()
        
        # # Autoscaling
        # self.autoscale_btn = tk.Button(self.toolbar_frame, text = "Toggle Autoscale", command = self.plotter.toggle_autoscale)
        # self.autoscale_btn.pack()

        # Cursor snap to data point - disabled for now
        # self.fig.canvas.mpl_connect('motion_notify_event', self.plotter.on_mouse_move)
        
        # self.canvas.draw()    
    
    # test
    def close(self):
        if self.data_collect_id:
            self.root.after_cancel(self.data_collect_id)
        self.root.destroy()
        self.client.close_server()
        sys.exit()
    
    def change_harmonic(self):
        try:
            self.instrument.set_harmonic(int(self.harmonic_entry.get()))
            self.harmonic_text.configure(text=f"Set Harmonic Number. Current: {self.harmonic_entry.get()}")
        except:
            self.harmonic_text.configure(text="Error: enter 1, 2, or 3")

    #  To change the type of plot from line plot to scatter plot or vice versa.
    def change_plot(self):
        
        self.xlim = self.plotter.ax.get_xlim()
        self.ylim = self.plotter.ax.get_ylim()
        self.plotter.ax.clear()
        
        if not self.plotter.autoscale:
            self.plotter.ax.set_xlim(self.xlim)
            self.plotter.ax.set_ylim(self.ylim)
            
        if self.plotter.plot_type == "line_graph":
            self.plotter.plot_type = "scatter_plot"
            self.plot_btn.configure(text = "Line Graph")
            
        elif self.plotter.plot_type == "scatter_plot":
            self.plotter.plot_type = "line_graph"
            self.plot_btn.configure(text = "Scatter Plot")
    
    
    # Executes when we click "Enter" under the "Enter your name" text box.
    def name_btn_clicked(self):
        current_time = datetime.datetime.now().strftime("%m-%d-%Y %I.%M%p")
        self.data_handler.csv_file_path = f"C:\\Users\\ppms\\Documents\\CSV Data Outputs\\{self.name_entry.get()}{current_time}.csv"
        self.filepath_text.configure(text=self.data_handler.csv_file_path)

    def start_run(self):
        threading.Thread(target=self.run, daemon=True).start()
        self.start_btn.config(command = self.run)
        self.data_collect()  # begin the process

    def stop(self):
        self.collecting = False

    def run(self):
        self.collecting = True

    def update_gui(self, harm, voltage, freq, channel1, channel2, temp, field):
        self.data_handler.append_data(self.time_value, harm, voltage, freq, channel1, channel2, temp, field)
        self.tree.insert("", "0", values = (self.time_value, harm, voltage, freq, channel1, channel2, temp, field))
        # self.plotter.update_plot(self.data_handler.data, self.x_option.get(), self.y_option.get())

    def data_collect(self):
        if self.collecting:
            try:  # hopefully this stops the socket connection error
                harm = self.instrument.get_harmonic()
                voltage = self.instrument.get_voltage()
                freq = self.instrument.get_frequency()
                channel1 = self.instrument.get_channel1()
                channel2 = self.instrument.get_channel2()
                temp, _ = self.instrument.client.get_temperature()
                field, _ = self.instrument.client.get_field()
                self.root.after(0, self.update_gui(harm, voltage, freq, channel1, channel2, temp, field))
                self.instrument.autosens()

            except Exception as e:
                print(e)
            
        self.time_value += 0.3
        self.time_value = round(self.time_value, 1)
        self.data_collect_id = self.root.after(300, self.data_collect)