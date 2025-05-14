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

   
    input_folder = "/Volumes/ExternalSSD/eqipa_data/pcp_imd_monthly"
    for file in os.listdir(input_folder):
        if file.endswith(".tif"):
            full_path = os.path.join(input_folder, file)
            name = os.path.splitext(file)[0]  
            print(f"Importing {file} as {name}")
            gs.run_command('r.import', input=full_path, output=name)




if __name__ == '__main__':
    GISDBASE = "/Volumes/ExternalSSD/eqipa_data/grassdata"
    LOCATION_NAME = "eqipa"
    MAPSET = "data_monthly"                 

    # Call the main function
    main(GISDBASE, LOCATION_NAME, MAPSET)







