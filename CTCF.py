# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 20:33:13 2018

@author: davidtyrpak
"""

def CTCF(background_directory, nonbackground_directory, results_directory):
    """Corrected Total Cell Fluorescence
    CTCF = Integrated Density - (Area of selected cell * Mean fluorescence of background readings)
    
    Note that the Integrated Density (IntDen) in the above equation is the IntDen of the selected cell.
    
    Arguments
    -----------
    
    background_directory: str, the full path to the directory where your background fluorescence measurements and ROIsets are stored
    
    nonbackground_directory: str, the full path to the directory where your nonbackground fluorescence measurements and ROIsets are stored. 
    
    results_directory: str, the full path to the directory where you want the CTCF measurements to be stored.
    
    """
    
    
    
    