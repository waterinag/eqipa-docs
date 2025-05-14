# Zonal Statistics (Terminal)

Zonal statistics summarize raster values (e.g., mean, sum, count) within vector zones such as administrative boundaries, watersheds, or land parcels. This guide explains how to perform zonal statistics in GRASS GIS using a GeoJSON boundary file and a raster map.

---

### Import Vector Boundary (GeoJSON)

Use `v.in.ogr` to import a GeoJSON file:

```bash
v.in.ogr input=/path/to/boundaries.geojson output=zones
```
> 🔍 Check if the projection of your GeoJSON matches the current GRASS location. If not, reproject the vector (see section below).

### Import Raster Map

Use r.import to bring in a GeoTIFF or similar raster file:

```bash
r.import input=/path/to/raster.tif output=my_raster

```


### Set Computational Region

Match the region to your raster map:

```bash
g.region raster=my_raster -p

# (Optional) Expand region to fully cover vector zones:
g.region vector=zones align=my_raster

```



### Perform Zonal Statistics with v.rast.stats

Use the vector map (zones) to compute stats from the raster (my_raster) for each polygon:

```bash
v.rast.stats map=zones raster=my_raster column_prefix=stats method=average,sum,count
```

- column_prefix: Adds columns like stats_mean, stats_sum, etc.
- method: Can be one or more of: average, sum, count, min, max, stddev

This updates the attribute table of the vector map with the calculated values.


### View Results

Display the updated attribute table:

```bash
v.db.select map=zones

```



### Optional: Export the Results to GeoJSON or Shapefile

```bash
# Export GeoJSON
v.out.ogr input=zones output=zones_stats.geojson format=GeoJSON

# or Export Shapefile
v.out.ogr input=zones output=zones_stats.shp format=ESRI_Shapefile

# or Export Attribute Table to CSV
v.db.select map=zones separator=comma file=zones_stats.csv

```


### (Optional) Reproject GeoJSON if Needed

If your GeoJSON CRS doesn't match the current GRASS location, you can either:

- Reproject using GDAL before importing, or
- Import it into a matching GRASS location, and use v.proj

```bash
# Run this inside your target location
v.proj location=source_location mapset=PERMANENT input=zones output=zones_reprojected

```


---

##  GRASS Python Scripts

```bash
# Create a Python 3 virtual environment 
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies with `pip`
pip install pandas numpy geopandas openpyxl

# or from requirements.txt
pip install -r requirements.txt
pip3 freeze > requirements.txt
```

---

### Python Script: Monthly Zonal Stats




!!! info "Monthly Zonal Stats"

    ```bash
    import os
    import sys
    import subprocess
    import shutil
    import calendar
    import math
    import grass.script as gs
    from grass.pygrass.modules.shortcuts import general as g
    from grass.pygrass.modules.shortcuts import raster as r
    from grass.pygrass.modules.shortcuts import display as d
    from grass.pygrass.modules.shortcuts import vector as v
    from grass.pygrass.gis import *
    import grass.script as grass
    import grass.script.setup as gsetup
    import re
    import numpy as np
    import geopandas as gdf
    import pandas as pd
    import io


    # Main function
    def main(gisdb, location, mapset): 

        geojson_file = 'StatesBoundary.geojson'
        output_csv_path=f"IndiaStates_monthly_zonalstats.csv"
        start_yr = '2023'
        end_yr = '2024'

        os.environ['GISDBASE'] = gisdb
        os.environ['LOCATION_NAME'] = location

        # Check if mapset exists; if not, create it
        mapset_path = os.path.join(gisdb, location, mapset)
        if not os.path.exists(mapset_path):
            print(f"Mapset '{mapset}' does not exist. Creating new mapset...")
            # Create the new mapset
            gs.run_command('g.mapset', flags='c', mapset=mapset, location=location, dbase=GISDBASE)
        else:
            print(f"Mapset '{mapset}' already exists.")

        # Initialize GRASS session
        gsetup.init(gisdb, location, mapset)
        print(f"GRASS GIS session initialized in {gisdb}/{location}/{mapset}")


        vector_name = os.path.splitext(os.path.basename(geojson_file))[0]

        v.import_(input=geojson_file, output=vector_name, overwrite=True)
        
        g.mapsets(mapset="nrsc_lulc,data_annual,data_monthly", operation="add")

        gs.run_command('g.region', vector=vector_name, res=0.00292)


        for year in range(int(start_yr), int(end_yr) + 1):
            for month in range(1,13):

                raster_name=f"imd_pcp_resam_m_{year}_{month:02d}"
                gs.run_command('v.rast.stats', map=vector_name, raster=raster_name, 
                    column_prefix=raster_name, 
                    #    method='percentile',
                        # percentile=98,
                    method='average', 
                    #    method='coeff_var', 
                    # method='stddev',
                    overwrite=True)
                
        stats_output = gs.read_command(
            'v.db.select', map=vector_name, format="csv", overwrite=True
        )
        
        # Use StringIO to read the data into a Pandas DataFrame
        data = io.StringIO(stats_output)
        df = pd.read_csv(data)
        
        # Export the DataFrame to a CSV file
        df.to_csv(output_csv_path, index=False)


        print(f"zonalstats exported successfully: {vector_name}")




    if __name__ == '__main__':
        GISDBASE = "/Volumes/ExternalSSD/eqipa_data/grassdata"
        LOCATION_NAME = "eqipa"
        MAPSET = "eqipa_stats"                 

        # Call the main function
        main(GISDBASE, LOCATION_NAME, MAPSET)








    ```

