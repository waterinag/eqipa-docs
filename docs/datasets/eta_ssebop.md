# Evapotranspiration (SSEBop)
Actual ET (ETa) is produced using the operational Simplified Surface Energy Balance
(SSEBop) model (Senay et al., 2012) for the period 2000 to present. The SSEBop setup is
based on the Simplified Surface Energy Balance (SSEB) approach (Senay et al., 2011, 2013)
with unique parameterization for operational applications. It combines ET fractions generated
from remotely sensed MODIS thermal imagery, acquired every 8 days, with reference ET using
a thermal index approach. The unique feature of the SSEBop parameterization is that it uses
pre-defined, seasonally dynamic, boundary conditions that are unique to each pixel for the
“hot/dry” and “cold/wet” reference points. The original formulation of SSEB is based on the hot
and cold pixel principles of SEBAL (Bastiaanssen et al., 1998) and METRIC (Allen et al., 2007)
models.
---

## Dataset Overview

- **Source**: [USGS](https://edcintl.cr.usgs.gov/downloads/sciweb1/shared/fews/web/global/)
- **Spatial Resolution**: 1000m
- **Temporal Resolution**: Monthly and Annual

---

## Download Monthly ETa (SSEBop)

This script downloads monthly SSEBop ETa v6.1 GeoTIFFs.
> 📁 India Boundary file: [Link](https://github.com/waterinag/eqipa-docs/blob/main/docs/assets/IndiaBoundary.geojson)



```python
import requests
import os
import zipfile
from osgeo import gdal

# Config
firstyear = 2023
lastyear = 2024
output_folder = "eta_ssebop_monthly"
geojson_boundary = "IndiaBoundary.geojson"

# Ensure folders exist
os.makedirs(output_folder, exist_ok=True)


# Loop through dates
for year in range(firstyear, lastyear + 1):
    for month in range(1, 13):
        filename = f"m{year}{month:02d}.zip"
        output_filename = f"ssebop_eta_m_{year}_{month:02d}.tif"
        url = f"https://edcintl.cr.usgs.gov/downloads/sciweb1/shared/fews/web/global/monthly/etav61/downloads/monthly/{filename}"
        print(f"Downloading {filename} ...")

        zip_path = os.path.join(output_folder, filename)

        try:
            # Download
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(zip_path, "wb") as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            print(f"Downloaded {filename}")

            # Unzip
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(output_folder)

            # Find the GeoTIFF file (assume one tif per zip)
            tif_files = [f for f in os.listdir(output_folder) if f.endswith(".tif") and f.startswith(f"m{year}{month:02d}")]
            if not tif_files:
                print(f"No .tif found in {filename}")
                continue

            tif_path = os.path.join(output_folder, tif_files[0])
            clipped_path = os.path.join(output_folder, output_filename)

            # Clip using gdal.Warp
            gdal.Warp(
                clipped_path,
                tif_path,
                cutlineDSName=geojson_boundary,
                cropToCutline=True,
                dstNodata=-9999
            )
            print(f"Clipped and saved: {clipped_path}")
            os.remove(zip_path)
            os.remove(tif_path)
            

        except requests.exceptions.RequestException as e:
            print(f"Failed to download {filename}: {e}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")


```

