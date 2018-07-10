# -*- coding: utf-8 -*-
"""
Created on Tue May  3 17:40:28 2016

@author: davidtyrpak
"""
import getpass
import socket
import time
import sys
import pandas as pd
import os
import random
from shutil import copyfile
import glob

def listdir_nohidden(path): ## this function returns all the files in a directory, ignoring hidden files (those starting with ".")
    return glob.glob(os.path.join(path, '*'))


input_directory = "/Users/davidtyrpak/Desktop/python_playground"
output_directory = "/Users/davidtyrpak/Desktop/python_playground/output" ##Make sure this directory is empty!
extension = ".txt"

if len(listdir_nohidden(output_directory)) != 0:
    raise RuntimeError("Warning! Your output_directory is not empty! Please choose an empty directory.")


i = 0
file_list = []
    
for f in os.listdir(input_directory):
    if f.endswith(extension):
        i+=1
        file_list.append(f)
        
    
if len(file_list) == 0:
    raise RuntimeError("Warning! Your input directory has no %s files." % (extension))


 ## This for loop copies the files from the input directory into the output directory
for file in file_list:
    full_file_name = os.path.join(input_directory, file)
    copyfile(full_file_name, os.path.join(output_directory, file)) ## copy file to output directory

output_list = []
for f in os.listdir(output_directory):
    if f.endswith(extension):
        output_list.append(f)

assert(len(file_list) == len(output_list)) 

## generate random numbers for each file

random_list = []

while len(random_list) < len(file_list):
    n = random.randint(100, 999) ### Integer from 100 to 999, endpoints included
    assert(len(file_list) <= (900)) #100 to 999, including both endpoints, equals 900 possible numbers
    if n not in random_list:
        random_list.append(n)
    else:
        pass


assert(len(file_list) == len(output_list) and len(file_list) == len(random_list))

## create empty dictionary. This will store original filenames and their corresponding random number.
number_to_filename_dict = {} 
i = 0
for file in output_list:
    os.rename(os.path.join(output_directory, file), os.path.join(output_directory, str(random_list[i]) + extension))
    number_to_filename_dict[file] = random_list[i]
    i = i + 1
    
  

####Now we create Key.csv; Key.csv records the original filename for each random number

data = list(number_to_filename_dict.items()) #this gets your data (which is type dictionary) into the prpoer format for pd.Dataframe

key_df = pd.DataFrame(data, columns = ["filename", "random_number"]) ##convert number_to_filename_dict into a pd Dataframe

key_df.to_csv(os.path.join(output_directory, r'Key.csv'), index = False) ##write key_df into a csv file located in the output directory
    

####Now we create Details.csv, which records python version, input_directory, output_directory, timestamp, username, etc

#time stamps/ts
ts = time.time() 
readable = time.ctime(ts) ##human readable form
#hostname and username
hostname = socket.gethostname()
username = getpass.getuser()


details_dict = {"version": sys.version, "input_directory":input_directory, "output_directory":output_directory, "time_stamp":readable,
"hostname":hostname, "username": username}

details = list(details_dict.items())
details_df = pd.DataFrame(details)

details_df.to_csv(os.path.join(output_directory, r'Details.csv'), index=False, header = False)
