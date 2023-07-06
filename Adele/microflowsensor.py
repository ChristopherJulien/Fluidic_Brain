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
    def get_continuous_flowrate(duration,interval,save_data=False):
        assert duration > 0
        assert interval > 0.05
        t_start = time.time()
        t_end = time.time() + duration
        flow_rate_list = []
        time_list = []
        while time.time() < t_end:
            measurement = fgt_get_sensorValue(0)
            flow_rate_list.append(measurement)
            time_list.append(time.time()-t_start)
            time.sleep(interval)
        if save_data:
            np.savetxt('microflowrate_data.csv',np.c_[time_list,flow_rate_list],delimiter=',',header='time (s),flowrate'+self.unit)
        return flow_rate_list,time_list


