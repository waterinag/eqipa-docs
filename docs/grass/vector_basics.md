# Vector Operations
This section explains key vector operations in GRASS GIS using command-line modules. These include buffering, overlays, filtering, attribute queries, and conversions — all handled in terminal mode.

---

### List Vector Maps
```bash
# List all available vector maps in the current mapset:
g.list type=vector

# Get basic information about a vector map:
v.info map=roads

# Check the attribute table:
v.db.select map=roads

```

### Create Buffers Around Features
```bash
# Use v.buffer to create buffer zones (e.g., 1000-meter buffer around roads):
v.buffer input=roads output=roads_buffer distance=1000

```

### Select and Extract Features
```bash

# Select and Extract Features by Attribute
# Use v.extract to filter features using SQL-like queries.
v.extract input=roads output=highways where="type = 'highway'"

# Check the attribute table:
v.db.select map=roads

```

### Overlay Vector Layers
```bash
# Intersect
v.overlay ainput=landuse binput=admin_boundaries operator=and output=landuse_admin
# Union:
v.overlay ainput=layer1 binput=layer2 operator=or output=combined_layer

# Dissolve: Merge adjacent polygons with the same attribute
v.dissolve input=landuse output=landuse_dissolved column=category

```

### Convert Between Raster and Vector
```bash
# Raster to Vector:
r.to.vect input=classified_map output=land_units type=area


# Vector to Raster:
v.to.rast input=land_units output=land_raster use=cat


```

### Reproject a Vector Map
```bash
# To reproject from one location to another, use v.proj inside the target location
v.proj location=source_location mapset=PERMANENT input=roads output=roads_projected


```


### Export Vector Maps
```bash
# Export to Shapefile or GeoPackage:
v.out.ogr input=roads_buffer output=roads_buffer.shp format=ESRI_Shapefile

# Export to GeoJSON:
v.out.ogr input=roads output=roads.geojson format=GeoJSON

```



