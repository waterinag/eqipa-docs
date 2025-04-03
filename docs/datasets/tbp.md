# Actual Evapotranspiration
Total Biomass Production (TBP) is defined as the sum of the above-ground dry matter produced for a given year. TBP is calculated from Net Primary Production (NPP). TBP is expressed in kgDM/ha/day, and has thus different biomass units compared to NPP, with 1 gC/m2/day (NPP) = 22.222 kgDM/ha/day (DMP).

For further information on the methodology read the WaPOR documentation available at: https://bitbucket.org/cioapps/wapor-et-look/wiki/Home

---

## 🗂️ Dataset Overview

- **Source**: [WaPOR L1 v3](https://console.cloud.google.com/storage/browser/fao-gismgr-wapor-3-data/DATA/WAPOR-3/MAPSET)
- **Period of Use**: 2018–2023 crop years
- **Spatial Resolution**: 300m
- **Temporal Resolution**: Monthly
- **Output Format Used in EQIPA**: Monthly GeoTIFF

---

## 📌 Data Processing Summary

1. Monthly WaPOR L1 v3 NPP (300m) maps have been downloaded from WaPOR.
2. EMonthly TBP maps are calculated as = Monthly NPP × Scale Factor (0.001) × Unit Conversion Factor (22.222). See the scale factor for each WaPOR product here: https://data.apps.fao.org/wapor
3. Annual TBP maps is computed for all crop years by aggregating monthly TBP maps from June to May, covering crop years 2018-19 to 2022-23.

---


## ⬇️ Python Script: Download Monthly NPP (WaPOR v3)

This script downloads monthly NPP GeoTIFFs from FAO's WaPOR v3 Google-hosted URLs.


```python
import requests
import os
from tqdm import tqdm

firstyear = 2018
lastyear = 2024

# Create a folder to store downloads (optional)
download_folder = "npp_wapor_v3_monthly"
os.makedirs(download_folder, exist_ok=True)


for year in range(firstyear, lastyear):
    for month in range(1, 13):

        filename = f"WAPOR-3.L1-NPP-M.{year}-{month:02d}.tif"
        url = f"https://gismgr.fao.org/DATA/WAPOR-3/MAPSET/L1-NPP-M/{filename}"
        print(f"Downloading {filename} from {url} ...")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an error for bad responses
            
            # Get total file size from headers (if available)
            total_size = int(response.headers.get('content-length', 0))
            
            # Create a progress bar with tqdm
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc=filename)
            
            output_path = os.path.join(download_folder, filename)
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

