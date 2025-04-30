# 🌍 GDAL (Geospatial Data Abstraction Library)

**GDAL** is an open-source library used in GIS (Geographic Information Systems) for reading, writing, and processing raster and vector geospatial data. It acts as a translator between different geospatial data formats and is widely used in software like QGIS, GRASS GIS, and many Python-based GIS workflows.

### Key Features 
- Supports 100+ raster formats (GeoTIFF, NetCDF, HDF, etc.) and vector formats (Shapefile, GeoJSON, KML, etc.)
- Powerful command-line tools (like gdalwarp, gdal_translate, ogr2ogr) for data conversion, reprojection, clipping, mosaicking, and more.
- Allows raster and vector data transformation, such as projection changes, resampling, and format conversion.
- Well-supported Python bindings for automation and integration with geospatial workflows.
- Extensively used in remote sensing, cartography, and spatial analysis.

---

## Essential GDAL Commands

```bash
# View Raster Metadata
gdalinfo input.tif

# Reproject Raster to EPSG:4326
gdalwarp -t_srs EPSG:4326 input.tif output.tif

# Extract Band from Multi-band Raster
gdal_translate -b 1 input.tif output_band1.tif

# Convert Raster Format (e.g. TIFF to PNG)
gdal_translate input.tif output.png

# Clip Raster using Bounding Box (ULX, ULY, LRX, LRY)
gdal_translate -projwin ulx uly lrx lry input.tif output.tif

# Merge Multiple Rasters
gdal_merge.py -o output.tif input1.tif input2.tif

# Resample Raster to New Resolution
gdalwarp -tr 1000 1000 input.tif output.tif

# Compute Raster Statistics
gdalinfo -stats input.tif

# Convert to GeoTIFF Format
gdal_translate -of GTiff input.tif output.tif

# Polygonize Raster to Vector
gdal_polygonize.py input.tif -f "ESRI Shapefile" output.shp

# Build Raster Pyramids (Overviews)
gdaladdo -r average input.tif 2 4 8 16

# Warp Raster to Cutline Boundary
gdalwarp -cutline boundary.shp -crop_to_cutline input.tif output.tif

# Convert Raster to ASCII Grid
gdal_translate -of AAIGrid input.tif output.asc

# Get NoData Value
gdalinfo -mm input.tif

# Set NoData Value
gdalwarp -dstnodata -9999 input.tif output.tif

# Rasterize Vector Data
gdal_rasterize -a attribute -tr 1000 1000 -l layer vector.shp output.tif

# Compress the raster
gdal_translate -co COMPRESS=DEFLATE input.tif output.tif

```



---



### 📚 Learn More

- [GDAL Official Site](https://gdal.org/en/stable/)
- [Mastering GDAL Tools (Full Course)](https://courses.spatialthoughts.com/gdal-tools.html)

   