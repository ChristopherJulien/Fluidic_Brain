from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection, ShdlcDeviceBase
from sensirion_shdlc_driver.command import ShdlcCommand
from struct import pack, unpack
from time import sleep
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.style.use('fivethirtyeight')

MEASURING_INTERVAL = 10 # seconds
_100ms_HEX =b"\x00\x64"
SCALE_FACTOR = 500
# SLS_1500.py
def process_sls_1500(total_seconds, file_name):
    # Add the functionality from SLS_1500.py here
    print("SLS_1500 processing started")
    port = ShdlcSerialPort(port='COM3', baudrate=115200)  # Create a serial port object for communication on port 'COM3' with baudrate 115200
    flow_meter = SLS_1500Device(ShdlcConnection(port), slave_address=0)  # Create a flow meter device using the ShdlcConnection and the port,
    flow_meter.Continuous_Measure_and_Save(duration_s=total_seconds,filename=file_name, set_flow_rate_string=None,)
    

# Sensor Measurement Commands
class Get_Version(ShdlcCommand):
    def __init__(self):
        super(Get_Version, self).__init__(
            id=0xD1,  # Get device information
            data=b"",  # The payload data to send, 1 byte; 3 is serial number
            max_response_time=0.2,  # Maximum response time in Seconds
    )

class Get_Sensor_Status(ShdlcCommand):
    def __init__(self,):
        super(Get_Sensor_Status, self).__init__(
            id=0x30,  # Get device information
            data=b"",  # The payload data to send, 1 byte; 3 is serial number
            max_response_time=0.2,  # Maximum response time in Seconds
    )

class Start_Single_Measurement(ShdlcCommand):
    def __init__(self,):
        super(Start_Single_Measurement, self).__init__(
            id=0x31,  # Get device information
            data=b"",  # The payload data to send, 1 byte; 3 is serial number
            max_response_time=0.2,  # Maximum response time in Seconds
    )

class Get_Single_Measurement(ShdlcCommand): 
    def __init__(self,):
        super(Get_Single_Measurement, self).__init__(
            id=0x32,  # Get device information
            data=b"",  # The payload data to send, 1 byte; 3 is serial number
            max_response_time=0.2,  # Maximum response time in Seconds
    )
        
class Start_Continuous_Measurement(ShdlcCommand):
    def __init__(self,interval):
        super(Start_Continuous_Measurement, self).__init__(
            id=0x33,  # Command ID as specified in the device documentation
            data = interval,  # Payload with interaval of 64Hex = 100DEC ms and 
            max_response_time=0.001,  # Maximum response time in Seconds
        )

