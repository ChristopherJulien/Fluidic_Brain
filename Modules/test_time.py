calibration_flag = False
micro_flag = False
nb_controllers = 2
plateau_time = 18 if not calibration_flag else 10

start_p1 = 0 if not calibration_flag else 0
max_p1 = 200 if not calibration_flag else 10
nb_steps1 = 25 if not calibration_flag else 10
# or by number of steps: step_size = int((Pmax - Pmin) / 20.)

start_p2 = 0 if not calibration_flag else 0
max_p2 = 200 if not calibration_flag else 10
nb_steps2 = 25 if not calibration_flag else 10

zigzag: bool = False
nb_big_ramp_controller: int = 1


# Saleae Parameters
buffer_size_megabytes = 20000
analog_sample_rate = 781250

# Documenting Parameters
Lstring = ''
IDstring = ''
check_valve_type = ''
h_init_cm = ''
vl_init = ''

if nb_controllers == 2:
    possible_p1 = ((max_p1-start_p1)/nb_steps1) + 1
    possible_p2 = ((max_p2-start_p2)/nb_steps2) + 1
    all_steps = possible_p1*possible_p2
    total_seconds = all_steps*plateau_time
    total_mins = total_seconds // 60
    total_time = '{:.0f}mins{:d}s'.format(total_mins, int(total_seconds) % 60)
    print('Total Time: '+total_time)
    print('Total Seconds: '+str(total_seconds))
