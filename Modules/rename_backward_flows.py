import os
import glob
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
            new_filename = filename.replace("fls_flow_rate_forward_", "flg_flow_rate_forward_")

        #     # Construct the full paths of the original and new filenames
            original_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_filename)

        #     # Rename the file
            os.rename(original_path, new_path)
    exit()

folder_path = r'Data_Calibration\glycerol\flg\-0.1--0.01mL'
rename_csv_files(folder_path)
