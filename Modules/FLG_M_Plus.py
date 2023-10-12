import time
import numpy as np
import sys
import os
import json
import csv
from Fluigent.SDK import fgt_init, fgt_close
from Fluigent.SDK import fgt_get_sensorChannelsInfo
from Fluigent.SDK import fgt_get_sensorUnit, fgt_get_sensorRange, fgt_get_sensorValue


fgt_init()


def process_micro_flow(dict_parametrs):
    print("Micro Flow Meter started")
    exp_folder = dict_parametrs['exp_name']
    micro_flow_subfolder = dict_parametrs['micro_flow_flg_subfolder']
    for subfolder_path in [exp_folder+'/'+micro_flow_subfolder]:
        if not os.path.exists(exp_folder+'/'+subfolder_path):
            os.mkdir(subfolder_path)
            print(f"Subfolder {subfolder_path} created successfully.")
        else:
            print(f"Subfolder {subfolder_path} already exists.")
    micro_flow_sensor = MicroFlowMeter()
    micro_flow_sensor.get_continuous_flowrate(dict_parametrs)


class MicroFlowMeter:
    def __init__(self):
        sensorInfoArray, sensorTypeArray = fgt_get_sensorChannelsInfo()
        self.flowmeter = sensorInfoArray
        self.unit = fgt_get_sensorUnit(0)
        self.minSensor, self.maxSensor = fgt_get_sensorRange(0)

    def get_single_flowrate():
        measurement = fgt_get_sensorValue(0)
        return measurement

    def get_continuous_flowrate(self, dict):
        duration_s = dict["total_seconds"]
        exp_folder = dict["exp_name"]
        micro_flow_subfolder = dict["micro_flow_flg_subfolder"]
        master_folder_path = exp_folder+'/'+micro_flow_subfolder
        micro_measurments_directory = master_folder_path + r"/micro_flow.csv"

        assert duration_s > 0
        measure_interval_s = 0.05

        t_start = time.time()
        t_end = time.time() + duration_s
        flow_rate_list = []
        time_list = []

        while time.time() < t_end:
            measurement = fgt_get_sensorValue(0)
            flow_rate_list.append(measurement)
            time_list.append(time.time()-t_start)
            # print("Flow rate: ", measurement, " Time", time.time()-t_start)
            time.sleep(measure_interval_s)

        with open(micro_measurments_directory, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['s', 'uL/min'])
            for i in range(len(time_list)):
                csv_writer.writerow([time_list[i], flow_rate_list[i]])

        fgt_close()

    def get_continuous_flowrate_set_flow_rate(self, duration_s, interval, flow_rate_string=None, save_data=False):
        assert duration_s > 0
        assert interval > 0.05
        t_start = time.time()
        t_end = time.time() + duration_s
        flow_rate_list = []
        time_list = []
        flow_rate_raw = float(flow_rate_string)
        flow_rate_string = "{:.2f}".format(flow_rate_raw)
        experiment_name = "flg_micro_flow"+flow_rate_string+"_ul_min"
        filename = experiment_name+'.csv'

        while time.time() < t_end:
            measurement = fgt_get_sensorValue(0)
            flow_rate_list.append(measurement)
            time_list.append(time.time()-t_start)
            print("Flow rate: ", measurement, " Time", time.time()-t_start)
            time.sleep(interval)
        if save_data:
            print(len(time_list))
            print(len(flow_rate_list))
            np.savetxt(filename, np.c_[
                       time_list, flow_rate_list], delimiter=',', header='s,uL/min', comments='')

        fgt_close()

        return flow_rate_list, time_list


if __name__ == "__main__":
    microFlowMeter = MicroFlowMeter()
    print('MultiScripting FLG_M_Plus.py')
    param_dict = json.loads(sys.argv[1])
    process_micro_flow(param_dict)

    # microFlowMeter.get_continuous_flowrate(
    #     duration_s=10, interval=0.1, flow_rate_string='test', save_data=True)
