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

## ⬇️ Python Script: Download Monthly ETa (SSEBop)

This script downloads monthly SSEBop ETa v6.1 GeoTIFFs.



```python
import requests
import os


firstyear = 2000
lastyear = 2012

# Create a folder to store downloads (optional)
download_folder = "eta_ssebop_monthly"
os.makedirs(download_folder, exist_ok=True)


for year in range(firstyear,lastyear):
    for month in range(1,13):
        # Format filename as mYYYYmm.zip (e.g., m201202.zip)
        filename = f"m{year}{month:02d}.zip"
        url = f"https://edcintl.cr.usgs.gov/downloads/sciweb1/shared/fews/web/global/monthly/etav61/downloads/monthly/{filename}"
        print(f"Downloading {filename} from {url} ...")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # raise an error for bad responses
            output_path = os.path.join(download_folder, filename)
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Downloaded {filename} successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {filename}: {e}")

```