class Get_Continuous_Measurement_Status(ShdlcCommand):
    def __init__(self):
        super(Get_Continuous_Measurement_Status, self).__init__(
            id=0x33,  # Command ID as specified in the device documentation
            data=b"",  # Payload data
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Stop_Continuous_Measurement(ShdlcCommand):
    def __init__(self):
        super(Stop_Continuous_Measurement, self).__init__(
            id=0x34,  # Command ID as specified in the device documentation
            data=b"",  # Payload data
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Get_Measurement_Buffer(ShdlcCommand):
    def __init__(self):
        super(Get_Measurement_Buffer, self).__init__(
            id=0x36,  # Command ID as specified in the device documentation
            data=b"",  # Payload data
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Get_Last_Measurement_Mode_Duration(ShdlcCommand):
    def __init__(self):
        super(Get_Last_Measurement_Mode_Duration, self).__init__(
            id=0x38,  # Command ID as specified in the device documentation
            data=b"\x00",  # Payload data
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Set_Measurement_Type(ShdlcCommand):
    def __init__(self, measurement_type):
        super(Set_Measurement_Type, self).__init__(
            id=0x40,  # Command ID as specified in the device documentation
            data=b"\x00",  # Payload data
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Get_Measurement_Type(ShdlcCommand):
    def __init__(self):
        super(Get_Measurement_Type, self).__init__(
            id=0x40,  # Command ID as specified in the device documentation
            data=b"",  # Payload data
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Set_Resolution(ShdlcCommand):
    def __init__(self, resolution):
        super(Set_Resolution, self).__init__(
            id=0x41,  # Command ID as specified in the device documentation
            data=resolution,  # Payload u8t for 16 = 10Hex
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Get_Resolution(ShdlcCommand):
    def __init__(self):
        super(Get_Resolution, self).__init__(
            id=0x41,  # Command ID as specified in the device documentation
            data=b"",  # Payload data
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Set_Heater_Mode(ShdlcCommand):
    def __init__(self, heater_mode):
        super(Set_Heater_Mode, self).__init__(
            id=0x42,  # Command ID as specified in the device documentation
            data=b"\x00",  # Payload data
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Get_Heater_Mode(ShdlcCommand):
    def __init__(self):
        super(Get_Heater_Mode, self).__init__(
            id=0x42,  # Command ID as specified in the device documentation
            data=b"",  # Payload data
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Set_Calib_Field(ShdlcCommand):
    def __init__(self, calib_field):
        super(Set_Calib_Field, self).__init__(
            id=0x43,  # Command ID as specified in the device documentation
            data=calib_field,  # Payload data
            max_response_time=0.2,  # Maximum response time in Seconds
        )
    
class Get_Calib_Field(ShdlcCommand):
    def __init__(self):
        super(Get_Calib_Field, self).__init__(
            id=0x43,  # Command ID as specified in the device documentation
            data=b"",  # Payload data
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Set_Factory_Settings(ShdlcCommand):
    def __init__(self):
        super(Set_Factory_Settings, self).__init__(
            id=0x44,  # Command ID as specified in the device documentation
            data=b"\x00",  # Payload data
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Get_Factory_Settings(ShdlcCommand):
    def __init__(self):
        super(Get_Factory_Settings, self).__init__(
            id=0x44,  # Command ID as specified in the device documentation
            data=b"",  # Payload data
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Set_Linearization(ShdlcCommand):
    def __init__(self, bool):
        super(Set_Linearization, self).__init__(
            id=0x45,  # Command ID as specified in the device documentation
            data=pack("B", int(bool)),  # False: Raw Measurement, True: Linearized Measurement
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Get_Linearization(ShdlcCommand):
    def __init__(self):
        super(Get_Linearization, self).__init__(
            id=0x45,  # Command ID as specified in the device documentation
            data=b"",  # False: Raw Measurement, True: Linearized Measurement
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Get_Flow_Unit(ShdlcCommand):
    def __init__(self):
        super(Get_Flow_Unit, self).__init__(
            id=0x52,  # Command ID as specified in the device documentation
            data=b"",  # False: Raw Measurement, True: Linearized Measurement
            max_response_time=0.2,  # Maximum response time in Seconds
        )
        
class Get_Scale_Factor(ShdlcCommand):
    def __init__(self):
        super(Get_Scale_Factor, self).__init__(
            id=0x53,  # Command ID as specified in the device documentation
            data=b"",  # False: Raw Measurement, True: Linearized Measurement
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Get_Measurement_Data_Type(ShdlcCommand):
    def __init__(self):
        super(Get_Measurement_Data_Type, self).__init__(
            id=0x55,  # Command ID as specified in the device documentation
            data=b"",  # False: Raw Measurement, True: Linearized Measurement
            max_response_time=0.2,  # Maximum response time in Seconds
        )
        
class Sensor_Reset(ShdlcCommand):
    def __init__(self):
        super(Sensor_Reset, self).__init__(
            id=0x65,  # Command ID as specified in the device documentation
            data=b"",  # False: Raw Measurement, True: Linearized Measurement
            max_response_time=5,  # Maximum response time in Seconds
        )
    
def decode_unit(bitcode):
    '''
    Decode sensor flow unit bitcode into string.
    '''
    intcode = int.from_bytes(bitcode, 'big', signed=False) 
    vol_unit_code = int(intcode/256)
    time_unit_code = int((intcode%256)/16)
    dim_unit_code = int(intcode%16)
    
    time_dict = {0: r'', 1: r'$\mu$ s$^{-1}$', 2: r'ms$^{-1}$', 
                 3: r's$^{-1}$', 4: r'min$^{-1}$'}
    time_dict = {0: r'', 1: r'/$\mu$s$', 2: r'/ms', 
                 3: r'/s', 4: r'/min'}
    vol_dict = {0: r'L', 1:'L', 8:'L', 9:'g'}
    
    dim_dict = {3: 'n', 4: '$\mu$', 5:'m', 6:'c', 7:'d',
                8:'', 9:'da', 10:'h', 11:'k', 12:'M', 13:'G'}
    unit_string = dim_dict[dim_unit_code] + vol_dict[vol_unit_code] + time_dict[time_unit_code]
    return unit_string

class SLS_1500Device(ShdlcDeviceBase):
    def __init__(self, connection, slave_address):
        super(SLS_1500Device, self).__init__(connection, slave_address)

   
    def Get_Version(self):
        raw_response = self.execute(Get_Version())
        # print("Raw response: ", format(raw_response))
        firmware_Major, firmware_Minor,firmware_debug, hardware_Major, hardware_Minor, shdl_major, shdl_minor  = unpack('>BBBBBBB', raw_response)
        print("Firmware: {}.{}".format(firmware_Major,firmware_Minor))
        print("Firmware Debug: {}".format(firmware_debug))
        print("Hardware: {}.{}".format(hardware_Major,hardware_Minor))
        print("SHDL: {}.{}".format(shdl_major,shdl_minor))
    
    def Get_Sensor_Status(self):
        raw_response = self.execute(Get_Sensor_Status())
        print("Raw response: ", format(raw_response))
        uint8 = unpack('>B', raw_response)
        print("Response Unsigned Integer: {}".format(uint8))

    def Start_Single_Measurement(self):
        self.execute(Start_Single_Measurement())
        print("Single measurement started")
    
    def Get_Single_Measurement(self):
        raw_response = self.execute(Get_Single_Measurement())
        print("Raw response: ", format(raw_response))
        uint16 = unpack('>H', raw_response)
        print("Response Unsigned Integer: {}".format(uint16))
        int16 = unpack('>h', raw_response)
        print("Response signed Integer: {}".format(int16))
    
    def Start_Continuous_Measurement(self):
        self.execute(Start_Continuous_Measurement(interval=b"\x00\x64"))
        print("Continuous measurement started")
    
    def Get_Continuous_Measurement_Status(self):
        raw_response = self.execute(Get_Continuous_Measurement_Status())
        print("Raw response: ", format(raw_response))
        int16 = unpack('>h', raw_response)
        print("Response signed Integer: {}".format(int16))

    def Stop_Continuous_measurement(self):
        self.execute(Stop_Continuous_Measurement())
        print("Continuous measurement stopped")
    
    def Get_Measurement_Buffer(self, plot=False):
        raw_response = self.execute(Get_Measurement_Buffer())
        print("Raw response: ", format(raw_response))
        # Split the raw response into two-byte chunks
        byte_chunks = [raw_response[i:i+2] for i in range(0, len(raw_response), 2)]
        # Convert each chunk to a signed integer
        measurements = [unpack('>h', chunk)[0] for chunk in byte_chunks]
        # measurements = [int.from_bytes(chunk, 'big', signed=True) for chunk in byte_chunks]
        print(measurements)
        if plot:
            fig, ax = plt.subplots(1,1)
            ax.set_xlabel("Time [ms]") 
            ax.set_ylabel("Flow [mL/min]")
            ax.set_title("Sensor Measurement")
            ax.set_ylim(-33000, 33000)
            ax.plot(measurements)
            plt.show()
        return measurements
    
    def Get_Last_Measurement_Mode_Duration(self):
        raw_response = self.execute(Get_Last_Measurement_Mode_Duration())
        print("Raw response: ", format(raw_response))
        uint32 = unpack('>I', raw_response)
        print("Response Unsigned Integer: {}".format(uint32))

    def Set_Measurement_Type(self):
        self.execute(Set_Measurement_Type())
        print("Measurement type set to Flow")

    def Get_Measurement_Type(self):
        raw_response = self.execute(Get_Measurement_Type())
        print("Raw response: ", format(raw_response))
        uint8 = unpack('>B', raw_response)
        print("Response Unsigned Integer: {}".format(uint8))
        
    def Set_Resolution(self,resolution):
        self.execute(Set_Resolution(resolution))
        print("Resolution set")

    def Get_Resolution(self):
        raw_response = self.execute(Get_Resolution())
        # print("Raw response: ", format(raw_response))
        uint8 = unpack('>B', raw_response)
        print("Resolution bits: {}".format(uint8))
    
    def Set_Calib_Field(self,calib_field):
        self.execute(Set_Calib_Field(calib_field))
        print("Calibration field set")
    
    def Get_Calib_Field(self):
        raw_response = self.execute(Get_Calib_Field())
        # print("Raw response: ", format(raw_response))
        uint8 = unpack('>B', raw_response)
        print("Calibration Field: {}".format(uint8))
        

    def Set_Factory_Settings(self):
        self.execute(Set_Factory_Settings())
        print("Factory settings set")

    def Get_Factory_Settings(self):
        raw_response = self.execute(Get_Factory_Settings())
        print("Raw response: ", format(raw_response))
        uint8 = unpack('>B', raw_response)
        print("Response Unsigned Integer: {}".format(uint8))

    def Set_Linearization(self, bool):
        self.execute(Set_Linearization(bool))
        print("Linearization set")

    def Get_Linearization(self):
        raw_response = self.execute(Get_Linearization())
        # print("Raw response: ", format(raw_response))
        bool = unpack('>?', raw_response)
        print("Linearization: {}".format(bool)) 
    
    def Get_Flow_Unit(self):
        raw_response = self.execute(Get_Flow_Unit())
        print("Raw response: ", format(raw_response))
        uint16 = unpack('>H', raw_response)
        print("Response Unsigned Integer: {}".format(uint16))
        return raw_response

    def Get_Scale_Factor(self, vocal=False):
        raw_response = self.execute(Get_Scale_Factor())
        print("Raw response: ", format(raw_response))
        uint16 = unpack('>H', raw_response)
        print("Response Unsigned Integer: {}".format(uint16))
    
    def Get_Measurement_Data_Type(self):
        raw_response = self.execute(Get_Measurement_Data_Type())
        print("Raw response: ", format(raw_response))
        uint8 = unpack('>B', raw_response)
        print("Response Unsigned Integer: {}".format(uint8))
    
    def Sensor_Reset(self):
        self.execute(Sensor_Reset())
        print("Sensor reset")

    def Set_Heater_Mode(self):
        self.execute(Set_Heater_Mode())
        print("Heater mode set")
    
    def Get_Heater_Mode(self):
        raw_response = self.execute(Get_Heater_Mode())
        print("Raw response: ", format(raw_response))
        uint8 = unpack('>B', raw_response)
        print("Response Unsigned Integer: {}".format(uint8))

    def animate(i,filename):
        df = pd.read_csv(filename)
        xs = df['ms']
        ys = df['mL/min']
        return xs, ys
    
    def Continuous_Measure_and_Save(self, duration_s, filename, set_flow_rate_string=None):
        # Measure and save the data for the specified duration of a buffer size of 100 measurements
        print("Flow Measurement Started %ds " %duration_s)

        # self.Sensor_Command_Settings(resolution=b"\x10", calib_field=b"\x00", set_linearization=True) # 16 bit resolution, calib field 0, linearization on

        retrievals = np.ceil(duration_s /MEASURING_INTERVAL) #Duration divided by buffer fill duration (10ms)
        if MEASURING_INTERVAL*retrievals<duration_s:
            retrievals+=1
        if set_flow_rate_string is not None:
            flow_rate_raw = float(set_flow_rate_string)
            flow_rate_string = "{:.2f}".format(flow_rate_raw)
            experiment_name = "sls_flow_rate_forward_"+flow_rate_string+"_ul_min"
            filename=experiment_name+'.csv'
        else:
            experiment_name = filename
            filename=experiment_name+'sls_flow_measurments.csv'
            print("Filename: ", filename)


        df = pd.DataFrame(columns=['ms','mL/min']) # create an empty dataframe
        time_array = None
        q_array = None
        i = 0
        start_time = time.time()
        while i<retrievals:
            print("Retrieval %d" %i)
            self.Start_Continuous_Measurement()
            last_s_value = time.time() - start_time

            sleep(MEASURING_INTERVAL) #secondes
            elapsed_time_s = time.time() - start_time-last_s_value
            time_steps_s = elapsed_time_s / 100 # number of measurements per second
            if i == 0:
                time_array =np.linspace(0,elapsed_time_s,100)
                q_array = np.array(self.Get_Measurement_Buffer())/SCALE_FACTOR
                # df['ms'] = pd.DataFrame(np.linspace(0,elapsed_time_s,100)*1000) # Fill the dataframe with the time
                # df['mL/min'] = pd.DataFrame(self.Get_Measurement_Buffer())/SCALE_FACTOR # Fill the dataframe with the buffer
                # df.to_csv(filename, index=False, header=True, mode='a') # Write the buffer to csv 
            else:
                print("Last s value: ", last_s_value)
                print("Elapsed time: ", elapsed_time_s)
                time_step = np.linspace(last_s_value,last_s_value+elapsed_time_s,100)
                time_array= np.hstack((time_array,time_step))
                q_array_step = np.array(self.Get_Measurement_Buffer())/SCALE_FACTOR
                q_array = np.hstack((q_array,q_array_step))
                # print("Last ms value")
                # df['ms'] = pd.DataFrame(np.linspace(last_s_value,last_s_value+elapsed_time_s,100)*1000) # Fill the dataframe with the time
                # df['mL/min'] = pd.DataFrame(self.Get_Measurement_Buffer())/SCALE_FACTOR # Fill the dataframe with the buffer
                # df.to_csv(filename, index=False, header=False, mode='a') # Write the buffer to csv 
            self.Stop_Continuous_measurement() # Stopped the continuous measurement
            
            i+=1
            sleep(0.1)
        # df['ms'] = pd.DataFrame(time_array)# Fill the dataframe with the time
        # df['mL/min'] = pd.DataFrame(q_array) # Fill the dataframe with the buffer
        np.savetxt(filename, np.c_[time_array,q_array], delimiter=',', header='s,mL/min', comments='', fmt='%f')
    def Apply_Flow_Scale_Factor(self, filename):
        df = pd.read_csv(filename)
        column_name = 'mL/min'
        df['mL/min'] = df['mL/min'].div(SCALE_FACTOR)
        df.to_csv(filename, index=False)
    
    def Convert_ms_to_s(self, filename):
        df = pd.read_csv(filename)
        column_name = 'ms'
        df['ms'] = df['ms'].div(1000)
        df.to_csv(filename, index=False)
        df = df.rename(columns={"ms":'s'})

    def Plot_Flow_CSV(self, filename):
        self.Convert_ms_to_s(filename)
        df = pd.read_csv(filename)
        fig, ax = plt.subplots(1,1)
        ax.set_ylim(-60, 60)
        ax.plot('ms','mL/min',data=df, label='Flow Measurment')
        ax.plot(data=df, label='Flow Measurment')
        # ax.set_xlabel("Time [ms]", fontsize=20)
        ax.set_xlabel("Time [s]", fontsize=20)
        ax.set_ylabel("Flow [mL/min]", fontsize=20)
        ax.tick_params(axis='both',which='major',labelsize=16)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
        plt.legend(fontsize=16, frameon=False)
        plt.tight_layout()
        plt.show()

    
    def Sensor_Command_Settings(self,
                                resolution=None,
                                calib_field=None,
                                set_linearization=None,
                                ):
        self.Get_Resolution()
        self.Get_Calib_Field()
        self.Get_Linearization()
    
    def Get_Sensor_Information(self):
        self.Get_Version()
        self.Get_Sensor_Status()
        self.Get_Flow_Unit() # ml/min --> 8*256 + 4*16 + 5*1 = 2117
        self.Get_Scale_Factor() # 500
        self.Get_Measurement_Type
        self.Get_Measurement_Data_Type()
        self.Get_Heater_Mode()
    
    def Single_Measurement(self):
        self.Start_Single_Measurement()
        sleep(0.5) #secondes
        self.Get_Single_Measurement()
        

# with ShdlcSerialPort(port='COM3', baudrate=115200) as port:
#     fs = SLS_1500Device(ShdlcConnection(port), slave_address=0)
    
    # Sensor Command Settings
    # fs.Sensor_Command_Settings(resolution=b"\x10", calib_field=b"\x00", set_linearization=True) # 16 bit resolution, calib field 0, linearization on

    # Multiple Continuous Measurement with Buffer
    # fs.Continuous_Measure_and_Save(duration_s=15, plot=False, filename='output') # 100s, 100ms buffer interval, plot=True

if __name__ == "__main__":
    print("MultiScripting SLS.py")
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
    
    print('Time:{:d}mins, {:d}s'.format(int(total_mins), int(total_seconds % 60)))
    process_sls_1500(total_seconds=total_seconds,file_name=exp_folder)