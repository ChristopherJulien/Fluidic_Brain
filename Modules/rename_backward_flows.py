import os
import glob
import csv
import re

def rename_csv_files(folder_path):
    file_pattern = '*.csv'

    # Create the file path pattern by joining the folder path and file pattern
    file_path_pattern = os.path.join(folder_path, file_pattern)

    # Use glob to find files matching the pattern
    files = glob.glob(file_path_pattern)
    # print(files)

    # Iterate over the files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file ends with '.csv'
        if filename.endswith('.csv'):
            print(filename)
        #     # Create the new filename by adding a hyphen before the number
            new_filename = filename.replace("sls_flow_rate_forward_", "sls_flow_rate_forward_-")

        #     # Construct the full paths of the original and new filenames
            original_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_filename)

        #     # Rename the file
            os.rename(original_path, new_path)
    exit()

def rename_csv_headers(foldr_path):
    file_pattern = '*.csv'

    # Create the file path pattern by joining the folder path and file pattern
    file_path_pattern = os.path.join(folder_path, file_pattern)

    # Use glob to find files matching the pattern
    files = glob.glob(file_path_pattern)
    new_header = ['s', 'uL/min']

    # Iterate over the files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)

            with open (file_path, 'r') as file:
                reader = csv.reader(file)
                lines = list(reader)
            
            lines[0] = new_header

            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(lines)
            print(f"Header updated in {filename}")



# folder_path = r'Data_Calibration\glycerol\sls\-20--10mL'
# rename_csv_files(folder_path)