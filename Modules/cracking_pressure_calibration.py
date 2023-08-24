from Push_Pull_Pressure import *
from SLS_1500 import *
from Saleae import *
from datetime import datetime

Lstring = '30cm'
IDstring = '3-16'
check_valve_type = 'cv3'

# Pressure Coarse Parameters
Pmax = 700
Pmin = -int(Pmax / 4)
step_size = int((Pmax - Pmin) / 20.)
plateau_time = 2
# plateau_time = 30
exp_folder = 'node_tube_{:s}_ID_{:s}_{:s}_node_coarse/'.format(
    Lstring, IDstring, check_valve_type)
voltages_path = r'output/analog_voltages'
pressure_path = r'output/analog_pressures'


total_seconds = plateau_time * step_size
total_mins = total_seconds // 60
print("Total Duration: {}mins {}s".format(total_mins, total_seconds % 60))
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

# Pressure Fine Parameters
fine_parameters = {
    "nb_controllers": 1,
    "IDstring": IDstring,
    "Lstring": Lstring,
    "check_valve_type": check_valve_type,
    "plateau_time": 30,
    'Pstart': 0,
    "Pmax": 40,
    "Pmin": -40,
    "step_size": int((Pmax-Pmin)/20.),
    "file_string": './node_tube_{:s}_ID_{:s}_{:s}_node_fine/input_ramp'.format(Lstring, IDstring, check_valve_type)
}

if __name__ == "__main__":
    pass

    # FLUIGENT Push Pull Pressure
    # pressure_control = PP_Pressure(coarse_parameters["nb_controllers"], coarse_parameters["file_string"])
    # pressure_control.experiment_single_cycle(coarse_parameters)

    # SLS_1500 Flow Meter
    # port = ShdlcSerialPort(port='COM3', baudrate=115200)  # Create a serial port object for communication on port 'COM3' with baudrate 115200
    # flow_meter = SLS_1500Device(ShdlcConnection(port), slave_address=0)  # Create a flow meter device using the ShdlcConnection and the port,
    # flow_meter.Continuous_Measure_and_Save(duration_s=total_seconds, set_flow_rate_string=None,)

    # SALEAE Logic Analyzer
    # logic_capture = LogicCapture(duration_seconds=total_seconds)
    # logic_capture = LogicCapture(5)
    # analog_voltages = os.path.join(os.getcwd(), exp_folder + voltages_path)
    # logic_capture.start_capture(analog_voltages)
    # analog_pressures = os.path.join(os.getcwd(), exp_folder + pressure_path)
    # logic_capture.process_csv(r'C:\Users\Julien\OneDrive - Harvard University\Documents\Fluidic_Brain\Modules\node_tube_30cm_ID_3-16_cv3_node_coarse\output\analog_voltages\analog.csv',
    #                            analog_pressures)
