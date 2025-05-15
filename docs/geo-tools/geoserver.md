# GeoServer 

GeoServer is a powerful open-source server for sharing geospatial data using open standards such as WMS, WFS, and WCS. It allows you to publish raster and vector data formats from databases, files, and remote services with ease.

This tutorial walks through the installation, configuration, and usage of GeoServer for web-based geospatial data publishing.

---

### 1. Installation

- Download from the official site:  
   [https://geoserver.org/download](https://geoserver.org/download)


- Extract the ZIP file:

```bash

unzip geoserver-<version>.zip
cd geoserver-<version>/bin

```

- Run GeoServer:

```bash

# Linux/Mac
./startup.sh

# Windows
startup.bat

```


GeoServer will be accessible at:
http://localhost:8080/geoserver


---

### 2. Basic Interface Overview
Once logged in:

- Data → Stores: Register new raster/vector sources (Shapefile, PostGIS, GeoTIFF, etc.)
- Data → Layers: Publish individual layers from a Store
- Layer Preview: Test your services (WMS/WFS/WCS)
- Services: Configure WMS, WFS, and WCS capabilities

---

### 3. Add and Publish Data
Add a Data Store
To publish data:

- Navigate to Data → Stores
- Choose store type (e.g., Shapefile, GeoTIFF, PostGIS)
- Fill in connection details
- Save

Publish a Layer

- After creating a store, click Publish
- Configure the following:
    - Name
    - Coordinate Reference System (CRS)
    - Bounding box
- Save

Layer will now appear in Layer Preview.

---

### 4. Styling Layers (SLD)
You can style layers using SLD (Styled Layer Descriptor):

- Go to Styles → Add New Style
- Name your style and paste the SLD XML
- Save and apply to your layer
- Use GeoServer SLD Cookbook for examples.


---



### 📚 Learn More

- [GeoServer Official Site](https://docs.geoserver.org/)
- [GeoServer Tutorials](https://docs.geoserver.org/main/en/user/tutorials/index.html)
- [GeoServer REST API](https://docs.geoserver.org/stable/en/user/rest/)

