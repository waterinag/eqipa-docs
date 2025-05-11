# GRASS GIS Quickstart
When launching GRASS GIS for the first time, you will open a default project "world_latlog_wgs84" where you can find a map layer called "country_boundaries" showing a world map in the WGS84 coordinate system.


The main component of the Data tab is the Data Catalog which shows the GRASS GIS hierarchical structure consisting of database, project and mapset .


---

## Interface Overview

The GRASS GUI has several panels and tools:

- **Layer Manager**: Controls loaded map layers.
- **Map Display**: Shows raster/vector data.
- **Data Catalog**: Displays the GRASS data hierarchy.
- **Console**: Run GRASS commands directly.
- **Modules Search Bar**: Search for specific tools and commands.

---

## Getting Started with GRASS GIS

This section explains how to set up your working environment in GRASS GIS and import your geospatial data.


### 1. Create a GRASS Database Directory

Open a terminal and create a directory that will act as the GRASS GIS database:

```bash
mkdir -p /Volumes/ExternalSSD/eqipa_data/grassdata
```
>  This directory will store all Locations and Mapsets.


This is the root directory that will contain all your GRASS locations and mapsets.


### 2. Launch GRASS GIS
```bash
grass
```

In the startup screen:

- Set GIS Database to: /Volumes/ExternalSSD/eqipa_data/grassdata
- Click on New next to Location

### 3. Create a New Location Using EPSG Code
Use grass with the -c flag to create a new Location based on a coordinate reference system (CRS).
```bash
grass -c EPSG:4326 /Volumes/ExternalSSD/eqipa_data/grassdata/eqipa
```
This command:

- Creates a new Location named "eqipa"
- Uses EPSG:4326 (WGS 84 coordinate system)
- Initializes the default PERMANENT mapset


### 4. Create and Start a New Mapset
Create a New Mapset
```bash
# create a new mapset 
g.mapset -c mapset=ind_monthly_data location=eqipa

## Another way to ceate new mapset
# Navigate to the location directory
cd /Volumes/ExternalSSD/eqipa_data/grassdata/eqipa

# Create the new mapset directory
mkdir ind_monthly_data

# Copy the default region settings (WIND file) from PERMANENT
cp PERMANENT/DEFAULT_WIND ind_monthly_data/WIND

# Launch GRASS into the new mapset
grass /Volumes/ExternalSSD/eqipa_data/grassdata/eqipa/ind_monthly_data
```
> Notes:
- The new mapset must be inside an existing location.
- You cannot use grass -c for creating a mapset — it’s only for creating a new location.

List all available mapsets
```bash
g.mapsets -l
```

Switch to a different mapset within the same location
```bash
g.mapset mapset=ind_annual_data  
```






### 5. Set the Computational Region (Optional)
```bash
g.region raster=<existing_raster>
# or
g.region vector=<existing_vector>

# Set Resolution
g.region res=0.003

# To manually set region boundaries and resolution:
g.region n=25 s=10 e=90 w=70 res=0.01 -p

```

### 6. Import Raster Data
Single Raster Import
```bash
r.import input=/path/to/raster.tif output=my_raster
```

Bulk Import Raster Files
```bash
for file in /path/to/pcp_imd_monthly/*.tif; do
    name=$(basename "$file" .tif)
    r.import input="$file" output="$name"
done
```



### 7. Import Vector Data
Single Vector Import
```bash
v.import input=/path/to/vector.shp output=my_vector
```

Bulk Import Vector Files
```bash
for file in /path/to/folder/*.shp; do
    name=$(basename "$file" .shp)
    v.import input="$file" output="$name"
done

```

### 8. List Imported Layers
```bash
g.list type=raster
g.list type=vector
```

### 9. View Layer Metadata
```bash
r.info my_raster
v.info my_vector
```


### 10. Exit GRASS GIS
```bash
exit
```


## Common GRASS GIS Commands

Here are some frequently used GRASS GIS commands useful for working with rasters, vectors, regions, and exporting data.

---

### 1. Starting and Managing Sessions

```bash
# Create a new location from scratch
grass -c /mnt/mapdata/grassdata/new_location


# Start GRASS in an existing location/mapset
grass /path/to/mapset/location

# Create a new mapset inside an existing location
g.mapset -c mapset=test location=eqipa

# Switch to a different mapset
g.mapset mapset=pcp_mean_monthly

# Add multiple mapsets to current search path
g.mapsets mapset=nrsc_lulc,ind_annual_data operation=add
```

---

### 2. Map and Region Management

```bash
# Check raster resolution and extent
r.info -g pcpm_imd_2023_10

# List all rasters and vectors
g.list type=raster,vector

# List all rasters and export to file
g.list rast map=etg_etb_ind_monthly >> names.txt

# Set region to match a raster or vector map
g.region raster=your_raster_map
g.region vector=your_vector_map

# View current region settings
g.region -p
```

---

### 3. Import Data

```bash
# Import a raster file (GeoTIFF, NetCDF, etc.)
r.import input=chirps_pcp.tif output=chirps_pcp

# Import a vector file (GeoJSON, Shapefile, etc.)
v.import input=IndiaBoundary.geojson output=india_boundary
```

---

### 4. Raster & Vector Info

```bash
# View metadata of a raster or vector
r.info map=chirps_pcp
v.info map=india_boundary
```

---

### 5. Raster Operations

```bash
# Map algebra
r.mapcalc expression="output_map = raster1 + raster2"

# Zonal statistics
r.univar map=raster_map zones=vector_zones_map

# Raster statistics summary
r.stats -a input=raster_map_name

# Merge rasters
r.patch input=map1,map2 output=merged_map

# Clip raster with current region
r.clip input=your_raster output=clipped_raster

# Resample raster
r.resample input=your_raster output=resampled_raster

# Apply raster mask
r.mask raster=mask_map

# Export raster to GeoTIFF
r.out.gdal input=raster_map output=/path/output.tif format=GTiff
```

---

### 6. Vector Operations

```bash
# Buffer vector geometry
v.buffer input=your_vector output=buffered_vector distance=500

# Convert vector to raster
v.to.rast input=your_vector output=rasterized_vector use=cat

# Convert raster to vector
r.to.vect input=your_raster output=vector_map feature=area

# Merge vectors
v.patch input=vector1,vector2 output=merged_vector

# Export vector to Shapefile
v.out.ogr input=vector_map output=/path/output.shp format=ESRI_Shapefile
```

---

> Tip: Always verify the region and CRS settings (`g.region -p`) before running any spatial operation.


---

