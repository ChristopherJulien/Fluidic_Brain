import threading
import Saleae
import SLS_1500
import Push_Pull_Pressure
import subprocess
import sys
import json
import os

# Calibration
calibration_flag = 0
micro_flag = True
sls_flag = True
calibration_folder = 'Calibration_' if calibration_flag else ''

# Saleae Parameters
buffer_size_megabytes = 16000
analog_sample_rate = 781250  # analog_sample_rate = 781250 , :1562500 , 3125000

# SLS Parameters
sls_interval = "\x00\x64"  # recording interaval 100ms

# Pressure Parameters
nb_controllers = 1
calibration_time = 30
plateau_time = 30

# First Ramp
p1 = 0
p2 = 45
p3 = 55
p4 = 205
stp1 = 5
stp2 = 1
stp3 = 15


# Documenting Parameters
check_valve_type = '2'
tubeLength = '20cm'
exp_folder = '{:s}CV{:s}-20cm'.format(
    calibration_folder, check_valve_type)
print(exp_folder)

# ~~~~~~~~~~~~~~~~~~~~~~  Experiment Parameters ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Folder names and paths
master_folder_path = os.path.abspath(os.getcwd()) + r"/"+exp_folder
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

# Calculate total time
ramp1 = int((p2-p1)/stp1)+1
ramp2 = int((p3-p2)/stp2)+1
ramp3 = int((p4-p3)/stp3)+1
if calibration_flag:
    total_seconds = calibration_time
else:
    total_seconds = plateau_time * (ramp1+ramp2+ramp3)
total_mins = total_seconds // 60
total_time = '{:d}mins{:d}s'.format(total_mins, total_seconds % 60)
print('Total Time: '+total_time)

# Create a dictionary with all the parameters
parameters_dict = {
    "micro_flag": micro_flag,
    "calibration_flag": calibration_flag,
    "nb_controllers": nb_controllers,
    "check_valve_type": check_valve_type,
    "exp_name": exp_folder,
    "calibration_subfolder": calibration_subfolder,
    "voltages_subfolder": voltages_subfolder,
    'voltages_analog_subfolder': voltages_analog_subfolder,
    'flow_subfolder': flow_subfolder,
    'pressure_ramp_subfolder': pressure_ramp_subfolder,
    'micro_flow_flg_subfolder': micro_flow_flg_subfolder,
    "total_seconds": total_seconds,
    "total_time": total_time,
    'master_folder_path': master_folder_path,
    'buffer_size_megabytes': buffer_size_megabytes,
    'analog_sample_rate': analog_sample_rate,
    'sls_interval': sls_interval,
    "p1": p1,
    "p2": p2,
    "p3": p3,
    "p4": p4,
    "stp1": stp1,
    "stp2": stp2,
    "stp3": stp3,
    "plateau_time": plateau_time
}

# Save the dictionary to a JSON file in folder_path
with open(path_to_save_parameters, "w") as json_file:
    json.dump(parameters_dict, json_file)
print("Parameters Dictionary saved as JSON in 'parameters.json'")
json_string = json.dumps(parameters_dict)

# Replace these with the paths to your three Python scripts
script1_path_saleae = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\Saleae.py"
script2_path_sls = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\SLS_1500.py"
script3_path_push_pull = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\Push_Pull_One_ramp.py"
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
    calib_saleae = run_script(script1_path_saleae)
    calib_sls = run_script(script2_path_sls)
    calib_uflow = run_script(script4_path_micro_flow)
    close_script(calib_saleae)
    close_script(calib_sls)
    close_script(calib_uflow)
elif calibration_flag == False:
    print('Experiment started')
    # Start each script in a separate process
    exp_saleae = run_script(script1_path_saleae)
    exp_sls = run_script(script2_path_sls)
    exp_uflow = run_script(script4_path_micro_flow)
    exp_push_pull = run_script(script3_path_push_pull)
    close_script(exp_saleae)
    close_script(exp_sls)
    close_script(exp_uflow)
    close_script(exp_push_pull)
