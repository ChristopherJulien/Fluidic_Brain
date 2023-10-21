__author__ = "Julien Stocker, Louis-Justin Tallot, Alexia Allal and Anne Meeussen"
import threading
import Saleae
import SLS_1500
import Push_Pull_Pressure
import subprocess
import sys
import json
import os
# Import the required libraries
import customtkinter
import tkinterdnd2 as tkinterDnD
from tkinter import filedialog
import time
import os

customtkinter.set_ctk_parent_class(tkinterDnD.Tk)
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1400x780")
app.title("Combined Environment Control Interface")
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)

radiobutton_var = customtkinter.IntVar(value=1)
label_font = ("Arial", 14)
desktop_directory = os.path.expanduser("~/Desktop")

frames = []
for i in range(4):
    frame = customtkinter.CTkFrame(master=app)
    frame.grid(row=0, column=i, padx=20, pady=20, sticky="nsew")
    frames.append(frame)

bottom_frame = customtkinter.CTkFrame(master=app)
bottom_frame.grid(row=1, column=0, columnspan=4,
                  padx=20, pady=20, sticky="nsew")

flag_syringe_pump = False
COM_syringe_pump = None
type_syringe_pump = None
volume_syringe_pump = None
flow_rate_syringe_pump = None

flag_saleae = False
flag_calibration = False
COM_saleae = None
channels_saleae = None
buffer_size_saleae = None
sampling_rate_saleae = None
device_id_saleae = None


