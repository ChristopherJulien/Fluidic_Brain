# Need the salea to record the pressures and then to plot them with the corresponding prssurs
# take into account the downsample ratio and the datasheet of the pressure sensor (play to see if you can reduce the sampling )
# Have a file saving strucutre to how the experiments will be conducted
# Maybe talk to Anne about the specific pickle structures for that

# Need also to control the fluigent to get the corresponding pressure on the pressure ramp 
from Push_Pull_Pressure import *

def experiment_single_cycle(dict):
    nb_controllers = dict["nb_controllers"]
    file_string = dict["file_string"]
    plateau_time = dict["plateau_time"]
    max_p = dict["Pmax"]
    min_p = dict["Pmin"]
    step_size = dict["step_size"]

    ramp = PP_Pressure(nb_controllers,file_string)
    with Pressure_Controller(nb_controllers=ramp.nb_controllers):
        
        nstep_up1 = int((max_p - start_p)/step_size)+1
        max_p = start_p + step_size*(nstep_up1-1)
        nstep_down1 = int((max_p - min_p)/step_size)
        min_p = max_p - step_size*(nstep_down1)
        nstep_up2 = - nstep_up1 + nstep_down1+1
        
        # print(max_p, min_p, nstep_up2)
        # nstep_down = 1
        # nstep_up2 = 1
        ramp.perform_one_ramp_one_controller(
            start_p=start_p, end_p=max_p, nb_steps=nstep_up1, plateau_time=plateau_time
        )
        ramp.perform_one_ramp_one_controller(
            start_p=max_p-step_size, end_p=min_p, nb_steps=nstep_down1, plateau_time=plateau_time
        )
        ramp.perform_one_ramp_one_controller(
            start_p=min_p + step_size, end_p=0, nb_steps=nstep_up2, plateau_time=plateau_time
        )
        ramp.create_json_file()
        print(ramp.inputs_list)
        ramp.plot_intputs()

# Coarse Parameters
coarse_parameters = {
    "Nb_controllers": 1,
    "IDstring": '3-16',
    "Lstring": '30',
    "check_valve_type": 'cv3',
    "plateau_time": 30,
    'Pstart': 0,
    "Pmax":700,
    "Pmin": -int(Pmax/4),
    "step_size": int((Pmax-Pmin)/20.),
    "file_string": './node_tube_{:s}cm_ID_{:s}_{:s}_node_coarse/input_ramp'.format(Lstring, IDstring, check_valve_type)
}

# Fine Parameters
fine_parameters = {
    "Nb_controllers": 1,
    "IDstring": "3-16",
    "Lstring": '30',
    "check_valve_type": "cv3",
    "plateau_time": 30,
    'Pstart': 0,
    "Pmax":40,
    "Pmin": -40,
    "step_size": int((Pmax-Pmin)/20.),
    "file_string": './node_tube_{:s}cm_ID_{:s}_{:s}_node_coarse/input_ramp'.format(Lstring, IDstring,check_valve_type)
}

# Accessing values using keys
# print(my_dict["name"])           # Output: John
# coarse_parameters[IDstring]

if __name__=="__main__":
    
    experiment_single_cycle(coarse_parameters) 
    # experiment_single_cycle(fine_parameters) 