from Modules.syringe_control import *
from Modules.saleae_digitizer_v2 import *
import numpy as np
import time
import os
import json
import sys

def create_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def experiment(flow_rates,pump,syringe,digitizer,runtime, wait_time=1):
    digitizer.capture_data()        
    for fl in flow_rates:
        pump.inject(syringe, fl, runtime,"ul/min")
        time.sleep(runtime)
        pump.stop()
        time.sleep(wait_time) # Pause execution for 1 second
    digitizer.export_data3()
    
if __name__=="__main__":
    #User manual input
    channel_number = 1
    #Define flow rates in ul/min
    x1 = [0.01,0.02,0.05,0.1]
    x2 = [0.2,0.5,1., 2.]# Create a NumPy array with values ranging from 0.5 to 10 (inclusive) with a step of 0.5
    path_experiment = r"G:\Shared drives\Bertoldi Group Drive\Projects\Fluidic brain\Micro_channel_characterization\2023_08_18"
    runtime = 30  # Set the runtime value to 10 seconds
    waittime = 1 #stop between imposed flows
    pump_com = "COM9"
    syringeA = Syringe("a", '10', 'bdp')  # Create a Syringe object with syringe number 'a', volume '10 ml', and plastic type 'bdp'
    analog_channels_record = [0]
    saleae_device_id = "624C439C76D52E8B" #Find it by clicking on the 3 dots in logic software and then clicking on device info tab
    saleae_sample_rate = 781250
    #Experiment code

    pump_flow_rates = np.hstack((x1, x2)) * 1000  # Concatenate x1 and x2 arrays, then multiply by 1000 (ul/min)
    pump_flow_rates = pump_flow_rates[::-1]
    print(pump_flow_rates)
    volume = pump_flow_rates * runtime / (60*1000)  # Calculate the volume based on pump flow rates and runtime (ml)
    vtot = np.sum(volume)  # Calculate the total volume by summing all elements in the volume array
    print("total volume in mL ", vtot)  # Print the total volume (ml 
    # sys.exit()
    numsteps = len(pump_flow_rates)
    pump_flow_start_times = np.arange(0, numsteps)*(runtime+waittime)
    flowdict = {'pump_flow_rates_ulpmin': pump_flow_rates.tolist(),
                'pump_flow_start_times': pump_flow_start_times.tolist(),
                'runtime': runtime,
                'waittime': waittime}
    experiment_name = "Microfluidic_sweep_flowrate_"+str(np.min(pump_flow_rates)).zfill(4)+"ulpmin-"+str(np.max(pump_flow_rates)).zfill(4)+"ulpmin" + "_channel{:d}".format(channel_number)
    output_folder = os.path.join(path_experiment, experiment_name)
    create_folder(output_folder)

    jsonname = os.path.join(output_folder, 'imposed_flow_data.json')
    with open(jsonname, 'w') as fp:
        json.dump(flowdict, fp)

    # sys.exit()
    
    # Define pump
    pump = Pump("A", pump_com, syringe1=syringeA)  # Create a Pump object with pump number 'A', connected to serial port 'COM5', and using syringeA
    pump.stop()  # Stop the pump before performing any operations
    #Define saleae module
    digitizer= Digitizer(output_folder,saleae_device_id,sr = saleae_sample_rate, capture_duration=runtime*(pump_flow_rates.size+1),analog_channels=analog_channels_record)

    #Run experiment
    experiment(flow_rates=pump_flow_rates, pump=pump, syringe=syringeA, digitizer=digitizer, runtime=runtime, wait_time=waittime)
    pump.stop()  # Stop the pump after the experiment is completed
    pump.close()

