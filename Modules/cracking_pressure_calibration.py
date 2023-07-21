# Need the salea to record the pressures and then to plot them with the corresponding prssurs
# take into account the downsample ratio and the datasheet of the pressure sensor (play to see if you can reduce the sampling )
# Have a file saving strucutre to how the experiments will be conducted
# Maybe talk to Anne about the specific pickle structures for that

# Need also to control the fluigent to get the corresponding pressure on the pressure ramp 

from Push_Pull_Pressure import *

def course_pressure_sweep(self,pressure_meter,pressure_rates,runtime):
    for pressure in pressure_rates:
        pressure_meter.set_pressure(pressure)
        time.sleep(runtime)
        pressure_meter.stop()
        time.sleep(1)
    pass

def fine_pressure_sweep(self):
    pass

def experiment(pressure_pump,pressure_rates,runtime,Course_Flag=True):
    assert pressure_pump is not None, "Pressure meter not connected"

    for pressure in pressure_rates:
        
        pressure_pump.inject(syringe, fl, runtime,"ul/min")
        
        if SL1500_flag:
            flow_meter.Continuous_Measure_and_Save(duration_s=runtime,  plot=False, flow_rate_string=flow_rate)
        else:
            flow_meter.get_continuous_flowrate(duration_s=runtime, interval=0.1, flow_rate_string=flow_rate,save_data=True)
        
        pump.stop()
        time.sleep(1) # Interval between experiments

if __name__=="__main__":
    nb_controllers = 1

    # Experiment Nme 
    connection_start = 'node-tube'
    tube_length = '-30cm'
    inner_diameter = '-1-8in'
    connection_middle = '-cv3'
    connection_end = 'node'
    exp_name = connection_start + tube_length + inner_diameter + connection_middle + connection_end
    
    pp_pressure = PP_Pressure(nb_controllers,exp_name)
    experiment(pp_pressure,pressure_rates,runtime,Course_Flag=True)