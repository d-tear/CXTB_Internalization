# -*- coding: utf-8 -*-
"""
Created on Tue May  3 17:40:28 2016

@author: davidtyrpak
"""
import getpass
import socket
import time
import datetime
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
        print(i)
    
        if i==0:
            print("There are no files in this folder!")
        else:
            pass


number_of_files = len(file_list) 


output_file_list = [] ## This for loop copies the files from the input directory into the output directory
for file in file_list:
    full_file_name = os.path.join(input_directory, file)
    copyfile(full_file_name, os.path.join(output_directory, file)) ## copy file to output directory

file_output_list = [] ## I should make a test case here.

for f in os.listdir(output_directory):
    if f.endswith(extension):
        file_output_list.append(f)

print(tiff_output_list)
print(tiff_output_list)

## generate random numbers to assign as filenames for tiff files

random_list = []

while len(random_list) < len(file_list):
    n = random.randint(1, 100) ##if you need to randomize more than 100 files, select a higher number
    assert(len(file_list) <= 100)
    if n not in random_list:
        random_list.append(n)
    else:
        pass



i = 0
number_to_filename_dict = {} ## create empty dictionary. This will store original filenames and their corresponding random number.


for file in file_output_list:
    print(file)
    os.rename(os.path.join(output_directory, file), os.path.join(output_directory, str(random_list[i])+ extension))
    number_to_filename_dict[file] = random_list[i]
    i = i + 1
    print(i)

print(number_to_filename_dict)
print(len(number_to_filename_dict))
    

####Now we create Key.csv; Key.csv records the original filename for each random number

data = list(number_to_filename_dict.items()) #this gets your data (which is type dictionary) into the prpoer format for pd.Dataframe

key_df = pd.DataFrame(data, columns = ["filename", "random_number"]) ##convert number_to_filename_dict into a pd Dataframe

key_df.to_csv(os.path.join(output_directory, r'Key.csv'), index = False) ##write key_df into a csv file located in the output directory
    

####Now we create Details.csv, which prints version number, input_directory, output_directory, time stamp, user, etc

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
