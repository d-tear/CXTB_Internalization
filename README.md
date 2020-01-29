# Corrected-Total-Cell-Fluorescence [![DOI](https://zenodo.org/badge/140611525.svg)](https://zenodo.org/badge/latestdoi/140611525)
Purpose: The pipeline implements an adaption and automation of a commonly used method called Corrected-Total-Cell-Fluorescence (CTCF), which determines the level of cellular fluorescence from fluorescence microscopy images. I created this pipeline to calculate fluorescent cholera toxin binding from super-resolution confocal z-stacks of individual cells. 
However, this pipeline could be adapted to study fluorescent singal in a variety of contexts.  Simply put, CTCF normalizes the integrated density of your regions of interest (ROIs)  by subtracting the background fluorescence in your image. You can read more about CTCF here: https://celldivisionlab.com/2015/08/12/using-imagej-to-measure-cell-fluorescence/
This pipeline has been used in two different publications to quantify fluorescent microscope images:

1) Caveolin Elastin-Like Polypeptide Fusions Mediate Temperature-Dependent Assembly of Caveolar Microdomains
David R. Tyrpak, Yue Wang, Hugo Avila, Hao Guo, Runzhong Fu, Anh T. Truong, Mincheol Park, Curtis T. Okamoto, Sarah F. Hamm-Alvarez, and J.A. MacKay
ACS Biomaterials Science & Engineering 2020 6 (1), 198-204
DOI: 10.1021/acsbiomaterials.9b01331

2) Cathepsin S activation contributes to elevated CX3CL1 (fractalkine) levels in tears of a Sjögren’s syndrome murine model. Fu, R., Guo, H., Janga, S. et al.  Sci Rep 10, 1455 (2020). https://doi.org/10.1038/s41598-020-58337-4


Note that this pipeline is modular. Depending on your needs, you can pick and choose different parts of the pipeline to answer your research question. For example, Random_filename_generator.py could be used to blind yourself to images which are then scored (e.g. histology slides, or a cellular phenotype). In my workflow I first acquired super-resoultion confocal z-stacks of cells and then converted the z-stacks into sum projection images (i.e. STEP 1, sum_projections.ijm) before measuring CTCF. However, the CTCF method is typically used with fluorescent microscopy images acquired from a single focal plane. With images acquired from a single focal plane, simply skip step 1 and begin the pipeline with step 2.
------------------------------------------------------------------------------------------------------------------------------
STEP 1) sum_projections.ijm is used to convert each z-stack image into a sum projection. 
input: 

1) input_directory: type string, the full path to the directory where your z-stack images are located

2) output_directory: type string, the full path to the directory where you want the sum intensity projection images to be saved

3) extension: type string, the image format (e.g. ".czi" )

output: 

1) sum projection images are saved in your specified output_directory

------------------------------------------------------------------------------------------------------------------------------
STEP 2) Random_filename_generator.py is used to rename each sum projection image with a 3 digit random number.

input: 

1)  input_directory: str type; the full path to the directory where your files are located. Should only contain files to be renamed.
    
2) output_directory: str type; the full path to the directory where your renamed files will be located. Must be empty.

3) extension: str type; the file format (e.g. ".txt", ".czi", ".csv", ".tif")

Note: Random_filename_generator.py can be used to randomly rename any type of file.

output:

1) Randomly renamed files in the specified output_directory

2)  The code will also generate two .csv files in the specified output_directory:
    1) Details.csv, which records a timestamp, username, hostname, etc
    2) Key.csv, which matches each random number renamed file with its original filename
------------------------------------------------------------------------------------------------------------------------------

STEP 3) Measure nonbackground: use roi_recorder.ijm to draw ROIs around cells of interest.
Note: when measuring nonbackground, output directory must be named "nonbackground_output"
input: 

1) input directory: type string, the full path to the directory where your randomly renamed images are located

2) output_directory: type string, the full path to the directory where you want the csv results file and roiset for each image to be save. Must be different from input_directory. if background = true, must be named "background_output" else "nonbackground_output". Note that each analyzed image will produce one csv file and one roiset (2 files total). 
Thus, at any given time, the output directory will have exactly twice as many files as there are entries in the records_file. 


3) records_file: type string, the full path, including filename, to the directory where your records_file is located. 
Note that the records_file records the images from which you have already taken ROIs/analyzed. This way, you can stop the program at any time and then pick up where you left off. Note that you must create an empty records file before you run this code for the first time. Note also thatif background  = true, the records_file must be named "background_records_file.txt" else "nonbackground_records_file.txt" 

4) extension: type string, the image format (e.g. ".czi" )

5) lineseparator: type string, used to identify each new line/entry in records_file (e.g. "\n" )

