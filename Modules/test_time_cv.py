calibration_flag = 0
# Pressure Parameters
nb_controllers = 1
calibration_time = 30
plateau_time = 30

# First Ramp
p1 = 0
p2 = 45
p3 = 55
p4 = 205
stp1 = 5
stp2 = 1
stp3 = 15

# Calculate total time
ramp1 = int((p2-p1)/stp1)+1
ramp2 = int((p3-p2)/stp2)+1
ramp3 = int((p4-p3)/stp3)+1
if calibration_flag:
    total_seconds = calibration_time
else:
    total_seconds = plateau_time * (ramp1+ramp2+ramp3)
total_mins = total_seconds // 60
total_time = '{:d}mins{:d}s'.format(total_mins, total_seconds % 60)
print('Total Time: '+total_time)
