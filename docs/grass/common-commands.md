# Common GRASS GIS Commands
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

