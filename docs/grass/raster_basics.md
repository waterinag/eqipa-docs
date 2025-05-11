# Raster Analysis 

This section introduces fundamental raster operations in GRASS GIS. You'll learn how to perform map algebra, clipping rasters to a boundary, statistical summaries, LULC masking, raster algebra, and temporal aggregation.

---

### Clip Raster to a Boundary

```bash
# Set region to match vector boundary
g.region vector=command_boundary align=wapor_eta_m_2023_01 -p

# Create a mask using the boundary
r.mask vector=command_boundary

# Clip the raster
r.mapcalc "eta_clipped = wapor_eta_m_2023_01"

# Remove the mask after clipping
r.mask -r
```

### Get Raster Statistics (min, max, mean, median)
```bash
# Basic stats:
r.univar map=eta_clipped -g

# For median and advanced stats:
r.stats -aCn input=eta_clipped

# For raster category counts, area and values:
r.report map=eta_clipped units=h,c,p
```



### LULC Masking (e.g., Mask only Cropland Areas)
```bash
# Assuming you have an LULC raster (esa_lulc_2021) where value 40 = cropland:
r.mapcalc "cropland_mask = if(esa_lulc_2021 == 40, 1, null())"
r.mask raster=cropland_mask

# Apply it to another raster:
r.mapcalc "eta_cropland = wapor_eta_m_2023_01"

# Then remove the mask:
r.mask -r

```


### Raster Calculation
```bash
# Water Productivity (WP)
r.mapcalc "wp_2023_01 = tbp_2023_01 / (wapor_eta_m_2023_01 * 10)"
```

### Temporal Raster Analysis
```bash
# Mean over years
r.series input=wapor_eta_a_2018,wapor_eta_a_2019,wapor_eta_a_2020,wapor_eta_a_2021 output=eta_mean_2018_2021 method=average

# Max or Min over years
r.series input=wapor_eta_a_2018,wapor_eta_a_2019,wapor_eta_a_2020,wapor_eta_a_2021 output=eta_max_2018_2021 method=maximum

# Aggregate Monthly to Annual Raster: Annual Sum
r.series input=$(g.list type=raster pattern="wapor_eta_m_2023_*" separator=comma) output=wapor_eta_a_2023_sum method=sum

# Aggregate Monthly to Annual Raster: Annual Mean
r.series input=$(g.list type=raster pattern="wapor_eta_m_2023_*" separator=comma) output=wapor_eta_a_2023_mean method=average


```