class Widget():
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_directory.set(directory)

    def start(self):
        flag_syringe_pump = self.switch_1.get()
        COM_syringe_pump = self.combobox_1_0.get()
        type_syringe_pump = self.segmented_button_1.get()
        volume_syringe_pump = self.entry_1.get()
        flow_rate_syringe_pump = self.entry_1_2.get()

        flag_saleae = self.switch_2.get()
        flag_calibration = self.checkbox_2.get()
        COM_saleae = self.combobox_2.get()
        channels_saleae = self.segmented_button_2.get()
        buffer_size_saleae = self.combobox_2_1.get()
        sampling_rate_saleae = self.combobox_2_2.get()
        device_id_saleae = self.entry_2.get()

        exp_folder = self.entry_5_1.get()
        master_folder_path = self.selected_directory.get() + r"/"+exp_folder

        if flag_calibration:
            print("Calibration on everything")

        if flag_syringe_pump and flag_saleae:
            # run with the syringe pump
            print('Syringe Pump and Saleae are on')
            pass

        elif flag_syringe_pump:
            # run with the syringe pump
            print('Syringe Pump is on')
            pass

        elif flag_calibration and flag_saleae:
            print('Calibration and Saleae are on')
            # run without the syringe pump
            pass

        print('Switch Syringe Pump: ', self.switch_1.get())
        print('Syringe Pump COM: ', self.combobox_1_0.get())
        print('Syringe Pump Syringe: ', self.segmented_button_1.get())
        print('Syringe Pump Syringe Type: ', self.combobox_1_2.get())
        print('Syringe Pump Syringe Volume: ', self.entry_1.get())
        print('Syringe Pump Flow Rate: ', self.entry_1_2.get())

        print('Switch Saleae: ', self.switch_2.get())
        print('Saleae COM: ', self.combobox_2.get())
        print('Saleae Channels: ', self.segmented_button_2.get())
        print('Saleae Buffer Size: ', self.combobox_2_1.get())
        print('Saleae Sampling Rate: ', self.combobox_2_2.get())
        print('Saleae Device Id: ', self.entry_2.get())

        print('Switch Fluigent: ', self.switch_3.get())

        print('Switch SLS: ', self.switch_4.get())

        print('Experiment Folder Name: ', self.entry_5_1.get())
        print('Export Directory: ', self.selected_directory.get())
        print('Capture Duration: ', self.entry_5.get())
        # duration = int(self.entry_5.get())

        # if duration > 0:
        #     self.countdown(duration)
        #     self.time_remaining.set(0)
        #     self.progressbar_5.set(0)

    def switch_syringe_pump(self):
        # Define logic for Syringe Pump switch
        pass

    def switch_saleae(self):
        # Define logic for Saleae switch
        pass

    def switch_fluigent(self):
        # Define logic for Fluigent switch
        pass

    def switch_sls(self):
        # Define logic for SLS switch
        pass

    def check_calibration(self):
        # Define logic for calibration checkbox
        pass

    switch_1 = customtkinter.CTkSwitch(
        master=frames[0], text="On/Off", command=switch_syringe_pump)
    combobox_1_0 = customtkinter.CTkComboBox(
        frames[0], values=[str(i) for i in range(1, 13)], width=200)
    segmented_button_1 = customtkinter.CTkSegmentedButton(
        master=frames[0], values=["       Syringe A       ", "       Syringe B       "], width=200)
    combobox_1_2 = customtkinter.CTkComboBox(
        frames[0], values=["BDP", "BDG"], width=200)
    entry_1 = customtkinter.CTkEntry(
        master=frames[0], placeholder_text="Syringe Volume [mL] ", width=200)
    entry_1_2 = customtkinter.CTkEntry(
        master=frames[0], placeholder_text="Flow Rate [uL/min] ", width=200)

    switch_2 = customtkinter.CTkSwitch(
        master=frames[1], text="On/Off", command=switch_saleae)
    checkbox_2 = customtkinter.CTkCheckBox(
        master=frames[1], text="Calibration", command=check_calibration)
    combobox_2 = customtkinter.CTkComboBox(
        frames[1], values=[str(i) for i in range(1, 13)], width=200)
    segmented_button_2 = customtkinter.CTkSegmentedButton(
        master=frames[1], values=[" Channel 0-1-2-3 ", " Channel 4-5-6-7 "], width=200)
    combobox_2_1 = customtkinter.CTkComboBox(
        frames[1],  values=[f"{i} GB" for i in range(1, 13)], width=200)
    combobox_2_2 = customtkinter.CTkComboBox(
        frames[1], values=['781250', '1562500', '3125000'], width=200)
    entry_2 = customtkinter.CTkEntry(
        master=frames[1], placeholder_text="Device Id", width=200)

    switch_3 = customtkinter.CTkSwitch(
        master=frames[2], text="On/Off", command=switch_fluigent)
    switch_4 = customtkinter.CTkSwitch(
        master=frames[3], text="On/Off", command=switch_sls)

    entry_5_1 = customtkinter.CTkEntry(
        master=bottom_frame, placeholder_text="Experiment Folder Name", width=400)
    select_location_button = customtkinter.CTkButton(
        master=bottom_frame, text="Change Export Directory", command=browse_directory)
    selected_directory = customtkinter.StringVar()
    selected_directory.set(desktop_directory)
    selected_directory_label = customtkinter.CTkLabel(
        master=bottom_frame, textvariable=selected_directory)
    entry_5 = customtkinter.CTkEntry(
        master=bottom_frame, placeholder_text="Capture Duration [s]", width=400)
    time_remaining = customtkinter.IntVar()
    time_remaining.set(0)
    time_remaining_label = customtkinter.CTkLabel(
        master=bottom_frame, textvariable=time_remaining, font=("Arial", 14))
    progressbar_5 = customtkinter.CTkProgressBar(
        master=bottom_frame, width=400, height=20, fg_color="#333333")
    progressbar_5.set(1)
    start_button = customtkinter.CTkButton(
        master=bottom_frame, text="Start", command=start)

    def countdown(self, duration):
        for i in range(duration, -1, -1):
            self.time_remaining.set(i)
            progress = 1 - ((duration - i) / duration)
            self.progressbar_5.set(progress)
            app.update()
            time.sleep(1)

    def create_syringe_pump_frame(self, app, width_syringe_frame=200):
        width_syringe_frame = width_syringe_frame

        self.frame_1 = customtkinter.CTkFrame(master=app)
        self.frame_1.grid(row=0, column=0, padx=60, pady=20, sticky="nsew")

        label_1 = customtkinter.CTkLabel(
            master=self.frame_1, justify=customtkinter.LEFT, text="SYRINGE PUMP", font=label_font)
        label_1.pack(pady=10, padx=10)

        self.switch_1 = customtkinter.CTkSwitch(
            master=self.frame_1, text="On/Off", command=self.switch_syringe_pump)
        self.switch_1.pack(pady=10, padx=10)

        self.combobox_1_0 = customtkinter.CTkComboBox(
            self.frame_1, values=[str(i) for i in range(1, 13)], width=width_syringe_frame)
        self.combobox_1_0.pack(pady=10, padx=10)
        self.combobox_1_0.set("Choose COM")

        self.segmented_button_1 = customtkinter.CTkSegmentedButton(
            master=self.frame_1, values=["       Syringe A       ", "       Syringe B       "], width=width_syringe_frame)
        self.segmented_button_1.pack(pady=10, padx=10)

        self.combobox_1_2 = customtkinter.CTkComboBox(
            self.frame_1, values=["BDP", "BDG"], width=width_syringe_frame)
        self.combobox_1_2.pack(pady=10, padx=10)
        self.combobox_1_2.set("Syringe Type")

        self.entry_1_text_var = customtkinter.StringVar()
        self.entry_1 = customtkinter.CTkEntry(
            master=self.frame_1, placeholder_text="Syringe Volume [mL] ", width=width_syringe_frame)
        self.entry_1.pack(pady=10, padx=10)

        self.entry_1_2 = customtkinter.CTkEntry(
            master=self.frame_1, placeholder_text="Flow Rate [uL/min] ", width=width_syringe_frame)
        self.entry_1_2.pack(pady=10, padx=10)

    def create_saleae_frame(self, app, width_saleae_frame=220):
        width_saleae = width_saleae_frame
        frame_2 = customtkinter.CTkFrame(master=app)
        frame_2.grid(row=0, column=1, padx=60, pady=20, sticky="nsew")

        label_2 = customtkinter.CTkLabel(
            master=frame_2, justify=customtkinter.LEFT, text="SALEAE", font=label_font)
        label_2.pack(pady=10, padx=10)

        self.switch_2 = customtkinter.CTkSwitch(
            master=frame_2, text="On/Off", command=self.switch_saleae)
        self.switch_2.pack(pady=10, padx=10)

        checkbox_2 = customtkinter.CTkCheckBox(
            master=frame_2, text="Calibration", command=self.check_calibration)
        checkbox_2.pack(pady=10, padx=10)

        self.combobox_2 = customtkinter.CTkComboBox(
            frame_2, values=[str(i) for i in range(1, 13)], width=width_saleae)
        self.combobox_2.pack(pady=10, padx=10)
        self.combobox_2.set("Choose COM")

        self.segmented_button_2 = customtkinter.CTkSegmentedButton(
            master=frame_2, values=[" Channel 0-1-2-3 ", " Channel 4-5-6-7 "], width=width_saleae)
        self.segmented_button_2.pack(pady=10, padx=10)

        self.combobox_2_1 = customtkinter.CTkComboBox(
            frame_2,  values=[f"{i} GB" for i in range(1, 13)], width=width_saleae)
        self.combobox_2_1.pack(pady=10, padx=10)
        self.combobox_2_1.set("Buffer Size [GB]")

        self.combobox_2_2 = customtkinter.CTkComboBox(
            frame_2, values=['781250', '1562500', '3125000'], width=width_saleae)
        self.combobox_2_2.pack(pady=10, padx=10)

        entry_2_text_var = customtkinter.StringVar()
        self.entry_2 = customtkinter.CTkEntry(
            master=frame_2, placeholder_text="Device Id", width=width_saleae)
        self.entry_2.pack(pady=10, padx=10)

    def create_fluigent_frame(self, app):
        self.frame_3 = customtkinter.CTkFrame(master=app)
        self.frame_3.grid(row=0, column=2, padx=60, pady=20, sticky="nsew")

        label_fluigent = customtkinter.CTkLabel(
            master=self.frame_3, justify=customtkinter.LEFT, text="FLUIGENT", font=label_font)
        label_fluigent.pack(pady=10, padx=10)

        self.switch_3 = customtkinter.CTkSwitch(
            master=self.frame_3, text="On/Off", command=self.switch_fluigent)
        self.switch_3.pack(pady=10, padx=10)

    def create_sls_frame(self, app):
        frame_4 = customtkinter.CTkFrame(master=app)
        frame_4.grid(row=0, column=3, padx=60, pady=20, sticky="nsew")

        label_sls = customtkinter.CTkLabel(
            master=frame_4, justify=customtkinter.LEFT, text="SLS", font=label_font)
        label_sls.pack(pady=10, padx=10)

        self.switch_4 = customtkinter.CTkSwitch(
            master=frame_4, text="On/Off", command=self.switch_sls)
        self.switch_4.pack(pady=10, padx=10)

    def create_capture_param_frame(self, app):
        frame_bottom = customtkinter.CTkFrame(master=app)
        frame_bottom.grid(row=1, column=0, columnspan=4, padx=10,
                          pady=10, sticky="nsew")

        label_5 = customtkinter.CTkLabel(
            master=frame_bottom, justify=customtkinter.LEFT, text="CAPTURE PARAMETERS", font=label_font)
        label_5.pack(pady=10, padx=10)

        width_bottom = 400

        self.entry_5_1 = customtkinter.CTkEntry(
            master=frame_bottom, placeholder_text="Experiment Folder Name", width=width_bottom)
        self.entry_5_1.pack(pady=10, padx=10)

        self.selected_directory = customtkinter.StringVar()
        self.selected_directory.set(desktop_directory)

        self.select_location_button = customtkinter.CTkButton(
            master=frame_bottom, text="Change Export Directory", command=self.browse_directory)
        self.select_location_button.pack(pady=10, padx=10)

        self.selected_directory_label = customtkinter.CTkLabel(
            master=frame_bottom, textvariable=self.selected_directory)
        self.selected_directory_label.pack(pady=10, padx=10)

        self.entry_5 = customtkinter.CTkEntry(
            master=frame_bottom, placeholder_text="Capture Duration [s]", width=width_bottom,)
        self.entry_5.pack(pady=10, padx=10)

        self.time_remaining = customtkinter.IntVar()
        self.time_remaining.set(0)
        self.time_remaining_label = customtkinter.CTkLabel(
            master=frame_bottom, textvariable=self.time_remaining, font=("Arial", 14))
        self.time_remaining_label.pack(pady=10, padx=10)

        self.progressbar_5 = customtkinter.CTkProgressBar(
            master=frame_bottom, width=width_bottom, height=20, fg_color="#333333")
        self.progressbar_5.pack(pady=2, padx=10)
        self.progressbar_5.set(1)

        self.start_button = customtkinter.CTkButton(
            master=frame_bottom, text="Start", command=self.start)
        self.start_button.pack(pady=10, padx=10)


