import threading
import Saleae
import SLS_1500
import Push_Pull_Pressure

Lstring = '30cm'
IDstring = '3-16'
check_valve_type = 'cv3'

# Pressure Coarse Parameters
Pmax = 300
Pmin = -int(Pmax / 4)
step_size = int((Pmax - Pmin) / 20.)
plateau_time = 2
# plateau_time = 30
exp_folder = 'node_tube_{:s}_ID_{:s}_{:s}_node_coarse/'.format(Lstring, IDstring, check_valve_type)
voltages_path = r'output/analog_voltages'
pressure_path = r'output/analog_pressures'

coarse_parameters = {
    "nb_controllers": 1,
    "IDstring": IDstring,
    "Lstring": Lstring,
    "check_valve_type": check_valve_type,
    "plateau_time": plateau_time,
    'Pstart': 0,
    "Pmax": Pmax,
    "Pmin": Pmin,
    "step_size": step_size,
    "exp_name": exp_folder,
}

total_seconds = plateau_time* step_size
total_mins = total_seconds // 60
print("Total Duration: {}mins {}s".format(total_mins, total_seconds % 60))
if __name__ == "__main__":
    # Create threads for each script
    thread3 = threading.Thread(target=Push_Pull_Pressure.process_push_pull_pressure(coarse_parameters))
    thread2 = threading.Thread(target=SLS_1500.process_sls_1500(total_seconds=total_seconds,file_name=exp_folder))
    thread1 = threading.Thread(target=Saleae.process_saleae(exp_folder, voltages_path, pressure_path, total_seconds))

    # Start the threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for all threads to finish
    thread1.join()
    thread2.join()
    thread3.join()

    print("All scripts processed.")