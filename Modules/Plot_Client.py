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
from natsort import natsorted

SLS=1
FLG=2
WATER=3
GLYCEROL=4

def get_path_case(case, subcase):
    print("Getting path")
    switch = {
        SLS: {
            WATER: ('Data_Calibration\\water\\sls',r'Data_Calibration\\water\\sls\\.*\\sls_flow_rate_forward_(-?\d+\.\d+)_ul_min', "Medium: Water - SLS 1500"),
            GLYCEROL:('Data_Calibration\\glycerol\\sls',r'Data_Calibration\\glycerol\\sls\\.*\\sls_flow_rate_forward_(-?\d+\.\d+)_ul_min', "Medium: Glycerol - SLS 1500")
        },
        FLG: {
            WATER: ('Data_Calibration\\water\\flg', r'Data_Calibration\\water\\flg\\.*\\flg_flow_rate_forward_(-?\d+\.\d+)_ul_min', "Medium: Water - FLG M+"),
            GLYCEROL: ('Data_Calibration\\glycerol\\flg', r'Data_Calibration\\glycerol\\flg\\.*\\flg_flow_rate_forward_(-?\d+\.\d+)_ul_min', "Medium: Glycerol - FLG M+")
        }
    }
    return switch.get(case, {}).get(subcase, 'Invalid case or subcase')

class Plot:
    def __init__(self,SLS1500_flag=None ):
        self.directory = os.path.dirname(os.path.abspath(__file__)) 
        self.SLS1500_flag = SLS1500_flag
    
    def set_search_directory(self,SLS1500_flag,water_flag):
        pass

    def all_q_vs_qs_case(self, device:int, sub_case:int):
        q_set_list = []
        q_measured_list = []
        q_std_list = []
        q_percent_error_list = []
        folder_path, match_pattern ,plot_title = get_path_case(device, sub_case)
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path)

                    mL_min = df['mL/min'].tolist() if device == SLS else [(value / 1000) for value in df['uL/min'].tolist()]
                    s = [(value/1000) for value in df['ms'].tolist()] if device == SLS else df['s'].tolist()

                    s = np.array(s)
                    low_filter = s > 2
                    q = np.array(mL_min)
                    q = q[low_filter]
                    
                    match = re.search(match_pattern, file_path)
                    if match:
                        flow_rate = float(match.group(1))
                        # print(flow_rate)
                    else:
                        print("Error: Could not parse file name: {}".format(file_path))
                        sys.exit(1)

                    q_average = np.average(q)
                    q_error = abs(q_average - flow_rate / 1000) / (flow_rate / 1000) * 100 if flow_rate != 0 else 0
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

        # Remove right and top spines
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)

        # Plot percent error
        plt.subplot(1, 2, 2)
        plt.plot(q_set_list, q_percent_error_list, 'o')
        plt.xlabel("Set Flow Rate (mL/min)")
        plt.ylabel("Percent Error (%)")
        plt.title("Flow Rate Measurement - Percent Error")

        # Remove right and top spines
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)

        # Add a title for the entire figure
        plt.suptitle(plot_title, fontsize=16)

        plt.tight_layout()
        print("Plotting All Q vs Qs")
        plt.show()
            
   
    def q_vs_qs_and_relative_error(self):
        assert self.SLS1500_flag is not None, "SLS1500_flag must be set before calling this function"
        q_set_list = []
        q_measured_list = []
        q_std_list = []
        q_percent_error_list = []

        if self.SLS1500_flag:
            print("SLS1500 Plotting")
            file_pattern = 'sls_flow_rate_forward_*.csv'
            search_pattern = r'sls_flow_rate_forward_(-?\d+\.\d+)_ul_min'
            files = glob.glob(os.path.join(self.directory, file_pattern))
            files = natsorted(files)
        else:
            print("FLG Plotting")
            file_pattern = 'flg_flow_rate_forward_*.csv'
            search_pattern = r'flg_flow_rate_forward_(-?\d+\.\d+)_ul_min'
            files = glob.glob(os.path.join(self.directory, file_pattern))
            files = natsorted(files)

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
            mL_min = df['mL/min'].tolist() if self.SLS1500_flag else [(value / 1000) for value in df['uL/min'].tolist()]
            s = [(value / 1000) for value in df['ms'].tolist()] if self.SLS1500_flag else df['s'].tolist()

            s = np.array(s)
            low_filter = s > 2
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
        assert self.SLS1500_flag is not None, "SLS1500_flag must be set before calling this function"

        print("Plotting Flow Rate Over Time")
        fig, ax = plt.subplots(1, 1, figsize=(16, 9))  # Set the figsize to the screen aspect ratio

        if self.SLS1500_flag:
            print("SLS1500 Plotting")
            file_pattern = 'sls_flow_rate_forward_*.csv'
            search_pattern = r'sls_flow_rate_forward_(-?\d+\.\d+)_ul_min'
            files = glob.glob(os.path.join(self.directory, file_pattern)) 
            files = natsorted(files)
        else:
            print("FLG Plotting")
            file_pattern = 'flg_flow_rate_forward_*.csv'
            search_pattern = r'flg_flow_rate_forward_(-?\d+\.\d+)_ul_min'
            files = glob.glob(os.path.join(self.directory, file_pattern)) 
            files = natsorted(files)
              
        
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
            mL_min = df['mL/min'].tolist() if self.SLS1500_flag else [(value / 1000) for value in df['uL/min'].tolist()]
            s = [(value / 1000) for value in df['ms'].tolist()] if self.SLS1500_flag else df['s'].tolist()
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
    # plot = Plot(SLS1500_flag = False)
    # plot.q_vs_qs_and_relative_error()
    # plot.flow_rate_over_time()

    plot = Plot()
    plot.all_q_vs_qs_case(FLG,GLYCEROL)

