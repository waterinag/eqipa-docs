# 🛠️ System Setup

This section covers the complete setup of system dependencies and software required to run the **EQIPA (Evapotranspiration-based Quick Irrigation Performance Assessment)** application on a fresh **Ubuntu server**.

---

## Server Configuration
- The EQIPA Tool requires a Linux-based Ubuntu server with AMD or intel processor
minimum 8 cores, 5TB storage (considering future expansion of the database) and
minimum 126 GB RAM for efficient performance.
-  Full admin access to the server


---

## Prerequisite Software
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

## Install Required System Packages



Check Ubuntu version
```bash
lsb_release -a
```
Should be Ubuntu 22.04


```bash
sudo apt-get update
```

```bash
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
    python3-venv \
    pango1.0-tools
```

## Verify Installation

```bash
python3 --version
```

Install Python 3.10
```bash
sudo apt install -y python3.10 python3.10-venv python3.10-dev
```


Choose the default python version
```bash
sudo update-alternatives --config python3

  Selection    Path                Priority   Status
------------------------------------------------------------
* 0            /usr/bin/python3.8   2         auto mode
  1            /usr/bin/python3.8   2         manual mode
  2            /usr/bin/python3.10  1         manual mode

```



---

## Install PostgreSQL & PostGIS

```bash
sudo apt-get install -y postgresql postgresql-postgis
```

---

## Install GRASS GIS

```bash
sudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable
sudo apt-get install -y grass grass-dev
```

---



## Configure PostgreSQL User and Database

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

# Change password of postgres user*
ALTER USER postgres PASSWORD 'ipa_india';
ALTER USER ipa_india PASSWORD 'ipa_india123';

# Give more privileges to user ipa_india*
ALTER USER ipa_india WITH SUPERUSER;

# quit psql*
\q
```

Create the database and enable PostGIS:

```bash
# Create a new DB named "ipa_india":
createdb -U ipa_india -h localhost ipa_india

Pass: ipa_india123

psql -U ipa_india -h localhost ipa_india -c "CREATE EXTENSION postgis"
```

---

## ✅ Summary

| Component      | Version / Details                            |
|----------------|-----------------------------------------------|
| OS             | Ubuntu 22.04                 |
| Python         | 3.10                                          |
| PostgreSQL     | With PostGIS extension                        |
| GRASS GIS      | Installed via ubuntugis-unstable PPA          |
| Redis          | Required for Celery queue                     |
| Apache2 + uWSGI| For production deployment                     |


