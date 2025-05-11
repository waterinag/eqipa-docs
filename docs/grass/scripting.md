# GRASS GIS Scripting with Python

GRASS GIS can be automated and extended using Python. This page demonstrates how to write a complete geospatial analysis workflow using GRASS GIS commands in Python using `grass.script` and `pygrass`.

---

###  Setting Up the Python Environment

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

### Script Overview
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




    GISDBASE = "/Volumes/ExternalSSD/grassdata"
    LOCATION_NAME = "wagen"
    MAPSET = "eqipa_stats"


    geojson_file = 'StatesBoundary.geojson'
    selectedYear="2022_2023"


    os.environ['GISDBASE'] = GISDBASE
    os.environ['LOCATION_NAME'] = LOCATION_NAME

    # Check if mapset exists; if not, create it
    mapset_path = os.path.join(GISDBASE, LOCATION_NAME, MAPSET)
    if not os.path.exists(mapset_path):
        print(f"Mapset '{MAPSET}' does not exist. Creating new mapset...")
        # Create the new mapset
        gs.run_command('g.mapset', flags='c', mapset=MAPSET, location=LOCATION_NAME, dbase=GISDBASE)
    else:
        print(f"Mapset '{MAPSET}' already exists.")

    # Initialize GRASS session
    gsetup.init(GISDBASE, LOCATION_NAME, MAPSET)
    print(f"GRASS GIS session initialized in {GISDBASE}/{LOCATION_NAME}/{MAPSET}")


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
    g.mapsets(mapset="nrsc_lulc,ind_annual_data", operation="add")


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


    lcc_map=f"LULC_250k_{selectedYear}"
    eta_map=f"wapor3_eta_a_{selectedYear}"
    tbp_map=f"wapor3_tbp_a_{selectedYear}"
    pcp_map=f"imd_pcp_resamp_a_{selectedYear}"
    bwp_map =f"wapor3_bwp_a_{selectedYear}"


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


    info_data = {
        "Abbreviation": [
            "ETa_average", 
            "ETa_cropland_average", 
            "ETa_cropland_coeff_var", 
            # "ETa_cropland_stddev", 
            # "etb_a_average", 
            # "etg_a_average", 
            # "tbp_a_average",
            "PCP_average", 
            "Equity", 
            "Adequacy", 
            "BLP", 
            "BWP", 
            "exclusive_kharif", 
            "exclusive_rabi", 
            "exclusive_zaid", 
            "double_crop", 
            "plantation", 
            "Cropland", 
            "Gross cropped area", 
            "Cropping Intensity", 
            "Year",
            "Annual period",
        ],
        "Definition": [
            "Average annual Evapotranspiration (ETa) in the command area",
            "Average annual ETa over cropland in the command area",
            "coefficient of variance of annual ETa over cropland in the command area",
            # "standard deviation of annual ETa over cropland in the command area",
            # "Average annual Blue ET in the command area",
            # "Average annual Green ET in the command area",
            # "Average annual Total biomass production in the command area",
            "Average annual precipitation in the command area",
            "1- CV of ETa",
            "ETa/ETp, [ETp = 98 percentile of ETa]",
            "Biomass land Productivity",
            "Biomass Water Productivity",
            "Seasonal Crop land with crops grown during June to November period of agricultural calendar year.",
            "Seasonal Crop land with crops grown during November to April period of agricultural calendar year.",
            "Seasonal Crop land with crops grown during April to June period of agricultural calendar year.",
            "Land with crops grown in more than one season specified above. This will also include annual crops.",
            "Trees which are artificially planted.",
            "Kharif + Rabi + Zaid + Double/Triple Crop  + Plantation/Orchard",
            "Kharif + Rabi + Zaid + Double/Triple Crop *2  + Plantation/Orchard",
            "Gross cropped area*100 / Cropland",
            selectedYear,
            "June to May"
        ],
        "Unit": [
            "mm/year", 
            "mm/year", 
            "mm/year", 
            # "mm/year", 
            # "mm/year", 
            # "mm/year", 
            # 'kg/ha/year',
            "mm/year", 
            "%", 
            "%", 
            "kg/ha", 
            "kg/m³", 
            "ha",
            "ha",
            "ha",
            "ha",
            "ha",
            "ha",
            "ha",
            "%", 
            "", 
            "",
        ]
    }

    info_df = pd.DataFrame(info_data)

    # Write to Excel with two sheets
    with pd.ExcelWriter(output_excel_path, engine="openpyxl") as writer:
        info_df.to_excel(writer, sheet_name="Info", index=False)
        df.to_excel(writer, sheet_name="Stats", index=False)


    print(f"zonalstats exported successfully: {vector_name}")

    ```




