import os
import csv

####################################################################################################
# User-defined variables (directories)
####################################################################################################

# Specify the directory paths and the CSV file names
directory_path_masks_L = '/path/to/your/left/hippocampal/VTK/models/'
directory_path_masks_R = '/path/to/your/right/hippocampal/VTK/models/'

output_directory = '/path/to/directory/where/CSV/files/will/be/saved/'

csv_file_name_masks_L = 'paths_masks_L.csv'
csv_file_name_masks_R = 'paths_masks_R.csv'

# Ensure the output directory exists, create it if not
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Create the full paths for the CSV files in the output directory
csv_file_path_masks_L = os.path.join(output_directory, csv_file_name_masks_L)
csv_file_path_masks_R = os.path.join(output_directory, csv_file_name_masks_R)

####################################################################################################
# masks_L
####################################################################################################

# List all files in the directory
file_names_masks_L = [os.path.join(directory_path_masks_L, f) for f in os.listdir(directory_path_masks_L) if os.path.isfile(os.path.join(directory_path_masks_L, f))]

# Write the file names to a CSV, each file name in a new row in the first column
with open(csv_file_path_masks_L, mode='w', newline='') as file:
    writer = csv.writer(file)
    for name in file_names_masks_L:
        writer.writerow([name])

print(f"\nCSV file '{csv_file_name_masks_L}' has been created with the names of all files from the directory '{directory_path_masks_L}'.")

####################################################################################################
# masks_R
####################################################################################################

# List all files in the directory
file_names_masks_R = [os.path.join(directory_path_masks_R, f) for f in os.listdir(directory_path_masks_R) if os.path.isfile(os.path.join(directory_path_masks_R, f))]

# Write the file names to a CSV, each file name in a new row in the first column
with open(csv_file_path_masks_R, mode='w', newline='') as file:
    writer = csv.writer(file)
    for name in file_names_masks_R:
        writer.writerow([name])

print(f"\nCSV file '{csv_file_name_masks_R}' has been created with the names of all files from the directory '{directory_path_masks_R}'.")

####################################################################################################
# End script
####################################################################################################

print("\nAll CSV files have been created.\n")
