# Actual Evapotranspiration
Total Biomass Production (TBP) is defined as the sum of the above-ground dry matter produced for a given year. TBP is calculated from Net Primary Production (NPP). TBP is expressed in kgDM/ha/day, and has thus different biomass units compared to NPP, with 1 gC/m2/day (NPP) = 22.222 kgDM/ha/day (DMP).

For further information on the methodology read the WaPOR documentation available at: [https://bitbucket.org/cioapps/wapor-et-look/wiki/Home](https://bitbucket.org/cioapps/wapor-et-look/wiki/Home)

---

## Dataset Overview

- **Source**: [WaPOR L1 v3](https://console.cloud.google.com/storage/browser/fao-gismgr-wapor-3-data/DATA/WAPOR-3/MAPSET)
- **Period of Use**: 2018–2023 crop years
- **Spatial Resolution**: 300m
- **Temporal Resolution**: Monthly
- **Output Format Used in EQIPA**: Monthly GeoTIFF

---

## 📌 Data Processing Summary

1. Monthly WaPOR L1 v3 NPP (300m) maps have been downloaded from WaPOR.
2. Monthly TBP maps are calculated as = Monthly NPP × Scale Factor (0.001) × Unit Conversion Factor (22.222). See the scale factor for each WaPOR product here: [https://data.apps.fao.org/wapor](https://data.apps.fao.org/wapor)
3. Annual TBP maps is computed for all crop years by aggregating monthly TBP maps from June to May, covering crop years 2018-19 to 2022-23.

---


## ⬇️ Python Script: Download Monthly NPP (WaPOR v3)

This script downloads monthly NPP GeoTIFFs from FAO's WaPOR v3 Google-hosted URLs.


```python
# tbp_wapor_v3.py
import requests
import os
from tqdm import tqdm

firstyear = 2023
lastyear = 2024

# Create a folder to store downloads (optional)
download_folder = "npp_wapor_v3_monthly"
os.makedirs(download_folder, exist_ok=True)


for year in range(firstyear, lastyear+1):
    for month in range(1, 13):
        filename = f"WAPOR-3.L1-NPP-M.{year}-{month:02d}.tif"
        output_path = os.path.join(download_folder, filename)

        if os.path.exists(output_path):
            print(f"File already exists: {filename}, skipping...")
            continue

        url = f"https://gismgr.fao.org/DATA/WAPOR-3/MAPSET/L1-NPP-M/{filename}"
        print(f"Downloading {filename} from {url} ...")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an error for bad responses
            
            # Get total file size from headers (if available)
            total_size = int(response.headers.get('content-length', 0))
            
            # Create a progress bar with tqdm
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc=filename)
            

            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        progress_bar.update(len(chunk))
            progress_bar.close()
            
            # Optional: Check if the download completed correctly
            if total_size != 0 and progress_bar.n != total_size:
                print(f"WARNING: Download size mismatch for {filename}")
            else:
                print(f"Downloaded {filename} successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {filename}: {e}")


```


---

## Clip Global Rasters to India Boundary
Once downloaded, use this script to clip the **global raster** to the **India boundary** using a boundary file.
> 📁 India Boundary file required: https://github.com/waterinag/eqipa-docs/blob/main/docs/assets/IndiaBoundary.geojson

```python
# tbp_wapor_v3_clip.py
import os
import numpy as np
import rasterio
from osgeo import gdal

# Set your paths
input_folder = "npp_wapor_v3_monthly"      
output_folder = "tbp_wapor_v3_monthly_ind"   
geojson_boundary = "IndiaBoundary.geojson" 
scale_factor=0.001*22.222
firstyear = 2023
lastyear = 2024

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all files in the input folder
for year in range(firstyear, lastyear+1):
    for month in range(1, 13):
        output_filename = f"wapor_tbp_m_{year}_{month:02d}.tif"
        temp_clip = os.path.join(output_folder, f"temp_{output_filename}")

        # Clip and Download raster from Cloud
        # fileURL=f"https://storage.googleapis.com/fao-gismgr-wapor-3-data/DATA/WAPOR-3/MAPSET/L2-NPP-M/WAPOR-3.L2-NPP-M.{year}-{month:02d}.tif" 
        # vrt_file=f"WAPOR-3.L2-NPP-M.{year}-{month:02d}.vrt"
        # gdal.BuildVRT(vrt_file, [f"/vsicurl/{fileURL}"])
        # gdal.Warp(temp_clip, vrt_file, cutlineDSName=geojson_boundary, cropToCutline=True, dstNodata=-9999)


        # Clip raster from local
        filename = f"WAPOR-3.L1-NPP-M.{year}-{month:02d}.tif"
        input_path = os.path.join(input_folder, filename)
        warp_options = gdal.WarpOptions(cutlineDSName=geojson_boundary, cropToCutline=True,dstNodata=-9999)
        gdal.Warp(destNameOrDestDS=temp_clip, srcDSOrSrcDSTab=input_path, options=warp_options)


        
        # Define the output path for the scaled raster
        output_path = os.path.join(output_folder, output_filename)
        
        # Open the clipped raster with Rasterio
        with rasterio.open(temp_clip) as src:
            profile = src.profile 
            data = src.read(1)
            nodata = src.nodata

            data = np.where(data == src.nodata, -9999, data)  
            scaled_data = np.where(data != -9999, data * scale_factor, -9999)

            
            # Update the profile for the output file
            profile.update(
                dtype=rasterio.float32, 
                nodata=nodata, 
                compress="LZW"  # Apply LZW compression
            )
            if nodata is not None:
                profile.update(nodata=nodata)
            
            # Write the scaled data to a new file
            with rasterio.open(output_path, "w", **profile) as dst:
                dst.write(scaled_data.astype(rasterio.float32), 1)
        
        # Optionally, remove the temporary clipped file
        os.remove(temp_clip)
        
        print(f"Processed: clipped and scaled saved to {output_path}")


```


