# Precipitation (CHIRPS)

Since 1999, USGS and CHC scientists—supported by funding from USAID, NASA, and NOAA—have developed techniques for producing rainfall maps, especially in areas where surface data is sparse.

---

## CHIRPS v3.0 Overview
CHIRPS v3.0 is available for three domains: Global, Africa, and Latin America. Similar to CHIRPS v2.0, two products of CHIRPS v3.0 are available. A preliminary version and a final version. The preliminary version is produced at the end of every pentad with rapidly available Global Telecommunication System (GTS) data, while the final version – produced about two weeks after the end of the month – incorporates data from the Global Historical Climatology Network (GHCN), and the Global Summary of the Day (GSOD).

CHIRPS v3.0 benefits from nearly four times more sources of gauge data compared to CHIRPS v2.0. This increased volume of observations significantly improves the spatial and temporal accuracy of rainfall estimates.

- **Source**: [CHIRPS v3](https://data.chc.ucsb.edu/products/CHIRPS/v3.0/)

---

## Download Monthly CHIRPS PCP

The following script downloads **monthly CHIRPS v3.0 GeoTIFFs** for a given year range:

```python
import requests
import os


firstyear = 2022
lastyear = 2023

# Create a folder to store downloads
download_folder = "pcp_chirps_v3_monthly"
os.makedirs(download_folder, exist_ok=True)


for year in range(firstyear, lastyear + 1):
    for month in range(1,13):
        filename = f"chirps-v3.0.{year}.{month:02d}.tif"
        url = f"https://data.chc.ucsb.edu/products/CHIRPS/v3.0/monthly/global/tifs/{filename}"
        print(f"Downloading {filename} from {url} ...")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  
            output_path = os.path.join(download_folder, filename)
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Downloaded {filename} successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {filename}: {e}")

```

---

## Clip CHIRPS Global Rasters to India Boundary
Once downloaded, use this script to clip the **global raster** to the **India boundary** using a GeoJSON file.
> 📁 Boundary file required: [`IndiaBoundary.geojson`](https://waterinag.github.io/eqipa-docs/assets/IndiaBoundary.geojson)

```python
import os
from osgeo import gdal

# Set your paths
input_folder = "pcp_chirps_v3_monthly"      
output_folder = "pcp_chirps_ind_monthly"   
geojson_boundary = "IndiaBoundary.geojson" 

firstyear = 2022
lastyear = 2023

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all files in the input folder
for year in range(firstyear, lastyear+1):
    for month in range(1, 13):
        # Build input filename: WAPOR-3.L1-AETI-M.YYYY-MM.tif
        filename = f"chirps-v3.0.{year}.{month:02d}.tif"
        input_path = os.path.join(input_folder, filename)
        output_filename = f"chirps_pcp_m_{year}_{month:02d}.tif"

        output_path = os.path.join(output_folder, output_filename)

        # Clip the raster using GDAL.Warp with the GeoJSON boundary
        warp_options = gdal.WarpOptions(cutlineDSName=geojson_boundary, cropToCutline=True,dstNodata=-9999)
        gdal.Warp(destNameOrDestDS=output_path, srcDSOrSrcDSTab=input_path, options=warp_options)
        
        print(f"Processed {filename}: clipped and scaled saved to {output_path}")

```