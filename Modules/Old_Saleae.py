import os
import csv
import subprocess
import json
import sys
import time
import saleae


def process_saleae(dict_parameters):
    # def process_saleae(exp_folder, voltages_path, pressure_path, total_seconds):
    print("Saleae processing started")
    master_folder_path = dict_parameters['master_folder_path']
    exp_folder = dict_parameters['exp_name']
    calibration_subfolder = dict_parameters['calibration_subfolder']
    voltages_subfolder = dict_parameters['voltages_subfolder']
    voltages_analog_subfolder = dict_parameters['voltages_analog_subfolder']

    # for subfolder_path in [exp_folder+'/'+calibration_subfolder, exp_folder+'/'+voltages_subfolder]:
    for subfolder_path in [exp_folder+'/'+voltages_subfolder]:
        if not os.path.exists(exp_folder+'/'+subfolder_path):
            os.mkdir(subfolder_path)
            print(f"Subfolder {subfolder_path} created successfully.")
        else:
            print(f"Subfolder {subfolder_path} already exists.")

    analog_voltages_path = os.path.join(
        os.getcwd(), master_folder_path+'/'+voltages_analog_subfolder)
    buffer_size_megabytes = dict_parameters['buffer_size_megabytes']
    analog_sample_rate = dict_parameters['analog_sample_rate']
    print(f"analog_sample_rate: {analog_sample_rate}")
    capture_time = dict_parameters['total_seconds']
    client = saleae.Saleae()
    analog_sample_rate = (0, analog_sample_rate)
    sr_available = client.get_all_sample_rates()
    # Sampling Rates
    # (0, 50000000), (0, 12500000), (0, 6250000), (0, 3125000), (0, 1562500), (0, 781250), (0, 125000), (0, 5000), (0, 1000), (0, 100), (0, 10)
    time.sleep(1)
    if (analog_sample_rate) in sr_available:
        client.set_sample_rate(analog_sample_rate)
    else:
        print("Wrong sample rate tuple")
        print(sr_available)
        raise client.CommandNAKedError

    client.set_capture_seconds(capture_time)
    print("capture time set")
    channels = client.get_active_channels()
    print(channels)
    print("Active channels verified")
    os.makedirs(analog_voltages_path)
    client.capture_start_and_wait_until_finished()
    print("capture finished!")
    while not client.is_processing_complete():
        time.sleep(1)

    # Use the current directory as the path for saving
    client.export_data2(os.path.join(analog_voltages_path,
                        "analog.csv"), analog_channels=channels[1])


if __name__ == "__main__":
    print("MultiScripting Saleae")
    param_dict = json.loads(sys.argv[1])
    process_saleae(param_dict)
