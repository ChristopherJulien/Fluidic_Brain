# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 14:03:02 2023

@author: Masca
"""
from saleae import automation
# import os
# import os.path
# from datetime import datetime
# import time
class Digitizer():
    def __init__(self,output_folder,device_id,sr=625000,capture_duration = 10,analog_channels = [4,5,6,7]):
        self.manager = automation.Manager.connect(port=10430)
        self.analog_channels = analog_channels
        self.device_configuration = automation.LogicDeviceConfiguration(enabled_analog_channels=self.analog_channels, analog_sample_rate=sr)
        self.capture_configuration = automation.CaptureConfiguration(capture_mode=automation.TimedCaptureMode(capture_duration))
        self.output_folder = output_folder
        self.device_id = device_id
    def capture_data(self):
        print("Capture start....")
        self.capture = self.manager.start_capture(device_id=self.device_id, device_configuration=self.device_configuration, capture_configuration=self.capture_configuration)
        # self.capture.wait()
        
    def export_data3(self,analog_downsample_ratio=25000):
        self.capture.export_raw_data_csv(directory=self.output_folder, analog_channels=self.analog_channels, analog_downsample_ratio=analog_downsample_ratio)
        print("Finished Capture")        
        
# if __name__=="__main__":
#     path_output = r"D:\Dropbox\Postdoc\project_topoflow\20230208_head_loss_characterization\202307_microfluidictubes_v1"
#     digitizer = Digitizer(path_output)
#     digitizer.capture_data()
#     digitizer.export_data()