# CXTB_Internalization
Purpose: This pipeline is used to calculate cholera toxin (CXTB) internalization from confocal z-stacks. 
However, this pipeline could be adapted to study ligand internalization in a variety of contexts. 

Step 1) sum_projections.ijm is used to convert each z-stack image into a sum projection. 
input: confocal z-stack images
output: sum projection images

Step 2) Random_filename_generator.py is used to rename each sum projection image with a 3 digit random number.
input: the sum projection images from sum_projections.ijm
output: randomly renamed sum projection images
Note: Random_filename_generator.py can actually be used to randomly rename any type of file.

Step 3) use roi_recorder.ijm to draw ROIs around their cells of interest (i.e. measure nonbackground)
However, you could also measure background first by using roi_recorder.ijm to select background ROIs in each of your images.
input: The randomly renamed sum projection images output from Random_filename_generator.py
output: 

