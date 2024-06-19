# # #1 PICK RGB ..CONVERT TO 8 BIT AND CREATE PATCHES
# import rasterio
# from rasterio.windows import Window
# import os
#
# import numpy as np
# #CONVERT 16 TO 8 HERE##############
# from osgeo import gdal
# #
# # def convert_16bit_to_8bit_stretched(input_path, output_path):
# #     # Open the input image
# #     dataset = gdal.Open(input_path, gdal.GA_ReadOnly)
# #     # Get spatial reference and geotransform
# #     geo_transform = dataset.GetGeoTransform()
# #     projection = dataset.GetProjection()
# #
# #     # Create output dataset
# #     driver = gdal.GetDriverByName('GTiff')
# #     out_dataset = driver.Create(output_path, dataset.RasterXSize, dataset.RasterYSize, 3, gdal.GDT_Byte)
# #
# #     # Set geo transform and projection
# #     out_dataset.SetGeoTransform(geo_transform)
# #     out_dataset.SetProjection(projection)
# #
# #     # Process each band
# #     for band in range(1, 4):  # Bands 1, 2, and 3 for R, G, B
# #         src_band = dataset.GetRasterBand(band)
# #         out_band = out_dataset.GetRasterBand(band)
# #
# #         # Read raster as numpy array
# #         array = src_band.ReadAsArray()
# #
# #         # Stretch the histogram to utilize full range
# #         lower_percentile, upper_percentile = np.percentile(array, [2, 98])
# #         array_scaled = np.clip((array - lower_percentile) / (upper_percentile - lower_percentile) * 255, 0, 255)
# #         array_8bit = array_scaled.astype('uint8')
# #
# #         # Write to output band
# #         out_band.WriteArray(array_8bit)
# #         out_band.FlushCache()
# #
# #     # Close datasets
# #     out_dataset = None
# #     dataset = None
#
# #
# # # Paths for the input and output images
# # # input_file_path = 'RGB'
# # input_file_path = 'RGB/MH_Original_16.tif'
# # output_file_path ='prete/rgb_108.tiff'
# #
# # # Perform conversion
# # convert_16bit_to_8bit_stretched(input_file_path, output_file_path)
# #
# # # Return the path of the output file to confirm the operation
# # output_file_path
# #
# #
# #PATCHIFYBEST
# def get_patches(input_file, patch_size, output_dir):
#     os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
#     with rasterio.open(input_file) as src:
#         print(f"Opened input file with dimensions: {src.width}x{src.height}")
#         # Calculate number of full patches and account for remaining pixels
#         num_cols = (src.width + patch_size - 1) // patch_size  # Rounds up to include partial patches
#         num_rows = (src.height + patch_size - 1) // patch_size
#         k = 0  # Initialize patch counter
#         for col in range(num_cols):
#             for row in range(num_rows):
#                 # Calculate the width and height of the patch, which may be less than patch_size for edge patches
#                 width = min(patch_size, src.width - col * patch_size)
#                 height = min(patch_size, src.height - row * patch_size)
#                 window = Window(col * patch_size, row * patch_size, width, height)
#                 patch = src.read(window=window)
#                 output_path = os.path.join(output_dir, f'patch_{k}.tif')
#                 with rasterio.open(
#                     output_path, 'w',
#                     # driver='GTiff',
#                     height=height,
#                     width=width,
#                     count=src.count,
#                     dtype=src.dtypes[0],
#                     crs=src.crs,
#                     transform=src.window_transform(window)
#                 ) as patch_file:
#                     patch_file.write(patch)
#                 print(f"Created patch {k} at {output_path}")
#                 k += 1
#
# # Specify the output directory for patches
# output_dir = 'test_data'
# input_file = 'prete/res_0000.png'
#
# patch_size = 512
# get_patches(input_file, patch_size, output_dir)
#
# #Approved!

import subprocess
from fastapi import FastAPI, HTTPException
import os


def run_srgan():
    mode = "test_only"
    generator_path = "pretrained_models/SRGAN.pt"
    lr_folder = "test_data"

    # Get a sorted list of files in the directory
    files = sorted(os.listdir(lr_folder))

    for file in files:
        if file.startswith("patch_"):
            lr_path = os.path.join(lr_folder, file)
            # Build command
            command = f"python main.py --mode {mode} --LR_path {lr_path} --generator_path {generator_path}"

            try:
                # Execute command and capture output
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"Error in processing {file}: {result.stderr}")
                print(f"Processed {file}: {result.stdout}")

            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))


run_srgan()
