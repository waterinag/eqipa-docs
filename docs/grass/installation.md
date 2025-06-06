# Installation and Setup

GRASS GIS can be installed on all major operating systems, including Windows, macOS, and Linux. Follow the instructions below for your platform.


---

### Install GRASS GIS

Download the latest stable release from the official site: [https://grass.osgeo.org/download/](https://grass.osgeo.org/download/)
Installation Guide: [https://grasswiki.osgeo.org/wiki/Installation_Guide](https://grasswiki.osgeo.org/wiki/Installation_Guide)

Choose the installer based on your operating system:

- Standalone installer for **Windows**
- `.dmg` package for **MacOS**
- Ubuntu:
```bash
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
sudo apt-get update
sudo apt-get install grass grass-gui grass-dev
```


### Verifying Installation
After installation, launch GRASS GIS from your system menu or use the CLI:
```bash
grass
```
You should see the GRASS startup window asking you to select or create a Location and Mapset.


### Sample Data


- **India Boundary**  
  ➡️ [Download IndiaBoundary.geojson](https://waterinag.github.io/eqipa-docs/assets/IndiaBoundary.geojson)

- **India States**  
  ➡️ [Download IndiaStates.geojson](https://waterinag.github.io/eqipa-docs/assets/IndiaStates.geojson)

- **Bihar Commands**  
  ➡️ [Download Bihar_CA.geojson](https://waterinag.github.io/eqipa-docs/assets/Bihar_CA.geojson)

- **Western Kosi Command**  
  ➡️ [Download Western_Kosi.geojson](https://waterinag.github.io/eqipa-docs/assets/Western_Kosi.geojson)