for i in range(4):
    app.grid_columnconfigure(i, weight=1)

create_window = Widget()
create_window.create_syringe_pump_frame(app)
create_window.create_saleae_frame(app)
create_window.create_fluigent_frame(app)
create_window.create_sls_frame(app)
create_window.create_capture_param_frame(app)

app.mainloop()


# ~~~~~~~~~~~~~~~~~~~~~~  Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Calibration
calibration_flag = 0
micro_flag = False
calibration_folder = 'Calibration_' if calibration_flag else ''

# SLS Parameters
sls_interval = "\x00\x64"  # recording interaval 100ms

# # Pressure Parameters
# nb_controllers = 2
# plateau_time = 18 if not calibration_flag else 10

# start_p1 = -200 if not calibration_flag else 0
# max_p1 = 0 if not calibration_flag else 10
# nb_steps1 = 25 if not calibration_flag else 10
# or by number of steps: step_size = int((Pmax - Pmin) / 20.)

# start_p2 = -200 if not calibration_flag else 0
# max_p2 = 0 if not calibration_flag else 10
# nb_steps2 = 25 if not calibration_flag else 10

# # Dont matter for mp_two_controller
# min_p2 = -200 if not calibration_flag else 0
# min_p1 = -200 if not calibration_flag else 0

# zigzag: bool = False
# nb_big_ramp_controller: int = 1

