# Actual Evapotranspiration
Evapotranspiration is the sum of the soil evaporation (E), canopy transpiration (T) and interception (I). 
The sum of all three parameters i.e. the Actual Evapotranspiration and Interception (AETI) can be used to quantify the agricultural water consumption.
For further information on the methodology read the WaPOR documentation available at: https://bitbucket.org/cioapps/wapor-et-look/wiki/Home
---

## Dataset Overview

- **Source**: [WaPOR L1 v3](https://console.cloud.google.com/storage/browser/fao-gismgr-wapor-3-data/DATA/WAPOR-3/MAPSET)
- **Period of Use**: 2018–present
- **Spatial Resolution**: 300m
- **Temporal Resolution**: Monthly
- **Output Format Used in EQIPA**: Monthly GeoTIFF

---

## 📌 Data Processing Summary

1. Monthly WaPOR L1 v3 AETI (300m) maps have been downloaded from WaPOR.
2. Each monthly AETI raster have been multiplied by scale factor (0.1). See the scale factor for each WaPOR product here: https://data.apps.fao.org/wapor
3. Annual AETI is computed for all crop years by aggregating monthly AETI values from June to May, covering crop years 2018-19 to 2022-23.

---



## Download Clipped Raster and Apply Scale Factor
This script downloads monthly WaPOR v3 AETI raster files from FAO's WaPOR Google Cloud Bucket URLs, clips them  to the India boundary (using GDAL), and applies a scale factor.
> 📁 India Boundary file: [Link](https://github.com/waterinag/eqipa-docs/blob/main/docs/assets/IndiaBoundary.geojson)


```python

import os
import numpy as np
import rasterio
from osgeo import gdal

firstyear = 2023
lastyear = 2024

output_folder = "eta_wapor_v3_monthly_ind"
geojson_boundary = "IndiaBoundary.geojson"
os.makedirs(output_folder, exist_ok=True)

for year in range(firstyear, lastyear + 1):
    for month in range(1, 13):
        filename = f"WAPOR-3.L1-AETI-M.{year}-{month:02d}.tif"
        output_filename = f"wapor_eta_m_{year}_{month:02d}.tif"
        output_path = os.path.join(output_folder, output_filename)

        # Skip if already processed
        if os.path.exists(output_path):
            print(f"✅ {output_filename} already exists, skipping...")
            continue

        # Remote file URL via /vsicurl/
        url = f"https://gismgr.fao.org/DATA/WAPOR-3/MAPSET/L1-AETI-M/{filename}"
        vsicurl_url = f"/vsicurl/{url}"
        temp_clip = os.path.join(output_folder, f"temp_{output_filename}")

        print(f"Downloading...{filename}")

        try:
            warp_options = gdal.WarpOptions(
                cutlineDSName=geojson_boundary,
                cropToCutline=True,
                dstNodata=-9999
            )
            gdal.Warp(destNameOrDestDS=temp_clip, srcDSOrSrcDSTab=vsicurl_url, options=warp_options)
        except Exception as e:
            print(f"❌ GDAL warp failed for {filename}: {e}")
            continue

        # Scale and write output with compression
        try:
            with rasterio.open(temp_clip) as src:
                profile = src.profile
                data = src.read(1)
                nodata = src.nodata

                data = np.where(data == nodata, -9999, data)
                scaled_data = np.where(data != -9999, data * 0.1, -9999)

                profile.update(
                    dtype=rasterio.float32,
                    nodata=-9999,
                    compress="LZW"
                )

                with rasterio.open(output_path, "w", **profile) as dst:
                    dst.write(scaled_data.astype(rasterio.float32), 1)

            os.remove(temp_clip)
            print(f"✅ Processed and saved: {output_filename}")
        except Exception as e:
            print(f"❌ Failed to scale/write {filename}: {e}")
            if os.path.exists(temp_clip):
                os.remove(temp_clip)


```
