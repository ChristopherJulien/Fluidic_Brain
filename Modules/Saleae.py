import os
from saleae import automation

class LogicCapture:
    def __init__(self, duration_seconds=5.0):
        self.duration_seconds = duration_seconds

    def add_offset(self, filename, offset):
        print("add offset")
        # TODO: Add offset to the file look into the file and calculate the offset

    def volt_to_mbar(self, filename, sensor, volt_signal, volt_source):
        cdict = {'25kPa': 0.018, '7kPa': 0.057, '2kPa': 0.2}
        pressure = (volt_signal / volt_source - 0.5) / cdict[sensor] * 10
        return pressure

    def start_capture(self, output_dir):
        with automation.Manager.connect(port=10430) as manager:
            device_configuration = automation.LogicDeviceConfiguration(
                enabled_analog_channels=[4, 5, 6, 7],
                analog_sample_rate=5_000_000
            )

            capture_configuration = automation.CaptureConfiguration(
                capture_mode=automation.TimedCaptureMode(self.duration_seconds)
            )

            with manager.start_capture(
                    device_id='B98F3792BA08E057',
                    device_configuration=device_configuration,
                    capture_configuration=capture_configuration) as capture:

                print(f"Starting Capture {self.duration_seconds} seconds")
                capture.wait()

                os.makedirs(output_dir)

                capture.export_raw_data_csv(
                    directory=output_dir, analog_channels=[4, 5, 6, 7], analog_downsample_ratio=10000
                )
                print("Finished Capture")

                # Make a file system that copies this raw data and analyzes it to something different.

                capture_filepath = os.path.join(output_dir, 'example_capture.sal')
                capture.save_capture(filepath=capture_filepath)
        
        # make method that retieves data from one two or all three signals to plot them all together

if __name__ == "__main__":
    logic_capture = LogicCapture(duration_seconds=5.0)

    # Start the capture and specify the output directory
    output_dir = os.path.join(os.getcwd(), 'output_voltages')
    logic_capture.start_capture(output_dir)