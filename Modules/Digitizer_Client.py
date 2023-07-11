import os
import time
import saleae


trig = saleae.Trigger(3)
perf = saleae.PerformanceOption(20)
path_saving = "C:/Users/mugen/PycharmProjects/saleae_interface/Data/"
file_saving = "data_test.logicdata"


def init_client(mode,analog_sample_rate,buffer_time = None,capture_time=None,digital_sample_rate=None):

    client = saleae.Saleae()
    while not client.is_logic_running():
        time.sleep(1)
    time.sleep(5)
    print("running")
    # client.set_performance(perf)
    # print("perf set")
    time.sleep(5)
    if capture_time is None:
        capture_time = 200000
    client.set_capture_seconds(capture_time)
    print("capture time set")

    sr_available = client.get_all_sample_rates()
    print("sr obtained")
    time.sleep(5)
    channels = client.get_active_channels()
    print(channels)
    print("Active channels verified")

    if mode.lower()=="trigger":
        client.set_trigger_one_channel(1, trig)
        print("trig set")
        time.sleep(1)
        if (digital_sample_rate, analog_sample_rate) in sr_available:
            client.set_sample_rate((digital_sample_rate, analog_sample_rate))
            print("sr set")
        else:
            print("Wrong sample rate tuple")
            print(sr_available)
            raise client.CommandNAKedError
        client.set_capture_pretrigger_buffer_size(digital_sample_rate * pre_trig_time)
        print("Pre-trigger buffer set")
    else:
        try:
            client.set_sample_rate((0, analog_sample_rate))
        except:
            print(sr_available)
    return client,channels

# if __name__ == "__main__":
#
#     print("starting capture...")
#     client,channels = init_client(mode="analog",analog_sample_rate=1000)
#     client.capture_start_and_wait_until_finished()
#     client.capture_start()
#     client.capture_stop()
#     print("capture finished!")
#     while not client.is_processing_complete():
#         time.sleep(1)
#     client.save_to_file(path_saving + file_saving)
#     client.export_data2(path_saving + "Data_CSV.csv", digital_channels=channels[0], analog_channels=channels[1])

