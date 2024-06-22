import configparser
import os
import subprocess
import sys

####################################################################################################
# User-defined variables (directories, files)
####################################################################################################

# Define the input and output directories for the SlicerSALT SPHARM-PDM computation
input_directory = '/path/to/your/input/masks/directory/' # CHECK!
output_directory = '/path/to/your/output/directory/' # CHECK!

# Create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
    print("\n")
    print(output_directory + " created.\n")

# Define the registration options
reg_template_TorF = 'True'
reg_template_path = '/path/to/your/registration/template/file.vtk' # CHECK!
flip_template_TorF = 'True'
flip_template_path = '/path/to/your/flip/template/file.coef' # CHECK!

# Define path to blank .ini file (template)
ini_file = '/path/to/SPHARM-PDM-parameters_blank.ini'

# Define name for new .ini file (do not include full path)
new_ini_file = 'new_file.ini' # CHECK!

####################################################################################################
# Edit the .ini file
####################################################################################################

# Initialize the ConfigParser
config = configparser.ConfigParser()

# Read the existing .ini file
config.read(ini_file)

# Update the paths in the [DirectoryPath] section
config['DirectoryPath']['inputDirectoryPath'] = input_directory
config['DirectoryPath']['outputDirectoryPath'] = output_directory

# Update the options/paths in the [ParaToSPHARMMesh] section
config['ParaToSPHARMMesh']['RegParaTemplateFileOn'] = reg_template_TorF
config['ParaToSPHARMMesh']['regParaTemplate'] = reg_template_path
config['ParaToSPHARMMesh']['fliptemplateon'] = flip_template_TorF
config['ParaToSPHARMMesh']['fliptemplate'] = flip_template_path

# Write the changes to a new .ini file
with open(output_directory + new_ini_file, 'w') as configfile:
    config.write(configfile)

# Define full path of the newly created .ini file
new_ini_file_path = output_directory + new_ini_file

print("\nA new .ini file has been created. The SPHARM-PDM computation using this .ini file will now begin using the following .ini file:\n")
print(new_ini_file_path)

####################################################################################################
# Begin the SPHARM-PDM computation
####################################################################################################

print("\nStarting SPHARM-PDM computation. This may take a while...")

# Build command to execute the SPHARM-PDM.py script from SlicerSALT
spharm_command = ["/path/to/your/executable/of/SlicerSALT", "--no-main-window", "--python-script", "/path/to/your/main/SlicerSALT/folder/share/SlicerSALT-5.1/CommandLineTool/SPHARM-PDM.py", new_ini_file_path]

# Run the SlicerSALT/SPHARM-PDM command and enable stdout and stderr to be piped. text=True allows stdout to be interpreted and printed as a string
run_spharm = subprocess.Popen(spharm_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

exit_phrase = "All pipelines took:" # This is the final output line when SPHARM-PDM is completed. If this phrase is detected while the output is being printed, this python script will end.

# Continuously read lines from the run_spharm process output
while True:
    output_line = run_spharm.stdout.readline()

    # If EOF, break the loop
    if not output_line:
        break

    # Check if the specific substring (i.e., the exit phrase) is in the current line of output
    #if exit_phrase in output_line:
        #print(f"\nDetected substring '{exit_phrase}' in shell output. Terminating process.")
        #print("\n----------------------------------------------------------------------------------------------------\n") 
        #print('\nThe SPHARM-PDM computation has completed.')
        #sys.exit() # Terminate the script

    print(output_line, end='') # Print lines as they are being read

# Checking the process return code (0 typically means successful execution)
if run_spharm.returncode == 0:

    print("Command executed successfully.")

else:

    print("Command failed with return code", run_spharm.returncode)

####################################################################################################
# End script
####################################################################################################
