from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection, ShdlcDeviceBase
from sensirion_shdlc_driver.command import ShdlcCommand
from struct import pack, unpack
from time import sleep
import matplotlib.pyplot as plt
import pandas as pd

# Sensor Measurement Commands
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
    def __init__(self):
        super(Start_Continuous_Measurement, self).__init__(
            id=0x33,  # Command ID as specified in the device documentation
            data=b"\x01",  # Payload data
            max_response_time=0.2,  # Maximum response time in Seconds
        )

class Get_Continuous_Measurement_Status(ShdlcCommand):
    def __init__(self):
        super(Get_Continuous_Measurement_Status, self).__init__(
            id=0x33,  # Command ID as specified in the device documentation
            data=b"",  # Payload data
            max_response_time=0.2,  # Maximum response time in Seconds
        )

# class Get_Continuous_Measurement(ShdlcCommand):
#     def __init__(self, response_time=1):
#         super(Get_Continuous_Measurement, self).__init__(
#             id=0x36,  # Command ID as specified in the device documentation
#             data=b"",  # Payload data
#             measured_2bytes = [], # Where the continuous measurement will be stored
#             max_response_time=response_time,  # Maximum response time in Seconds
#         )

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

class Get_Resolution(ShdlcCommand):
    def __init__(self):
        super(Get_Resolution, self).__init__(
            id=0x41,  # Command ID as specified in the device documentation
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
    def __init__(self):
        super(Set_Linearization, self).__init__(
            id=0x45,  # Command ID as specified in the device documentation
            data=b"\x00",  # False: Raw Measurement, True: Linearized Measurement
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


    # def interpret_response(self, data, measured_2bytes):
    #     # Convert the received raw bytes to the proper data types
    #     # uint32, uint8 = unpack('>IB', data)
    #     # return uint32, uint8
    #     print("Interpreting Get_Continuous_Measurement response...")
    #     for i in range(int(len(data)/2)):
    #         sig = data[2*i:2*i+2]
    #         #2 bytes, hex encoding
    #         sig_dec = int.from_bytes(sig, 'big', signed=True)
        
    #         # sig_dec = int(sig.hex(),16)
    #         measured_2bytes.append(sig_dec)
    
    # def print_continous_measurement(self,measured_2bytes):
    #     print(measured_2bytes)
    #     fig, ax = plt.subplots(1,1)
    #     ax.set_ylim(-33000, 33000)
    #     ax.plot(measured_2bytes)


class SLS_1500Device(ShdlcDeviceBase):
    def __init__(self, connection, slave_address):
        super(SLS_1500Device, self).__init__(connection, slave_address)

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
        self.execute(Start_Continuous_Measurement())
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
            ax.set_ylim(-33000, 33000)
            ax.plot(measurements)
            plt.show()
        return measurements
    
    def Set_Measurement_Type(self):
        self.execute(Set_Measurement_Type())
        print("Measurement type set to Flow")

    def Get_Measurement_Type(self):
        raw_response = self.execute(Get_Measurement_Type())
        print("Raw response: ", format(raw_response))
        uint8 = unpack('>B', raw_response)
        print("Response Unsigned Integer: {}".format(uint8))
        
    def Get_Resolution(self):
        raw_response = self.execute(Get_Resolution())
        print("Raw response: ", format(raw_response))
        uint8 = unpack('>B', raw_response)
        print("Response Unsigned Integer: {}".format(uint8))
    
    def Set_Factory_Settings(self):
        self.execute(Set_Factory_Settings())
        print("Factory settings set")

    def Get_Factory_Settings(self):
        raw_response = self.execute(Get_Factory_Settings())
        print("Raw response: ", format(raw_response))
        uint8 = unpack('>B', raw_response)
        print("Response Unsigned Integer: {}".format(uint8))

    def Set_Linearization(self):
        self.execute(Set_Linearization())
        print("Linearization set")

    def Get_Linearization(self):
        raw_response = self.execute(Get_Linearization())
        print("Raw response: ", format(raw_response))
        bool = unpack('>?', raw_response)
        print("Response Unsigned Integer: {}".format(bool)) 
    
    def Get_Flow_Unit(self):
        raw_response = self.execute(Get_Flow_Unit())
        print("Raw response: ", format(raw_response))
        uint16 = unpack('>H', raw_response)
        print("Response Unsigned Integer: {}".format(uint16))

    def Get_Scale_Factor(self):
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
    


with ShdlcSerialPort(port='COM3', baudrate=115200) as port:
    fs = SLS_1500Device(ShdlcConnection(port), slave_address=0)

    # Check and Start-Up
    # print("Get_Sensor_Status")
    # fs.Get_Sensor_Status()
    # print("Get_Measurement_Type")
    # fs.Get_Measurement_Type()
    # print("Get_Resolution")
    # fs.Get_Resolution()
    # print("Get_Flow_Unit")
    # fs.Get_Flow_Unit()
    # print("Get_Linearization")
    # fs.Get_Linearization()
    # print("Get_Scale_Factor")
    # fs.Get_Scale_Factor()
    # print("Get_Measurement_Data_Type")
    # fs.Get_Measurement_Data_Type()
    


    # Single Measurement
    # fs.Start_Single_Measurement()
    # sleep(0.5) #secondes
    # fs.Get_Single_Measurement()
    
    # Continuous Measurement
    fs.Start_Continuous_Measurement()
    sleep(5) #secondes
    fs.Get_Continuous_Measurement_Status()
    buffer_data = fs.Get_Measurement_Buffer(plot=False)
    fs.Stop_Continuous_measurement()
    
    # # Saving Data to CSV
    df = pd.DataFrame(buffer_data)
    df.to_csv('output.csv', index=False, header=False)




  

  