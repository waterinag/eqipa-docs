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

