# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 20:33:13 2018

@author: davidtyrpak
"""
import os
import pandas as pd
import glob

def basename(filename):
    """basename is the filename after the prefix "background" or "nonbackground (e.g. basename('background_2_22_a.csv') == '2_22_a.csv')
   
   Parameters
   -----------
   filename: str, the filename including the extension (e.g. "background_2_22_a.csv")
   """
    basename = "_".join(filename.split("_")[1:])
    return basename
    
    

def CTCF(background_directory, nonbackground_directory, CTCF_results_directory, extension = ".csv"):
    """Corrected Total Cell Fluorescence
    CTCF = Integrated Density - (Area of selected cell * Mean fluorescence of background readings)
    
    Note that the Integrated Density (IntDen) in the above equation is the IntDen of the selected cell.
    
    Parameters
    -----------
    
    background_directory: str, the full path to the directory where your background fluorescence measurements and ROIsets are stored. Must be named background_output
    
    nonbackground_directory: str, the full path to the directory where your nonbackground fluorescence measurements and ROIsets are stored. Must be named nonbackground_output
    
    CTCF_results_directory: str, the full path to the directory where you want the CTCF measurements to be stored. Must be named CTCF_results
    
    extension: str, the file format of your results files. The default is ".csv" 
    """
    
    background_dir_list = os.listdir(background_directory) #list all files in background_directory
    nonbackground_dir_list = os.listdir(nonbackground_directory) #list all files in nonbackground_directory
    CTCF_results_dir_list = os.listdir(CTCF_results_directory) # list allfiles in CTCF_results_directory, should initially be empty
    
    
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
        
        IntDen = df_NonBackground.loc[0:nrows, "IntDen"].values
        
        Area = df_NonBackground.loc[0:nrows, "Area"].values
        
        df_NonBackground["CTCF"] = IntDen - Area * mean_background_intensity
        
        os.chdir(CTCF_results_directory)
        df_NonBackground.to_csv("CTCF_results_" + basename(background_file))
        
        i  = i + 1
    return
    
    

        
       
        
        
        
        
        
    
CTCF("/Users/davidtyrpak/Desktop/FIJI_playground/random_number_output/background_output", "/Users/davidtyrpak/Desktop/FIJI_playground/random_number_output/nonbackground_output", 
     "/Users/davidtyrpak/Desktop/FIJI_playground/random_number_output/CTCF_results")