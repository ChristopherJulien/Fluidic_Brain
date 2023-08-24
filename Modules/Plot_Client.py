import os
import glob
import re
import pandas as pd
import matplotlib.pyplot as plt
import sys
from datetime import datetime
import numpy as np
from numpy.polynomial.polynomial import Polynomial
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from natsort import natsorted
import pickle

SLS = 1
FLG = 2
WATER = 3
GLYCEROL = 4
channel_dict = {
    "Time [s]": ('Time [s]', 'none', 's', 'none'),
    "Channel 0": ('Channel 0', 'black', '25kPa', 0.018),
    "Channel 1": ('Channel 1', 'brown', '2kPa', 0.2),
    "Channel 2": ('Channel 2', 'red',  'Source', 5.0),
    "Channel 3": ('Channel 3', 'yellow', '7kPa', 0.057)
}


def get_path_case(case, subcase):
    print("Getting path")
    switch = {
        SLS: {
            WATER: ('Data_Calibration\\water\\sls', r'Data_Calibration\\water\\sls\\.*\\sls_flow_rate_forward_(-?\d+\.\d+)_ul_min', "Medium: Water - SLS 1500"),
            GLYCEROL: ('Data_Calibration\\glycerol\\sls',
                       r'Data_Calibration\\glycerol\\sls\\.*\\sls_flow_rate_forward_(-?\d+\.\d+)_ul_min', "Medium: Glycerol - SLS 1500")
        },
        FLG: {
            WATER: ('Data_Calibration\\water\\flg', r'Data_Calibration\\water\\flg\\.*\\flg_flow_rate_forward_(-?\d+\.\d+)_ul_min', "Medium: Water - FLG M+"),
            GLYCEROL: ('Data_Calibration\\glycerol\\flg',
                       r'Data_Calibration\\glycerol\\flg\\.*\\flg_flow_rate_forward_(-?\d+\.\d+)_ul_min', "Medium: Glycerol - FLG M+")
        }
    }
    return switch.get(case, {}).get(subcase, 'Invalid case or subcase')


