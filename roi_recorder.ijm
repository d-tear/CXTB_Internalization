
function roi_recorder(input_directory, output_directory, records_file, extension, lineseparator, background) {

// input directory: type string, the full path to the directory where your images are located

/* output_directory: type string, the full path to the directory where you want the csv results file and roiset for each image to be save. 
Must be named "background_output" or "nonbackground_output"
Must be different from input_directory. 
Note that each analyzed image will produce one csv file and one roiset (2 files total). Thus, at any given time, 
the output directory will have exactly twice as files as there are entires in the records_file. */ 


/* records_file: type string, the full path, including filename, to the directory where your records_file is located. 
Note that the records_file is a txt file which records the images \hich you have already taken ROIs/analyzed. This way, you can stop the program at any time 
and then pick up where you left off. You must create an empty records file before you run this code for the first time. */

// extension: type string, the image format (e.g. ".czi" )

// lineseparator: type string, used to identify each new line/entry in records_file (e.g. "\n" )

// background: type boolean, if True, output_directory must be named "background_directory", else "nonbackground_directory"


//The below if else code block ensures that if background = true, the output_directory is named 'background_output, else 'nonbackground_output
if (background){
	if (File.getName(output_directory) != "background_output" || File.getName(records_file) != "background_records_file.txt") {
		exit("Warning! output_directory for background measurements must be named 'background_output' AND records_file must be named 'background_records_file.txt'")}
}

else{

if (File.getName(output_directory) != "nonbackground_output" || File.getName(records_file) != "nonbackground_records_file.txt"){
	exit("Warning! output_directory for nonbackground measurements must be named 'nonbackground_output' AND records_file must be named 'nonbackground_records_file.txt'")}

}




record_lines = split(File.openAsString(records_file), lineseparator); // Convert records_file contents to a string, and then converts that string to an array of lines

file_list = getFileList(input_directory); // all files in the input_directory

extension_files = newArray(0); //empty array which will be filled with only the files with the specified extension

for(i = 0; i < file_list.length; i++){
	
	if (endsWith(file_list[i], extension)){ 
		
	extension_files = Array.concat(extension_files, file_list[i]); 


	}
}

output_file_list = getFileList(output_directory); // all files in the output_directory


//test that records_file is not already full. A full records_file indicates that the analysis was already completed. 
if (record_lines.length == extension_files.length) {
	exit("Your records file has as many entires as there are " + extension + " files in your input directory. Have you already completed this analysis?"); 
	}
//test that records_file and input_directory are correctly specified.
if (record_lines.length > extension_files.length) {
	exit("Something is wrong. Your records file has more entires than there are " + extension + " files in your input directory."); 
	}

//Each analyzed image produces a csv file and and an roiset, so we need to test that the output_directory has exactly twice the number of files as listed in the reocrds file
if (output_file_list.length != 2*record_lines.length ){
	print("Number of files in your output directory: " + output_file_list.length);
	print("Number of entries/lines in your records file: " + record_lines.length);
	exit("Something is wrong. Your output directory should have exactly twice as many files as there are entries in your records file. See Log for details.");
}

else{
	
//Update extension_files so that the array only contains those files not already record_lines (i.e. not already in the records file).
extension_files = ArrayDiff(extension_files, record_lines);


run("Set Measurements...", "area mean standard modal min centroid center perimeter shape feret's integrated median skewness area_fraction display redirect=None decimal=3");

for(i = 0; i < extension_files.length; i++){
	
open(input_directory + "/" + extension_files[i]);

name_of_source_image = getTitle; 
dotIndex = indexOf(name_of_source_image, "."); 
title = substring(name_of_source_image, 0, dotIndex);


run("ROI Manager...");

waitForUser( "Pause","Select your ROIs and add them to the ROI manager. Then press OK"); //User selects their ROIs

//ensure that user has selected ROIs before pressing OK
nROIs = roiManager("count");
if (nROIs == 0){

selectWindow("ROI Manager"); 
run("Close"); 

while (nImages>0) { 
          selectImage(nImages); 
          close(); 
      } 
exit("You pressed OK without first selecting ROIs!")

}

if (nROIs == 1){
roiManager("Combine");
}

roiManager("Add");
roiManager("Measure");

//close Results table
selectWindow("Results"); 
saveAs("Results", output_directory + "/" + title + ".csv");//ROI results
run("Close");

//close open image
selectWindow(name_of_source_image);
close();

//close ROI manager
roiManager("Save", output_directory + "/" + title + "_RoiSet.zip"); 
selectWindow("ROI Manager"); 
run("Close"); 



File.append(name_of_source_image, records_file);
	}
}

selectWindow("ROI Manager"); 
run("Close"); 

}




/////This function was written by Rainer M. Engel, 2012: https://imagej.nih.gov/ij/macros/Array_Functions.txt
function ArrayDiff(array1, array2) {
	diffA	= newArray();
	unionA 	= newArray();	
	for (i=0; i<array1.length; i++) {
		for (j=0; j<array2.length; j++) {
			if (array1[i] == array2[j]){
				unionA = Array.concat(unionA, array1[i]);
			}
		}
	}
	c = 0;
	for (i=0; i<array1.length; i++) {
		for (j=0; j<unionA.length; j++) {
			if (array1[i] == unionA[j]){
				c++;
			}
		}
		if (c == 0) {
			diffA = Array.concat(diffA, array1[i]);
		}
		c = 0;
	}
	for (i=0; i<array2.length; i++) {
		for (j=0; j<unionA.length; j++) {
			if (array2[i] == unionA[j]){
				c++;
			}
		}
		if (c == 0) {
			diffA = Array.concat(diffA, array2[i]);
		}
		c = 0;
	}	
	return diffA;
}

//output_directory = "/Users/davidtyrpak/Desktop/FIJI_playground/output"
//input_directory = "/Users/davidtyrpak/Desktop/FIJI_playground"
//records_file = "/Users/davidtyrpak/Desktop/FIJI_playground/records_file.txt";
//extension = ".czi";
//lineseparator = "\n";

roi_recorder("/Users/davidtyrpak/Desktop/FIJI_playground", "/Users/davidtyrpak/Desktop/FIJI_playground/background_output", "/Users/davidtyrpak/Desktop/FIJI_playground/background_records_file.txt",
".czi", "\n", true)






