# from Digitizer_Client import *
from syringe_control import *
import os
import sys
import json
def create_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)
from SLS_1500 import *
from FLG_M_Plus import *
from Plot_Client import Plot

def experiment_name(Sls1500_flag,):
    pass

def experiment(flow_rates,pump,syringe,runtime=None,flow_meter=None,SL1500_flag=True):
    assert flow_meter is not None, "Flow meter not connected"

    for fl in flow_rates:
        flow_rate = str(fl).zfill(4)
        pump.inject(syringe, fl, runtime,"ul/min")
        
        if SL1500_flag:
            flow_meter.Continuous_Measure_and_Save(duration_s=runtime,  plot=False, flow_rate_string=flow_rate)
        else:
            flow_meter.get_continuous_flowrate(duration_s=runtime, interval=0.1, flow_rate_string=flow_rate,save_data=True)
        
        pump.stop()
        time.sleep(1) # Interval between experiments

# Glycerol Test
# --------------------
# SLS (Flow duration of 10 s-step)
# -20-2mL/min steps: 0.5mL/min
# FLG (Flow duration of  20 seconds)
# 0.1- 2 mL/min stps 0.1mL/min ! wil need a 1ml syringe which can be found on the fifth floor!)
# 0.01 0 0.1 ml/min stps 0.010 mL/min stps
# see if you can make a lookup table from qmeas and qset
# see if it can record forward and back flow and if so repeat the top test in the negative space
# EXTRA
# integrate the delta p (v) curve

if __name__=="__main__":
    SLS1500_flag = True
    syringe_name = "A"
    syringe_volume = "60"
    syringe_type = "bdp"
    runtime_s = 10  # Set the runtime value to 10 seconds
    start_value = np.array([-20.1])  # First value of appended to flow rates in mL/min
    flow_range = np.arange(-20, -8.1, 0.5)  # Flow Rate ranges and step size in mL/min
    end_value = np.array([-2.1])  # First value of appended to flow rates in mL/min
    pump_flow_rates = np.hstack((start_value, flow_range,end_value)) * 1000  # Concatenate x1 and x2 arrays, then multiply by 1000 (ul/min)
    pump_flow_rates = pump_flow_rates[::-1]
    print("FLow Rates [uL/min]: {}".format(pump_flow_rates))
    

    

    volume = pump_flow_rates * runtime_s / (60*1000)  # Calculate the volume based on pump flow rates and runtime (ml)
    vtot = np.sum(volume)  # Calculate the total volume by summing all elements in the volume array
    minutes_tot = len(pump_flow_rates) * runtime_s //60
    seconds_tot =len(pump_flow_rates) * runtime_s %60 + len(pump_flow_rates)
    print("Total volume {:.2f} mL".format(vtot))  # Print the total volume (ml 
    print("Total time: {}mins {}s".format(minutes_tot,seconds_tot))  # Print the total volume (ml

    input_dic = {"SLS1500_flag":SLS1500_flag,"syringe_name":syringe_name,"syringe_volume":syringe_volume,"syringe_type":syringe_type,"runtime_s":runtime_s,"pump_flow_rates":pump_flow_rates.tolist(),"vtot":vtot,"minutes_tot":minutes_tot,"seconds_tot":seconds_tot}
    output_folder = os.path.join(os.getcwd(),"output")
    # create_folder(output_folder)
    json_file = os.path.join("Parameters.json")
    with open(json_file, 'w') as fp:
        json.dump(input_dic, fp)

        
    syringeA = Syringe("A", '60', 'bdp')  # Create a Syringe object with syringe number 'a', volume '10 ml', and plastic type 'bdp'
    # syringeB = Syringe("B", '1', 'bdp')  # Create a Syringe object with syringe number 'b', volume '10 ml', and plastic type 'bdp'

    pumpA = Pump("A", "COM5", syringe1=syringeA)  # Create a Pump object with pump number 'A', connected to serial port 'COM5', and using syringeA
    # pumpB = Pump("B", "COM5", syringe1=syringeB)  # Create a Pump object with pump number 'B', connected to serial port 'COM', and using syringeB
    
    pumpA.stop()  # Stop the pump before performing any operations
    # pumpB.stop()  # Stop the pump before performing any operations


    if SLS1500_flag:
        port = ShdlcSerialPort(port='COM3', baudrate=115200)  # Create a serial port object for communication on port 'COM3' with baudrate 115200
        flow_meter = SLS_1500Device(ShdlcConnection(port), slave_address=0)  # Create a flow meter device using the ShdlcConnection and the port, with a slave address of 0
        # Call the experiment function with the specified parameters
        experiment(flow_rates=pump_flow_rates, pump=pumpA, syringe=syringeA, runtime=runtime_s, flow_meter=flow_meter)
    
    else:
        microFlowMeter = MicroFlowMeter()
        # experiment(flow_rates=pump_flow_rates, pump=pumpB, syringe=syringeB, runtime=runtime_s, flow_meter=microFlowMeter, SL1500_flag=False)

    pumpA.stop()  # Stop the pump after the experiment is completed
    # pumpB.stop()  # Stop the pump after the experiment is completed
    
    
    plot = Plot(SLS1500_flag)
    plot.flow_rate_over_time()
    plot.q_vs_qs_and_relative_error()
    


    


