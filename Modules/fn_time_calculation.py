plateau_time = 30

start_p1 = 0
max_p1 = 200
nb_steps1 = 20
# or by number of steps: step_size = int((Pmax - Pmin) / 20.)

start_p2 = 0
max_p2 = 200
nb_steps2 = 20

possible_p1 = abs(((max_p1-start_p1)/nb_steps1)) + 1
possible_p2 = abs(((max_p2-start_p2)/nb_steps2)) + 1
all_steps = possible_p1*possible_p2
total_seconds = all_steps*plateau_time
total_mins = total_seconds // 60
total_time = '{:.0f}mins{:d}s'.format(total_mins, int(total_seconds) % 60)
print('Total Time: '+total_time)
