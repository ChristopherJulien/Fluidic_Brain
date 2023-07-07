import os
import glob
import re
import pandas as pd
import matplotlib.pyplot as plt
import sys
from datetime import datetime
import numpy as np

# Function to plot measured vs. set flow rate
def plot_flow_rate(q_set_list, q_measured_list, q_std_list, q_percent_error_list):
    plt.figure(figsize=(10, 5))

    # Plot measured vs. set flow rate   
    plt.subplot(1, 2, 1)
    plt.errorbar(q_set_list, q_measured_list, yerr=q_std_list, fmt='o', capsize=5, label='Measured')
    plt.plot(q_set_list, q_set_list, label='Set', linestyle='--')
    plt.xlabel("Set Flow Rate (mL/min)")
    plt.ylabel("Measured Flow Rate (mL/min)")
    plt.title("Flow Rate Measurement")
    plt.legend()

    # Plot percent error
    plt.subplot(1, 2, 2)
    plt.plot(q_set_list, q_percent_error_list, 'o')
    plt.xlabel("Set Flow Rate (mL/min)")
    plt.ylabel("Percent Error (%)")
    plt.title("Flow Rate Measurement - Percent Error")

    plt.tight_layout()
    plt.show()

# Function to plot flow rate over time
def plot_flow_rate_over_time(files, search_pattern):
    fig, ax = plt.subplots(1, 1)
    ax.set_ylim(-60, 60)
    ax.set_xlabel("Time [ms]", fontsize=20)
    ax.set_xlabel("Time [s]", fontsize=20)
    ax.set_ylabel("Flow [mL/min]", fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.legend(fontsize=16, frameon=False)
    plt.tight_layout()

    for filename in files:
        match = re.search(search_pattern, filename)
        if match:
            flow_rate = float(match.group(1))
            if flow_rate == 11000.0:
                continue
        else:
            print("Error: Could not parse file name: {}".format(filename))
            sys.exit(1)

        df = pd.read_csv(filename)
        mL_min = df['mL/min'].tolist()
        s = (df['ms'] / 1000).tolist()

        ax.plot(s, mL_min, label='q measured {} mL/min'.format(flow_rate / 1000))

    ax.autoscale(axis='y')  # Adjust y-axis limits automatically
    ax.legend(fontsize=8, frameon=False)
    
    save_directory = os.path.join(directory, "Flow_Calibration_plots")
    os.makedirs(save_directory, exist_ok=True)

    save_path = os.path.join(save_directory, "100uL_min_to_10mL_min-{}.png".format(datetime.now().strftime("%d-%m-%Y_%H-%M-%S")))
    plt.savefig(save_path)
    print("Plot saved: {}".format(save_path))

    plt.show()
    plt.close()

# Main code
directory = os.getcwd()
file_pattern = 'flow_rate_forward_*.csv'
search_pattern = r'flow_rate_forward_(\d+\.\d+)_ul_min'
files = glob.glob(os.path.join(directory, file_pattern))

q_set_list = []
q_measured_list = []
q_std_list = []
q_percent_error_list = []

for filename in files:
    match = re.search(search_pattern, filename)
    if match:
        flow_rate = float(match.group(1))
        if flow_rate == 11000.0:
            continue
    else:
        print("Error: Could not parse file name: {}".format(filename))
        sys.exit(1)

    df = pd.read_csv(filename)
    mL_min = df['mL/min'].tolist()
    s = (df['ms'] / 1000).tolist()
    s = np.array(s)
    low_filter = s > 1
    q = np.array(mL_min)
    q = q[low_filter]

    q_average = np.average(q)
    q_error = abs(q_average - flow_rate / 1000) / (flow_rate / 1000) * 100
    q_percent_error_list.append(q_error)

    q_std = np.std(q)
    q_measured_list.append(q_average)
    q_std_list.append(q_std)
    q_set_list.append(flow_rate / 1000)

# Plot measured vs. set flow rate
plot_flow_rate(q_set_list, q_measured_list, q_std_list, q_percent_error_list)

# Plot flow rate over time
plot_flow_rate_over_time(files, search_pattern)
