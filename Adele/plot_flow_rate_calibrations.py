import os
import glob
import re
import pandas as pd
import matplotlib.pyplot as plt
import sys
from datetime import datetime
import numpy as np


# plt.style.use('fivethirtyeight')

# Iterate over the files
directory = os.getcwd()
file_pattern = 'flow_rate_forward_*.csv'
search_pattern = r'flow_rate_forward_(\d+\.\d+)_ul_min'
files = glob.glob(os.path.join(directory, file_pattern))


fig, ax = plt.subplots(1, 1)
q_measured_list = []
q_std_list = []
q_set_list = []

for filename in files:
    match = re.search(search_pattern, filename)
    if match:
        flow_rate = float(match.group(1))
        print("Flow rate:", flow_rate)
    else:
        print("Error: Could not parse file name: {}".format(filename))
        sys.exit(1)

    df = pd.read_csv(filename)
    mL_min = df['mL/min'].tolist()
    s = (df['ms']/1000).tolist()
    s = np.array(s)
    mask = s > 1
    q = np.array(mL_min)
    q = q[mask]
    q_average = np.average(q)
    q_std = np.std(q)
    q_measured_list.append(q_average)
    q_std_list.append(q_std)
    q_set_list.append(flow_rate/1000)

ax.errorbar(q_set_list, q_measured_list, yerr=q_std_list, fmt='o', capsize=5, label='Measured')
ax.plot(q_set_list, q_set_list, label='Set',linestyle='--')
plt.show()
# plt.close()  

# q measured vs q imposed, cut out the first second and then add the color gradients




# import os
# import glob
# import re
# import pandas as pd
# import matplotlib.pyplot as plt
# import sys
# from datetime import datetime



# # plt.style.use('fivethirtyeight')

# # Iterate over the files
# directory = os.getcwd()
# file_pattern = 'flow_rate_forward_*.csv'
# search_pattern = r'flow_rate_forward_(\d+\.\d+)_ul_min'
# files = glob.glob(os.path.join(directory, file_pattern))


# fig, ax = plt.subplots(1, 1)
# ax.set_ylim(-60, 60)
# ax.set_xlabel("Time [ms]", fontsize=20)
# ax.set_xlabel("Time [s]", fontsize=20)
# ax.set_ylabel("Flow [mL/min]", fontsize=20)
# ax.tick_params(axis='both', which='major', labelsize=16)
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# plt.legend(fontsize=16, frameon=False)
# plt.tight_layout()

# for filename in files:
#     match = re.search(search_pattern, filename)
#     if match:
#         flow_rate = float(match.group(1))
#         print("Flow rate:", flow_rate)
#     else:
#         print("Error: Could not parse file name: {}".format(filename))
#         sys.exit(1)

#     df = pd.read_csv(filename)
#     mL_min = df['mL/min'].tolist()
#     s = (df['ms']/1000).tolist()

#     ax.plot(s, mL_min, label='q measured {} mL/min'.format(flow_rate/1000))

# ax.autoscale(axis='y')  # Adjust y-axis limits automatically
# # ax.legend(fontsize=16, frameon=False)  # Display legend
# ax.legend(fontsize=8, frameon=False)
# # ax.set_title("Flow Rate Over Time", fontsize=24)  # Set the title


# save_directory = os.path.join(directory, "Flow_Calibration_plots")
# os.makedirs(save_directory, exist_ok=True)

# save_path = os.path.join(save_directory, "100uL_min_to_10mL_min-{}.png".format(datetime.now().strftime("%d-%m-%Y_%H-%M-%S")))
# # ax.set_title("Flow Calibration 100uL/min to 10mL/min ", fontsize=16)
# plt.savefig(save_path)
# print("Plot saved: {}".format(save_path))

# plt.show()
# plt.close()  


# # q measured vs q imposed, cut out the first second and then add the color gradients