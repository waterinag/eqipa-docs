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

   
    
    # Directory to export rasters
    export_dir = "/Volumes/ExternalSSD/eqipa_data/pcp_resamp"
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    # create list of all rasters to export
    raster_names=[]
    start_yr = '2023'
    end_yr = '2023'

    for year in range(int(start_yr), int(end_yr) + 1):
        for month in range(1, 13):
            file_name = f"imd_pcp_resamp_m_{year}_{month:02d}"
            raster_names.append(file_name)



    # raster_names=gs.list_grouped(type=['raster'], pattern=f'imd_pcp_resamp_m_*')['data_monthly']



    # Export rasters using r.out.gdal
    for raster in raster_names:
        output_tif = f"{export_dir}/{raster}.tif"
        gs.run_command(
            'r.out.gdal',
            input=raster,
            output=output_tif,
            format='GTiff',
            # createopt="COMPRESS=LZW",
            overwrite=True
        )
        print(f"Raster {raster} exported to {output_tif}")








if __name__ == '__main__':
    GISDBASE = "/Volumes/ExternalSSD/eqipa_data/grassdata"
    LOCATION_NAME = "eqipa"
    MAPSET = "data_monthly"                 

    # Call the main function
    main(GISDBASE, LOCATION_NAME, MAPSET)







