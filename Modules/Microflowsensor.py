import time
import numpy as np
from Fluigent.SDK import fgt_init, fgt_close
from Fluigent.SDK import fgt_get_sensorChannelsInfo
from Fluigent.SDK import fgt_get_sensorUnit, fgt_get_sensorRange, fgt_get_sensorValue

## Initialize the session
# This step is optional, if not called session will be automatically created
fgt_init()


class MicroFlowMeter:
    def __init__(self):
        sensorInfoArray, sensorTypeArray = fgt_get_sensorChannelsInfo()
        self.flowmeter = sensorInfoArray
        self.unit = fgt_get_sensorUnit(0)
        self.minSensor, self.maxSensor = fgt_get_sensorRange(0)

    def get_single_flowrate():
        measurement = fgt_get_sensorValue(0)
        return measurement
    def get_continuous_flowrate(self, duration, interval, flow_rate_string, save_data=False):
        assert duration > 0
        assert interval > 0.05
        t_start = time.time()
        t_end = time.time() + duration
        flow_rate_list = []
        time_list = []
        
        flow_rate_string = float(flow_rate_string)
        flow_rate_string = "{:.2f}".format(flow_rate_string)
        print(flow_rate_string)
        experiment_name= "flg_flow_rate_forward_"+flow_rate_string+"_ul_min"
        filename = experiment_name+'.csv'

        while time.time() < t_end:
            measurement = fgt_get_sensorValue(0)
            flow_rate_list.append(measurement)
            time_list.append(time.time()-t_start)
            time.sleep(interval)
        if save_data:
            np.savetxt(filename ,np.c_[time_list*1000,flow_rate_list *1000],delimiter=',',header='ms,mL/min')
        return flow_rate_list,time_list


# if __name__=="__main__":
#     microFlowMeter = MicroFlowMeter()
#     microFlowMeter.get_continuous_flowrate(duration=10,interval=0.1,save_data=True)
#     fgt_close()