import tkinter as tk
from tkinter import filedialog, messagebox
import glob
import shutil
from pathlib import Path
import sys
import os
import subprocess

####################################################################################################
# Define some functions (user_input)
####################################################################################################

def get_user_confirmation():

        while True:

            user_input = input("\nPlease check the listed files in the above and verify that these are the correct files.\n\nDo you want to proceed? (Y/N): ").strip().lower()  # Get user input, strip whitespace, and convert to lowercase
            
            if user_input == 'y':

                return True
            
            elif user_input == 'n':

                return False
            
            else:

                print("Invalid input. Please enter 'Y' for yes or 'N' for no.")

####################################################################################################
# Select .nii files for hippodeep segmentation
####################################################################################################

# Create a root window but keep it hidden
root = tk.Tk()
root.withdraw()

# Open the file dialog to select a directory
directory_path = filedialog.askdirectory()

# Search for ".nii" files in the selected directory
T1_nii_files = glob.glob(os.path.join(directory_path, "*.nii"))

# Check if the list of files is empty
if not T1_nii_files:

    # Show an error message if no files are found
    messagebox.showerror("Error", "No .nii files found in the selected directory. Please run the script again and select the correct directory.")
    sys.exit()

else:

    # If files are found, print on a new line
    print("\nSelected directory:", directory_path)

    for nii_file_path in T1_nii_files:

        # Normalize/convert file paths to be in UNIX format
        normalized_nii_path = nii_file_path.replace('\\', '/')
        normalized_nii_path = normalized_nii_path.replace('K:/', '/k/')

        print("\nFound .nii file:", normalized_nii_path)

# Confirm if user wants to continue.
if get_user_confirmation():

    print("\nOk, continuing with segmentation via hippodeep_pytorch. (Warning: It will look like the script has frozen after clicking 'Yes', but it is still working! Please do not terminate the script.)")

else:

    print("\nOk. Ending the script.")
    sys.exit()

####################################################################################################
# Run hippodeep_pytorch on selected files
####################################################################################################

print ("\nProceeding with the hippodeep_pytorch segmentation. Just a moment...")
print("\n----------------------------------------------------------------------------------------------------\n")

# Define the path to the hippodeep program (deepseg1.sh)
hippodeep_path = "/home/kedar/hippodeep_pytorch/deepseg1.sh"

# Build the hippodeep command (to run on all files with the .nii extension)
run_hippodeep = "bash" + " " + hippodeep_path + " " + directory_path + "/*.nii"

# Run the hippodeep command
try:

    # Run the hippodeep script
    result = subprocess.run(run_hippodeep, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)

    # Print the stdout and stderr
    print("Output:\n", result.stdout)
    print("Errors:\n", result.stderr)
    
    print("\n\nhippodeep_pytorch segmentation complete.\n\n")

except subprocess.CalledProcessError as e:

    # Handle errors in the called hippodeep script
    print("Error running the hippodeep script:", e)

####################################################################################################
# Move files into separate folders
####################################################################################################
    
# Create subdirectories
masks_L_directory = directory_path + "/masks_L"
masks_R_directory = directory_path + "/masks_R"
cerebrum_mask_directory = directory_path + "/masks_cerebrum"
brain_mask_directory = directory_path + "/masks_brain"
volume_reports_directory = directory_path + "/volume_reports"

if not os.path.exists(masks_L_directory):
    os.makedirs(masks_L_directory)
    print(masks_L_directory + " created.\n")

if not os. path.exists(masks_R_directory):
    os.makedirs(masks_R_directory)
    print(masks_R_directory + " created.\n")

if not os.path.exists(cerebrum_mask_directory):
    os.makedirs(cerebrum_mask_directory)
    print(cerebrum_mask_directory + " created.\n")

if not os.path.exists(brain_mask_directory):
    os.makedirs(brain_mask_directory)
    print(brain_mask_directory + " created.\n")

if not os.path.exists(volume_reports_directory):
    os.makedirs(volume_reports_directory)
    print(volume_reports_directory + " created.\n")

# Move files into respective folders
for file in glob.glob(os.path.join(directory_path, "*mask_L.nii.gz")):
    shutil.move(file, masks_L_directory)
    print(f"\nMoved {file} to {masks_L_directory}.")

for file in glob.glob(os.path.join(directory_path, "*mask_R.nii.gz")):
    shutil.move(file, masks_R_directory)
    print(f"\nMoved {file} to {masks_R_directory}.")

for file in glob.glob(os.path.join(directory_path, "*cerebrum_mask.nii.gz")):
    shutil.move(file, cerebrum_mask_directory)
    print(f"\nMoved {file} to {cerebrum_mask_directory}.")

for file in glob.glob(os.path.join(directory_path, "*brain_mask.nii.gz")):
    shutil.move(file, brain_mask_directory)
    print(f"\nMoved {file} to {brain_mask_directory}.")

for file in glob.glob(os.path.join(directory_path, "*.csv")):
    shutil.move(file, volume_reports_directory)
    print(f"\nMoved {file} to {volume_reports_directory}.")

####################################################################################################
# End script
####################################################################################################

print("\n----------------------------------------------------------------------------------------------------\n")    
print("\nThe segmentation process is complete and all files have be placed into their respective folders.\n")