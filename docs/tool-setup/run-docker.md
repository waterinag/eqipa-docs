# 🐳 Run EQIPA Using Docker

This guide explains how to build and run the EQIPA platform using Docker and `docker-compose` in localhost.

---

## 1: Install Docker

Install Docker Desktop for your OS:

- **Windows / macOS**:  
  👉 [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
  
- **Ubuntu/Linux**:  
  👉 [Install Docker Engine](https://docs.docker.com/engine/install/ubuntu/)

Make sure Docker and Docker Compose are installed:

```bash
docker --version
docker-compose --version
```

---

## 2: Build and Run Containers

### 🔨 Build Docker Image

```bash
docker-compose build
```

??? info "Dockerfile"
    Below is a sample `Dockerfile` that builds the full Django + GRASS + GDAL + Python environment inside Ubuntu 22.04:

    ```bash
    # Use Ubuntu as the base image
    FROM ubuntu:22.04

    # Set environment variables to avoid prompts during installation
    ENV DEBIAN_FRONTEND=noninteractive

    # Install required system dependencies
    RUN apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        python3-venv \
        git \
        gdal-bin \
        postgis \
        redis-server \
        virtualenv \
        build-essential \
        python3-dev \
        libpq-dev \
        pango1.0-tools \
        postgresql \
        postgresql-postgis \
        grass \
        grass-dev \
        && apt-get clean


    RUN mkdir /app

    # Set GRASS GIS environment variables (PERSISTENT)
    ENV GRASS_BIN=/usr/bin/grass
    ENV GRASS_DB=/app/grassdata
    ENV GRASS_LOCATION=wagen
    ENV GISBASE=/usr/lib/grass78
    ENV LD_LIBRARY_PATH=/usr/lib/grass78/lib:$LD_LIBRARY_PATH
    ENV PYTHONPATH=/usr/lib/grass78/etc/python:$PYTHONPATH


    # Set working directory
    WORKDIR /app


    COPY . /app

    COPY requirements.txt .
    RUN pip install --upgrade pip && pip install -r requirements.txt

    # Expose the port and define the default command
    EXPOSE 8000

    ```

### 🚀 Start All Services

```bash
docker-compose up -d
```


??? info "docker-compose.yml"
    Here’s a sample docker-compose.yml to bring up the full stack:

    ```    
    services:
        db:
            image: postgis/postgis:15-3.3
            container_name: postgres_db
            restart: always
            environment:
            POSTGRES_DB: ipa_test
            POSTGRES_USER: ipa_test
            POSTGRES_PASSWORD: ipa_test123
            # volumes:
            #   - postgres_data:/var/lib/postgresql/data
            volumes:
            - /Volumes/ExternalSSD/Docker/ipa_docker/postgres_data:/var/lib/postgresql/data
            ports:
            - "5433:5432"  # Host port 5433 mapped to container's port 5432

        redis:
            image: redis:alpine
            container_name: redis
            restart: always
            ports:
            - "6379:6379"

        web:
            build: .
            container_name: ipa_docker
            restart: always
            depends_on:
            - db
            ports:
            - "8000:8000"
            environment:
            DATABASE_URL: postgresql://ipa_test:ipa_test123@db:5432/ipa_test
            REDIS_URL: redis://redis:6379  # Define or remove if not using Redis
            volumes:
            - .:/app  # For development only; remove in production to use the baked image
            - /Volumes/ExternalSSD/grassdata:/mnt/grassdata
            command: sh -c "python3 manage.py makemigrations webapp && python3 manage.py migrate && python3 manage.py collectstatic --noinput && python3 manage.py runserver 0.0.0.0:8000"

        

        celery:
            build: .
            container_name: celery_worker
            restart: always
            depends_on:
            - redis
            - web
            - db
            environment:
            DATABASE_URL: postgresql://ipa_test:ipa_test123@db:5432/ipa_test
            REDIS_URL: redis://redis:6379
            volumes:
            - .:/app
            - /Volumes/ExternalSSD/grassdata:/mnt/grassdata
            command: celery -A ipa_india worker --loglevel=info

    volumes:
        postgres_data:

    ```




This will start:
- Django app (`ipa_docker`)
- PostgreSQL (`postgres_db`)
- Redis (`redis_cache`)
- Celery worker (`celery_worker`)

---

## Stop All Services

```bash
docker-compose down
```

---

## Rebuild Without Cache (Force Clean Build)

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## Check Logs

To verify that containers are running correctly, view logs for each service:

```bash
docker logs celery_worker
docker logs redis_cache
docker logs postgres_db
docker logs ipa_docker
```

---

## Enter the Django Container

You can access the app container directly and run Django management commands:

```bash
docker exec -it ipa_docker bash
```

Inside the container, you can:

```bash
# Create superuser (only first time)
python3 manage.py createsuperuser
```

> 💡 Tip: You can also run migrations or collectstatic here if needed.

---

✅ Your EQIPA platform should now be running at:
```
http://localhost:8000/
```

Update your `.env` and `docker-compose.yml` files as needed.
