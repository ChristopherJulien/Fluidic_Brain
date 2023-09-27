"""
Multi-Process Script to for TWO Fluigent Push-Pull Pressure Controller"

Based on the Basic Set Pressure from Fluigent SDK
​Install locally the sdk with:
```bash
    python -m pip install fluigent_sdk-22.0.0.zip
```
"""

__author__ = "Julien Stocker, Louis-Justin Tallot, Alexia Allal and Anne Meeussen"
import threading
import Saleae
import SLS_1500
import Push_Pull_Pressure
import subprocess
import sys
import json
import os

# Calibration
sls_calibration_flag = False

# SLS Parameters
sls_interval = "\x00\x64"  # recording interaval 100ms

# Pressure Parameters
nb_controllers = 2
plateau_time = 8

start_p1 = -10
max_p1 = 30
min_p1 = 0
# or by number of steps: step_size = int((Pmax - Pmin) / 20.)
nb_steps1 = 10

start_p2 = 0
max_p2 = 10
min_p2 = 0
# or by number of steps: step_size = int((Pmax - Pmin) / 20.)
nb_steps2 = 10

zigzag: bool = False
nb_big_ramp_controller: int = 0


# Saleae Parameters
buffer_size_megabytes = 16000
analog_sample_rate = 781250

# Documenting Parameters
Lstring = ''
IDstring = ''
check_valve_type = ''
h_init_cm = ''
vl_init = ''
# exp_folder = 'node_tube_{:s}_ID_{:s}_{:s}_node_h_init{:s}_vl_init{:s}/'.format(Lstring, IDstring, check_valve_type,h_init_cm,vl_init)
# exp_folder = ('A_II_plateau_time_{:d}_p_start_{:d}_p_max_{:d}_p_min{:d}_step_size_{:d}'.format(plateau_time, Pstart, Pmax, Pmin, step_size))
# exp_folder = ('TEST_plateau_time_s_{:d}_p_start_{:d}_p_max_{:d}_p_min{:d}_step_size_{:d}'.format(plateau_time, Pstart, Pmax, Pmin, step_size))
exp_folder = 'Test_zigzag_Controller'
# exp_folder = ('NO-FLOW-SLS-CALIBRATION'.format(
# exp_folder = ('FS-NoFlow-Threaded-plateau_time{:d}_p_start_{:d}_p_max_{:d}_p_min{:d}_step_size_{:f}'.format(
#     plateau_time, start_p1, max_p1, min_p1, nb_steps1))


# ~~~~~~~~~~~~~~~~~~~~~~  Experiment Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Folder names and paths
master_folder_path = os.path.abspath(os.getcwd()) + r"/"+exp_folder
calibration_time_s = 30
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

# Calculate total time in nb controller =1
if nb_controllers == 1:
    nstep_up1 = int((max_p1 - start_p1)/nb_steps1)+1
    max_p = start_p1 + nb_steps1*(nstep_up1-1)
    nstep_down1 = int((max_p - min_p1)/nb_steps1)
    min_p = max_p - nb_steps1*(nstep_down1)
    nstep_up2 = - nstep_up1 + nstep_down1+1
    total_seconds = plateau_time * (nstep_up1 + nstep_down1 + nstep_up2)
    total_mins = total_seconds // 60
    total_time = '{:d}mins{:d}s'.format(total_mins, total_seconds % 60)
    print('Total Time: '+total_time)

elif nb_controllers == 2:
    possible_p1 = ((max_p1-start_p1)/nb_steps1) + 1
    possible_p2 = ((max_p2-start_p2)/nb_steps2) + 1
    all_steps = possible_p1*possible_p2
    total_seconds = all_steps*plateau_time
    total_mins = total_seconds // 60
    total_time = '{:.0f}mins{:d}s'.format(total_mins, int(total_seconds) % 60)
    print('Total Time: '+total_time)


# Create a dictionary with all the parameters
parameters_dict = {"calibration_flag": sls_calibration_flag, "nb_controllers": nb_controllers, "IDstring": IDstring, "Lstring": Lstring,
                   "check_valve_type": check_valve_type, "plateau_time": plateau_time, "start_p1": start_p1, "start_p2": start_p2, "max_p1": max_p1, "max_p2": max_p2, "min_p1": min_p1, "min_p2": min_p2, "nb_steps1": nb_steps1, "nb_steps2": nb_steps2, "h_init_cm": h_init_cm, "vl_init_mL": vl_init,
                   "exp_name": exp_folder, "calibration_subfolder": calibration_subfolder, "voltages_subfolder": voltages_subfolder, 'voltages_analog_subfolder': voltages_analog_subfolder, 'flow_subfolder': flow_subfolder, 'pressure_ramp_subfolder': pressure_ramp_subfolder, 'micro_flow_flg_subfolder': micro_flow_flg_subfolder,
                   "total_seconds": total_seconds, "total_time": total_time, "calibration_time_s": calibration_time_s, 'master_folder_path': master_folder_path, 'buffer_size_megabytes': buffer_size_megabytes, 'analog_sample_rate': analog_sample_rate, 'sls_interval': sls_interval, 'zigzag': zigzag, 'nb_big_ramp_controller': nb_big_ramp_controller}

# Save the dictionary to a JSON file in folder_path
with open(path_to_save_parameters, "w") as json_file:
    json.dump(parameters_dict, json_file)
print("Parameters Dictionary saved as JSON in 'parameters.json'")
json_string = json.dumps(parameters_dict)

# Replace these with the paths to your three Python scripts
script1_path_saleae = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\Saleae.py"
script2_path_sls = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\SLS_1500.py"
script3_path_push_pull = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\Push_Pull_Pressure.py"

# Define a function to run the scripts and pass json file as arguments to each script


def run_script(script_path):
    process = subprocess.Popen(["python", script_path, json_string])
    return process


def close_script(process):
    process.communicate()
    process.kill()


if sls_calibration_flag:
    print("Calibration started")
    process2 = run_script(script2_path_sls)
    close_script(process2)
else:
    print('Experiment started')
    # Start each script in a separate process
    process1_saleae = run_script(script1_path_saleae)
    process2_sls = run_script(script2_path_sls)
    process3_push_pull = run_script(script3_path_push_pull)

    close_script(process1_saleae)
    close_script(process2_sls)
    close_script(process3_push_pull)