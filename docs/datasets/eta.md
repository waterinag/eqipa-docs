# Actual Evapotranspiration
Evapotranspiration is the sum of the soil evaporation (E), canopy transpiration (T) and interception (I). 
The sum of all three parameters i.e. the Actual Evapotranspiration and Interception (AETI) can be used to quantify the agricultural water consumption.
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

1. Monthly WaPOR L1 v3 AETI (300m) maps have been downloaded from WaPOR.
2. Each monthly AETI raster have been multiplied by scale factor (0.1). See the scale factor for each WaPOR product here: https://data.apps.fao.org/wapor
3. Annual AETI is computed for all crop years by aggregating monthly AETI values from June to May, covering crop years 2018-19 to 2022-23.

---

## ⬇️ Python Script: Download Monthly AETI (WaPOR v3)

This script downloads monthly AETI GeoTIFFs from FAO's WaPOR v3 Google-hosted URLs.



```python
import requests
import os
from tqdm import tqdm

firstyear = 2018
lastyear = 2024

# Create a folder to store downloads (optional)
download_folder = "eta_wapor_v3_monthly"
os.makedirs(download_folder, exist_ok=True)


for year in range(firstyear, lastyear):
    for month in range(1, 13):
        # Format filename as WAPOR-3.L1-AETI-M.YYYY-MM.tif
        filename = f"WAPOR-3.L1-AETI-M.{year}-{month:02d}.tif"
        url = f"https://gismgr.fao.org/DATA/WAPOR-3/MAPSET/L1-AETI-M/{filename}"
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

