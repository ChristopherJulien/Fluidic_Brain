from Digitizer_Client import *
from syringe_control import *
import SLS_1500 as flow_client
def create_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def experiment(flow_rates,digitizer,channels,pump,syringe,path,runtime=60,run_backward=False):
    if not run_backward:
        for fl in flow_rates:
            experiment_name = "flow_rate_forward_"+str(fl).zfill(4)+"_ul_min"
            digitizer.capture_start()
            flow_client()
            pump.inject(syringe, fl, runtime,"ul/min")
            time.sleep(runtime)
            pump.stop()
            # flow_sensor_stop()    
            digitizer.capture_stop()
            while not digitizer.is_processing_complete():
                time.sleep(1)
            file_saving = experiment_name+".logicdata"
            digitizer.save_to_file(path + file_saving)
            file_saving = experiment_name + ".csv"
            digitizer.export_data2(path + file_saving, digital_channels=channels[0], analog_channels=channels[1])
            time.sleep(1)
            ans = 'o'
            while ans.lower()!="y":
                print("Open Valve")
                ans = input("Are you done?")
    else:
        for fl in flow_rates:
            flw = -1*fl
            experiment_name = "flow_rate_backward_" + str(fl).zfill(4) + "_ul_min"
            digitizer.capture_start()
            pump.inject(syringe, flw, runtime,"ul/min")
            time.sleep(runtime)
            pump.stop()
            digitizer.capture_stop()
            while not digitizer.is_processing_complete():
                time.sleep(1)
            file_saving = experiment_name + ".logicdata"
            digitizer.save_to_file(path + file_saving)
            file_saving = experiment_name + ".csv"
            digitizer.export_data2(path + file_saving, digital_channels=channels[0], analog_channels=channels[1])
            time.sleep(1)
            ans = 'o'
            while ans.lower() != "y":
                print("Open Valve")
                ans = input("Are you done?")


if __name__=="__main__":
    path="D:/fluidic_network/valve_colepalmer_30s_4/"
    create_folder(path)
    pump_flow_rates = [10,20,50,100,200,500,1000,2000,5000]
    runtime = 60
    digitizer,channels = init_client(mode="analog",analog_sample_rate=5000,capture_time=runtime)
    syringeA = Syringe("a", '1', 'bdp')
    pump = Pump("A", "COM5", syringe1=syringeA)
    pump.stop()
    experiment(flow_rates=pump_flow_rates,digitizer=digitizer,channels=channels,pump=pump,syringe=syringeA,path=path,runtime=runtime)
    digitizer.exit()
    pump.stop()

