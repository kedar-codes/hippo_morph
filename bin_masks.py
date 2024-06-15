import subprocess
import os
import glob

####################################################################################################
# User-defined variables (directories)
####################################################################################################

print("\nBeginning rigid binarization via fslmaths.\n")

# Define the input directories that contain the .nii.gz segmentation masks to be binarized
segmentation_masks_L_dir = 'path/to/your/left/segmentation/masks/'
segmentation_masks_R_dir = 'path/to/your/right/segmentation/masks/'

# Define the output directories for the binarized images (and create it if it doesn't exist)
output_directory_masks_L = 'path/to/your/binarized/left/outputs/'
output_directory_masks_R = 'path/to/your/binarized/right/outputs/'

if not os.path.exists(output_directory_masks_L):
    os.makedirs(output_directory_masks_L)
    print(output_directory_masks_L + " created.\n")

if not os.path.exists(output_directory_masks_R):
    os.makedirs(output_directory_masks_R)
    print(output_directory_masks_R + " created.\n")

# Use glob to find all .nii.gz files in the segmentation masks directories
segmentation_masks_L = glob.glob(os.path.join(segmentation_masks_L_dir, '*.nii.gz'))
segmentation_masks_R = glob.glob(os.path.join(segmentation_masks_R_dir, '*.nii.gz'))

####################################################################################################
# fslmaths binarization for masks_L
####################################################################################################

print("Beginning binarization for left hippocampal masks.\n")

for mask_path_L in segmentation_masks_L:

    # Extract the filename without extension for output naming
    mask_name_L = os.path.splitext(os.path.basename(mask_path_L))[0]
    
    # Append "-aligned" to the filename before the extension
    output_filename_L = f'{mask_name_L}_bin.nii.gz'
    output_path_L = os.path.join(output_directory_masks_L, output_filename_L)
    output_path_L = output_path_L.replace(".nii_bin", "_bin") # Remove the first ".nii"
    
    # Construct the fslmaths -bin command
    fslmaths_command = f'fslmaths {mask_path_L} -bin {output_path_L}'
    
    # Execute the fslmaths -bin command
    try:

        subprocess.run(fslmaths_command, check=True, shell=True)
        print(f'Binarization successful for {mask_path_L}')

    except subprocess.CalledProcessError as e:
        
        print(f'Error during binarization of {mask_path_L}: {e}')

####################################################################################################
# fslmaths binarization for masks_R
####################################################################################################

print("\nBeginning binarization for right hippocampal masks.\n")

for mask_path_R in segmentation_masks_R:

    # Extract the filename without extension for output naming
    mask_name_R = os.path.splitext(os.path.basename(mask_path_R))[0]

    # Append "-aligned" to the filename before the extension
    output_filename_R = f'{mask_name_R}_bin.nii.gz'
    output_path_R = os.path.join(output_directory_masks_R, output_filename_R)
    output_path_R = output_path_R.replace(".nii_bin", "_bin") # Remove the first ".nii"
    
    # Construct the fslmaths -bin command
    fslmaths_command = f'fslmaths {mask_path_R} -bin {output_path_R}'
    
    # Execute the fslmaths -bin command
    try:

        subprocess.run(fslmaths_command, check=True, shell=True)
        print(f'Binarization successful for {mask_path_R}')

    except subprocess.CalledProcessError as e:
        
        print(f'Error during binarization of {mask_path_R}: {e}')

####################################################################################################
# End script
####################################################################################################

print("\n----------------------------------------------------------------------------------------------------\n") 
print('\nAll binarizations completed.')