# Saleae Parameters
buffer_size_megabytes = 20000
analog_sample_rate = 781250

# Documenting Parameters
Lstring = ''
IDstring = ''
check_valve_type = ''
h_init_cm = ''
vl_init = ''

# ~~~~~~~~~~~~~~~~~~~~~~  Experiment Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# If experiment name is too long Saleae will have trouble saving the file at this folder

# exp_folder = 'node_tube_{:s}_ID_{:s}_{:s}_node_h_init{:s}_vl_init{:s}/'.format(Lstring, IDstring, check_valve_type,h_init_cm,vl_init)
# exp_folder = ('A_II_plateau_time_{:d}_p_start_{:d}_p_max_{:d}_p_min{:d}_step_size_{:d}'.format(plateau_time, Pstart, Pmax, Pmin, step_size))
# exp_folder = ('TEST_plateau_time_s_{:d}_p_start_{:d}_p_max_{:d}_p_min{:d}_step_size_{:d}'.format(plateau_time, Pstart, Pmax, Pmin, step_size))
# exp_folder = ('NO-FLOW-SLS-CALIBRATION'.format(
# exp_folder = ('FS-NoFlow-Threaded-plateau_time{:d}_p_start_{:d}_p_max_{:d}_p_min{:d}_step_size_{:f}'.format(
# plateau_time, start_p1, max_p1, min_p1, nb_steps1))
exp_folder = ("{:s}FNetwork-1_8_Diode2_neg2".format(
    calibration_folder))
# exp_folder = ('{:s}Forward_Netowork-plat_time_{:d}_p1_start_{:d}_p1_max_{:d}_p1_min{:d}_step_size1_{:0.2f}-_p2_start_{:d}_p2_max_{:d}_p2_min{:d}_step_size2_{:0.2f}'.format(
#     calibration_folder, plateau_time, start_p1, max_p1, min_p1, nb_steps1, start_p2, max_p2, min_p2, nb_steps2))


