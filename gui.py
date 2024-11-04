# -*- coding: utf-8 -*-
"""
GUI SETUP
Created on Mon Nov  4 16:03:00 2024
@author: laqm
Creator: Sana Naik
"""
import tkinter as tk
from tkinter import ttk
from main import *

def create_gui():
    
    root = tk.Tk()
    root.title("LAQM Lock-In Amplifier Data Visualizer")
    root.geometry('1600x900')

    # Name frame
    name_frame = tk.Frame(root, padx=20, pady=20)  
    name_frame.pack(pady = 50)

    name_text = tk.Label(name_frame, text="Enter your name (this will go in the CSV file name)", font = 16)
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

    start_text = tk.Label(start_frame, text="Begin Program?", font = 20, justify = "center")
    start_text.pack()

    start_btn = tk.Button(start_frame, text="Start", command=start_run, font = 10)
    start_btn.pack(side="left", padx=5)

    stop_btn = tk.Button(start_frame, text="Stop", command=stop, font = 10)
    stop_btn.pack(side="right", padx=5)

    # ----------------------- Output Frame ----------------------- #
    output_frame = tk.Frame(root, padx=10, pady=20)
    output_frame.pack()

    # Left frame
    left_frame = tk.Frame(output_frame, padx=10, pady=20)
    left_frame.pack(side="left", padx = 0)

    output_title = tk.Label(left_frame, text="Output Data", font = 16)
    output_title.pack()

    # Data frame
    data_frame = tk.Frame(left_frame, padx = 10, pady = 0)
    data_frame.pack()

    # Table of data
    tree = ttk.Treeview(data_frame, columns = ("Time", "Voltage", "Frequency", "Channel1(X)", "Channel2(Y)"), show="headings")
    tree.heading("Time", text = "Time (Seconds)")
    tree.heading("Voltage", text = "Voltage")
    tree.heading("Frequency", text = "Frequency")
    tree.heading("Channel1(X)", text = "Channel1(X)")
    tree.heading("Channel2(Y)", text = "Channel2(Y)")

    tree.column("Time", width=100)
    tree.column("Voltage", width=100)
    tree.column("Frequency", width=100)
    tree.column("Channel1(X)", width=100)
    tree.column("Channel2(Y)", width=100)


    # Scrollbar
    vsb = ttk.Scrollbar(data_frame, command = tree.yview)
    vsb.pack(side = 'right', fill = 'y')
    tree.configure(yscrollcommand=vsb.set)

    tree.pack()

    # Right frame
    right_frame = tk.Frame(output_frame, padx=10, pady=20)
    right_frame.pack(side="right")

    # ----------------------- Plotting stuff ----------------------- #
    header_frame = tk.Frame(right_frame)
    header_frame.pack()

    # Axes Options
    x_option = tk.StringVar()
    x_option.set("Time")

    y_option = tk.StringVar()
    y_option.set("Channel1(X)")

    x_drop = tk.OptionMenu(header_frame, x_option, *fieldnames)
    y_drop = tk.OptionMenu(header_frame, y_option, *fieldnames)

    x_drop.pack(side = 'right')
    y_drop.pack(side = 'left')

    plot_title = tk.Label(header_frame, text="vs.")
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
    ax.autoscale(autoscale)
    ax.plot(data['Time'], data['Channel1(X)'])
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Channel1(X)')
    ax.set_title('Channel1(X) vs. Time')

    # Scatter plot and line graph options
    plot_btn = tk.Button(toolbar_frame, text = "Scatter Plot", command = change_plot)
    plot_btn.pack()

    # Autoscaling
    autoscale_btn = tk.Button(toolbar_frame, text = "Toggle Autoscale", command = toggle_autoscale)
    autoscale_btn.pack()

    # Cursor snap to data point
    fig.canvas.mpl_connect('motion_notify_event', on_mouse_move)

    canvas._tkcanvas.pack(fill=tk.BOTH, expand=True)
    
    return root

