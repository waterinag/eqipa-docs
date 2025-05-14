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
```

```bash
# Launch GRASS into the new mapset
grass /Volumes/ExternalSSD/eqipa_data/grassdata/eqipa/ind_monthly_data
```


> Notes:
- The new mapset must be inside an existing location.


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
r.info -g my_raster

v.info my_vector
```


### 10. Exit GRASS GIS
```bash
exit
```

