

function sum_projections(input_directory, output_directory, extension) {


/* 

 Description
 ------------
 This function converts z-stacks into sum intensity projections. The original z-stacks are left unchanged. Note that the sum intensity projections are saved as .tiff files

 WINDOWS USERS: you have to use double backslashes in your file paths, ex. "C:\\Users\\user\\Desktop\\test"

 Parameters
 ---------
input_directory: type string, the full path to the directory where your z-stack images are located

output_directory: type string, the full path to the directory where you want the sum intensity projection images to be saved

extension: type string, the image format (e.g. ".czi" )

*/

file_list = getFileList(input_directory); // all files in the input_directory


extension_files = newArray(0); //empty array which will be filled with only the files with the specified extension

for(i = 0; i < file_list.length; i++){
	
	if (endsWith(file_list[i], extension)){ 
		
	extension_files = Array.concat(extension_files, file_list[i]); 


	}
}

output_file_list = getFileList(output_directory); // all files in the output_directory

//ensure that output_directory is clean before we run this macro
if (output_file_list.length != 0){
	exit("Warning! output_directory is not empty.")}


//go to input_directory and create a sum intensity projection of each image. Then save each sum intensity projection into the output_directory
for(i = 0; i < extension_files.length; i++){
	
open(input_directory + File.separator + extension_files[i]);

name_of_source_image = getTitle; 


//sum intensity projection
selectWindow(name_of_source_image);
run("Z Project...", "projection=[Sum Slices]");

//close original image to conserve memory
selectWindow(name_of_source_image);
close();

//select sum intensity projection window and get file name
name_of_SumProjection = getTitle; 
dotIndex = indexOf(name_of_SumProjection, "."); //the index where the "." is located (the "." marks the beginning of the file extension)
title = substring(name_of_SumProjection, 0, dotIndex);
selectWindow(name_of_SumProjection);

//save sum projection into the output_directory
saveAs("Tiff",  output_directory + File.separator + title);

//close sum projection
close();

} //end of for loop



}//end of function


//Uncomment the below call to sum_projections and modify to your specific input directory, output directory, and extension type
sum_projections("/home/rcf-proj/drt1/tyrpak/Data/CXTB_Internalization/Master", "/home/rcf-proj/drt1/tyrpak/Data/CXTB_Internalization/Master/HPC_SumProjections", ".czi")

