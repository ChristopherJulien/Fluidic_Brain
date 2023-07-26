import subprocess
import sys
import json
import os

#Parameters to manually set
calibration_flag = False
nb_controllers = 1
Lstring = '30cm'
IDstring = '3-32'
check_valve_type = 'tube'

plateau_time = 30
Pstart = 0
# Pmax = 300
Pmax = 30
Pmin = -int(Pmax / 4)
# num_steps = 20
num_steps = 2
step_size = int((Pmax - Pmin) / num_steps)
h_init_cm = '8.5cm'
vl_init   = '1000mL'
exp_folder = 'node_tube_{:s}_ID_{:s}_{:s}_node_h_init{:s}_vl_init{:s}/'.format(Lstring, IDstring, check_valve_type,h_init_cm,vl_init)
calibration_subfolder = r'calibration'
calibration_time_s = 30
voltages_subfolder = r'voltages'
voltages_analog_subfolder = r'voltages/analog_voltages'
flow_subfolder = r'flow'

#Setup Folder
master_folder_path = os.path.abspath(os.getcwd()) + r"/"+exp_folder
print(master_folder_path)

# Check if the folder already exists before creating it
if not os.path.exists(master_folder_path):
    os.mkdir(master_folder_path)
    calibration_subfolder_path =os.path.join(master_folder_path, calibration_subfolder)
    voltages_subfolder_path = os.path.join(master_folder_path, voltages_subfolder)
    voltages_analog_subfolder_path = os.path.join(master_folder_path, voltages_analog_subfolder)
    flow_subfolder_path = os.path.join(master_folder_path, flow_subfolder)
    print("Folder created successfully.")
else:
    print("Folder already exists.")

dict_name = r"\parameters.json"
path_to_save_parameters = master_folder_path+ dict_name

#Calculate total time
nstep_up1 = int((Pmax - Pstart)/step_size)+1
max_p = Pstart + step_size*(nstep_up1-1)
nstep_down1 = int((max_p - Pmin)/step_size)
min_p = max_p - step_size*(nstep_down1)
nstep_up2 = - nstep_up1 + nstep_down1+1
total_seconds = plateau_time* (nstep_up1 + nstep_down1 + nstep_up2)
total_mins = total_seconds // 60
total_time = '{:d}mins{:d}s'.format(total_mins, total_seconds % 60)
print('Total Time: '+total_time)

parameters_dict = {"calibration_flag" : calibration_flag, "nb_controllers": nb_controllers, "IDstring": IDstring, "Lstring": Lstring,
                    "check_valve_type": check_valve_type, "plateau_time": plateau_time, "Pstart": Pstart, "Pmax": Pmax, "Pmin": Pmin, "num_steps": num_steps, "step_size": step_size, "h_init_cm": h_init_cm, "vl_init_mL": vl_init,
                      "exp_name": exp_folder, "calibration_subfolder":calibration_subfolder, "voltages_subfolder": voltages_subfolder, 'voltages_analog_subfolder':voltages_analog_subfolder,'flow_subfolder':flow_subfolder,
                      'total_seconds':total_seconds ,"total_time": total_time, "calibration_time_s": calibration_time_s,'master_folder_path':master_folder_path}

# Save the dictionary to a JSON file in folder_path
with open(path_to_save_parameters, "w") as json_file:
    json.dump(parameters_dict, json_file)
print("Parameters Dictionary saved as JSON in 'parameters.json'")
json_string = json.dumps(parameters_dict)

# Replace these with the paths to your three Python scripts
script1_path = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\Saleae.py"
script2_path = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\SLS_1500.py"
script3_path = r"C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\Push_Pull_Pressure.py"

# Define a function to run the scripts and pass json file as arguments to each script
def run_script(script_path):
    process = subprocess.Popen(["python", script_path,json_string])
    return process

def close_script(process):
    process.communicate()
    process.kill()    

if calibration_flag:
    print("Calibration started")
    process2 = run_script(script2_path)    
    close_script(process2)
else:
    print('Experiment started')
    # Start each script in a separate process
    process3 = run_script(script3_path)
    process1 = run_script(script1_path)
    process2 = run_script(script2_path)

    close_script(process3)
    close_script(process1)
    close_script(process2)

