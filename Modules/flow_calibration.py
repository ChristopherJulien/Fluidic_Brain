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
from Plot_Client import *

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
    SLS1500_flag = True
    syringe_name = "B"
    syringe_volume = "5" # mL
    syringe_type = "bdp"
    runtime_s = 10  # Set the runtime value to 10 seconds
    # start_value = np.array([-2.0])  # First value of appended to flow rates in mL/min
    flow_range = np.arange(0, 20.1, 2.0)  # Flow Rate ranges and step size in mL/min
    # end_value = np.array([2.0])  # First value of appended to flow rates in mL/min

    # pump_flow_rates = np.hstack((start_value, flow_range,end_value)) * 1000  # Concatenate x1 and x2 arrays, then multiply by 1000 (ul/min)
    pump_flow_rates = flow_range*1000
    pump_flow_rates = pump_flow_rates[::-1]
    print("FLow Rates [uL/min]: {}".format(pump_flow_rates))
    volume = abs(pump_flow_rates )* runtime_s / (60*1000)  # Calculate the volume based on pump flow rates and runtime (ml)
    vtot = np.sum(volume)  # Calculate the total volume by summing all elements in the volume array
    minutes_tot = (len(pump_flow_rates) * runtime_s + len(pump_flow_rates)) //60
    seconds_tot =(len(pump_flow_rates) * runtime_s + len(pump_flow_rates)) %60 
    print("Total volume {:.2f} mL".format(vtot))  # Print the total volume (ml 
    print("Total time: {}mins {}s".format(minutes_tot,seconds_tot))  # Print the total volume (ml

    if int(syringe_volume) < vtot:
        print("Total volume {:.2f}mL exceeds syringe volume {}mL".format(vtot,syringe_volume))
        sys.exit()

    input_dic = {"SLS1500_flag":SLS1500_flag,"syringe_name":syringe_name,"syringe_volume":syringe_volume,"syringe_type":syringe_type,"runtime_s":runtime_s,"pump_flow_rates":pump_flow_rates.tolist(),"vtot":vtot,"minutes_tot":minutes_tot,"seconds_tot":seconds_tot}
    output_folder = os.path.join(os.getcwd(),"output")
    # create_folder(output_folder)
    json_file = os.path.join("Parameters.json")
    with open(json_file, 'w') as fp:
        json.dump(input_dic, fp)
        
    syringe = Syringe(syringe_name, syringe_volume, syringe_type=syringe_type)  # Create a Syringe object with syringe number 'a', volume '10 ml', and plastic type 'bdp'
    pump = Pump(syringe_name, "COM5", syringe1=syringe)  # Create a Pump object with pump number 'B', connected to serial port 'COM', and using syringeB
    pump.stop()  # Stop the pump before performing any operations

    if SLS1500_flag:
        port = ShdlcSerialPort(port='COM3', baudrate=115200)  # Create a serial port object for communication on port 'COM3' with baudrate 115200
        flow_meter = SLS_1500Device(ShdlcConnection(port), slave_address=0)  # Create a flow meter device using the ShdlcConnection and the port, with a slave address of 0
        # experiment(flow_rates=pump_flow_rates, pump=pump, syringe=syringe, runtime=runtime_s, flow_meter=flow_meter)
    
    else:
        microFlowMeter = MicroFlowMeter()
        # experiment(flow_rates=pump_flow_rates, pump=pump, syringe=syringe, runtime=runtime_s, flow_meter=microFlowMeter, SL1500_flag=False)
    pump.stop()  # Stop the pump after the experiment is completed
   
    # plot = Plot(SLS1500_flag)
    # plot.flow_rate_over_time()
    # plot.q_vs_qs_and_relative_error()
    