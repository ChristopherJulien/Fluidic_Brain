import os
import csv
import subprocess
from saleae import automation

def process_saleae(exp_folder, voltages_path, pressure_path, total_seconds):
    print("Saleae processing started")
    logic_capture = LogicCapture(duration_seconds=total_seconds)
    analog_voltages = os.path.join(os.getcwd(), exp_folder + voltages_path)
    logic_capture.start_capture(analog_voltages)
    # analog_pressures = os.path.join(os.getcwd(), exp_folder + pressure_path)


class LogicCapture:
    def __init__(self, duration_seconds=5.0):
        self.duration_seconds = duration_seconds

    def add_offset(self, filename, offset):
        print("add offset")
        # TODO: Add offset to the file look into the file and calculate the offset

    def volt_to_mbar(self, sensor, volt_signal, volt_source):
        cdict = {'25kPa': 0.018, '7kPa': 0.057, '2kPa': 0.2}
        pressure = (volt_signal / volt_source - 0.5) / cdict[sensor] * 10
        return pressure
    
    # Function to process the CSV file and create a new CSV with pressures
    def process_csv(self,input_file, output_file):
        os.makedirs(output_file)
        try:
            with open(input_file, 'r', newline='') as input_file:
                with open(output_file, 'w', newline='') as output_file:
                    reader = csv.reader(input_file)
                    writer = csv.writer(output_file)

                    # Example: Copying the content from the input file to the output file
                    for row in reader:
                        writer.writerow(row)
                        
                    # You can add your data processing logic here if needed
                    # For example, manipulating the data or performing calculations.

            print("CSV processing complete. Output file created successfully.")

        except FileNotFoundError:
            print("Error: Input file not found.")
        except Exception as e:
            print("An error occurred during CSV processing:", e)
            
        # with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        #     reader = csv.DictReader(infile)
        #     fieldnames = ['s', '25kPa', '2kPa', '7kPa', 'V_source']  # Define the fieldnames for the output CSV
        #     writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        #     writer.writeheader()

        #     for row in reader:
        #         new_row = {
        #             's': row['Time [s]'],
        #             'V_source': row['Channel 7'], 
        #             '25kPa': self.volt_to_mbar(float(row['Channel 4']), 5.0, "25kPa"),  # Replace 5.0 with the actual voltage source value
        #             # '2kPa': volt_to_mbar(float(row['Channel 5']), 5.0, "2kPa"),
        #             # '7kPa': volt_to_mbar(float(row['Channel 6']), 5.0, "7kPa"),
        #         }
    
        #         writer.writerow(new_row)

    def change_file_permission(self,file_path, permissions= 'Everyone:(R,W)'):
            try:
                # Use icacls command to change permissions
                subprocess.run(['icacls', file_path, '/grant', permissions], check=True)
                print(f"Permissions changed for {file_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error: Unable to change permissions for {file_path}")
                print(e)

    def start_capture(self, output_dir):
        with automation.Manager.connect(port=10430) as manager:
            device_configuration = automation.LogicDeviceConfiguration(
                enabled_analog_channels=[4, 5, 6, 7],
                analog_sample_rate=625000
                # sample rates <= 31250 are currently unsupported from the automation API
            )

            capture_configuration = automation.CaptureConfiguration(
                capture_mode=automation.TimedCaptureMode(self.duration_seconds),
                buffer_size_megabytes= 10000
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
                # self.change_file_permission(output_dir)
                print("Finished Capture")

                # Make a file system that copies this raw data and analyzes it to something different.

                capture_filepath = os.path.join(output_dir, 'example_capture.sal')
                capture.save_capture(filepath=capture_filepath)

            
        
if __name__ == "__main__":
    print("MultiScripting Saleae")
    Lstring = '30cm'
    IDstring = '3-32'
    check_valve_type = 'tube'
    # Pressure Coarse Parameters
    Pmax = 300
    Pmin = -int(Pmax / 4)
    Pstart = 0
    num_steps = 20
    step_size = int((Pmax - Pmin) / num_steps)
    plateau_time = 30
    h_init_cm = '8.3cm'
    vl_init   = '1000mL'


    exp_folder = 'node_tube_{:s}_ID_{:s}_{:s}_node-h_init{:s}_vl_init{:s}/'.format(Lstring, IDstring, check_valve_type,h_init_cm,vl_init)
    calibration_folder = exp_folder+r'/calibration_'
    voltages_path = r'output/analog_voltages'
    pressure_path = r'output/analog_pressures'

    coarse_parameters = {
        "nb_controllers": 1,
        "IDstring": IDstring,
        "Lstring": Lstring,
        "check_valve_type": check_valve_type,
        "plateau_time": plateau_time,
        'Pstart': Pstart,
        "Pmax": Pmax,
        "Pmin": Pmin,
        'h_init': h_init_cm,
        'vl_init': vl_init,
        "step_size": step_size,
        "exp_name": exp_folder,
    }

    nstep_up1 = int((Pmax - Pstart)/step_size)+1
    max_p = Pstart + step_size*(nstep_up1-1)
    nstep_down1 = int((max_p - Pmin)/step_size)
    min_p = max_p - step_size*(nstep_down1)
    nstep_up2 = - nstep_up1 + nstep_down1+1

    total_seconds = plateau_time* (nstep_up1 + nstep_down1 + nstep_up2)
    total_mins = total_seconds // 60
    calibration_time_s = 3
    

    process_saleae(exp_folder, voltages_path, pressure_path, total_seconds)
    # process_saleae(calibration_folder, voltages_path, pressure_path, calibration_time_s )

    