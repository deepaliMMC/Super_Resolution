#
# #4 RUN THIS
# import os
# import numpy as np
# from PIL import Image
# import rasterio
# from rasterio.transform import from_origin
# # from fastapi import FastAPI, HTTPException
#
# def super(input_folder):
#     # Convert PNG to tiff and reduce the pixel size, image size
#     #  Step1:
#     #  Convert PNG to tiff
#     for file in os.listdir(input_folder):
#         file_without_extension = file.rsplit('.', 1)[0]
#         img1 = os.path.join('test_data', file)
#         # open the image with rasterio and change the projection
#         # List all files in the output folder
#         output_image_folder = "result"
#
#
#         try:
#             for filename in os.listdir(output_image_folder):
#                 if filename.endswith('.png') and os.path.splitext(filename)[0] == os.path.splitext(file)[0]:
#                     full_path = os.path.abspath(os.path.join(output_image_folder, filename))
#                     print(filename)
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Error listing output images: {str(e)}")
#
#         with rasterio.open(img1) as src:
#             # Read the image as a NumPy array
#             satellite_image = src.read()
#             transform = src.transform
#             # Get the coordinate reference system (CRS)
#             crs = src.crs
#             img = Image.open(full_path)
#             lr_img = np.array(img)
#             # Save the resized image using rasterio
#             # Set the custom path and filename for the cropped TIFF file
#             filename_s = "Superresolution"+file+".tiff"
#             output_path = os.path.abspath(os.path.join(output_image_folder, filename_s))
#             with rasterio.open(
#                     output_path,
#                     'w',
#                     driver='GTiff',
#                     width=lr_img.shape[1],
#                     height=lr_img.shape[0],
#                     count=lr_img.shape[2],  # Set count to the number of bands in the image
#                     dtype=lr_img.dtype
#             ) as dst:
#                 # Assuming your original image has specific CRS and transform values, replace them with your actual CRS and transform values
#                 dst.crs = src.crs  # Example CRS, replace it with your actual CRS
#                 dst.transform = transform  # Replace these values with your actual coordinates
#                 dst.write(lr_img.transpose(2, 0, 1))  # Transpose to match rasterio's expected order
#
#         # Reduce the pixel size
#         # reduce the number of pixels
#         def reduce_pixel_size(input_path, output_path):
#             with rasterio.open(input_path) as src:
#                 # Calculate new pixel dimensions (half of the original)
#                 new_pixel_width = src.transform.a / 12
#                 new_pixel_height = src.transform.e / 12
#
#                 # Calculate new dimensions of the image (half of the original)
#                 new_width = int(src.width)
#                 new_height = int(src.height)
#
#                 # Adjust the transform to maintain the correct orientation
#                 transform = from_origin(src.bounds.left, src.bounds.top, new_pixel_width, -new_pixel_height)
#
#                 # Prepare metadata for the new raster
#                 kwargs = src.meta.copy()
#                 kwargs.update({
#                     'driver': 'GTiff',
#                     'count': 3,
#                     'width': new_width,
#                     'height': new_height,
#                     'transform': transform
#                 })
#
#                 # Read the data, apply resampling, and write to the new file for each band
#                 with rasterio.open(output_path, 'w', **kwargs) as dst:
#                     for band in range(1, src.count + 1):
#                         data = src.read(band, out_shape=(new_height, new_width))
#                         dst.write(data, band)
#
#         input_path = os.path.abspath(os.path.join(output_image_folder, filename_s))
#         output_image_folder = "result"
#         filename_s1 = "Superresolution2.5"+file+".tiff"
#         output_path = os.path.abspath(os.path.join(output_image_folder, filename_s1))
#         reduce_pixel_size(input_path, output_path)
#
#
# super(r"C:\Users\Admin\Downloads\SRG\test_data")
# ######

import os
import numpy as np
from PIL import Image
import rasterio
from rasterio.transform import from_origin


# from fastapi import FastAPI, HTTPException

def super(input_folder):
    output_image_folder = "result"

    # Step1: Convert PNG to tiff
    for file in os.listdir(input_folder):
        file_without_extension = file.rsplit('.', 1)[0]
        img1 = os.path.join(input_folder, file)
        full_path = None

        try:
            for filename in os.listdir(output_image_folder):
                if filename.endswith('.png') and os.path.splitext(filename)[0] == os.path.splitext(file)[0]:
                    full_path = os.path.abspath(os.path.join(output_image_folder, filename))
                    print(filename)
                    break  # Exit the loop after finding the match
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error listing output images: {str(e)}")

        # Ensure full_path has been set
        if full_path is None:
            print(f"No matching PNG file found for {file}, skipping.")
            continue  # Skip this iteration if no matching file found

        with rasterio.open(img1) as src:
            satellite_image = src.read()
            transform = src.transform
            crs = src.crs

            img = Image.open(full_path)
            lr_img = np.array(img)

            filename_s = "Superresolution" + file + ".tiff"
            output_path = os.path.abspath(os.path.join(output_image_folder, filename_s))
            with rasterio.open(output_path, 'w', driver='GTiff', width=lr_img.shape[1], height=lr_img.shape[0],
                               count=lr_img.shape[2], dtype=lr_img.dtype) as dst:
                dst.crs = src.crs
                dst.transform = transform
                dst.write(lr_img.transpose(2, 0, 1))

        def reduce_pixel_size(input_path, output_path):
            with rasterio.open(input_path) as src:
                new_pixel_width = src.transform.a / 16
                new_pixel_height = src.transform.e / 16

                new_width = int(src.width)
                new_height = int(src.height)

                transform = from_origin(src.bounds.left, src.bounds.top, new_pixel_width, -new_pixel_height)

                kwargs = src.meta.copy()
                kwargs.update({
                    'driver': 'GTiff',
                    'count': 3,
                    'width': new_width,
                    'height': new_height,
                    'transform': transform
                })

                with rasterio.open(output_path, 'w', **kwargs) as dst:
                    for band in range(1, src.count + 1):
                        data = src.read(band, out_shape=(new_height, new_width))
                        dst.write(data, band)

        input_path = os.path.abspath(os.path.join(output_image_folder, filename_s))
        filename_s1 = "Superresolution2.5" + file + ".tiff"
        output_path = os.path.abspath(os.path.join(output_image_folder, filename_s1))
        reduce_pixel_size(input_path, output_path)


super(r"C:\Users\Admin\Downloads\SRG\test_data")

