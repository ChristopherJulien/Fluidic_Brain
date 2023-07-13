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

if __name__=="__main__":
    SLS1500_flag = False
    syringe_name = "B"
    syringe_volume = "1"
    syringe_type = "bdp"
    runtime_s = 10  # Set the runtime value to 10 seconds
    x1 = np.array([0.0])  # First value of appended to flow rates in mL/min
    x2 = np.arange(0.01, 0.11, 0.01)  # Flow Rate ranges and step size in mL/min
    pump_flow_rates = np.hstack((x1, x2)) * 1000  # Concatenate x1 and x2 arrays, then multiply by 1000 (ul/min)
    pump_flow_rates = pump_flow_rates[::-1]
    print("FLow Rates [uL/min]: {}".format(pump_flow_rates))
    input_dic = {"SLS1500_flag":SLS1500_flag,"syringe_name":syringe_name,"syringe_volume":syringe_volume,"syringe_type":syringe_type,"runtime_s":runtime_s,"pump_flow_rates":pump_flow_rates.tolist()}
    output_folder = os.path.join(os.getcwd(),"output")
    create_folder(output_folder)
    json_file = os.path.join(output_folder,"input.json")
    with open(json_file, 'w') as fp:
        json.dump(input_dic, fp)
    
    sys.exit()

    volume = pump_flow_rates * runtime_s / (60*1000)  # Calculate the volume based on pump flow rates and runtime (ml)
    vtot = np.sum(volume)  # Calculate the total volume by summing all elements in the volume array
    minutes_tot = len(pump_flow_rates) * runtime_s //60
    seconds_tot =len(pump_flow_rates) * runtime_s %60
    print("Total volume {:.2f} ".format(vtot))  # Print the total volume (ml 
    print("Total time: {}mins {}s".format(minutes_tot,seconds_tot))  # Print the total volume (ml

    # syringeA = Syringe("A", '60', 'bdp')  # Create a Syringe object with syringe number 'a', volume '10 ml', and plastic type 'bdp'
    syringeB = Syringe("B", '1', 'bdp')  # Create a Syringe object with syringe number 'b', volume '10 ml', and plastic type 'bdp'

    # pumpA = Pump("A", "COM5", syringe1=syringeA)  # Create a Pump object with pump number 'A', connected to serial port 'COM5', and using syringeA
    pumpB = Pump("B", "COM5", syringe1=syringeB)  # Create a Pump object with pump number 'B', connected to serial port 'COM', and using syringeB
    
    # pumpA.stop()  # Stop the pump before performing any operations
    pumpB.stop()  # Stop the pump before performing any operations


    if SLS1500_flag:
        port = ShdlcSerialPort(port='COM3', baudrate=115200)  # Create a serial port object for communication on port 'COM3' with baudrate 115200
        flow_meter = SLS_1500Device(ShdlcConnection(port), slave_address=0)  # Create a flow meter device using the ShdlcConnection and the port, with a slave address of 0
        # Call the experiment function with the specified parameters
        # experiment(flow_rates=pump_flow_rates, pump=pumpA, syringe=syringeA, runtime=runtime, flow_meter=flow_meter)
    
    else:
        microFlowMeter = MicroFlowMeter()
        experiment(flow_rates=pump_flow_rates, pump=pumpB, syringe=syringeB, runtime=runtime_s, flow_meter=microFlowMeter, SL1500_flag=False)

    # pumpA.stop()  # Stop the pump after the experiment is completed
    pumpB.stop()  # Stop the pump after the experiment is completed
    
    
    plot = Plot(SLS1500_flag)
    plot.flow_rate_over_time()
    plot.q_vs_qs_and_relative_error()
    


    


