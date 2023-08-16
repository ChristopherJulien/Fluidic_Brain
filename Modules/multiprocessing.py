import threading
import Saleae
import SLS_1500
import Push_Pull_Pressure

Lstring = '30cm'
IDstring = '3-16'
check_valve_type = 'cv3'

# Pressure Coarse Parameters
Pmax = 180
Pmin = 0
step_size = int((Pmax - Pmin) / 20.)
plateau_time = 5
# plateau_time = 30
# exp_folder = 'node_tube_{:s}_ID_{:s}_{:s}_node_coarse/'.format(Lstring, IDstring, check_valve_type)
exp_folder = ('Actuator_in_water_test_0_180')
voltages_path = r'output/analog_voltages'
pressure_path = r'output/analog_pressures'

coarse_parameters = {
    "nb_controllers": 1,
    "IDstring": IDstring,
    "Lstring": Lstring,
    "check_valve_type": check_valve_type,
    "plateau_time": plateau_time,
    'Pstart': 50,
    "Pmax": Pmax,
    "Pmin": Pmin,
    "step_size": step_size,
    "exp_name": exp_folder,
}

total_seconds = plateau_time * step_size
total_mins = total_seconds // 60
print("Total Duration: {}mins {}s".format(total_mins, total_seconds % 60))

if __name__ == "__main__":
    # Create master test folder
    master_folder_path = coarse_parameters['master_folder_path']

    # Create threads for each script
    push_pull_pressure = threading.Thread(
        target=Push_Pull_Pressure.process_push_pull_pressure(coarse_parameters))
    # sls_thread = threading.Thread(target=SLS_1500.process_sls_1500(
    #     total_seconds=total_seconds, file_name=exp_folder))
    # saleae_thread = threading.Thread(target=Saleae.process_saleae(
    #     exp_folder, voltages_path, pressure_path, total_seconds))

    # Start the threads
    # saleae_thread.start()
    # sls_thread.start()
    push_pull_pressure.start()

    # Wait for all threads to finish
    # saleae_thread.join()
    # sls_thread.join()
    push_pull_pressure.join()

    print("All scripts processed.")