class Plot:
    def __init__(self, folder_path, SLS1500_flag=None):
        self.directory = os.path.dirname(os.path.abspath(__file__))
        self.folder_path = folder_path
        self.SLS1500_flag = SLS1500_flag
        self.exp_name = os.path.basename(self.folder_path)

    def unpickle(self, filename):
        inputfile = open(filename, 'rb')
        pickled = pickle.load(inputfile)
        inputfile.close()
        return pickled

    def nupickle(self, data, filename):
        outputfile = open(filename, 'wb')
        pickle.dump(data, outputfile, protocol=pickle.HIGHEST_PROTOCOL)
        outputfile.close()

    def set_search_directory(self, SLS1500_flag, water_flag):
        pass

    def all_q_vs_qs_case(self, device: int, sub_case: int, polyfit=True):
        q_set_list = []
        q_measured_list = []
        q_std_list = []
        q_percent_error_list = []
        folder_path, match_pattern, plot_title = get_path_case(
            device, sub_case)

        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.csv'):
                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path)

                    mL_min = df['mL/min'].tolist() if device == SLS else [(value / 1000)
                                                                          for value in df['uL/min'].tolist()]
                    s = [(value/1000) for value in df['ms'].tolist()
                         ] if device == SLS else df['s'].tolist()
                    # mL_min = df['mL/min'].tolist() if self.SLS1500_flag else [(value / 1000) for value in df['flowrate µl/min'].tolist()]
                    # s = [(value / 1000) for value in df['ms'].tolist()] if self.SLS1500_flag else df['# time (s)'].tolist()

                    s = np.array(s)
                    low_filter = s > 2
                    q = np.array(mL_min)
                    q = q[low_filter]

                    match = re.search(match_pattern, file_path)
                    if match:
                        flow_rate = float(match.group(1))
                        # print(flow_rate)
                    else:
                        print(
                            "Error: Could not parse file name: {}".format(file_path))
                        sys.exit(1)

                    q_average = np.average(q)
                    q_error = abs(q_average - flow_rate / 1000) / \
                        (flow_rate / 1000) * 100 if flow_rate != 0 else 0
                    q_percent_error_list.append(q_error)

                    q_std = np.std(q)
                    q_measured_list.append(q_average)
                    q_std_list.append(q_std)
                    q_set_list.append(flow_rate / 1000)

        # Make Polynomial Fit Graph
        degree = 1
        poly = Polynomial.fit(q_set_list, q_measured_list, deg=degree)

        # Generate points along the x-axis for plotting the fitted line
        q_set_fit = np.linspace(min(q_set_list), max(q_set_list), 100)

        # Calculate the fitted values for the y-axis using the polynomial function
        q_measured_fit = poly(q_set_fit)

        # Get Pickles files
        filename = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\Previous_Data_Calibration\glycerol\sls\msmt_data_2.pkl"
        data_dict = self.unpickle(filename=filename)
        p_q_measured_list = data_dict['flow_mean_mlpermin']
        p_q_std_list = data_dict['flow_std_mlpermin']
        p_q_set_list = data_dict['flow_imposed_mlpermin']

        plt.figure(figsize=(10, 5))  # Fix to make plots appear larger

        # Plot q measured vs. q set
        plt.subplot(1, 2, 1)
        plt.errorbar(q_set_list, q_measured_list, yerr=q_std_list,
                     fmt='o', capsize=5, label='Measured')
        plt.plot(q_set_list, q_set_list, label='Set', linestyle='--')
        plt.plot(q_set_fit, q_measured_fit, color='red',
                 label='Fitted Line  (Degree '+str(degree) + ')')
        plt.xlabel("Set Flow Rate (mL/min)")
        plt.ylabel("Measured Flow Rate (mL/min)")
        plt.title("Flow Rate Measurement")
        # Plot pickledq measured vs. q set

        plt.errorbar(p_q_set_list, p_q_measured_list, yerr=p_q_std_list,
                     color='green', fmt='o', capsize=5, label='Previous Measured')
        plt.legend()
        # plt.show()

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
            mL_min = df['mL/min'].tolist() if self.SLS1500_flag == True else [(value / 1000)
                                                                              for value in df['uL/min'].tolist()]
            s = [(value/1000) for value in df['ms'].tolist()
                 ] if self.SLS1500_flag == True else df['s'].tolist()

            s = np.array(s)
            low_filter = s > 2
            q = np.array(mL_min)
            q = q[low_filter]

            q_average = np.average(q)
            q_error = abs(q_average - flow_rate / 1000) / \
                (flow_rate / 1000) * 100
            q_percent_error_list.append(q_error)

            q_std = np.std(q)
            q_measured_list.append(q_average)
            q_std_list.append(q_std)
            q_set_list.append(flow_rate / 1000)

        plt.figure(figsize=(10, 5))  # Fix to make plots appear larger

        # q vs qs
        plt.subplot(1, 2, 1)
        plt.errorbar(q_set_list, q_measured_list, yerr=q_std_list,
                     fmt='o', capsize=5, label='Measured')
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

    def flow_rate_over_time(self, search_pattern, file_pattern,):
        assert self.SLS1500_flag is not None, "SLS1500_flag must be set before calling this function"

        print("Plotting Flow Rate Over Time")
        # Set the figsize to the screen aspect ratio
        fig, ax = plt.subplots(1, 1, figsize=(16, 9))

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

        colors = cm.viridis(np.linspace(0.1, 0.9, len(files)))
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
            mL_min = df['mL/min'].tolist() if self.SLS1500_flag == SLS else [(value / 1000)
                                                                             for value in df['uL/min'].tolist()]
            s = [(value/1000) for value in df['ms'].tolist()
                 ] if self.SLS1500_flag == SLS else df['s'].tolist()
            ax.plot(
                s, mL_min, label='q measured {} mL/min'.format(flow_rate / 1000), c=colors[i])

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
        # Decrease the fontsize value to make the legend smaller
        plt.legend(fontsize=12, frameon=False)

        plt.show()
        # save_directory = os.path.join(directory, "Flow_Calibration_plots")
        # os.makedirs(save_directory, exist_ok=True)
        # save_path = os.path.join(save_directory, "100uL_min_to_10mL_min-{}.png".format(datetime.now().strftime("%d-%m-%Y_%H-%M-%S")))
        # plt.savefig(save_path)
        # print("Plot saved: {}".format(save_path))

    def channels_vs_time(self, save=None):
        try:
            # Load data from CSV using pandas
            filepath = self.folder_path + r'\voltages_saleae\analog_voltages\analog.csv'

            df = pd.read_csv(filepath)

            # Extract columns for time and channels
            time = df[channel_dict['Time [s]'][0]]
            channel_0 = df[channel_dict['Channel 0'][0]]
            channel_1 = df[channel_dict['Channel 1'][0]]
            channel_2 = df[channel_dict['Channel 2'][0]]
            channel_3 = df[channel_dict['Channel 3'][0]]

            # Create the plot
            plt.figure(figsize=(10, 6))
            plt.plot(
                time, channel_0, label=channel_dict['Channel 0'][2], color=channel_dict['Channel 0'][1])
            plt.plot(
                time, channel_1, label=channel_dict['Channel 1'][2], color=channel_dict['Channel 1'][1])
            plt.plot(
                time, channel_2, label=channel_dict['Channel 2'][2], color=channel_dict['Channel 2'][1])
            plt.plot(
                time, channel_3, label=channel_dict['Channel 3'][2], color=channel_dict['Channel 3'][1])

            plt.autoscale(axis='y')
            plt.xlabel('Time [s]', fontsize=20)
            plt.ylabel('Voltage [V]', fontsize=20)
            plt.title('Channel Voltage vs Time')
            plt.tick_params(axis='both', which='major', labelsize=16)

            # Customize the spines
            ax = plt.gca()
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            # Adjust the linewidth of the left spine
            ax.spines['left'].set_linewidth(0.5)
            # Adjust the linewidth of the bottom spine
            ax.spines['bottom'].set_linewidth(0.5)

            # Add gridlines to the plot
            plt.grid(color='gray', linestyle='--', linewidth=0.5)

            # Customize the legend
            plt.rcParams['figure.autolayout'] = True
            plt.rcParams['font.size'] = 9
            plt.rcParams['legend.edgecolor'] = '1'
            plt.legend(fontsize=12, frameon=False)

            # Save the plot
            if save:
                save_directory = self.exp_name
                save_path = os.path.join(
                    save_directory, f"channels_vs_time_{self.exp_name}.png")
                plt.savefig(save_path)
            # Show the plot
            plt.show()

        except Exception as e:
            print(f"Error: {e}")

    def create_pressure_vs_time(self, folder_path):
        analog_path = folder_path + r'/voltages_saleae/analog_voltages/analog.csv'

        os.makedirs(
            folder_path + r'/voltages_saleae/analog_pressures', exist_ok=True)
        pressure_path = folder_path + r'\voltages_saleae\analog_pressures\pressures.csv'

        # Read the original CSV file
        df = pd.read_csv(analog_path)

        # Change column headers to our desired names
        df.columns = [channel_dict["Time [s]"][2],
                      channel_dict["Channel 0"][2],
                      channel_dict["Channel 1"][2],
                      channel_dict["Channel 2"][2],
                      channel_dict["Channel 3"][2]]
        df.to_csv(pressure_path, index=False)

        # Apply formula to convert voltage to pressure
        df[channel_dict["Channel 0"][2]] = (
            df[channel_dict["Channel 0"][2]] / 5 - 0.5) / channel_dict["Channel 0"][3] * 10
        df[channel_dict["Channel 1"][2]] = (
            df[channel_dict["Channel 1"][2]] / 5 - 0.5) / channel_dict["Channel 1"][3] * 10
        df[channel_dict["Channel 3"][2]] = (
            df[channel_dict["Channel 3"][2]] / 5 - 0.5) / channel_dict["Channel 3"][3] * 10

        # Save the modified DataFrame to the new CSV file
        df.to_csv(pressure_path, index=False)
        print(f"New pressures.csv created successfully.")

    def pressure_vs_time(self, save=None):
        pressure_path = self.folder_path + \
            r'\voltages_saleae\analog_pressures\pressures.csv'
        df = pd.read_csv(pressure_path)

        plt.figure(figsize=(10, 6))
        plt.plot(df['s'], df['25kPa'], label='25kPa')
        plt.plot(df['s'], df['2kPa'], label='2kPa')
        plt.plot(df['s'], df['7kPa'], label='7kPa')

        plt.autoscale(axis='y')
        plt.xlabel('Time [s]', fontsize=20)
        plt.ylabel('Pressure [kPa]', fontsize=20)
        plt.title('Pressure vs Time')
        plt.tick_params(axis='both', which='major', labelsize=16)

        # Customize the spines
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(0.5)
        ax.spines['bottom'].set_linewidth(0.5)
        plt.grid(color='gray', linestyle='--', linewidth=0.5)

        # Customize the legend
        plt.rcParams['figure.autolayout'] = True
        plt.rcParams['font.size'] = 9
        plt.rcParams['legend.edgecolor'] = '1'
        plt.legend(fontsize=12, frameon=False)

        # Save the plot
        if save:
            save_directory = self.exp_name
            save_path = os.path.join(
                save_directory, f"pressures_vs_time_{self.exp_name}.png")
            plt.savefig(save_path)

        plt.show()

    def sls_flow_measurements(self, folder_path, save=None):
        flow_path = folder_path + r'\sls_flow_measurments.csv'
        # flow_path = r'C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\testsls_flow_measurments.csv'
        print("Plotting Flow Rate Over Time")
        # Set the figsize to the screen aspect ratio
        fig, ax = plt.subplots(1, 1, figsize=(16, 9))

        df = pd.read_csv(flow_path)
        print(df)

        mL_min = df['mL/min'].tolist()
        s = df['ms'].tolist()

        ax.plot(s, mL_min, label='q measured mL/min')
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
        # Decrease the fontsize value to make the legend smaller
        plt.legend(fontsize=12, frameon=False)

        plt.show()


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

if __name__ == "__main__":
    # folder_path_7kp = r'C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Pressure_Ramp_7kp_p_start_0_p_max_70_p_min0_step_size_5'
    # plot = Plot(folder_path=folder_path_7kp)
    # plot.channels_vs_time(save=True)
    # plot.create_pressure_vs_time(folder_path_7kp)
    # plot.pressure_vs_time(save=True)

    folder_path_25kp = r'C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Pressure_Ramp_25kp_plateau_time_s_5_p_start_0_p_max_70_p_min0_step_size_5'
    plot = Plot(folder_path=folder_path_25kp)
    plot.channels_vs_time(save=True)
    plot.create_pressure_vs_time(folder_path_25kp)
    plot.pressure_vs_time(save=True)
