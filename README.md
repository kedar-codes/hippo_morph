# hippo_morph
![spherical_harmonics](https://github.com/kedar-codes/hippo_morph/assets/172929607/833be570-14aa-4122-b9f9-3a11a0fa78b2)

Current code for my Python-based hippocampal morphometry pipeline, based on the hippodeep_pytorch segmentation program and the SlicerSALT shape analysis software.

Requires [hippodeep_pytorch](https://github.com/bthyreau/hippodeep_pytorch) and [SlicerSALT](https://salt.slicer.org/). For some functions of the pipeline (_i.e_., binarization, registration), [FSL](https://fsl.fmrib.ox.ac.uk/fsl/docs/#/) is optional, but highly recommended.

_Disclaimer: I am not affiliated in any way with the developers of these programs, nor does my code represent any official additions/modifications to the original programs. This pipeline is for academic research purposes only._

# Instructions for use:

1. Run `select_files_hippodeep.py`. This program will open a file explorer window in which the directory that contains the whole-brain T1-weighted MR images (in .nii format) is selected. After confirming that the folder and the files are correct, the _hippodeep_pytorch_ segmentation will begin. You will notice that your T1 image directory will populate with left and right hippocampal masks (in .nii format) for each of your subject images. 
   
2. Run `slicersalt_spharm.py`. This program will run the [SPHARM-PDM](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3062073/) computation on all hippocampal masks located in a directory specified within the script. Before running the program, please take note of the following:
   - Download the `SPHARM-PDM-parameters_blank.ini` config file and save it to an appropriate location, but _do not fill out the (blank) text fields in the config file itself_.
     
   - Instead, fill out the required fields (input directory path, output directory path, registration template file path, flip template file path) **in the** `slicersalt_spharm.py` **script**. Optionally, modify the other default settings as desired **in the config file**; refer to the [SlicerSALT documentation](https://salt.slicer.org/documentation/) and `SPHARM-PDM-parameters_template.ini` for explanations on the various settings and features. Set `regParaTemplateFileOn` to `False` if you wish to disable the (rigid) Procrustes alignment/registration feature and set `flipTemplateOn` to `False` to disable the flipping of the SPHARM output (this setting is sometimes necessary to correct the occassional flipped/rotated model that results from a shape with challenging geometry, especially something with a high degree of rotational symmetry).
     
   - Make sure your left and right masks are separated into their own directories. SPHARM-PDM should run on only one set of hippocampal masks (left or right) at a time. However, you can run two instances of this script in separate terminal windows if you wish—one for the left hippocampal masks and one for the right hippocampal masks.
     
   - Binarization of the hippocampal masks is highly recommended. The masks that result from _hippodeep_pytorch_ are not 100% binary; instead, the segmentations are probabilistic along the outer edges to account for the uncertainty of voxels and/or the partial volume effect along the perimeter of the hippocampus in native space. SPHARM-PDM works best with fewer errors when the masks are binary. The provided `bin_masks.py` script implements FSL's `fslmaths` tool to binarize a whole directory of hippocampal masks.
     
   - SPHARM-PDM requires that your input volumes conform to spherical topology, _i.e._, they **do not contain any holes or geometrical abnormalities**. Ensure that your hippocampal objects are free of such holes/handles and are contiguous in shape. Though _hippodeep_pytorch_'s outputs are generally error-free and SPHARM-PDM does its best to resolve any potential geometry issues, you may need to visually inspect the quality of your input segmentations and manually correct any errors.
     
   - This script calls upon SlicerSALT's command line tool for SPHARM-PDM (`SPHARM-PDM.py`) and pipes the output to your terminal. Make sure to note the path for your installation of SlicerSALT and replace the file path of `SPHARM-PDM.py` with the appropriate path.
     
   - SlicerSALT's command line tool for SPHARM-PDM may sometimes stall or error out on a particular mask for no apparent reason, without the ability to stop the program or skip to a less problematic mask. For large batches of files, it may be best to simply run SPHARM-PDM in SlicerSALT's GUI. Even then, an error may occur in which you will need to remove (or manually edit) the problematic mask and restart the SPHARM-PDM process/script. SlicerSALT/SPHARM-PDM will identify any completed outputs and will only re-run on any unprocessed input masks.
  
# Optional pre-SPHARM tools:

* As described above, use `bin_masks.py` to binarize the input masks before running SPHARM-PDM. This will result in fewer errors (flipped VTK models, etc.).
  
* `flirt_align.py` optionally uses [FLIRT](https://fsl.fmrib.ox.ac.uk/fsl/docs/#/registration/flirt/index) (FMRIB's Linear Image Registration Tool) to perform a linear registration/alignment of the input masks before SPHARM-PDM. Though SlicerSALT's SPHARM-PDM tool provides a built-in Procrustes registration function, FLIRT may sometimes provide better-aligned output models. Use instead of—or even in addition to—SlicerSALT's provided registration tools.

# Optional tools for post-SPHARM analyses:

SlicerSALT's SPHARM-PDM process simply generates correspondent surface meshes (in VTK file format) of the input volumes/masks. SlicerSALT contains a variety of modules and tools to perform any desired quantitative or statistical operations on these VTK models (see SlicerSALT's documentation). Though it is best to work in SlicerSALT's GUI for these modules, here are a few scripts that may help with any such analyses:

* `CST_MFSDA.py` allows for the automation of the "Covariate Significance Testing" module and is particularly useful for batch processing of multiple linear modeling computations (instead of using the SlicerSALT GUI for each instance). The script will search a chosen "master" directory and any subdirectories within for the CSV files that serve as inputs for the "Covariate Significance Testing" module (see documentation on the [SlicerSALT website](https://salt.slicer.org/documentation/)). The script operates by calling the `MFSDA_run.py` and `MFSDA_createShapes.py` functions included in the SlicerSALT binaries (The "Covariate Significance Testing" module is simply a GUI wrapper for these very functions).
  - **Important:** Ensure that each input CSV is housed within its own subdirectory so that no output files are overwritten (the outputs of each computation will be `pvalues.json`, `efit.json`, `out.vtk`, and `output.csv`).
 
  - The script assumes that the header of the first column in each CSV file is named "Subject"; you can change this, however.
 
  - The first column of each input CSV should contain the absolute file paths of all VTK shape models to be included in the regression computation. The following columns should include the variables/covariates associated with each shape model (age, sex, group, etc.).
 
  - **Important:** All variables must be numerical (i.e., no characters/strings). The MFSDA computation treats all integer variables as categorical and ordinal by default. In order to specify an integer variable as continuous (e.g., age), add a very small number to each number to make it a non-integer (e.g., 75 -> 75.00000001). Utilize one-hot/dummy-coding to specify non-ordinal categorical variables (e.g., Male = 0, Female = 1). 
 
  - As mentioned above, the script calls upon the `MFSDA_run.py` and `MFSDA_createShapes.py` functions provided by SlicerSALT. These functions have been developed independently from SlicerSALT and were collaboratively incorporated into the shape analysis software. All credit belongs to the original developers and their respective GitHub pages (as seen [here](https://github.com/DCBIA-OrthoLab/MFSDA_Python) and [here](https://github.com/BIG-S2/MFSDA_Python)). The scientific manuscript that details the MFSDA statistical method can be viewed on [PubMed Central](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6494085/).
 
  - The MFSDA process requires the spherical parameterization VTKs (for both left and right hippocampal shapes) to serve as templates for the regression computation. These VTK files are produced via SPHARM-PDM and can be found in the `Step3_ParaToSPHARMMESH` folder. Note that these models are _not_ the reconstructed SPHARM shape models, but rather the uniformly-sampled unit spheres from which the final SPHARM shapes are unparameterized (...reparameterized?) and reconstructed as triangular shape meshes; these models have the filename `*_pp_surf_para.vtk`. Since all shapes models in a single SPHARM-PDM computation are constructed from the same spherical parameterization, you can use any arbitrary spherical template generated by the SPHARM-PDM computation, provided that the models being statistically analyzed are from that very same SPHARM-PDM computation (or were created using identical input parameters/settings in another computation). Alternatively, you can use the spherical template generated by a registration template, given the same aforementioned conditions.
 
  - The script also requires two SPHARM shape VTKs (for both left and right hippocampal shapes) upon which to overlay the p-value/signficance maps. These VTK models _are_ the reconstructed SPHARM shape models and have the filename `*pp_surf_SPHARM.vtk`. You can use the SPHARM-generated registration template (recommended), an average VTK shape model, or any arbitrary VTK of your choosing, provided it contains the same SPHARM-PDM parameters/settings.
 
  - The MFSDA process is computationally intensive. The script allows you to set the number of CPU cores allocated to running the program (one regression computation per core) so that the system is bogged down by excessive CPU usage while still being able to run multiple analyses in parallel via Windows multi-threading.

* `dir2csv.py` is a simple script that creates a CSV file listing the full file paths of all the VTK files in the directories containing the left and right hippocampal VTK models. Modify the directory paths as needed. Particularly helpful for SlicerSALT's "Covariate Signficance Testing" module or `M2MD.py`.

* `check_files.py` is another simple script that goes through a given CSV file (such as one created with `dir2csv.py`) and checks to see if all of the files actually exist, according to their listed file paths. Useful for identifying errors when running SlicerSALT's "Covariate Significance Testing" module.

* `excel2csv.py` is a helpful script that can generate CSVs from each worksheet in a Microsoft Excel file. It's particularly useful to avoid the tedious task of manually saving each worksheet as a CSV file within Excel. The primary use-case for this script is for the preparation of statistical testing via `CST_MFSDA.py`, as each CSV file is saved into its own individual folder (as required by `CST_MFSDA.py`).
  
* `M2MD.py` allows for the batch processing of multiple VTK model pairs in SlicerSALT's 'Model to Model Distance' module (the GUI only allows for the processing of one pair at a time).
  - This module computes the vertex-by-vertex distances (as vectors) between correspondent points of both VTK models (a "source" and a "target"). Here, this script is intended to compute such vectors between VTK models representing a subject at two different timepoints.
    
  - A single CSV file listing all the model pairs **must** be used as an input for this script; refer to `M2MD_example.csv` as a template to structure this CSV file. Column 1 must have the header "Timepoint 1" and list the **full file path** of all subjects and their timepoint 1 models. Column 2 must have the header "Timepoint 2" and list the **full file path** of all the subjects and their corresponding timepoint 2 models, matched row by row. Column 3 must contain the header "Output" and the **basename** of the output VTK to be created, _not_ the file path or its .vtk extension.
    
  - As this script is written, the outputs for each model pair will be 1) a VTK file of the timepoint 1 model, encoding the computed distances between correspondent vertices (points) of both models, 2) a CSV file containing the normal projections of the point-to-point distance vectors (i.e., vectors computed by projecting the distance vectors onto their corresponding surface normals, thereby giving only the distance directly inward or outward relative/perpendicular to the surface), and 3) a CSV file (`M2MD_results.csv`) listing all the model pairs and their successfully created output files. Note that the distances between points are computed as (timepoint 2 - timepoint 1), and as such are relative to the timepoint 1 model.
    
  - `M2MD_results.csv` is particularly useful for `vtk_points2vectors.py` (see below).

* `vtk_points2vectors.py` is a script that "injects" a VTK model with 3D vector data and replaces the 3D coordinates with said vectors. It does this by locating both a base VTK model and a CSV file of vectors as specified by the `M2MD_results.csv` file created by the above `M2MD.py`; by default, the base VTK model and vector file are the "Timepoint 1 Model" and the corresponding "MagNormVectors File", respectively. Executing the script will perform this operation on all "Timepoint 1" models listed in `M2MD_results.csv`. Upon completion, the new VTK models will be located in the specified output directory with filenames beginning with `deltas_...vtk`; the base "Timepoint 1" VTK models will remain unmodified in their original directories.
  - The 3D vector data contained in each `...MagNormVectors.csv` file will replace the "POINTS" field of its corresponding "Timepoint 1" VTK model. Instead of listing 3D coordinates, the VTK model will now list 3D vectors (as xyz tuples).
    
  - Opening the new `deltas_...vtk` VTK models in 3D Slicer/SlicerSALT will display a nonsensical object in the Render View. **_This is normal and intended!_** The original VTK model contained 3D coordinates with polygon data instructing 3D Slicer/SlicerSALT on how to connect the points into a logical shape. However, with the "points" now being vectors, the program still tries to connect the "points" to create a shape, but the resulting object will appear illogical as the coordinates of the "points" have now changed to vector components instead.
 
  - The primary use-case for this script is to create VTK models that encode time-based vector deformations instead of simple coordinate data. These models can then be utilized in SlicerSALT's "Covariate Significance Testing" module. By creating VTK models with vector data instead of coordinate data, the "Covariate Significance Testing" module is tricked into accepting them as inputs for its statistical testing. Thus, the module will identify surface regions of signficantly different _change_ between groups, instead of simple differences in shape (_i.e._, What surface regions experienced significantly different deformations over time, between groups?). Note, however, that a standard VTK shape model is required as a template upon which to view the significance/_p_-value map.
