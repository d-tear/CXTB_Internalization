# -*- coding: utf-8 -*-
"""
Created on Tue May  3 17:40:28 2016

@author: davidtyrpak
"""

import csv
import os
import random
from shutil import copyfile
import glob

def listdir_nohidden(path): ## this function returns all the files in a directory, ignoring hidden files (those starting with ".")
    return glob.glob(os.path.join(path, '*'))


input_directory = "/Users/davidtyrpak/Desktop/python_playground"
output_directory = "/Users/davidtyrpak/Desktop/python_playground/output" ##Make sure this directory is empty!

print(os.listdir(output_directory))

if len(listdir_nohidden(output_directory)) != 0:
    raise RuntimeError("Warning! Your output_directory is not empty! Please choose an empty directory.")


i = 0
tiff_list = []
    
for f in os.listdir(input_directory):
    if f.endswith(".txt"):
        i+=1
        tiff_list.append(f)
        print(i)
    
        if i==0:
            print("There are no tiff files in this folder!")
        else:
            pass


number_of_tiff_files = len(tiff_list) 
print(tiff_list)
print(number_of_tiff_files)

output_tiff_list = [] ## This for loop copies the tiff files from the input directory into the output directory
for tiff_file in tiff_list:
    full_tiff_name = os.path.join(input_directory, tiff_file)
    copyfile(full_tiff_name, os.path.join(output_directory, tiff_file)) ## copy file to output directory

tiff_output_list = [] ## I should make a test case here. I should test that len(tiff_output_list) == len(tiff_list)

for f in os.listdir(output_directory):
    if f.endswith(".txt"):
        tiff_output_list.append(f)

print(tiff_output_list)
print(tiff_output_list)

## generate random numbers to assign as filenames for tiff files

random_list = []

while len(random_list) < len(tiff_list):
    n = random.randint(1, 100) ##if you need to randomize more than 100 files, select a higher number
    if n not in random_list:
        random_list.append(n)
    else:
        pass

print(random_list)
print(len(random_list))

i = 0
number_to_filename_dict = {} ## create empty dictionary. This will store tiff filenames and their corresponding random number.


for tiff_file in tiff_output_list:
    print(tiff_file)
    os.rename(os.path.join(output_directory, tiff_file), os.path.join(output_directory, str(random_list[i])+ ".txt"))
    number_to_filename_dict[tiff_file] = random_list[i]
    i = i + 1
    print(i)

print(number_to_filename_dict)
print(len(number_to_filename_dict))
    
# Create Key csv file. Use this key to to determine what the original file name of the tiff file was.
    
#results_filename = "Key.csv"
#with open(os.path.join(output_directory, results_filename), 'wb') as results_file:
#    writer = csv.writer(results_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    for key in number_to_filename_dict.keys():
#        row = [key, str(number_to_filename_dict[key])]
#        print(row)
#        writer.writerow(row)
#        
    
    
    




