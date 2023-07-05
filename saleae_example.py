from saleae import automation
import os
import os.path
from datetime import datetime

# {"Model":"Logic 8","Serial #":"B98F3792BA08E057","Hardware Revision":"1.0.0"}
duration_seconds = 5.0



def add_offset(filename, offset):
    print ("add offset")

def volt_to_mbar(filename, sensor, volt_signal, volt_source):
    cdict = {'25kPa': 0.018,
                '7kPa': 0.057,
                '2kPa': 0.2}
    pressure = (volt_signal/volt_source - 0.5)/cdict[sensor]*10
    return pressure

# Connect to the running Logic 2 Application on port `10430`.
# Alternatively you can use automation.Manager.launch() to launch a new Logic 2 process - see
# the API documentation for more details.
# Using the `with` statement will automatically call manager.close() when exiting the scope. If you
# want to use `automation.Manager` outside of a `with` block, you will need to call `manager.close()` manually.
with automation.Manager.connect(port=10430) as manager:

    # Configure the capturing device to record on analog channels 0, 1, 2, and 3,
    # with a sampling rate of 5 MSa/s, and a logic level of 3.3V.
    # The settings chosen here will depend on your device's capabilities and what
    # you can configure in the Logic 2 UI.
    device_configuration = automation.LogicDeviceConfiguration(
        enabled_analog_channels=[4,5,6,7],
        analog_sample_rate=5_000_000,
        # digital_threshold_volts=3.3,
        # samplerates<= 31250 are currently unsupported from the automation API. 
        # Allowed sample rates with channel configuration: 
        # {"analog":5_000_000}, {"analog":2_500_000}, {"analog":1_250_000}, {"analog":625_000}, {"analog":1_250_000},
        # {"analog":1_250_000}, {"analog":1_250_000}, {"analog":1_250_000}, {"analog":1_250_000}
    )

    # Record 5 seconds of data before stopping the capture
    capture_configuration = automation.CaptureConfiguration(
        capture_mode=automation.TimedCaptureMode(duration_seconds)
    )

    # Start a capture - the capture will be automatically closed when leaving the `with` block
    # Note: The serial number 'F4241' is for the Logic Pro 16 demo device.
    #       To use a real device, you can:
    #         1. Omit the `device_id` argument. Logic 2 will choose the first real (non-simulated) device.
    #         2. Use the serial number for your device. See the "Finding the Serial Number
    #            of a Device" section for information on finding your device's serial number.
    with manager.start_capture(
            device_id='B98F3792BA08E057',
            device_configuration=device_configuration,
            capture_configuration=capture_configuration) as capture:

        # Wait until the capture has finished
        # This will take about 5 seconds because we are using a timed capture mode
        print("Starting Capture %d",duration_seconds)
        capture.wait()

        # Add an analyzer to the capture
        # Note: The simulator output is not actual SPI data
        # spi_analyzer = capture.add_analyzer('SPI', label=f'Test Analyzer', settings={
        #     'MISO': 0,
        #     'Clock': 1,
        #     'Enable': 2,
        #     'Bits per Transfer': '8 Bits per Transfer (Standard)'
        # })

        # Store output in a timestamped directory
        output_dir = os.path.join(os.getcwd(), 'output_voltages}')
        os.makedirs(output_dir)
    

        # Export analyzer data to a CSV file here we could potential do the conversion of voltage to pressure
        # analyzer_export_filepath = os.path.join(output_dir, 'export.csv')
        # capture.export_data_table(
        #     filepath=analyzer_export_filepath,
        #     analyzers=[spi_analyzer]
        # )

        # Export raw digital data to a CSV file
        capture.export_raw_data_csv(directory=output_dir, analog_channels=[4,5,6,7], analog_downsample_ratio=10000)
        print("Finished Capture")

        # Finally, save the capture to a file
        capture_filepath = os.path.join(output_dir, 'example_capture.sal')
        capture.save_capture(filepath=capture_filepath)
        