6) background: type boolean, if True, output_directory must be named "background_directory", else "nonbackground_directory"

7) channel: type int, the specific channel where you are taking measuremenets. Should be the same for both background and nonbackground measurments. 

output:  
Each image ouputs 
1) a csv file of measurements for each of its ROIs. 
2) an ROIset containing the ROIs for that image.

------------------------------------------------------------------------------------------------------------------------------
STEP 4) Measure background: use roi_recorder.ijm to draw ROIs around empty spaces in the channel of interest. To be accuarate, draw at least 3 background ROIs.
Note: when measuring background, output directory must be named "background_output"
input: Excatly the same as for STEP 3, EXCEPT: if you are measuring background, your output directory must be named
background_output and your records file must be named "background_records_file.txt"

output: The same as in STEP 3.
Each image outputs
1) a csv file of measurements for each of its ROIs.
2) an ROIset containing the ROIs for that image.

------------------------------------------------------------------------------------------------------------------------------
STEP 5) Use CTCF.CTCF (python file named CTCF, function named CTCF) to measure Corrected Total Cell Fluorescence (CTCF). CTCF is a simple method for normnalizing the integrated density of your nonbackground ROIs by subtracting the background fluorescence in your image. You can read more about CTCF here: https://celldivisionlab.com/2015/08/12/using-imagej-to-measure-cell-fluorescence/

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

------------------------------------------------------------------------------------------------------------------------------
STEP 6) Use CTCF.UnrandomRename (python file named CTCF, function named UnrandomRename) to update the Summary_CTCF_File from Step 5 with the original file name for each image.
In more detail: Up to this point, all your images have been renamed with a random number. To get back the original image names, you will now use CTCF.UnrandomRename to update the Summary_CTCF_File and convert the random nubmers back to their original filename.

input: 
1) Summary_CTCF_File: str, the full file path the Summary_CTCF_results.csv file produced by the CTCF function
    
2) Key: str, the full file path to the Key.csv file produced by the Random_filename_generator function
    
3) output_directory: str, the full file path where you want the Master.csv file, which contains the Summary_CTCF_results with
unrandomized file names, to be saved. There are no restrictions on output_directory

output:

1)  This function saves a Master_CTCF.csv file in the specified output_directory. You can upload this csv file into your statistics software of choice and explore whether there are differences in CTCF for your different treatments, **but be sure to average your CTCF results for each image by the number of cells/nonbackground ROIs you collected for that image!** . More details on why you need to average below.
-----------------------------------------------------------------------------------------------------------------------

**How CTCF is calculated and why you need to average your final CTCF value for each image by the number of cells/nonbackground ROIs you collected for that image:**

For both nonbackground and background csv files, the final summary row contains the following values for each named column:
IntDen column: The integrated density of all your individual ROIs treated as one ROI (Sum of individual ROI areas * The average of the mean gray values of your individual ROIs)

Area column: The sum of the individual areas from your ROIs
Mean column: The average of the mean gray values for each ROI.
There are likely other columns in csv files as well, but the code ignores these columns as they are not used to calculate CTCF

In your individual CTCF_results files (e.g. CTCF_results_994.csv) the CTCF for each individual nonbackground ROI is calculated as follows:
CTCF = (Integrated Density of Nonbackground ROI) – (The average of the mean gray values of your Background ROIs) *( Area of Nonbackground ROI)
The average of the mean gray values of your background ROIs is of course obtained from the final summary row of your background csv file, as mentioned above.
The CTCF value in the final summary row of your individual CTCF_results files (e.g. CTCF_results_994.csv) is calculated as follows:
CTCF in Final/Summary Row = (The integrated density of all your individual ROIs treated as one ROI) – (The Average of the Mean Gray Values of your Background ROIs) *( Sum of Areas of Nonbackground ROIs)
For brevity, we will refer to CTCF in Final/Summary Row as CTCF_Final. 
Note that The integrated density of all your individual ROIs treated as one ROI and Sum of Areas of Nonbackground ROIs are obtained from the final summary row of your nonbackground csv file, as mentioned above.

**Why you need to average your final CTCF value for each image by the number of cells/nonbackground ROIs you collected for that image:**

Each row in your Master_CTCF_results.csv and Summary_CTCF_results.csv file contains CTCF_Final for each image. Because CTCF_Final is obtained treating all your individual ROIs as one giant ROI, you will need to average each CTCF_Final value by the number of nonbackground ROIs you collected. For example, given two images with identical intensities and cells of identicial size, if in one image you analyzed ten cells (i.e. ten nonbackground ROIs) and in the second image you only analyzed five cells, the first image will have a higher CTCF_Final value simply because analyzed twice the area! 






