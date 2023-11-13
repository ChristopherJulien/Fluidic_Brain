import os
import time
import saleae
​
digital_sample_rate = int(5e8)
analog_sample_rate = int(125e3)
pre_trig_time = 2
capture_time = 10
trig = saleae.Trigger(3)
perf = saleae.PerformanceOption(20)
path_saving = "C:/Users/mugen/PycharmProjects/saleae_interface/Data/"
file_saving = "data_test.logicdata"
client = saleae.Saleae()
while not client.is_logic_running():
    time.sleep(1)
time.sleep(5)
print("running")
client.set_trigger_one_channel(1,trig)
print("trig set")
time.sleep(1)
client.set_performance(perf)
print("perf set")
time.sleep(1)
sr_available = client.get_all_sample_rates()
print("sr obtained")
time.sleep(1)
if (digital_sample_rate,analog_sample_rate) in sr_available:
    client.set_sample_rate((digital_sample_rate,analog_sample_rate))
    print("sr set")
else:
    print("Wrong sample rate tuple")
    print(sr_available)
    raise client.CommandNAKedError
client.set_capture_seconds(capture_time)
print("capture time set")
channels = client.get_active_channels()
print(channels)
print("Active channels verified")
client.set_capture_pretrigger_buffer_size(digital_sample_rate*pre_trig_time)
print("Pre-trigger buffer set")
print("starting capture...")
client.capture_start_and_wait_until_finished()
print("capture finished!")
while not client.is_processing_complete():
    time.sleep(1)
client.save_to_file(path_saving+file_saving)
client.export_data2(path_saving+"Data_CSV.csv",digital_channels=channels[0],analog_channels=channels[1])