# ~~~~~~~~~~~~~~~~~~~~~~  Experiment Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Folder names and paths
master_folder_path = os.path.abspath(os.getcwd()) + r"/"+exp_folder
calibration_time_s = 40
calibration_subfolder = r'calibration_saleae'
voltages_subfolder = r'voltages_saleae'
voltages_analog_subfolder = voltages_subfolder + r'/analog_voltages'
flow_subfolder = r'flow_sls'
pressure_ramp_subfolder = r'pressure_ramp_flg'
micro_flow_flg_subfolder = r'micro_flow_flg'

# Check and create each subfolder
for subfolder_path in [exp_folder]:
    if not os.path.exists(exp_folder+'/'+subfolder_path):
        os.mkdir(subfolder_path)
        print(f"Subfolder {subfolder_path} created successfully.")
    else:
        print(f"Subfolder {subfolder_path} already exists.")

dict_name = r"\parameters.json"
path_to_save_parameters = master_folder_path + dict_name
print(f"Path to save parameters: {path_to_save_parameters}")

if nb_controllers == 2:
    possible_p1 = ((max_p1-start_p1)/nb_steps1) + 1
    possible_p2 = ((max_p2-start_p2)/nb_steps2) + 1
    all_steps = possible_p1*possible_p2
    total_seconds = all_steps*plateau_time
    total_mins = total_seconds // 60
    total_time = '{:.0f}mins{:d}s'.format(total_mins, int(total_seconds) % 60)
    print('Total Time: '+total_time)


# Create a dictionary with all the parameters
parameters_dict = {"micro_flag": micro_flag, "calibration_flag": calibration_flag, "nb_controllers": nb_controllers, "nb_big_ramp_controller": nb_big_ramp_controller, "IDstring": IDstring, "Lstring": Lstring,
                   "check_valve_type": check_valve_type, "plateau_time": plateau_time, "start_p1": start_p1, "start_p2": start_p2, "max_p1": max_p1, "max_p2": max_p2, "min_p1": min_p1, "min_p2": min_p2, "nb_steps1": nb_steps1, "nb_steps2": nb_steps2, "h_init_cm": h_init_cm, "vl_init_mL": vl_init,
                   "exp_name": exp_folder, "calibration_subfolder": calibration_subfolder, "voltages_subfolder": voltages_subfolder, 'voltages_analog_subfolder': voltages_analog_subfolder, 'flow_subfolder': flow_subfolder, 'pressure_ramp_subfolder': pressure_ramp_subfolder, 'micro_flow_flg_subfolder': micro_flow_flg_subfolder,
                   "total_seconds": total_seconds, "total_time": total_time, "calibration_time_s": calibration_time_s, 'master_folder_path': master_folder_path, 'buffer_size_megabytes': buffer_size_megabytes, 'analog_sample_rate': analog_sample_rate, 'sls_interval': sls_interval}

# Save the dictionary to a JSON file in folder_path
with open(path_to_save_parameters, "w") as json_file:
    json.dump(parameters_dict, json_file)
print("Parameters Dictionary saved as JSON in 'parameters.json'")
json_string = json.dumps(parameters_dict)

# Replace these with the paths to your three Python scripts
script1_path_saleae = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\Saleae.py"
script2_path_sls = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\SLS_1500.py"
script3_path_push_pull = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\Push_Pull_Pressure.py"
script4_path_micro_flow = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\FLG_M_Plus.py"

# Define a function to run the scripts and pass json file as arguments to each script


def run_script(script_path):
    process = subprocess.Popen(["python", script_path, json_string])
    return process


def close_script(process):
    process.communicate()
    process.kill()


if calibration_flag:
    print("Calibration started")
    if micro_flag:
        calib_salea = run_script(script1_path_saleae)
        # calib_uflow = run_script(script4_path_micro_flow)
        close_script(calib_salea)
        # close_script(calib_uflow)
    else:
        calib_salea = run_script(script1_path_saleae)
        close_script(calib_salea)
        # calib_sls = run_script(script2_path_sls)
        # close_script(calib_sls)

elif calibration_flag == False:
    print('Experiment started')
    # Start each script in a separate process
    if micro_flag:
        process1_saleae = run_script(script1_path_saleae)
        # process0_uflow = run_script(script4_path_micro_flow)
        process2_push_pull = run_script(script3_path_push_pull)
        close_script(process1_saleae)
        # close_script(process0_uflow)
        close_script(process2_push_pull)

    else:
        process1_saleae = run_script(script1_path_saleae)
        # process0_flow_sls = run_script(script2_path_sls)
        process3_push_pull = run_script(script3_path_push_pull)
        close_script(process1_saleae)
        # close_script(process0_flow_sls)
        close_script(process3_push_pull)
