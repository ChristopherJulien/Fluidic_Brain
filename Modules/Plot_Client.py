import os
import glob
import re
import pandas as pd
import matplotlib.pyplot as plt
import sys
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class Plot:
    def __init__(self,SLS1500_flag ):
        self.directory = os.path.dirname(os.path.abspath(__file__)) 
        self.SLS1500_flag = SLS1500_flag
        
    # Function to plot measured vs. set flow rate
    def q_vs_qs_and_relative_error(self):
        q_set_list = []
        q_measured_list = []
        q_std_list = []
        q_percent_error_list = []

        if self.SLS1500_flag:
            print("SLS1500 Plotting")
            file_pattern = 'sls_flow_rate_forward_*.csv'
            search_pattern = r'sls_flow_rate_forward_(-?\d+\.\d+)_ul_min'
            files = glob.glob(os.path.join(self.directory, file_pattern))
        else:
            print("FLG Plotting")
            file_pattern = 'flg_flow_rate_forward_*.csv'
            search_pattern = r'sls_flow_rate_forward_(-?\d+\.\d+)_ul_min'
            files = glob.glob(os.path.join(self.directory, file_pattern))

        for i, filename in enumerate(files):
            match = re.search(search_pattern, filename)
            if match:
                flow_rate = float(match.group(1))
                # if flow_rate == 11000.0: #TODO FIX TO ELIMINTATE LAST VARIABLE
                #     continue
            else:
                print("Error: Could not parse file name: {}".format(filename))
                sys.exit(1)

            df = pd.read_csv(filename)
            mL_min = (df['mL/min']).tolist()
            # print(mL_min)
            s = (df['ms']).tolist()
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

        plt.figure(figsize=(10, 5)) # Fix to make plots appear larger

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

    def flow_rate_over_time(self):

        print("Plotting Flow Rate Over Time")
        fig, ax = plt.subplots(1, 1, figsize=(16, 9))  # Set the figsize to the screen aspect ratio

        if self.SLS1500_flag:
            print("SLS1500 Plotting")
            file_pattern = 'sls_flow_rate_forward_*.csv'
            search_pattern = r'sls_flow_rate_forward_(-?\d+\.\d+)_ul_min'
            files = glob.glob(os.path.join(self.directory, file_pattern)) 
            
        else:
            print("FLG Plotting")
            file_pattern = 'flg_flow_rate_forward_*.csv'
            search_pattern = r'sls_flow_rate_forward_(-?\d+\.\d+)_ul_min'
            files = glob.glob(os.path.join(self.directory, file_pattern)) 
            
        colors = cm.viridis(np.linspace(0.1,0.9, len(files)))
        for i, filename in enumerate(files):
            match = re.search(search_pattern, filename)
            if match:
                flow_rate = float(match.group(1))
                # if flow_rate == 25000.0: #TODO FIX TO ELIMINTATE LAST VARIABLE
                #     continue
            else:
                print("Error: Could not parse file name: {}".format(filename))
                sys.exit(1)

            df = pd.read_csv(filename)
            mL_min = (df['mL/min']).tolist()
            s = (df['ms']).tolist()
            ax.plot(s, mL_min, label='q measured {} mL/min'.format(flow_rate / 1000), c= colors[i])

        ax.autoscale(axis='y')
        ax.legend(fontsize=8, frameon=False)
        ax.set_xlabel("Time [s]", fontsize=20)
        ax.set_ylabel("Flow [mL/min]", fontsize=20)
        ax.tick_params(axis='both', which='major', labelsize=16)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.rcParams['figure.autolayout'] = True
        plt.rcParams['font.size'] = 9
        plt.rcParams['legend.edgecolor'] = '1'
        plt.legend(fontsize=12, frameon=False)  # Decrease the fontsize value to make the legend smaller



        plt.show()

        # save_directory = os.path.join(directory, "Flow_Calibration_plots")
        # os.makedirs(save_directory, exist_ok=True)
        # save_path = os.path.join(save_directory, "100uL_min_to_10mL_min-{}.png".format(datetime.now().strftime("%d-%m-%Y_%H-%M-%S")))
        # plt.savefig(save_path)
        # print("Plot saved: {}".format(save_path))


# def volt_to_mbar(sensor, volt_signal, volt_source):
#     '''
#     Convert MXP sensor voltage to differential pressure.
#     No error or zero-offset included. Values outside of [0.5,4.5]V
#     are excluded (returned as np.nan).
#     '''
#     cdict = {'25kPa': 0.018,
#              '7kPa': 0.057,
#              '2kPa': 0.2}
#     pressure = (volt_signal/volt_source - 0.5)/cdict[sensor]*10
#     pressure [volt_signal < 0.5] = np.nan
#     pressure [volt_signal > 4.5] = np.nan
#     return pressure

        

if __name__=="__main__":
    plot_module = Plot(SLS1500_flag = True)
    plot_module.q_vs_qs_and_relative_error()
    plot_module.flow_rate_over_time()