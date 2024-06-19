#4 STITCH AND CONVERT OUTPUT TO 16 BIT

#combine here to create single RGBw
import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob
import os

# Directory containing TIFFs
dir_path = 'result'
search_criteria = "Superresolution2.5patch_*.tif.tiff"
q = os.path.join(dir_path, search_criteria)

# List of raster files
tiff_files = glob.glob(q)

# Open the files
src_files_to_mosaic = [rasterio.open(fp) for fp in tiff_files]

# Merge function
mosaic, out_trans = merge(src_files_to_mosaic)

# Copy the metadata
out_meta = src_files_to_mosaic[0].meta.copy()

# Update the metadata
out_meta.update({"driver": "GTiff",
                 "height": mosaic.shape[1],
                 "width": mosaic.shape[2],
                 "transform": out_trans})

# Write the mosaic raster to disk
with rasterio.open('result/rgbsr8.tif', 'w', **out_meta) as dest:
    dest.write(mosaic)

# Close the files
for f in src_files_to_mosaic:
    f.close()


#CONVERT 8 TO 16 HERE
from osgeo import gdal


def convert_8bit_to_16bit(input_path, output_path):
    # Open the input image
    dataset = gdal.Open(input_path, gdal.GA_ReadOnly)

    # Get spatial reference and geotransform
    geo_transform = dataset.GetGeoTransform()
    projection = dataset.GetProjection()

    # Create output dataset
    driver = gdal.GetDriverByName('GTiff')
    out_dataset = driver.Create(output_path, dataset.RasterXSize, dataset.RasterYSize, 3, gdal.GDT_UInt16)

    # Set geo transform and projection
    out_dataset.SetGeoTransform(geo_transform)
    out_dataset.SetProjection(projection)

    # Process each band
    for band in range(1, 4):  # Bands 1, 2, and 3 for R, G, B
        src_band = dataset.GetRasterBand(band)
        out_band = out_dataset.GetRasterBand(band)

        # Read raster as numpy array
        array = src_band.ReadAsArray()
        # Convert 8-bit to 16-bit by scaling
        array_16bit = array.astype('uint16') * 257
        # Write to output band
        out_band.WriteArray(array_16bit)
        out_band.FlushCache()

    # Close datasets
    out_dataset = None
    dataset = None


# Convert the image
convert_8bit_to_16bit('result/rgbsr8.tif', 'final_output/TCI/TCI.tif')

#SAVE OUTPUT TO OUTPUT_FINAL :CREATE NEW DIR EVERYTIME HERE