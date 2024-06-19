###CORRECTED WORKING CODE:
from osgeo import gdal
import numpy as np

def composite_tiff(band1_path, band2_path, band3_path, output_path):
    # Open datasets
    band1_ds = gdal.Open(band1_path)
    band2_ds = gdal.Open(band2_path)
    band3_ds = gdal.Open(band3_path)

    # Read bands as arrays and convert to uint16
    band1 = band1_ds.GetRasterBand(1).ReadAsArray().astype(np.uint16) #######DIFF
    band2 = band2_ds.GetRasterBand(1).ReadAsArray().astype(np.uint16)
    band3 = band3_ds.GetRasterBand(1).ReadAsArray().astype(np.uint16)

    # Handle no-data values
    band1_no_data = band1_ds.GetRasterBand(1).GetNoDataValue()
    band2_no_data = band2_ds.GetRasterBand(1).GetNoDataValue()
    band3_no_data = band3_ds.GetRasterBand(1).GetNoDataValue()

    if band1_no_data is not None:
        band1[band1 == band1_no_data] = 0  # Replace no-data with 0  ######DIFFFFFFF
    if band2_no_data is not None:
        band2[band2 == band2_no_data] = 0 # Replace no-data with 0
    if band3_no_data is not None:
        band3[band3 == band3_no_data] = 0 # Replace no-data with 0

    # Create composite image   #M3
    # COMPOsite = np.dstack((band3, band2, band1))  # Stack bands in BGR order  ######DIFFFFFFF
    composite = np.dstack((band3, band2, band1))  # Stack bands in BGR order  ######DIFFFFFFF
                                           #---M3
    # Create output dataset
    driver = gdal.GetDriverByName('GTiff')
    rows, cols = band1.shape
    bands = 3
    composite_ds = driver.Create(output_path, cols, rows, bands, gdal.GDT_UInt16)  ######DIFFFFFFF

    # Set the projection and geotransform
    composite_ds.SetProjection(band1_ds.GetProjection())
    composite_ds.SetGeoTransform(band1_ds.GetGeoTransform())

    # Write bands to the output dataset   #m2
    # for i in range(bands):
    #     composite_ds.GetRasterBand(i + 1).WriteArray(composite[:, :, i])

    # # Close datasets
    # composite_ds = None
    # band1_ds = None
    # band2_ds = None
    # band3_ds = None
    # print("Composite image saved successfully.")


    for i in range(bands):
        raster_band = composite_ds.GetRasterBand(i + 1)
        raster_band.WriteArray(composite[:, :, i])
    composite_ds = None
    print("Composite image saved successfully.")  #m2---

# Input paths for the three bands
band1_path = '/content/drive/MyDrive/Super resolution/PipelineRequirementssentinel2.5all bands/Data/This/B04.tif'
band2_path = '/content/drive/MyDrive/Super resolution/PipelineRequirementssentinel2.5all bands/Data/This/B03.tif'
band3_path = '/content/drive/MyDrive/Super resolution/PipelineRequirementssentinel2.5all bands/Data/This/B02.tif'

#output is this image
output_path = 'final_output/multiband'
# Call the function to create and save the composite image
composite_tiff(band1_path, band2_path, band3_path, output_path)

#make this dynamic! for the whole folder :'final_output/raw'