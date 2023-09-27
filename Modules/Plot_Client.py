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
import json
import addcopyfighandler
from matplotlib.colors import Normalize

SLS = 1
FLG = 2
WATER = 3
GLYCEROL = 4
channel_dict = {
    "Time [s]": ('Time [s]', 'none', 's', 'none'),
    "Channel 0": ('Channel 0', 'black', '25kPa', 0.018),
    "Channel 1": ('Channel 1', 'brown', '7kPa', 0.057),
    "Channel 2": ('Channel 2', 'red',  '2kPa', 0.2),
    "Channel 3": ('Channel 3', 'orange', 'none', 'none'),
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

    def channels_vs_time(self, save=None, moving_average=0):
        try:
            # Load data from CSV using pandas
            filepath = self.folder_path + r'\voltages_saleae\analog_voltages\analog.csv'

            df = pd.read_csv(filepath)

            # Extract columns for time and channels
            time = df[channel_dict['Time [s]'][0]]
            channel_0 = df[channel_dict['Channel 0'][0]]
            channel_1 = df[channel_dict['Channel 1'][0]]
            channel_2 = df[channel_dict['Channel 2'][0]]

            # Apply moving average filter
            if moving_average > 0:
                channel_0 = channel_0.rolling(
                    window=moving_average).mean()
                channel_1 = channel_1.rolling(
                    window=moving_average).mean()
                channel_2 = channel_2.rolling(
                    window=moving_average).mean()
                time = time.rolling(window=moving_average).mean()

            # Create the plot
            plt.figure(figsize=(10, 6))
            plt.plot(
                time, channel_0, label=channel_dict['Channel 0'][2], color=channel_dict['Channel 0'][1])
            plt.plot(
                time, channel_1, label=channel_dict['Channel 1'][2], color=channel_dict['Channel 1'][1])
            plt.plot(
                time, channel_2, label=channel_dict['Channel 2'][2], color=channel_dict['Channel 2'][1])

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
                      channel_dict["Channel 3"][2]
                      ]
        df.to_csv(pressure_path, index=False)

        # Apply formula to convert voltage to pressure
        df[channel_dict["Channel 0"][2]] = (
            df[channel_dict["Channel 0"][2]] / 5 - 0.5) / channel_dict["Channel 0"][3] * 10
        df[channel_dict["Channel 1"][2]] = (
            df[channel_dict["Channel 1"][2]] / 5 - 0.5) / channel_dict["Channel 1"][3] * 10
        df[channel_dict["Channel 2"][2]] = (
            df[channel_dict["Channel 2"][2]] / 5 - 0.5) / channel_dict["Channel 2"][3] * 10

        # Save the modified DataFrame to the new CSV file
        df.to_csv(pressure_path, index=False)
        print(f"New pressures.csv created successfully.")

    def pressure_vs_time(self, save=None, moving_average=0):
        pressure_path = self.folder_path + \
            r'\voltages_saleae\analog_pressures\pressures.csv'
        df = pd.read_csv(pressure_path)

        if moving_average > 0:
            df['25kPa'] = df['25kPa'].rolling(window=moving_average).mean()
            df['2kPa'] = df['2kPa'].rolling(window=moving_average).mean()
            df['7kPa'] = df['7kPa'].rolling(window=moving_average).mean()
            df['s'] = df['s'].rolling(window=moving_average).mean()

        fig, ax = plt.subplots(figsize=(9.0, 3.0))
        line_25, = ax.plot(df['s'], df['25kPa'], lw=2,
                           label='25kPa', color='black')
        line_7, = ax.plot(df['s'], df['7kPa'], lw=2,
                          label='7kPa', color='brown')
        line_2, = ax.plot(df['s'], df['2kPa'], lw=2, label='2kPa', color='red')
        leg = ax.legend(fancybox=True, shadow=True)

        lines = [line_25, line_7, line_2]
        lined = {}

        for legline, origline in zip(leg.get_lines(), lines):
            legline.set_picker(True)
            lined[legline] = origline

        def on_pick(event):
            print('Picked')
            legline = event.artist
            origline = lined[legline]
            visible = not origline.get_visible()
            origline.set_visible(visible)
            legline.set_alpha(1.0 if visible else 0.2)
            fig.canvas.draw()
        fig.canvas.mpl_connect('pick_event', on_pick)

        plt.autoscale(axis='y')
        plt.xlabel('Time [s]', fontsize=20)
        plt.ylabel('Pressure [mbar]', fontsize=20)
        plt.title('Pressure vs Time')
        plt.tick_params(axis='both', which='major', labelsize=16)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Customize the spines
        # ax = plt.gca()
        # ax.spines['top'].set_visible(False)
        # ax.spines['right'].set_visible(False)
        # ax.spines['left'].set_linewidth(0.5)
        # ax.spines['bottom'].set_linewidth(0.5)
        # plt.grid(color='gray', linestyle='--', linewidth=0.5)

        # Customize the legend
        # plt.rcParams['figure.autolayout'] = True
        # plt.rcParams['font.size'] = 9
        # plt.rcParams['legend.edgecolor'] = '1'
        # plt.legend(fontsize=12, frameon=False)

        # Save the plot
        if save:
            save_directory = self.exp_name
            save_path = os.path.join(
                save_directory, f"set_pressures_vs_time_{self.exp_name}.png")
            plt.savefig(save_path)

        plt.show()

    def set_pressure_vs_time(self, save=None):
        set_pressure_path = self.folder_path + \
            r'\pressure_ramp_flg\push_pull\ramp.json'

        with open(set_pressure_path) as json_file:
            data = json.load(json_file)

        times = data['times']
        input_pressures = data['input_pressures']

        time_pressure_pairs = list(zip(times, input_pressures))

        for time, pressures in time_pressure_pairs:
            print(f"Time: {time}, Pressures: {pressures}")

        fig, ax = plt.subplots(1, 1, figsize=[2.5, 2.5])
        ax.plot(times, input_pressures, label="ctrl 1", marker='o',
                color=[0, 0, 0])
        ax.legend()
        ax.set_title(f"Inputs - {self.exp_name}")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Input pressures (mbar)")
        plt.tight_layout()
        if save:
            fig.savefig(f'{self.folder_path}/pressure_inputs.png', dpi=300)
        plt.show()

    def measured_pressure_vs_time(self, save=None, moving_average=0, zoomed=False, nb_controllers=1):
        measured_pressure_path = self.folder_path + \
            r'\pressure_ramp_flg\pressure_measurements.csv'
        df = pd.read_csv(measured_pressure_path)

        if moving_average > 0 and nb_controllers == 1:
            df['mbar'] = df['mbar'].rolling(window=moving_average).mean()
            df['s'] = df['s'].rolling(window=moving_average).mean()

        if moving_average > 0 and nb_controllers == 2:
            df['mbar_p1'] = df['mbar_p1'].rolling(window=moving_average).mean()
            df['mbar_p2'] = df['mbar_p2'].rolling(window=moving_average).mean()
            df['s'] = df['s'].rolling(window=moving_average).mean()

        fig, ax = plt.subplots(figsize=(9.0, 3.0))
        if nb_controllers == 2:
            plt.plot(df['s'], df['mbar_p1'],
                     color='blue', label='controller 1')
            plt.plot(df['s'], df['mbar_p2'], color='red', label='controller 2')
        else:
            plt.plot(df['s'], df['mbar'], color='blue')
        plt.autoscale(axis='y')
        plt.xlabel('Time [s]', fontsize=20)
        plt.ylabel('Pressure [mbar]', fontsize=20)
        plt.title('FLG Pressure vs Time')
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

        if zoomed:
            figzoom, axzoom = plt.subplots(figsize=(9.0, 3.0))
            axzoom.set(xlim=(0.0, 75), ylim=(0.0, 0.1),
                       autoscale_on=False, title='Zoom window')
            axzoom.plot(df['s'], df['mbar'], color='blue')
            axzoom.autoscale(axis='y')
            axzoom.legend(fontsize=8, frameon=False)
            axzoom.set_xlabel("Time [s]", fontsize=20)
            axzoom.set_ylabel("Pressure [mbar]", fontsize=20)
            axzoom.tick_params(axis='both', which='major', labelsize=16)
            axzoom.spines['top'].set_visible(False)
            axzoom.spines['right'].set_visible(False)

            def on_press(event):
                if event.button != 1:
                    return
                x, y = event.xdata, event.ydata
                axzoom.set_xlim(x - 35, x + 35)
                axzoom.set_ylim(y - 0.03, y + 0.03)
                axzoom.tick_params(axis='both', which='major', labelsize=16)
                figzoom.canvas.draw()
                print("Zoomed")

            fig.canvas.mpl_connect('button_press_event', on_press)

        # Save the plot
        if save:
            save_directory = self.exp_name
            save_path = os.path.join(
                save_directory, f"measured_pressures_vs_time_{self.exp_name}.png")
            plt.savefig(save_path)
            if zoomed:
                save_path = os.path.join(
                    save_directory, f"measured_pressures_vs_time_zoomed_{self.exp_name}.png")
                figzoom.savefig(save_path)

        plt.show()

    def double_pressure_controller_command_overview(self, save=None, moving_average=0, nb_controllers=2):
        assert nb_controllers == 2, "Number of controllers must be equal to 2"

        measured_pressure_path = os.path.join(
            self.folder_path, 'pressure_ramp_flg', 'pressure_measurements.csv')
        df = pd.read_csv(measured_pressure_path)

        if moving_average > 0 and nb_controllers == 2:
            df['mbar_p1'] = df['mbar_p1'].rolling(window=moving_average).mean()
            df['mbar_p2'] = df['mbar_p2'].rolling(window=moving_average).mean()
            df['s'] = df['s'].rolling(window=moving_average).mean()

        fig, ax = plt.subplots(figsize=(9.0, 3.0))

        if nb_controllers == 2:
            plt.scatter(df['mbar_p1'], df['mbar_p2'], c=df['s'],
                        cmap='viridis', label='Pressure1 vs Pressure2')

        plt.autoscale(axis='y')
        plt.xlabel('Pressure Controller 1 [mbar]', fontsize=20)
        plt.ylabel('Pressure Controller 2 [mbar]', fontsize=20)
        plt.colorbar(label='Time [s]')
        plt.title('Commanded vs Measured Pressure')
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

        if save:
            save_directory = self.exp_name
            save_path = os.path.join(
                save_directory, f"commanded_vs_recorded_pressures_{self.exp_name}.png")
            plt.savefig(save_path)

        plt.show()

    def on_press(event, axzoom, figzoom):
        if event.button != 1:
            return
        x, y = event.xdata, event.ydata
        x, y = event.xdata, event.ydata
        axzoom.set_xlim(x - 0.1, x + 0.1)
        axzoom.set_ylim(y - 0.1, y + 0.1)
        figzoom.canvas.draw()

    def sls_flow_measurements(self, save=None, moving_average=0, zoomed=False):
        flow_path = self.folder_path + r'\flow_sls\sls_flow_measurments.csv'
        # flow_path = r'C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\testsls_flow_measurments.csv'
        print("Plotting Flow Rate Over Time")
        # Set the figsize to the screen aspect ratio
        fig, ax = plt.subplots(figsize=(9.0, 3.0))

        df = pd.read_csv(flow_path)

        window_size = moving_average
        if window_size > 0:
            df['mL/min'] = df['mL/min'].rolling(window=window_size).mean()
            df['s'] = df['s'].rolling(window=window_size).mean()

        mL_min = df['mL/min'].tolist()
        s = df['s'].tolist()

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
        plt.title('SLS Flow vs Time')
        plt.grid(color='gray', linestyle='--', linewidth=0.5)

        if zoomed:
            figzoom, axzoom = plt.subplots(figsize=(9.0, 3.0))
            axzoom.set(xlim=(0.0, 50), ylim=(0.0, 0.1),
                       autoscale_on=False, title='Zoom window')
            axzoom.plot(s, mL_min, label='q measured mL/min')
            axzoom.autoscale(axis='y')
            axzoom.legend(fontsize=8, frameon=False)
            axzoom.set_xlabel("Time [s]", fontsize=20)
            axzoom.set_ylabel("Flow [mL/min]", fontsize=20)
            axzoom.tick_params(axis='both', which='major', labelsize=16)
            axzoom.spines['top'].set_visible(False)
            axzoom.spines['right'].set_visible(False)

            def on_press(event):

                if event.button != 1:
                    return
                x, y = event.xdata, event.ydata
                axzoom.set_xlim(x - 25, x + 25)
                axzoom.set_ylim(y - 0.03, y + 0.03)
                axzoom.tick_params(axis='both', which='major', labelsize=16)
                figzoom.canvas.draw()
                print("Zoomed")

            fig.canvas.mpl_connect('button_press_event', on_press)

        if save:
            fig.savefig(
                f'{self.folder_path}/sls_flow_measurements.png', dpi=300)
            if zoomed:
                figzoom.savefig(
                    f'{self.folder_path}/sls_flow_measurements_zoomed.png', dpi=300)

        plt.show()

    def flow_vs_pressure(self, save=None, flow_moving_average=0, pressure_moving_average=0, pressure_sensor_value=None):
        flow_path = self.folder_path + r'\flow_sls\sls_flow_measurments.csv'
        pressure_path = self.folder_path + \
            r'\voltages_saleae\analog_pressures\pressures.csv'

        df_flow = pd.read_csv(flow_path)
        df_pressure = pd.read_csv(pressure_path)

        # Get the corresponding values
        flow_mL_min = df_flow['mL/min'].tolist()
        flow_s = df_flow['s'].tolist()

        pressure_sensor_value_kPa = str(pressure_sensor_value) + 'kPa'
        pressure_mbar = df_pressure[pressure_sensor_value_kPa].tolist()
        pressure_s = df_pressure['s'].tolist()

        if flow_moving_average > 0:
            flow_mL_min = df_flow['mL/min'].rolling(
                window=flow_moving_average).mean()
            flow_s = df_flow['s'].rolling(window=flow_moving_average).mean()

        if pressure_moving_average > 0:
            pressure_mbar = df_pressure[pressure_sensor_value_kPa].rolling(
                window=pressure_moving_average).mean()
            pressure_s = df_pressure['s'].rolling(
                window=pressure_moving_average).mean()

        # Create a figure and axis
        fig, ax1 = plt.subplots(figsize=(12.0, 6.0))

        # Plot pressure vs. time on the left y-axis (ax1)
        ax1.plot(pressure_s, pressure_mbar,
                 'b-', label=str(pressure_sensor_value)+'0 mbar Sensor')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Pressure [mbar]', color='blue')
        ax1.tick_params('y', colors='blue')

        # Create a secondary y-axis (ax2) on the right for flow
        ax2 = ax1.twinx()
        ax2.plot(flow_s, flow_mL_min,
                 'r-', label='mL/min')
        ax2.set_ylabel('Flow [mL/min]', color='red')
        ax2.tick_params('y', colors='red')

        # # Add legends
        ax1.legend(loc='upper left', bbox_to_anchor=(0.05, 0.9))
        plt.grid(color='gray', linestyle='--', linewidth=0.5)

        # # Display the plot
        plt.title('Pressure and Flow vs. Time')

        if (save):
            save_directory = self.exp_name
            save_path = os.path.join(
                save_directory, f"flow_vs_pressure_{pressure_sensor_value}0mbar.png")
            plt.savefig(save_path)
        plt.show()


if __name__ == "__main__":
    # folder_path_7kp = r'C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Pressure_Ramp_7kp_p_start_0_p_max_70_p_min0_step_size_5'
    # plot = Plot(folder_path=folder_path_7kp)
    # plot.channels_vs_time(save=True)
    # plot.create_pressure_vs_time(folder_path_7kp)
    # plot.pressure_vs_time(save=True)

    folder_path = r'C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Test_zigzag_Controller'
    plot = Plot(folder_path=folder_path, SLS1500_flag=False)

    # plot.set_pressure_vs_time(save=True)
    plot.double_pressure_controller_command_overview(
        save=False, moving_average=40, nb_controllers=2)
    # plot.measured_pressure_vs_time(
    #     save=True, moving_average=10, zoomed=False, nb_controllers=2)
    # plot.sls_flow_measurements(save=False, moving_average=5, zoomed=False)
    # plot.channels_vs_time(save=True, moving_average=100)
    # plot.create_pressure_vs_time(folder_path)
    # plot.pressure_vs_time(save=False, moving_average=50)
    # plot.flow_vs_pressure(save=True, flow_moving_average=50, pressure_moving_average=50,
    #                       pressure_sensor_value=7)
