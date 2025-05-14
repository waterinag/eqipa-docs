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

   

    # Argi year: June - May
    start_month='6'
    end_month='5'

    start_yr = '2023'
    end_yr = '2023'

    agri_yr_timerange = []

    for year in range(int(start_yr), int(end_yr) + 1):
        months_range = []

        if int(start_month) > int(end_month):
            for month in range(int(start_month), 13):
                months_range.append(f"{year}_{month:02d}")
            for month in range(1, int(end_month) + 1):
                months_range.append(f"{year + 1}_{month:02d}")
        else:
            for month in range(int(start_month), int(end_month) + 1):
                months_range.append(f"{year}_{month:02d}")
        agri_yr_timerange.append(months_range)

        print('agri_yr_timerange',agri_yr_timerange)

        timerange = range(int(start_yr), int(end_yr) + 1)
        years = list(timerange)

        # Create strings like "2022_2023"
        years_str = [f"{y}_{y + 1}" for y in years]

        print("years_str")
        print(years_str)

    # Add other mapsets to the current session
    gs.run_command('g.mapsets', mapset="data_monthly", operation="add")
    vector_name = os.path.splitext(os.path.basename(shapefile))[0]


    # Import shapefile
    gs.run_command('v.import', input=shapefile, output=vector_name, overwrite=True)

    # Set region
    gs.run_command('g.region', vector=vector_name, res=0.00292)


    for y in agri_yr_timerange:
        yr = int(y[0].split("_")[0]) 
        yr_string = f'{yr}_{yr + 1}' 
        print(yr_string)

        eta_maps_list = [f"wapor_eta_m_{i}" for i in y]
        eta_out_map_name = f'wapor_eta_a_{yr_string}'

        tbp_maps_list = [f"wapor_tbp_m_{i}" for i in y]
        tbp_out_map_name = f'wapor_tbp_a_{yr_string}'
    
        pcp_maps_list = [f"imd_pcp_resam_m_{i}" for i in y]
        pcp_out_map_name = f'imd_pcp_resamp_a_{yr_string}'

        gs.run_command('r.series', input=eta_maps_list, output=eta_out_map_name, method='sum', overwrite=True)
        gs.run_command('r.series', input=tbp_maps_list, output=tbp_out_map_name, method='sum', overwrite=True)
        gs.run_command('r.series', input=pcp_maps_list, output=pcp_out_map_name, method='sum', overwrite=True)




if __name__ == '__main__':
    GISDBASE = "/Volumes/ExternalSSD/eqipa_data/grassdata"
    LOCATION_NAME = "eqipa"
    MAPSET = "data_annual"                 

    # Call the main function
    main(GISDBASE, LOCATION_NAME, MAPSET)

