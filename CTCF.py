# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 20:33:13 2018

@author: davidtyrpak
"""
import os

def CTCF(background_directory, nonbackground_directory, CTCF_results_directory):
    """Corrected Total Cell Fluorescence
    CTCF = Integrated Density - (Area of selected cell * Mean fluorescence of background readings)
    
    Note that the Integrated Density (IntDen) in the above equation is the IntDen of the selected cell.
    
    Arguments
    -----------
    
    background_directory: str, the full path to the directory where your background fluorescence measurements and ROIsets are stored. Must be named background_output
    
    nonbackground_directory: str, the full path to the directory where your nonbackground fluorescence measurements and ROIsets are stored. Must be named nonbackground_output
    
    CTCF_results_directory: str, the full path to the directory where you want the CTCF measurements to be stored. Must be named CTCF_results
    
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
        
    
CTCF("/Users/davidtyrpak/Desktop/FIJI_playground/background_output", "/Users/davidtyrpak/Desktop/FIJI_playground/nonbackground_output", 
     "/Users/davidtyrpak/Desktop/FIJI_playground/CTCF_results")