import os
import glob
import re
import pandas as pd
import matplotlib.pyplot as plt

# Iterate over the files
directory = os.getcwd()
file_pattern = 'flow_rate_forward_*.csv'
files = glob.glob(os.path.join(directory, file_pattern))

# Initialize an empty list to store all the measured values and true values
all_measured_values = []
all_true_values = []

# Read the first file to obtain the common x-values
df = pd.read_csv(files[0])
x_values = df['ms'].tolist()

# Iterate over the files
for file in files:
    # Extract from the file name
    file_name = os.path.basename(file)
    match = re.search(r'flow_rate_forward_(\d+\.\d+)_ul_min', file_name)
    if match:
        xxx_x = match.group(1)
        true_value = float(xxx_x)
        all_true_values.append(true_value)
    else:
        print("Error: Could not parse file name: {}".format(file_name))
        continue

    # Extract measured values
    df = pd.read_csv(file)
    measured_values = df['mL/min'].tolist()
    
    # Check if the dimensions match
    if len(measured_values) == len(x_values):
        all_measured_values.append(measured_values)
    else:
        print("Error: Dimensions mismatch for file: {}".format(file))
        continue

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))
fig.suptitle('100-10000 [uL/min Flow Rate Tests', fontsize=16)

# Plot all the data
for true_value, measured_values in zip(all_true_values, all_measured_values):
    ax.plot(x_values, measured_values, label='Flow ' + str(true_value / 1000) + ' ml/min')

# Customize the plot
ax.set_xlabel("Time [ms]", fontsize=10)
ax.set_ylabel("Flow [mL/min]", fontsize=10)
ax.tick_params(axis='both', which='major', labelsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(fontsize=8, frameon=False)

plt.tight_layout()
plt.show()