#after rgb tiff

#1. PANSHARPEN ALL BANDS WRT RGB AND SAVE IN PAN BANDS (RGB AND OTHER BANDS IN SEPERATE SEPERATE FOLDERS)
#pansharpen to 10 m
#This code is for .py files

import subprocess
import os
################# CODE FOR PERFORMING PANSHARPENING ON MULTIPLE IMAGES THROUGH LOOPS
# Define the paths
panchromatic_image_path = 'input\RGB\MH_Original_16.tif'
input_folder = 'input'
output_folder = 'ten_m_bands'

# Get a list of all tif files in the input folder
multispectral_images = [file for file in os.listdir(input_folder) if file.endswith('.tif')]

# Loop through each multispectral image and process it
for image in multispectral_images:
    # Define the output file path
    output_file_path = os.path.join(output_folder, os.path.splitext(image)[0] + '_to_10m.tif')

    # Define the command
    command = [
        'pysharpen',
        '--method', 'brovey',  # Specify the pansharpening method (optional)
        '--preprocessing', 'none',  # Specify preprocessing method (optional)
        '--resampling', 'bilinear',  # Specify resampling method (optional)
        '--nogeo',  # Specify if the images are not georeferenced (optional)
        '--noclean',  # Specify if you want to keep intermediate files (optional)
        panchromatic_image_path,  # Use the same panchromatic image for each operation
        os.path.join(input_folder, image),  # Current multispectral image path
        output_file_path  # Output path for the pansharpened image
    ]

    # Run the command
    subprocess.run(command)




# USE SRRGB16 FROM OUTPUT_FINAL/RGB TO PANSHARPEN ALL OTHER BANDS AND SAVE TO OUTPUT_FINAL/RAW
#(CREATE PS FUNCTION SOMEWHERE ELSE AND USE IT HERE)
#PANSHARPEN HERE

#pansharpen to 10 m
#This code is for .py files

#   There is a requirements.txt too attached to this

import subprocess
import os

################# CODE FOR PERFORMING PANSHARPENING ON MULTIPLE IMAGES THROUGH LOOPS
# Define the paths
panchromatic_image_path = 'final_output/TCI/TCI.tif'
input_folder = 'ten_m_bands'
output_folder = 'final_output/raw/'

# Get a list of all tif files in the input folder
multispectral_images = [file for file in os.listdir(input_folder) if file.endswith('.tif')]

# Loop through each multispectral image and process it
for image in multispectral_images:
    # Define the output file path
    output_file_path = os.path.join(output_folder, os.path.splitext(image)[0] + '_SR.tif')

    # Define the command
    command = [
        'pysharpen',
        '--method', 'brovey',  # Specify the pansharpening method (optional)
        '--preprocessing', 'none',  # Specify preprocessing method (optional)
        '--resampling', 'bilinear',  # Specify resampling method (optional)
        '--nogeo',  # Specify if the images are not georeferenced (optional)
        '--noclean',  # Specify if you want to keep intermediate files (optional)
        panchromatic_image_path,  # Use the same panchromatic image for each operation
        os.path.join(input_folder, image),  # Current multispectral image path
        output_file_path  # Output path for the pansharpened image
    ]

    # Run the command
    subprocess.run(command)


#approved!