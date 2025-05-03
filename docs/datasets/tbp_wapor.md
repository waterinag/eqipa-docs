# Total Biomass Production (TBP)
Total Biomass Production (TBP) is defined as the sum of the above-ground dry matter produced for a given year. TBP is calculated from Net Primary Production (NPP). TBP is expressed in kgDM/ha/day, and has thus different biomass units compared to NPP, with 1 gC/m2/day (NPP) = 22.222 kgDM/ha/day (DMP).

For further information on the methodology read the WaPOR documentation available at: [https://bitbucket.org/cioapps/wapor-et-look/wiki/Home](https://bitbucket.org/cioapps/wapor-et-look/wiki/Home)

---

## Dataset Overview

- **Source**: [WaPOR L1 v3](https://console.cloud.google.com/storage/browser/fao-gismgr-wapor-3-data/DATA/WAPOR-3/MAPSET)
- **Period of Use**: 2018–present
- **Spatial Resolution**: 300m
- **Temporal Resolution**: Monthly
- **Output Format Used in EQIPA**: Monthly GeoTIFF

---

## 📌 Data Processing Summary

1. Monthly WaPOR L1 v3 NPP (300m) maps have been downloaded from WaPOR.
2. Monthly TBP maps are calculated as = Monthly NPP × Scale Factor (0.001) × Unit Conversion Factor (22.222). See the scale factor for each WaPOR product here: [https://data.apps.fao.org/wapor](https://data.apps.fao.org/wapor)
3. Annual TBP maps is computed for all crop years by aggregating monthly TBP maps from June to May, covering crop years 2018-19 to 2022-23.

---


## Download Clipped Monthly NPP Raster, Apply Scale Factor and convert to Monthly TBP
This script downloads monthly WaPOR v3 NPP raster files from FAO's WaPOR Google Cloud Bucket URLs, clips them to the India boundary (using GDAL), and applies a scale factor and unit conversion and produce Monthly TBP Rasters.
> 📁 India Boundary file: [Link](https://github.com/waterinag/eqipa-docs/blob/main/docs/assets/IndiaBoundary.geojson)



```python

import os
import numpy as np
import rasterio
from osgeo import gdal

firstyear = 2023
lastyear = 2024

output_folder = "tbp_wapor_v3_monthly_ind"
geojson_boundary = "IndiaBoundary.geojson"
os.makedirs(output_folder, exist_ok=True)

for year in range(firstyear, lastyear + 1):
    for month in range(1, 13):
        filename = f"WAPOR-3.L1-NPP-M.{year}-{month:02d}.tif"
        output_filename = f"wapor_tbp_m_{year}_{month:02d}.tif"
        output_path = os.path.join(output_folder, output_filename)

        if os.path.exists(output_path):
            print(f"✅ {output_filename} already exists, skipping...")
            continue

        url = f"https://gismgr.fao.org/DATA/WAPOR-3/MAPSET/L1-NPP-M/{filename}"
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

        try:
            with rasterio.open(temp_clip) as src:
                profile = src.profile
                data = src.read(1)
                nodata = src.nodata

                data = np.where(data == nodata, -9999, data)
                scaled_data = np.where(data != -9999, data * 0.001 * 22.222, -9999)

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