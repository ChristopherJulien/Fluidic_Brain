import threading
import Saleae
import SLS_1500
import Push_Pull_Pressure
import subprocess
import sys
import json
import os

# Parameters to manually set
sls_calibration_flag = False
nb_controllers = 1
Lstring = '30cm'
IDstring = '3-16'
check_valve_type = 'cv3'

# Pressure Parameters
plateau_time = 30
Pstart = 0
Pmax = 600
Pmin = -Pmax
# step_size = int((Pmax - Pmin) / 20.)
step_size = 200
h_init_cm = '8.5cm'
vl_init = '1000mL'
# exp_folder = 'node_tube_{:s}_ID_{:s}_{:s}_node_h_init{:s}_vl_init{:s}/'.format(Lstring, IDstring, check_valve_type,h_init_cm,vl_init)
# exp_folder = ('A_II_plateau_time_{:d}_p_start_{:d}_p_max_{:d}_p_min{:d}_step_size_{:d}'.format(plateau_time, Pstart, Pmax, Pmin, step_size))
# exp_folder = ('TEST_plateau_time_s_{:d}_p_start_{:d}_p_max_{:d}_p_min{:d}_step_size_{:d}'.format(plateau_time, Pstart, Pmax, Pmin, step_size))
exp_folder = ('CV1-PVC-1_8-30cm-GLYCEROL-plateau_time_s_{:d}_p_start_{:d}_p_max_{:d}_p_min{:d}_step_size_{:d}'.format(
    plateau_time, Pstart, Pmax, Pmin, step_size))
calibration_time_s = 30
calibration_subfolder = r'calibration_saleae'
voltages_subfolder = r'voltages_saleae'
voltages_analog_subfolder = voltages_subfolder + r'/analog_voltages'
flow_subfolder = r'flow_sls'
pressure_ramp_subfolder = r'pressure_ramp_flg'
micro_flow_flg_subfolder = r'micro_flow_flg'

buffer_size_megabytes = 15000
analog_sample_rate = 3125000

# Setup Folder
master_folder_path = os.path.abspath(os.getcwd()) + r"/"+exp_folder

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
nstep_up1 = int((Pmax - Pstart)/step_size)+1
max_p = Pstart + step_size*(nstep_up1-1)
nstep_down1 = int((max_p - Pmin)/step_size)
min_p = max_p - step_size*(nstep_down1)
nstep_up2 = - nstep_up1 + nstep_down1+1
total_seconds = plateau_time * (nstep_up1 + nstep_down1 + nstep_up2)
total_mins = total_seconds // 60
total_time = '{:d}mins{:d}s'.format(total_mins, total_seconds % 60)
print('Total Time: '+total_time)

parameters_dict = {"calibration_flag": sls_calibration_flag, "nb_controllers": nb_controllers, "IDstring": IDstring, "Lstring": Lstring,
                   "check_valve_type": check_valve_type, "plateau_time": plateau_time, "Pstart": Pstart, "Pmax": Pmax, "Pmin": Pmin, "step_size": step_size, "h_init_cm": h_init_cm, "vl_init_mL": vl_init,
                   "exp_name": exp_folder, "calibration_subfolder": calibration_subfolder, "voltages_subfolder": voltages_subfolder, 'voltages_analog_subfolder': voltages_analog_subfolder, 'flow_subfolder': flow_subfolder, 'pressure_ramp_subfolder': pressure_ramp_subfolder, 'micro_flow_flg_subfolder': micro_flow_flg_subfolder,
                   'total_seconds': total_seconds, "total_time": total_time, "calibration_time_s": calibration_time_s, 'master_folder_path': master_folder_path, 'buffer_size_megabytes': buffer_size_megabytes, 'analog_sample_rate': analog_sample_rate}

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
    process3_push_pull = run_script(script3_path_push_pull)
    process1_saleae = run_script(script1_path_saleae)
    process2_sls = run_script(script2_path_sls)

    close_script(process3_push_pull)
    close_script(process1_saleae)
    close_script(process2_sls)
