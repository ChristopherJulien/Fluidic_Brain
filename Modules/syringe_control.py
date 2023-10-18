# Developed by Binhong Lin @ Stanford University and IBM-Almaden Research (2018)
# This Python application is intended for use with Harvard syringe pumps to generate
# import sys
import serial
import time
# import datetime

# Classes: Pump() and Reaction()
# The Pump class is used to communicate with the syringe pumps - setting the flow rates / syringe diameter / start / stop.


class Syringe(object):
    # Constructor for the syringe class.
    def __init__(self, identifier, syringeVolume, syringe_type=None):
        self.identifier = identifier+" "
        if syringe_type is None:
            self.syringe_type = "bdp"+" "
        else:
            self.syringe_type = syringe_type
            self.syringe_type += " "

        self.syringeBDPDiameterLookup = {"1": 0, "3": 1, "5": 2, "10": 3, "20": 4, "30": 5, "50": 6,
                                         "60": 7}  # Convenient access to the syringes' index (Becton Dickinson, Plasti-pak syringes).
        self.syringeBDGDiameterLookup = {"0.5": 0, "1": 1, "2.5": 2, "5": 3, "10": 4, '20': 5, '30': 6,
                                         '50': 7}  # Convenient access to the syringes' index (Becton Dickinson, Becton Dickinson, Glass (all types)).
        if type(syringeVolume) == type(1):
            syringeVolume = str(syringeVolume)

        if self.syringe_type == 'bdp ':

            self.syringeIndex = str(
                self.syringeBDPDiameterLookup[syringeVolume])+" "
        elif syringe_type == 'bdg ':
            self.syringeIndex = str(
                self.syringeBDGDiameterLookup[syringeVolume])+" "
        else:
            self.syringeIndex = None


class Pump(object):
    # Send the command to the pump, unless testMode is enabled.
    def writePort(self, command):
        self.pump.write(command.encode())

    def set_syringe(self, syringe):
        syringe_code = syringe.syringe_type
        syringe_index = syringe.syringeIndex
        identifier = syringe.identifier
        self.writePort('syr ' + identifier + syringe_code + syringe_index+'\r')
    # Constructor for the Pump class.

    def __init__(self, name, USBAddress, syringe1, syringe2=None):
        self.name = name  # The name describes the inlet, i.e. THF 1 or Monomer 1
        self.USBAddress = USBAddress
        self.syringeA = syringe1

        if syringe2 is not None:
            self.syringeB = syringe2
        # This is used to keep track of solution consumption.
        self.amountUsed = 0
        # Connect to the pump, unless testMode is enabled.
        self.pump = serial.Serial(
            port=self.USBAddress, baudrate=115200, stopbits=2, bytesize=8)
        # Initialize pump settings
        # Turn off non-volatile RAM to increase pump CPU process speed and protect the pumps.
        self.writePort('nvram none\r')
        if syringe2 is not None:
            # Set to the pump's maximum force to ensure they  don't stall.
            self.writePort('force ' + 'ab ' + '100\r')
        else:
            c = self.syringeA.identifier
            # Set to the pump's maximum force to ensure they  don't stall.
            self.writePort('force ' + self.syringeA.identifier + '100\r')
        self.set_syringe(self.syringeA)
        if syringe2 is not None:
            self.set_syringe(self.syringeB)

    def close(self):
        # The extra time delay ensures that the last command has time to be processed due to pump lag time.
        time.sleep(0.05)
        self.pump.close()

    # This method tells the pump to inject for the specified flow rate for the specified amount of time.
    def inject(self, syringe, flowRate, time, unit):
        # flow rate in ml/min
        # time in seconds
        identifier = syringe.identifier
        if flowRate != 0:  # Guard against any flow rate of 0, as that cannot be set in the pumps.
            # Clear any target time.
            self.writePort('ctime ' + identifier + '\r')
            # Clear any target volume.
            self.writePort('cvolume ' + identifier + '\r')
            self.writePort('tvolume ' + identifier +
                           str(abs(flowRate) * time / 60) + 'ml\r')
            if flowRate > 0:
                # Set the target volume. Need to set by volume instead of by target time because the Dual Motor Pumps do not allow decimals for setting the target time.
                self.writePort('irate ' + identifier +
                               str(flowRate) + ' '+unit+'\r')
                # Set the flow rate.
                # Start the injection.
                self.writePort('irun ' + identifier + '\r')
                # Add to the amount of solution used.
                self.amountUsed += flowRate * time / 60
                # Print to the console that the syringe injection information.
                print('Injecting ' + self.name + ' at ' +
                      str(format(flowRate, '.2f')) + unit+' for ' + str(time) + 's.')
            else:
                self.writePort('wrate ' + identifier +
                               str(abs(flowRate)) + ' '+unit+'\r')
                # Set the flow rate.
                # Start the injection.
                self.writePort('wrun ' + identifier + '\r')
                # Add to the amount of solution used.
                self.amountUsed += flowRate * time / 60
                print('Withdrawing ' + self.name + ' at ' + str(format(flowRate, '.2f')) + unit + ' for ' + str(
                    time) + 's.')

    def stop(self, syringe=None):
        if syringe is None:
            identifer = "ab "
        else:
            identifer = syringe.identifier
        self.writePort("stop " + identifer + "\r")


if __name__ == "__main__":
    syringeA = Syringe("a", '10', 'bdp')
    test = Pump("test", "COM5", syringe1=syringeA)
    test.stop()
    # flow rate in ml/min
    # time in seconds
    fr = 10
    t = 60
    test.inject(syringeA, fr, t, "ul/min")
