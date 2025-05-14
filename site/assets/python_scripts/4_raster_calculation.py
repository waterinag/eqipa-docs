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

    g.mapsets(mapset="nrsc_lulc", operation="add")


    # Set region
    gs.run_command('g.region', vector=vector_name, res=0.00292)

    start_yr = '2023'
    end_yr = '2023'


    timerange = range(int(start_yr), int(end_yr) + 1)
    years = list(timerange)

    years_str = [f"{y}_{y + 1}" for y in years]

    print("years_str")
    print(years_str)


    for y in years_str:
        # Apply raster mask
        # gs.run_command('r.mask', raster=f'LULC_250k_{y}', maskcats='2 3 4 5 7', overwrite=True)
        gs.run_command('r.mask', raster=f'LULC_250k_2022_2023', maskcats='2 3 4 5 7', overwrite=True)

        # Perform map calculations
        gs.mapcalc(f"wapor_eta_a_cropland_{y} = wapor_eta_a_{y}", overwrite=True)
        gs.mapcalc(f"wapor_tbp_a_cropland_{y} = wapor_tbp_a_{y}", overwrite=True)
        gs.mapcalc(f"wapor_bwp_a_{y} = wapor_tbp_a_{y} / (wapor_eta_a_{y} * 10)",overwrite=True)
        gs.run_command('r.mask', flags='r')


if __name__ == '__main__':
    GISDBASE = "/Volumes/ExternalSSD/eqipa_data/grassdata"
    LOCATION_NAME = "eqipa"
    MAPSET = "data_annual"                 

    # Call the main function
    main(GISDBASE, LOCATION_NAME, MAPSET)







