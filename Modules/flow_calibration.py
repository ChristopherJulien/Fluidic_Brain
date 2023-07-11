# from Digitizer_Client import *
from syringe_control import *
def create_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)
from sls_1500 import *
from Microflowsensor import *

def experiment(flow_rates,pump,syringe,runtime=None,flow_meter=None,SL1500_flag=True):
    assert flow_meter is not None, "Flow meter not connected"

    for fl in flow_rates:
        experiment_name = str(fl).zfill(4)
        print(experiment_name)
        pump.inject(syringe, fl, runtime,"ul/min")
        if SL1500_flag:
            flow_meter.Continuous_Measure_and_Save(duration_s=runtime,  plot=False, flow_rate_string=experiment_name)
        else:
            flow_meter.get_continuous_flowrate(duration=runtime,interval=0.1, flow_rate_string=experiment_name,save_data=True)
        pump.stop()
        time.sleep(1) # Pause execution for 1 second

if __name__=="__main__":
    SL1500_flag = True

    x1 = np.array([15.])  # Create a NumPy array with a single value 0.1
    x2 = np.arange(16.0, 21., .5)  # Create a NumPy array with values ranging from 100uL to 2ml (inclusive) with a step of 100uL
    pump_flow_rates = np.hstack((x1, x2)) * 1000  # Concatenate x1 and x2 arrays, then multiply by 1000 (ul/min)
    pump_flow_rates = pump_flow_rates[::-1]
    print(pump_flow_rates)

    runtime = 10  # Set the runtime value to 10 seconds
    volume = pump_flow_rates * runtime / (60*1000)  # Calculate the volume based on pump flow rates and runtime (ml)
    vtot = np.sum(volume)  # Calculate the total volume by summing all elements in the volume array
    print("Total volume {:.2f} mL ".format(vtot))  # Print the total volume (ml 

    syringeA = Syringe("A", '30', 'bdp')  # Create a Syringe object with syringe number 'a', volume '10 ml', and plastic type 'bdp'
    # syringeB = Syringe("B", '10', 'bdp')  # Create a Syringe object with syringe number 'b', volume '10 ml', and plastic type 'bdp'

    pumpA = Pump("A", "COM5", syringe1=syringeA)  # Create a Pump object with pump number 'A', connected to serial port 'COM5', and using syringeA
    # pumpB = Pump("B", "COM5", syringe1=syringeB)  # Create a Pump object with pump number 'B', connected to serial port 'COM', and using syringeB
    
    pumpA.stop()  # Stop the pump before performing any operations
    # pumpB.stop()  # Stop the pump before performing any operations


    if SL1500_flag:
        port = ShdlcSerialPort(port='COM3', baudrate=115200)  # Create a serial port object for communication on port 'COM3' with baudrate 115200
        flow_meter = SLS_1500Device(ShdlcConnection(port), slave_address=0)  # Create a flow meter device using the ShdlcConnection and the port, with a slave address of 0
        # Call the experiment function with the specified parameters
        experiment(flow_rates=pump_flow_rates, pump=pumpA, syringe=syringeA, runtime=runtime, flow_meter=flow_meter)
    
    else:
        microFlowMeter = MicroFlowMeter()
        # experiment(flow_rates=pump_flow_rates, pump=pumpB, syringe=syringeB, runtime=runtime, flow_meter=microFlowMeter, SL1500_flag=False)

    pumpA.stop()  # Stop the pump after the experiment is completed
    # pumpB.stop()  # Stop the pump after the experiment is completed

    


