import os
import sys
import subprocess
import grass.script as gs
from grass.pygrass.modules.shortcuts import general as g
from grass.pygrass.modules.shortcuts import raster as r
from grass.pygrass.modules.shortcuts import display as d
from grass.pygrass.modules.shortcuts import vector as v
from grass.pygrass.gis import *
import grass.script as grass
import grass.script.setup as gsetup
import re




# Main function
def main(gisdb, location, mapset): 

    shapefile = 'IndiaBoundary.geojson' 

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

   

    vector_name = os.path.splitext(os.path.basename(shapefile))[0]


    # Import shapefile
    gs.run_command('v.import', input=shapefile, output=vector_name, overwrite=True)

    # Set region
    gs.run_command('g.region', vector=vector_name, res=0.00292)

    start_yr = '2023'
    end_yr = '2024'



    for year in range(int(start_yr), int(end_yr) + 1):
        for month in range(1,13):
            input_raster = f"imd_pcp_m_{year}_{month:02d}"
            resampled_raster = f"imd_pcp_resamp_m_{year}_{month:02d}"

            # This resampling only change the pixel size, will not apply any interpolation or will not change pixel value
            gs.run_command(
                'r.resample',
                input=input_raster,
                output=resampled_raster,
                overwrite=True
            )





if __name__ == '__main__':
    GISDBASE = "/Volumes/ExternalSSD/eqipa_data/grassdata"
    LOCATION_NAME = "eqipa"
    MAPSET = "data_monthly"                 

    # Call the main function
    main(GISDBASE, LOCATION_NAME, MAPSET)







