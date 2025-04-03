# 🛠️ System Setup

This section covers the complete setup of system dependencies and software required to run the **EQIPA (Evapotranspiration-based Quick Irrigation Performance Assessment)** application on a fresh Ubuntu server (tested on Ubuntu 20.04+).

---

## 🧰 Prerequisite Software

Ensure the following software is installed:

- Python 3.10
- PostgreSQL
- PostGIS
- GRASS GIS
- GDAL
- Redis
- Apache2
- Virtualenv
- Git
- Build tools & Python development headers

---

## 📦 Install Required System Packages

```bash
sudo apt-get update

sudo apt-get install -y \
    git \
    gdal-bin \
    apache2 \
    postgis \
    redis-server \
    virtualenv \
    build-essential \
    python3-dev \
    libpq-dev \
    pango1.0-tools
```

---

## 🧭 Install PostgreSQL & PostGIS

```bash
sudo apt-get install -y postgresql postgresql-postgis
```

---

## 🌱 Install GRASS GIS

```bash
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
sudo apt-get update
sudo apt-get install -y grass grass-dev
```

---

## 🗺️ Create a GRASS GIS Location

```bash
grass -c EPSG:4326 -e /mnt/mapdata/grassdata/ipa_india
```

Verify the mapset:

```bash
ls /mnt/mapdata/grassdata/ipa_india
```

> **Note:** In `settings.py`, the value of `GRASS_DB` should be set as `/mnt/mapdata/grassdata`

---

## 🗄️ Configure PostgreSQL User and Database

Create a new PostgreSQL user:

```bash
sudo -u postgres createuser ipa_india
```

Login to PostgreSQL:

```bash
sudo -u postgres psql
```

Inside psql:

```sql
ALTER USER postgres PASSWORD 'ipa_india';
ALTER USER ipa_india PASSWORD 'ipa_india123';
ALTER USER ipa_india WITH SUPERUSER;
\q
```

Create the database and enable PostGIS:

```bash
createdb -U ipa_india -h localhost ipa_india
psql -U ipa_india -h localhost ipa_india -c "CREATE EXTENSION postgis"
```

---

## ✅ Summary

| Component      | Version / Details                            |
|----------------|-----------------------------------------------|
| OS             | Ubuntu 20.04 or later                         |
| Python         | 3.10                                          |
| PostgreSQL     | With PostGIS extension                        |
| GRASS GIS      | Installed via ubuntugis-unstable PPA          |
| Redis          | Required for Celery queue                     |
| Apache2 + uWSGI| For production deployment                     |

You're now ready to proceed with setting up the Django app. → [Continue to Running App Locally](run-locally.md)
