# ⚙️ Environment Setup for Dataset Download

To download or process these dataset, you need to set up a Python environment with all required libraries.

## 1: On Local PC

### 1: Install Conda (Recommended)

Conda is a cross-platform environment manager that makes it easy to install geospatial libraries like GDAL.

### Windows

1. Download the **Miniconda installer**:  
   👉 [Miniconda Windows 64-bit](https://docs.conda.io/en/latest/miniconda.html#windows-installers)
2. Run the installer and choose “Add Miniconda to PATH” during setup.
3. After installation, open **Anaconda Prompt** or **Command Prompt** and test:

```bash
conda --version
```

---

### MacOS OS

1. Download the installer for macOS from:  
   👉 [Miniconda macOS](https://docs.conda.io/en/latest/miniconda.html#macos-installers)

2. Run the installer


3. Restart terminal and verify:

```bash
conda --version
```

---

### 2: Create a Conda Environment

Conda makes it easy to isolate packages:

```bash
conda create --name eqipa_env python=3.10
conda activate eqipa_env
```

---

### 3: Install GDAL and Geospatial Libraries

Use the `conda-forge` channel:

```bash
conda install -c conda-forge gdal libgdal-jp2openjpeg 
```

Verify installation:

```bash
gdalinfo --version
```

Then install required Python libraries:

```bash
pip install pandas tqdm geopandas numpy xarray rioxarray rasterio netCDF4 requests
```

---

### Optional: Save Environment for Future Use

```bash
conda env export > eqipa_env.yml
```

Others can recreate the environment with:

```bash
conda env create -f eqipa_env.yml
```

---




## On Ubuntu (Without Conda)

### 1. Install GDAL system packages:
```bash
sudo apt-get install gdal-bin libgdal-dev libspatialindex-dev
```
---

### 2. Create and Activate a Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Required Python Libraries

```bash
pip install pandas tqdm geopandas numpy xarray rioxarray rasterio netCDF4
```

---

### 4. Recommended `requirements.txt`

You can create a `requirements.txt` for reuse:

```txt
pandas
tqdm
geopandas
numpy
xarray
rioxarray
rasterio
netCDF4
```

Install with:

```bash
pip install -r requirements.txt
```

---

## ✅ Next Step

Once the environment is set up, proceed to the dataset you want to download.