import os
import subprocess
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed

##################################################
# User-defined variables

# Define the master directory containing all subdirectories with CSV files
master_directory = '/path/to/your/master/directory/'

# Define the paths to the template *spherical parameterization* VTKs for MFSDA_run.py (*_pp_surf_para.vtk)
L_sphere_template_vtk = '/path/to/your/left/spherical/parameterization/template_pp_surf_para.vtk'
R_sphere_template_vtk = '/path/to/your/right/spherical/parameterization/template_pp_surf_para.vtk'

# Define the paths to the template *shape VTKs* for MFSDA_createShapes.py (*_pp_surf_SPHARM.vtk)
L_template_mask_vtk = '/path/to/your/left/shape/template_pp_surf_SPHARM.vtk'
r_template_mask_vtk = '/path/to/your/right/shape/template_pp_surf_SPHARM.vtk'

# Define the maximum number of parallel processes
max_workers = 4  # Adjust this number based on the number of CPU cores you want to use

##################################################
# Functions

def get_covariates(csv_path):
    """Extract covariate names from the CSV file, skipping the first 'Subject' column."""
    df = pd.read_csv(csv_path)
    covariates = df.columns[1:]  # Skip the 'Subject' column
    return ' '.join(covariates)

def run_command(file_path, output_dir):
    """Run the MFSDA_run.py and MFSDA_createShapes.py commands for a given CSV file."""
    # Determine the appropriate VTK mask file and template based on the CSV file name
    filename = os.path.basename(file_path)
    if filename.startswith('L'):
        coord_data = L_sphere_template_vtk
        shape_vtk = L_template_mask_vtk
    elif filename.startswith('R'):
        coord_data = R_sphere_template_vtk
        shape_vtk = r_template_mask_vtk
    else:
        return f"\nSkipped {filename}: doesn't start with 'L' or 'R'"
    
    # Construct the command to run MFSDA_run.py
    mfsda_run_command = [
        'python', r'C:\Program Files\SlicerSALT 4.0.1\lib\SlicerSALT-5.1\qt-scripted-modules\MFSDA_run.py',
        '--shapeData', file_path,
        '--coordData', coord_data,
        '--outputDir', output_dir
    ]
    
    # Print the MFSDA_run.py command for verification
    print(f"\nRunning command: {' '.join(mfsda_run_command)}")
    
    # Run the MFSDA_run.py command and capture the result
    try:
        subprocess.run(mfsda_run_command, check=True)
        print(f"\nSuccessfully processed {filename} with MFSDA_run.py")
    except subprocess.CalledProcessError as e:
        return f"\nError processing {filename} with MFSDA_run.py: {e}"
    
    # Prepare the arguments for MFSDA_createShapes.py
    pvalues_file = os.path.join(output_dir, 'pvalues.json')
    efit_file = os.path.join(output_dir, 'efit.json')
    covariates = get_covariates(file_path)
    output_vtk = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.vtk")
    
    # Construct the command to run MFSDA_createShapes.py
    mfsda_create_shapes_command = [
        'python', r'C:\Program Files\SlicerSALT 4.0.1\lib\SlicerSALT-5.1\qt-scripted-modules\MFSDA_createShapes.py',
        '--shape', shape_vtk,
        '--pvalues', pvalues_file,
        '--efit', efit_file,
        '--covariates', covariates,
        '--output', output_vtk
    ]
    
    # Print the MFSDA_createShapes.py command for verification
    print(f"\nRunning command: {' '.join(mfsda_create_shapes_command)}")
    
    # Run the MFSDA_createShapes.py command and capture the result
    try:
        subprocess.run(mfsda_create_shapes_command, check=True)
        return f"\nSuccessfully processed {filename} with MFSDA_createShapes.py"
    except subprocess.CalledProcessError as e:
        return f"\nError processing {filename} with MFSDA_createShapes.py: {e}"

def find_csv_files(master_directory):
    """Find all CSV files in subdirectories starting with 'L' or 'R'."""
    csv_files = []
    for root, _, files in os.walk(master_directory):
        for filename in files:
            if filename.startswith(('L', 'R')) and filename.endswith('.csv'):
                csv_files.append(os.path.join(root, filename))
    return csv_files

if __name__ == '__main__':
    # Get a list of CSV files to process
    csv_files = find_csv_files(master_directory)

    # Run commands in parallel using ProcessPoolExecutor
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks for each CSV file
        futures = {
            executor.submit(run_command, file_path, os.path.dirname(file_path)): file_path 
            for file_path in csv_files
        }
        
        # Process results as they complete
        for future in as_completed(futures):
            result = future.result()
            print(result)
