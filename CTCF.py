# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 20:33:13 2018

@author: davidtyrpak
"""
import os
import pandas as pd
import glob

def listdir_nohidden(path):
    """
    Description
    -----------
    This function returns a list of all nonhidden files in the directory specified by path
    
    Parameters
    -----------
    
    path: str, the full path to the directory
    
    Returns
    -------
    
    returns a list containing all nonhidden files in the directory. 
    """
    return glob.glob(os.path.join(path, '*'))
   

def basename(filename):
    """basename is the filename after the prefix "background" or "nonbackground (e.g. basename('background_2_22_a.csv') == '2_22_a.csv')
   
   Parameters
   -----------
   filename: str, the filename including the extension (e.g. "background_2_22_a.csv")
   """
    basename = "_".join(filename.split("_")[1:])
    return basename
    
    

def CTCF(background_directory, nonbackground_directory, CTCF_results_directory, extension = ".csv"):
    """
    Description
    ------------
    This function calculates Corrected Total Cell Fluorescence (CTCF)
    
    CTCF = Integrated Density - (Area of selected cell * Mean fluorescence of background readings)
    
    Note that the Integrated Density (IntDen) in the above equation is the IntDen of the selected cell.
    
    Workflow
    ---------
    
    Random_filename_generator.py --> roi_recorder.ijm --> CTCF.CTCF.py --> CTCF.UnrandomRename.py
     
    Parameters
    -----------
    
    background_directory: str, the full path to the directory where your background fluorescence measurements and ROIsets are stored. Must be named background_output
    
    nonbackground_directory: str, the full path to the directory where your nonbackground fluorescence measurements and ROIsets are stored. Must be named nonbackground_output
    
    CTCF_results_directory: str, the full path to the directory where you want the CTCF measurements to be stored. Must be named CTCF_results
    
    extension: str, the file format of your results files. The default is ".csv" 
    
    Returns
    -------
    
   This function does not return anything
    
   This function calculates the CTCF for each background/nonbackground pair. These CTCF results are saved in csv files in the specified
   CTCF_results_directory.
   
   This function also creates a "Summary_CTCF_results.csv" file. This file appends the
   summary rows from each individual CTCF results csv file. Summary_CTCF_results.csv
   is also saved in the specified CTCF_results directory.
    
    
    """
    
    background_dir_list = listdir_nohidden(background_directory) #list all nonhidden files in background_directory
    nonbackground_dir_list = listdir_nohidden(nonbackground_directory) #list all nonhidden files in nonbackground_directory
    CTCF_results_dir_list = listdir_nohidden(CTCF_results_directory) # list all nonhidden files in CTCF_results_directory. Should initially be empty (except for hidden files)
    
    
    ##The below if statements ensure that the directories are properly specified, have the correct number of files, and that we are not overwriting results
    if len(background_dir_list) != len(nonbackground_dir_list): 
        raise RuntimeError("Warning! Your background_directory and nonbackground_directory must have an equal number of files.")
        
    if len(background_dir_list) == 0:
        raise RuntimeError("Warning! Your background_directory is empty.")
        
    if len(nonbackground_dir_list) == 0:
        raise RuntimeError("Warning! Your nonbackground_directory is empty.")
        
    if len(CTCF_results_dir_list) != 0:
        raise RuntimeError("Warning! Your CTCF_results_directory is not empty. Have you run this analysis before or misspecified the directory?")
    
    ## The below if statements ensure that the directories are properly named. Naming standards enhance reproducibility
    # Note that these are the same naming standards that are enforced in roi_recorder.ijm
    if os.path.basename(background_directory) != "background_output":
        raise RuntimeError("Warning! Your background_directory must be named 'background_output'.")
    
    if os.path.basename(nonbackground_directory) != "nonbackground_output":
        raise RuntimeError("Warning! Your background_directory must be named 'nonbackground_output'.")
    
    if os.path.basename(CTCF_results_directory) != "CTCF_results":
        raise RuntimeError("Warning! Your CTCF_results_directory must be named 'CTCF_results'.")
###This is the end of the intial test cases###    
    
    #find all csv files in background directory
    os.chdir(background_directory)
    background_csv_files = [i for i in glob.glob('*{}'.format(extension))] ##find all the csv files in the background directory
    background_csv_file_basenames = [basename(i) for i in background_csv_files] #the basename is the file name after "background"
    
     
    
    #find all csv files in nonbackground directory
    os.chdir(nonbackground_directory)
    nonbackground_csv_files = [i for i in glob.glob('*{}'.format(extension))]
    nonbackground_csv_file_basenames = [basename(i) for i in nonbackground_csv_files] #the basename is the file name after "nonbackground"
    
    
    ##background and nonbackground files should have exactly the same basenames. The only difference in their filesnames is the prefix "background" or "nonbackground"
    if nonbackground_csv_file_basenames != background_csv_file_basenames:
        raise RuntimeError("""Warning! Your background and nonbackground directories do not have corresponding results files. 
        Each image should have a background results file and a nonbackground results file.""")
    
    ##Create empty pandas df which will be our Summary csv file
    df_Summary = pd.DataFrame(columns = ["Nonbackground_Input_File_Name", "Background_Input_File_Name", "CTCF_Summary","Number_of_Cells"])
    CTCF_list = []
    ncells_list = []
    
    
    i = 0 #index used to go through nonbackground_csv_files
    for background_file in background_csv_files:
        
        ##go to the background directory and caculate the mean intensity of the background ROIs
        os.chdir(background_directory)
        df_Background = pd.read_csv(background_file) # convert csv file to pandas df
        
        nrows = df_Background.shape[0] # find the number of rows in the df
        
        mean_background_intensity = df_Background.loc[df_Background.index[nrows - 1], "Mean"] ##The mean of the mean background measurements. The column name is "Mean"
        
        ##go to nonbackground directory and extract the IntDen and Area for each nonbackground ROI
        os.chdir(nonbackground_directory)
        
        assert(basename(nonbackground_csv_files[i]) == basename(background_file))
        
        df_NonBackground = pd.read_csv(nonbackground_csv_files[i])
        
        nrows = df_NonBackground.shape[0]
        
        ncells = nrows - 1 #The number of cells/ROIs equals the number of rows minus the final summary row
        
        IntDen = df_NonBackground.loc[0:nrows, "IntDen"].values
        
        Area = df_NonBackground.loc[0:nrows, "Area"].values
        
        CTCF_ = IntDen - Area * mean_background_intensity ##CTCF_ (with underscore) to distinguish from the function CTCF. Note that CTCF_ is a list
        
        df_NonBackground["CTCF"] = CTCF_
        
        os.chdir(CTCF_results_directory)
        df_NonBackground.to_csv("CTCF_results_" + basename(background_file), index = False)
        
        CTCF_list.append(CTCF_[-1]) ##Append the last CTCF_ value/theSummary CTCF_ value. CTCF_ is a list (Because CTCF measurment is calculated for each Cell/ROI)
        ncells_list.append(ncells)
        
        i  = i + 1
        
    df_Summary["Nonbackground_Input_File_Name"] = nonbackground_csv_files
    df_Summary["Background_Input_File_Name"] = background_csv_files
    df_Summary["Number_of_Cells"] = ncells_list
    df_Summary["CTCF_Summary"] = CTCF_list
     
    df_Summary.to_csv("Summary_CTCF_results.csv", index = False)
    
   
    return
    
def UnrandomRename(Summary_CTCF_File, Key, output_directory):
    
    """
    Description
    ------------
    This function unrandomizes file names which were randomized with the Random_filename_generator function
    
    Workflow
    ------------
    Random_filename_generator.py --> roi_recorder.ijm --> CTCF.CTCF.py --> CTCF.UnrandomRename.py
    
    Parameters
    -----------
    Summary_CTCF_File: str, the full file path the Summary_CTCF_results.csv file produced by the CTCF function
    
    Key: str, the full file path to the Key.csv file produced by the Random_filename_generator function
    
    output_directory: str, the full file path where you want the Master.csv file, which contains the Summary_CTCF_results with
    unrandomized file names, to be saved. There are no restrictions on output_directory
    
    Returns
    -------
    This function does not return anything.
    
    This function saves a Master_CTCF.csv file in the specified output_directory
    
    """
    
    
    df_Summary = pd.read_csv(Summary_CTCF_File)
    df_Key = pd.read_csv(Key)
    
    
    
    nrows_key = df_Key.shape[0] #number of rows in Key file
    row_index = 0 
    random_dict = {} #key is random filename, and value is the original filename
    
    ##go through Key file and collect random numbers and their corresponding original filenames
    while row_index < nrows_key: ##go through each row in the Key file
        random_filename = df_Key.loc[row_index, "random_number"] #collect the random number from Key.csv
        
        original_filename = df_Key.loc[row_index, "filename"] #collect its corresponding original filename from Key.csv
        
        random_dict[random_filename] = original_filename #key is random number, value is original filename
        row_index = row_index + 1
        
    ##Now we will go through the Summary_CTCF_File, go to the column named "Input_File_Name", and match each filename with its original fielname via random_dict 
    original_filename_list = []
    nrows_summary = df_Summary.shape[0]
    row_index = 0
    random_number_list = []
    while row_index < nrows_summary:
        
        random_csvfile_name = df_Summary.loc[row_index, "Nonbackground_Input_File_Name"] # (e.g. "nonbackground_256.csv")
        
        base_filename = basename(random_csvfile_name) #(e.g. "256.csv")
        
        random_number = base_filename.split(".")[0] # (e.g. "256", the random number/part of the filename before the file format extension)
        
        random_number = int(random_number) #remember that base_filename is a random number, but because we use the random number as filename, we converted the random number to a string
        
        assert(type(random_number) == int)
        
        random_number_list.append(random_number)
        
        filename = random_dict[random_number] 
        
        original_filename_list.append(filename)
        
        row_index = row_index + 1
    
    df_Summary["Original_Image"] = original_filename_list
    df_Summary["Random_Number"] = random_number_list
    
    os.chdir(output_directory)
    
    df_Summary.to_csv("Master_CTCF.csv", index = False)
        
    return    
        
    
CTCF("/Volumes/Untitled/CXTB_Internalization/Master/SumProjections/Randomized_Filenames/background_output", "/Volumes/Untitled/CXTB_Internalization/Master/SumProjections/Randomized_Filenames/nonbackground_output", 
     "/Volumes/Untitled/CXTB_Internalization/Master/SumProjections/Randomized_Filenames/CTCF_results")

UnrandomRename("/Volumes/Untitled/CXTB_Internalization/Master/SumProjections/Randomized_Filenames/CTCF_results/Summary_CTCF_results.csv",
               "/Volumes/Untitled/CXTB_Internalization/Master/SumProjections/Randomized_Filenames/Key.csv", "/Volumes/Untitled/CXTB_Internalization/Master/SumProjections/Randomized_Filenames/CTCF_results")    