# CXTB_Internalization
Purpose: This pipeline is used to calculate fluorescsnet cholera toxin (CXTB) internalization from confocal z-stacks. 
However, this pipeline could be adapted to study fluorescent ligand internalization in a variety of contexts. 

Step 1) sum_projections.ijm is used to convert each z-stack image into a sum projection. 
input: confocal z-stack images
output: sum projection images

Step 2) Random_filename_generator.py is used to rename each sum projection image with a 3 digit random number.
input: the sum projection images from sum_projections.ijm
output: randomly renamed sum projection images
Note: Random_filename_generator.py can actually be used to randomly rename any type of file.

Step 3) Measure nonbackground: use roi_recorder.ijm to draw ROIs around cells of interest.
Note: when measuring nonbackground, output directory must be named "nonbackground_output"
input: 
1) The randomly renamed sum projection images output from Random_filename_generator.py
2) absolute path to an emtpy .txt file named "nonbackground_records_file.txt"
output:  
Each image ouputs 
1) a csv file of measurements for each of its ROIs. 
2) an ROIset containing the ROIs for that image.

Step 4) Measure background: use roi_recorder.ijm to draw ROIs around empty spaces in the channel of interest.
Note: when measuring background, output directory must be named "background_output"
input:
1) The randomly renamed sum projection images output from Random_filename_generator.py (the same images
you measured nonbackground)
2) absolute path to an emtpy .txt file named "background_records_file.txt"
output:
Each image outputs
1) a csv file of measurements for each of its ROIs.
2) an ROIset containing the ROIs for that image.

Step 5) Use CTCF.CTCF (python file named CTCF, function named CTCF) to measure Corrected Total Cell Fluorescence (CTCF). CTCF is a simple method for normnalizing the integrated density of your nonbackground ROIs by subtracting the background fluorescnce in your image. You can read more about CTCF here: https://celldivisionlab.com/2015/08/12/using-imagej-to-measure-cell-fluorescence/

input:

1) background_directory: str, the full path to the directory where your background fluorescence measurements and ROIsets are stored. Must be named background_output

2) nonbackground_directory: str, the full path to the directory where your nonbackground fluorescence measurements and ROIsets are stored. Must be named nonbackground_output
    
3) CTCF_results_directory: str, the full path to the directory where you want the CTCF measurements to be stored. Must be named "CTCF_results"
    
4) extension: str, the file format of your results files. The default is ".csv" 

output:

1) This function calculates the CTCF for each background/nonbackground pair. These CTCF results are saved in csv files in the specified CTCF_results_directory.
   
2) This function also creates a "Summary_CTCF_results.csv" file. This file appends the
summary rows from each individual CTCF results csv file. Summary_CTCF_results.csv
is also saved in the specified CTCF_results directory.

Step 6) Use CTCF.UnrandomRename (python file named CTCF, function named UnrandomRename) to update the Summary_CTCF_File from Step 5 with the original file name for each image.
In more detail: Up to this point, all your images have been renamed with a random number. To get back the original image names, you will now use CTCF.UnrandomRename to update the Summary_CTCF_File and convert the random nubmers back to their original filename.

input: 
1) Summary_CTCF_File: str, the full file path the Summary_CTCF_results.csv file produced by the CTCF function
    
2) Key: str, the full file path to the Key.csv file produced by the Random_filename_generator function
    
3) output_directory: str, the full file path where you want the Master.csv file, which contains the Summary_CTCF_results with
unrandomized file names, to be saved. There are no restrictions on output_directory

output:

1)  This function saves a Master_CTCF.csv file in the specified output_directory. You can upload this csv file into your statistics software of choice and explore whether there are differences in ligand internalization for your different treatments. 


