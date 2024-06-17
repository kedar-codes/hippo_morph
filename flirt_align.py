import subprocess
import os
import glob

####################################################################################################
# User-defined variables (directories)
####################################################################################################

print("\nBeginning rigid (affine) alignment via FSL FLIRT.\n")

# Define the input directories that contain the .nii.gz segmentation masks to be registered
segmentation_masks_L_dir = '/path/to/your/left/hippocampal/masks/directory/'
segmentation_masks_R_dir = '/path/to/your/right/hippocampal/masks/directory/'

# Define the paths to the reference masks
reference_image_mask_L = '/path/to/your/left/registration/template.nii.gz'
reference_image_mask_R = '/path/to/your/right/registration/template.nii.gz'

# Define the output directories for the registered images (and create it if it doesn't exist)
output_directory_masks_L = '/path/to/your/left/output/directory/'
output_directory_masks_R = '/path/to/your/right/output/directory/'

if not os.path.exists(output_directory_masks_L):
    os.makedirs(output_directory_masks_L)
    print(output_directory_masks_L + " created.\n")

if not os.path.exists(output_directory_masks_R):
    os.makedirs(output_directory_masks_R)
    print(output_directory_masks_R + " created.\n")

# Use glob to find all .nii.gz files in the segmentation masks directories
segmentation_masks_L = glob.glob(os.path.join(segmentation_masks_L_dir, '*.nii.gz'))
segmentation_masks_R = glob.glob(os.path.join(segmentation_masks_R_dir, '*.nii.gz'))

# FLIRT options (parameters)
flirt_options = '-searchcost labeldiff -cost labeldiff -dof 6 -interp nearestneighbour'  # Example options; adjust as needed

####################################################################################################
# FLIRT for masks_L
####################################################################################################

print("Beginning alignment for left hippocampal masks.")

for mask_path_L in segmentation_masks_L:

    # Extract the filename without extension for output naming
    mask_name_L = os.path.splitext(os.path.basename(mask_path_L))[0]
    
    # Append "-aligned" to the filename before the extension
    output_filename_L = f'{mask_name_L}_aligned.nii.gz'
    output_path_L = os.path.join(output_directory_masks_L, output_filename_L)
    output_path_L = output_path_L.replace(".nii_aligned", "_aligned") # Remove the first ".nii"
    
    # Construct the FLIRT command
    flirt_command = f'flirt -in {mask_path_L} -ref {reference_image_mask_L} -out {output_path_L} {flirt_options}'
    
    # Execute the FLIRT command
    try:

        subprocess.run(flirt_command, check=True, shell=True)
        print(f'Registration successful for {mask_path_L}')

    except subprocess.CalledProcessError as e:
        
        print(f'Error during registration of {mask_path_L}: {e}')

####################################################################################################
# FLIRT for masks_R
####################################################################################################

print("\nBeginning alignment for right hippocampal masks.")

for mask_path_R in segmentation_masks_R:

    # Extract the filename without extension for output naming
    mask_name_R = os.path.splitext(os.path.basename(mask_path_R))[0]

    # Append "-aligned" to the filename before the extension
    output_filename_R = f'{mask_name_R}_aligned.nii.gz'
    output_path_R = os.path.join(output_directory_masks_R, output_filename_R)
    output_path_R = output_path_R.replace(".nii_aligned", "_aligned") # Remove the first ".nii"
    
    # Construct the FLIRT command
    flirt_command = f'flirt -in {mask_path_R} -ref {reference_image_mask_R} -out {output_path_R} {flirt_options}'
    
    # Execute the FLIRT command
    try:

        subprocess.run(flirt_command, check=True, shell=True)
        print(f'Registration successful for {mask_path_R}')

    except subprocess.CalledProcessError as e:
        
        print(f'Error during registration of {mask_path_R}: {e}')

####################################################################################################
# End script
####################################################################################################

print("\n----------------------------------------------------------------------------------------------------\n") 
print('\nAll registrations completed.')
