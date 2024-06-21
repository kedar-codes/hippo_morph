# IMPORTANT: This script must be executed in 3D Slicer/SlicerSALT's Python interpreter (copy/paste the 'exec' command below)
# IMPORTANT: Follow the template as specified in 'M2MD_example.csv'.
# Column 1 of the CSV file should have header 'Timepoint 1' and contain the FULL PATH of the VTK model
# Column 2 of the CSV file should have header 'Timepoint 2' and contain the FULL PATH of the VTK model
# Column 3 of the CSV file should have header 'Output' and contain ONLY the basename of the output file to be created (NO path, NO '.vtk' extension)

import numpy as np
import pandas as pd
import os
import slicer

# exec(open(r"/path/to/M2MD.py").read())

# Path to the CSV file
csv_file = r"/path/to/your/CSV/file.csv"

# Output directory path
output_dir = r"/path/to/your/output/directory/"

# Make sure output directory exists, and create it if not
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load the CSV file with headers
data = pd.read_csv(csv_file)

# Set column 1 (Timepoint 1) as 'tp1_subjects' and column 2 (Timepoint 2) as 'tp2_subjects'; Set column 3 (Output VTKs) as the output VTK to be created
tp1_subjects = data['Timepoint 1']
tp2_subjects = data['Timepoint 2']
output_subjects = data['Output']

# Initialize a two-column array for a final CSV file (M2MD_results.csv) containing all the model file paths and their corresponding MagNormVectors.csv files (useful for 'vtk_points2vectors.py')
results_array = pd.DataFrame(columns = ['Timepoint 1 Model', 'Timepoint 2 Model', 'Output M2MD Model', 'MagNormVectors File'])

# Iterate through a loop, where SlicerSALT's 'Model to Model Distance' module is performed on a matched pair of VTK files (tp1_subj and tp2_subj) to create the output VTK (output_subj)
for tp1_subj, tp2_subj, output_subj in zip(tp1_subjects, tp2_subjects, output_subjects):

    # Load timepoint 1, timepoint 2 models in Slicer
    model1 = slicer.util.loadModel(tp1_subj)
    model2 = slicer.util.loadModel(tp2_subj)

    # Create new output node to assign difference to
    output_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", output_subj)

    # Set parameters for SlicerSALT's 'Model to Model Distance' module
    params = {'vtkFile1': model1.GetID(), 'vtkFile2': model2.GetID(), 'vtkOutput': output_node.GetID(), 'distanceType': 'corresponding_point_to_point', 'targetInFields': False}

    # Execute 'Model to Model Distance' module using the above parameters
    slicer.cli.runSync(slicer.modules.modeltomodeldistance, None, parameters=params)

    # Get node in proper format for array extraction
    model_node = slicer.util.getNode(output_node.GetID())

    # Convert node to array of MagNormVector data
    MagNormVectors = slicer.util.arrayFromModelPointData(model_node, 'MagNormVector')

    # Construct output model filename
    output_model_fullpath = (output_dir + "\\" + output_subj + ".vtk")

    # Save output .vtk models in output directory
    slicer.util.saveNode(output_node, output_model_fullpath)
    print("\nOutput model (Model to Model Distance) created: " + output_model_fullpath)

    # Construct output MagNormVectors filename
    magNormVectors_output_fullpath = (output_dir + "\\" + output_subj + "_MagNormVectors.csv")
    print("Output file for MagNormVector distances created: " + magNormVectors_output_fullpath)

    # Save output MagNormVectors.csv file in output directory
    np.savetxt(magNormVectors_output_fullpath, MagNormVectors, delimiter=",", comments='')

    # Append timepoint 1 file path, timepoint 2 file path, output model file path, and new MagNormVectors.csv to results_array
    new_row = {'Timepoint 1 Model': tp1_subj, 'Timepoint 2 Model': tp2_subj, 'Output M2MD Model': output_model_fullpath, 'MagNormVectors File': magNormVectors_output_fullpath}
    results_array = pd.concat([results_array, pd.DataFrame([new_row])], ignore_index=True)

# Save results_array as a CSV file (M2MD_results.csv)
results_array_fullpath = (output_dir + "/" + "M2MD_results.csv") # Change to "\\" if using Windows
results_array.to_csv(results_array_fullpath, index=False)

print("\nView all model pairs and output files in M2MD_results.csv.")

print("\nModel to Model Distance batch processing script has completed.\n")
