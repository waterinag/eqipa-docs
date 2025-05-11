# Zonal Statistics (Terminal)

Zonal statistics summarize raster values (e.g., mean, sum, count) within vector zones such as administrative boundaries, watersheds, or land parcels. This guide explains how to perform zonal statistics in GRASS GIS using a GeoJSON boundary file and a raster map.

---

### Import Vector Boundary (GeoJSON)

Use `v.in.ogr` to import a GeoJSON file:

```bash
v.in.ogr input=/path/to/boundaries.geojson output=zones
```
> 🔍 Check if the projection of your GeoJSON matches the current GRASS location. If not, reproject the vector (see section below).

### Import Raster Map

Use r.import to bring in a GeoTIFF or similar raster file:

```bash
r.import input=/path/to/raster.tif output=my_raster

```


### Set Computational Region

Match the region to your raster map:

```bash
g.region raster=my_raster -p

# (Optional) Expand region to fully cover vector zones:
g.region vector=zones align=my_raster

```



### Perform Zonal Statistics with v.rast.stats

Use the vector map (zones) to compute stats from the raster (my_raster) for each polygon:

```bash
v.rast.stats map=zones raster=my_raster column_prefix=stats method=average,sum,count
```

- column_prefix: Adds columns like stats_mean, stats_sum, etc.
- method: Can be one or more of: average, sum, count, min, max, stddev

This updates the attribute table of the vector map with the calculated values.


### View Results

Display the updated attribute table:

```bash
v.db.select map=zones

```



### Optional: Export the Results to GeoJSON or Shapefile

```bash
# Export GeoJSON
v.out.ogr input=zones output=zones_stats.geojson format=GeoJSON

# or Export Shapefile
v.out.ogr input=zones output=zones_stats.shp format=ESRI_Shapefile

# or Export Attribute Table to CSV
v.db.select map=zones separator=comma file=zones_stats.csv

```


### (Optional) Reproject GeoJSON if Needed

If your GeoJSON CRS doesn't match the current GRASS location, you can either:

- Reproject using GDAL before importing, or
- Import it into a matching GRASS location, and use v.proj

```bash
# Run this inside your target location
v.proj location=source_location mapset=PERMANENT input=zones output=zones_reprojected

```
