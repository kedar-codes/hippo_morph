import os
import vtk
from vtk import *
import numpy as np
import pandas as pd

####################################################################################################
# User-defined variables (directories)
####################################################################################################

csv_file = r"/path/to/your/M2MD_results.csv"

output_dir = r"/path/to/your/output/directory/"

# Make sure the output directory exists, and create it if not
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

####################################################################################################
# Define custom functions
####################################################################################################

def read_vtk(filename):

    # Read all the data from the file
    reader = vtk.vtkPolyDataReader() # Create a reader object to read the data from the file
    reader.SetFileName(filename) # Set the filename of the reader object to be read
    reader.Update() # Update the reader object with new data from file

    polydata = reader.GetOutput() # Get output of the reader object and store it in a polydata variable

    points = polydata.GetPoints() # Get points from polydata and store it in points variable

    numPoints = points.GetNumberOfPoints() # Get number of points in points variable and store it in a numPoints variable

    pointCoordinates = np.zeros((numPoints,3)) # Create an arrray with zeros with size numPoints x 3 and store it in pointCoordinates variable

    for i in range(0, numPoints): # Loop through all the points in points variable

            pointCoordinates[i, :] = points.GetPoint(i) # Get the coordinates of each point and store it in pointCoordinates vairable

    return pointCoordinates

####################################################################################################

def write_vtk(filename, data):

    numPoints = data.shape[0] # Get number of rows in data and store it in numPoints variable

    polydata = vtk.vtkPolyData() # Create a polydata object to store the data to be written into a file

    points = vtk.vtkPoints() # create a vtkPoints object to store the coordinates of each point

    for i in range(0, numPoints): # Loop through all the rows in data

        points.InsertNextPoint(data[i, 0], data[i,1], data[i, 2]) # Insert the next point into vtkPoints object with coordinates from each row of data

    polydata.SetPoints(points) # Set the points of polydata object with vtkPoints object created above

    writer = vtk.vtkPolyDataWriter() # Create a writer object to write the data into a file

    writer.SetFileVersion(51) # IMPORTANT: This will write out the VTK in 5.1 file format, for compatibility when opening in SlicerSALT for Windows. Change to 42 (for VTK DataFile version 4.2) if using SLicerSALT for Linux.

    writer.SetFileName(filename) # Set the filename of the writer object to be written

    writer.SetInputData(polydata) # Set the input data of the writer object with the polydata created above

    writer.Write() # Write the data into a file

####################################################################################################

def write_vtk_from_csv(filename, csv_path):

    data = []

    with open(csv_path, 'r') as f:

        lines = f.readlines()

        for line in lines:

            data.append([i for i in map(float, line.split(','))])

    return write_vtk(filename, np.array(data))

####################################################################################################
# Begin program
####################################################################################################

# Load the CSV file (M2MD_results.csv) with headers
m2md_data = pd.read_csv(csv_file)

# Set column 1 (Timepoint 1 Model) as 'base_VTKs' and column 4 ('MagNormVectors File) as 'mnv_files'
base_VTKs = m2md_data['Timepoint 1 Model']
m2md_VTKs = m2md_data['Output M2MD Model']
mnv_files = m2md_data['MagNormVectors File']

for base_VTK, m2md_VTK, mnv_file in zip(base_VTKs, m2md_VTKs, mnv_files):
     
     print("\n####################################################################################################")
     print("\nOriginal (base) VTK file found: " + base_VTK)
     print("\nCorresponding MagNormVectors CSV file found: " + mnv_file)

     # Read VTK file using above function
     vtk_data = read_vtk(base_VTK)
     print("\nPOINTS data from base VTK file:\n\n", vtk_data)

     # Get the basename for the deltas VTK model to be created, using the 'Output M2MD Model' from the input CSV
     vtk_basename = os.path.splitext(os.path.basename(m2md_VTK))[0]

     # Create the filename for the deltas VTK model to be created (append 'deltas_' and '.vtk' to vtk_basename)
     new_VTK_filename = "deltas_" + vtk_basename + ".vtk"

     # Create the full path for the deltas VTK model to be created
     new_VTK_fullpath = (output_dir + "/" + new_VTK_filename) # Change to "\\" if using Windows

     # Write data from the MagNormVectors CSV file to the VTK model
     write_vtk_from_csv(new_VTK_fullpath, mnv_file)
     print("\nPOINTS data from base VTK file replaced with vector data from MagNormVectors CSV file.")

     # Split on newLine to get polygon data
     with open(base_VTK) as f:
          
          polygons = f.read().split('\n\n')[1]

          f.close()

     # Append base_VTK's original polygon data to new VTK file
     vtkfile = open(new_VTK_fullpath, 'a+')
     vtkfile.write(polygons)
     vtkfile.close()

     print("\nNew VTK file created:", new_VTK_fullpath)
     print("\nPOINTS data from new VTK file:\n\n", read_vtk(new_VTK_fullpath))

####################################################################################################
# End script
####################################################################################################

print("\n####################################################################################################")
print("\nAll modified VTK files have been created and are located in: ", output_dir)