---


### Python script: EQIPA Overview Stats
We will build a Python script that:

- Initializes a GRASS session
- Imports a vector (GeoJSON) file
- Calculates zonal statistics for multiple rasters
- Derives Irrigation Performance Indicators (IPA) like Equity, Adequacy, and Cropping Intensity
- Exports results to Excel




###  Analysis Workflow

The script includes the following:

- Imports the GeoJSON vector layer
- Computes zonal statistics (v.rast.stats) on multiple rasters
- Computes IPA metrics like Equity and Adequacy
- Calculates Cropland and Gross Cropped Area from pixel counts
- Exports to Excel with two sheets (Info and Stats)
- See the Full Python Script below for the complete implementation.


!!! info "Full Python Script"

    ```bash
    import os
    import sys
    import subprocess
    import shutil
    import calendar
    import math
    import grass.script as gs
    from grass.pygrass.modules.shortcuts import general as g
    from grass.pygrass.modules.shortcuts import raster as r
    from grass.pygrass.modules.shortcuts import display as d
    from grass.pygrass.modules.shortcuts import vector as v
    from grass.pygrass.gis import *
    import grass.script as grass
    import grass.script.setup as gsetup
    import re
    import numpy as np
    import geopandas as gdf
    import pandas as pd



    # Main function
    def main(gisdb, location, mapset): 

        geojson_file = 'StatesBoundary.geojson'
        selectedYear="2023_2024"

        os.environ['GISDBASE'] = gisdb
        os.environ['LOCATION_NAME'] = location

        # Check if mapset exists; if not, create it
        mapset_path = os.path.join(gisdb, location, mapset)
        if not os.path.exists(mapset_path):
            print(f"Mapset '{mapset}' does not exist. Creating new mapset...")
            # Create the new mapset
            gs.run_command('g.mapset', flags='c', mapset=mapset, location=location, dbase=GISDBASE)
        else:
            print(f"Mapset '{mapset}' already exists.")

        # Initialize GRASS session
        gsetup.init(gisdb, location, mapset)
        print(f"GRASS GIS session initialized in {gisdb}/{location}/{mapset}")


        print("selected_year",selectedYear)

        file_name = os.path.splitext(geojson_file)[0]

        vector_name = re.sub(r'[^a-zA-Z0-9_]', '_', file_name)

        # Ensure the name starts with a letter
        if not vector_name[0].isalpha():
            vector_name = "v_" + vector_name  # Prefix with "v_"

        # Truncate if too long (max 256 chars)
        vector_name = vector_name[:256]


        output_excel_path=f"{vector_name}_{selectedYear}_zonalstats.xlsx"

        v.import_(input=geojson_file, output=vector_name, overwrite=True)
        g.mapsets(mapset="nrsc_lulc,data_annual", operation="add")


        grass.run_command(
            "v.to.db",
            map=vector_name,
            option="area",
            columns="geographical_area_ha",
            units="hectares",
            overwrite=True
        )


        # Set the region to match the raster
        # g.region(vector=vector_name, res=0.001)
        g.region(vector=vector_name, res=0.001)
        # 0.003 degrees ≈ 111 km * 0.003 ≈ 333 meters.
        # 0.001 degrees ≈ 111 km * 0.001 ≈ 111 meters.

        # LULC: 56m
        # WaPOR ETa: 300m
        # WaPOR TBP: 300m
        # IMD PCP: 0.25 degree


        # lcc_map=f"LULC_250k_{selectedYear}"
        lcc_map=f"LULC_250k_2022_2023"
        eta_map=f"wapor_eta_a_{selectedYear}"
        tbp_map=f"wapor_tbp_a_{selectedYear}"
        pcp_map=f"imd_pcp_resamp_a_{selectedYear}"
        bwp_map =f"wapor_bwp_a_{selectedYear}"


        grass.parse_command(
                'v.rast.stats',
                map=vector_name,
                raster=eta_map,
                method=['average'],
                column_prefix=f'ETa_{selectedYear}',
                overwrite=True
            )

        grass.parse_command(
                'v.rast.stats',
                map=vector_name,
                raster=pcp_map,
                method=['average'],
                column_prefix=f'PCP_{selectedYear}',
                overwrite=True
            )


        r.mask(raster=lcc_map, maskcats='2 3 4 5 7')

        grass.mapcalc(f"{bwp_map} = {tbp_map} / ({eta_map} * 10)",overwrite=True)


        grass.parse_command(
            'v.rast.stats',
            map=vector_name,
            raster=eta_map,
            method=["average","coeff_var" ],
            column_prefix=f'ETa_cropland_{selectedYear}',
            overwrite=True
        )
        grass.parse_command(
                "v.rast.stats",
                map=vector_name,
                raster=eta_map,
                column_prefix=f'ETa_cropland_{selectedYear}',
                method="percentile",
                percentile=98,
                overwrite=True,
            )


        grass.parse_command(
                "v.rast.stats",
                map=vector_name,
                raster=tbp_map,
                column_prefix=f'BLP_{selectedYear}',
                method=[ "average"],
                overwrite=True,
            )

        grass.parse_command(
            "v.rast.stats",
            map=vector_name,
            raster=bwp_map,
            column_prefix=f'BWP_{selectedYear}',
            method=[ "average"],
            overwrite=True,
        )

        r.mask(flags="r")

        cropland_classes = {
                'exclusive_kharif': '2',
                'exclusive_rabi': '3',
                'exclusive_zaid': '4',
                'double_crop': '5',
                'plantation': '7'
        }

        # Iterate over each class and perform zonal statistics
        for class_name, maskcats in cropland_classes.items():
            # Apply mask
            r.mask(raster=lcc_map, maskcats=maskcats)

            grass.parse_command(
                "v.rast.stats",
                map=vector_name,
                raster=lcc_map,
                column_prefix=f"{class_name}_pixelcount",
                method=["number"],
                overwrite=True,
            )


            # Remove mask
            r.mask(flags="r")

        output_csv_path = output_excel_path.replace(".xlsx", ".csv")

        v.out_ogr(
            input=vector_name,
            output=output_csv_path,
            format="CSV",
            overwrite=True
        )

        g.region(flags="d")  


        df = pd.read_csv(output_csv_path)
        df = df.drop_duplicates()  
        df.drop(columns=['cat'], inplace=True, errors='ignore')


        coeff_var_col = f"ETa_cropland_{selectedYear}_coeff_var"
        avg_col = f"ETa_cropland_{selectedYear}_average"
        perc_98_col = f"ETa_cropland_{selectedYear}_percentile_98"
        equity_col = f"Equity"
        adequacy_col = f"Adequacy"



        # Calculate Equity and Adequacy
        if (
            coeff_var_col in df.columns and 
            avg_col in df.columns and 
            perc_98_col in df.columns and 
            (df[coeff_var_col] != 0).any() and 
            (df[avg_col] != 0).any() and 
            (df[perc_98_col] != 0).any()
        ):
            df[equity_col] = 100 - df[coeff_var_col]
            df[adequacy_col] = (df[avg_col] * 100) / df[perc_98_col]
        else:
            print(f"Columns missing for class {class_name}. Skipping Equity and Adequacy calculations.")

        df.drop(columns=[ perc_98_col], errors='ignore', inplace=True)



        for class_name in cropland_classes.keys():
            pixel_count_col = f"{class_name}_pixelcount_number"
            area_col = f"{class_name}_area_ha"  
            # Calculate area in hectares for the class
            if pixel_count_col in df.columns:
                # df[area_col] = df[pixel_count_col] * 3020 / 10000  
                df[area_col] = df[pixel_count_col] * 2978 / 10000  
                df.drop(columns=[pixel_count_col], errors='ignore', inplace=True)


        cropland_area_cols = [f"{class_name}_area_ha" for class_name in cropland_classes.keys()]
        df["Cropland_Area_ha"] = df[cropland_area_cols].sum(axis=1)  # Sum all class areas

        for col in [f"{class_name}_area_ha" for class_name in cropland_classes.keys()]:
            if col not in df.columns:
                df[col] = 0
            df[col] = df[col].fillna(0)


        df["Gross_Cropped_Area_ha"] = (
            df["exclusive_kharif_area_ha"]
            + df["exclusive_rabi_area_ha"]
            + df["exclusive_zaid_area_ha"]
            + (df["double_crop_area_ha"] * 2)
            + df["plantation_area_ha"]
        )
        df["Cropping_Intensity"] = df["Gross_Cropped_Area_ha"] *100/ df["Cropland_Area_ha"]
        df["Cropping_Intensity"] = df["Cropping_Intensity"].replace([np.inf, -np.inf, np.nan], 0)


        df = df.round(2)
        df.to_csv(output_csv_path, index=False)



        print(f"zonalstats exported successfully: {vector_name}")




    if __name__ == '__main__':
        GISDBASE = "/Volumes/ExternalSSD/eqipa_data/grassdata"
        LOCATION_NAME = "eqipa"
        MAPSET = "eqipa_stats"                 

        # Call the main function
        main(GISDBASE, LOCATION_NAME, MAPSET)



    ```