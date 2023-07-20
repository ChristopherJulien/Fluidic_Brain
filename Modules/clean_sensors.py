# from Digitizer_Client import *
from syringe_control import *
import os
import sys
import json
import numpy as np

def clean(flow_rates,pump,syringe,runtime,cycles,SL1500_flag=True):
    counter=0
    while counter < cycles:
        for fl in flow_rates:
            pump.inject(syringe, fl, runtime,"ul/min")
            time.sleep(runtime) # Interval between experiments
            pump.stop()
        counter += 1
        print('Cycle: ',counter)

def volume_check_syringe(syring_volume, flow_rates, runtime):
    volume = syring_volume
    for fl in flow_rates:
        volume -= fl*runtime/60
    return volume
        

if __name__=="__main__":
    SLS1500_flag = True
    syringe_name = "B"
    syringe_volume = "30" # mL
    syringe_type = "bdp"
    runtime_s = 1.5*60  # Set the runtime value to 10 seconds    
    cycles = 25
    flow_range = np.arange(20.0,-20.1,-40.) # uL/min
    print(flow_range)
    
    pump_flow_rates = flow_range*1000
    syringe = Syringe(syringe_name, syringe_volume, syringe_type=syringe_type)  # Create a Syringe object with syringe number 'a', volume '10 ml', and plastic type 'bdp'
    pump = Pump(syringe_name, "COM5", syringe1=syringe)  # Create a Pump object with pump number 'B', connected to serial port 'COM', and using syringeB
    
    pump.stop()  # Stop the pump before performing any operations
    clean(pump_flow_rates,pump,syringe,runtime_s, cycles,SL1500_flag=SLS1500_flag)  # Run the experiment with the specified flow rates, pump, syringe, and runtime
    pump.stop()
    print('Done Cleaning')