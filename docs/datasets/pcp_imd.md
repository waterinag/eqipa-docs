# Precipitation (IMD)

For estimating precipitation, the EQIPA platform uses high-resolution daily gridded rainfall data provided by the **India Meteorological Department (IMD)**. The dataset spans a long period (1901–Present) and offers daily precipitation values across India at a **0.25° x 0.25° spatial resolution**.

---

## Dataset Overview

- **Source**: [IMD Daily Gridded Rainfall Data](https://www.imdpune.gov.in/cmpg/Griddata/Rainfall_25_NetCDF.html)
- **Format**: NetCDF (`.nc`)
- **Period of Use**: 2018–2023 crop years
- **Spatial Resolution**: 0.25° x 0.25°
- **Temporal Resolution**: Daily
- **Output Format Used in EQIPA**: Monthly GeoTIFF

---

## 📌 Data Processing Summary

1. **Daily NetCDF files** are downloaded from IMD.
2. Each file is converted to **daily GeoTIFF rasters**.
3. These daily rasters are aggregated to produce **monthly precipitation maps**.
4. **Annual precipitation** (per crop year) is computed by summing monthly rasters from **June to May** (e.g., June 2022 – May 2023).


---


## Download Annual NetCDF from IMD

```python
import requests
import os
import re
from tqdm import tqdm

# Create a folder to store downloaded files
download_folder = "imd_netcdf_files"
os.makedirs(download_folder, exist_ok=True)

firstyear = 2023
lastyear = 2024



# Define the URL
url = "https://www.imdpune.gov.in/cmpg/Griddata/RF25.php"

# Loop over the years for which you wish to download the netCDF files
for year in range(firstyear, lastyear + 1):  # Adjust the range as needed
    payload = {"RF25": str(year)}
    print(f"Downloading netCDF file for year {year} ...")
    
    try:
        # Post the request with the payload
        response = requests.post(url, data=payload, stream=True)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Determine filename (using a default if not provided in headers)
        filename = f"RF25_{year}.nc"

        # Get total file size from headers (if available) for the progress bar
        total_size = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc=filename)
        
        output_path = os.path.join(download_folder, filename)
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    progress_bar.update(len(chunk))
        progress_bar.close()

        # Check if the download completed correctly
        if total_size != 0 and progress_bar.n != total_size:
            print(f"WARNING: Download size mismatch for {filename}")
        else:
            print(f"Downloaded {filename} successfully.")
    
    except requests.RequestException as e:
        print(f"Failed to download netCDF file for year {year}: {e}")

```

---

## Convert NetCDF to Daily GeoTIFFs

The following Python script converts daily precipitation values from IMD NetCDF files to GeoTIFF format using `xarray` and `rioxarray`.

```python
import xarray as xr
import rioxarray
import os

firstyear = 2023
lastyear = 2024

input_folder = "imd_netcdf_files"

output_folder = "pcp_imd_daily"
os.makedirs(output_folder, exist_ok=True)


for year in range(firstyear, lastyear + 1):
    # Construct the full path to the netCDF file using f-string and os.path.join
    input_nc = os.path.join(input_folder, f"RF25_{year}.nc")
    
    # Open the netCDF file
    ds = xr.open_dataset(input_nc)
    # print(ds.variables)

    variable_name = "RAINFALL"
    da = ds[variable_name]

    # Loop over each day using the "TIME" coordinate
    for day in da.coords["TIME"]:
        # Select the slice for the specific day
        daily_data = da.sel(TIME=day)
        
        # Write the CRS if not already present
        daily_data.rio.write_crs("EPSG:4326", inplace=True)
        
        # Construct a filename based on the day (e.g., '2018-01-01')
        day_str = str(day.values).split("T")[0]
        output_path = os.path.join(output_folder, f"imd_pcp_{day_str}.tif")
        
        # Export the daily slice to a GeoTIFF file
        daily_data.rio.to_raster(output_path)
        print(f"Saved {output_path}")
```

---

## Aggregate Daily GeoTIFFs to Monthly

This script uses `rasterio` and `numpy` to aggregate daily rasters into **monthly precipitation maps** by summing values.

```python
import os
import glob
import rasterio
import numpy as np

firstyear = 2023
lastyear = 2024

output_folder = "pcp_imd_monthly"
os.makedirs(output_folder, exist_ok=True)

input_folder = "pcp_imd_daily"

for year in range(firstyear, lastyear + 1):
    for month in range(1, 13):
        # Daily files are assumed to be named: imd_pcp_YYYY-MM-DD.tif
        pattern = os.path.join(input_folder, f"imd_pcp_{year}-{month:02d}-*.tif")
        daily_files = sorted(glob.glob(pattern))
        
        if not daily_files:
            print(f"No daily files found for {year}-{month:02d}")
            continue
        
        daily_arrays = []
        meta = None
        nodata_val = None
        
        # Loop over daily files and read data as float32.
        # Replace no-data values with np.nan for summing.
        for daily_file in daily_files:
            with rasterio.open(daily_file) as src:
                data = src.read(1).astype(np.float32)
                if meta is None:
                    meta = src.meta.copy()
                    nodata_val = src.nodata
                    if nodata_val is None:
                        # If nodata isn't defined, set a default value (e.g., -9999)
                        nodata_val = -9999
                        meta.update(nodata=nodata_val)
                # Replace nodata with np.nan so it won't affect the sum
                data[data == nodata_val] = np.nan
                daily_arrays.append(data)
        
        # Stack daily arrays along a new axis
        stack = np.stack(daily_arrays, axis=0)
        monthly_sum = np.nansum(stack, axis=0)
        # Identify pixels that are no-data in all daily files
        all_nan_mask = np.all(np.isnan(stack), axis=0)
        monthly_sum[all_nan_mask] = nodata_val
        
        # Update metadata: ensure data type and single band output
        meta.update(dtype=rasterio.float32, count=1)
        output_filename = os.path.join(output_folder, f"imd_pcp_m_{year}_{month:02d}.tif")
        
        with rasterio.open(output_filename, 'w', **meta) as dst:
            dst.write(monthly_sum, 1)
        
        print(f"Saved monthly raster: {output_filename}")
```

---


## Aggregate Monthly GeoTIFFs to Annual

```python
import os
import numpy as np
import rasterio

firstyear = 2023
lastyear=2024

output_folder = "pcp_imd_annual"
os.makedirs(output_folder, exist_ok=True)

input_folder = "pcp_imd_monthly"

for year in range(firstyear, lastyear):
    # Annual period: June of current year to May of next year.
    monthly_files = []
    
    # June to December for the current year
    for month in range(6, 13):
        file_path = os.path.join(input_folder, f"imd_pcp_m_{year}_{month:02d}.tif")
        monthly_files.append(file_path)

    # January to May for the next year
    for month in range(1, 6):
        file_path = os.path.join(input_folder, f"imd_pcp_m_{year+1}_{month:02d}.tif")
        monthly_files.append(file_path)

    
    monthly_arrays = []
    meta = None
    nodata_val = None
    
    for monthly_file in monthly_files:
        with rasterio.open(monthly_file) as src:
            data = src.read(1).astype(np.float32)
            if meta is None:
                meta = src.meta.copy()
                nodata_val = src.nodata
                if nodata_val is None:
                    # If nodata is not defined, set a default value (e.g., -9999)
                    nodata_val = -9999
                    meta.update(nodata=nodata_val)
            # Replace nodata values with np.nan so they don't affect the sum
            data[data == nodata_val] = np.nan
            monthly_arrays.append(data)
    
    # Stack monthly arrays and compute the sum, ignoring NaNs
    stack = np.stack(monthly_arrays, axis=0)
    annual_sum = np.nansum(stack, axis=0)
    
    # For pixels that are nan in every month, set back to nodata
    all_nan_mask = np.all(np.isnan(stack), axis=0)
    annual_sum[all_nan_mask] = nodata_val
    
    meta.update(dtype=rasterio.float32, count=1)
    output_filename = os.path.join(output_folder, f"imd_pcp_a_{year}_{year+1}.tif")
    with rasterio.open(output_filename, 'w', **meta) as dst:
        dst.write(annual_sum, 1)
    
    print(f"Saved annual raster: {output_filename}")

```

---

