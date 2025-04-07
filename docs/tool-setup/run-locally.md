# 💻 Running App in Development Mode

This guide explains how to set up and run the EQIPA Django app in a development environment.

---

## 1: Copy the code to the system


---

## 2: Create and Activate a Virtual Environment

Create a Python 3 virtual environment inside the `webapp` folder:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3: Install Python Dependencies

Install all required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## 4: Configure Django Settings

Open `ipa_india/settings.py` and update the following:

- `DATABASES` section → add username, password, and DB name
- `GRASS_DB` path → e.g., `/mnt/mapdata/grassdata/ipa_india`

---

## 5: Apply Migrations & Collect Static Files

Run the following commands to prepare your database and static files:

```bash
python manage.py makemigrations webapp
python manage.py migrate
python manage.py collectstatic
```

---

## 6: Create a Superuser

```bash
python manage.py createsuperuser --username admin
```

Sample credentials:

- **Username:** `admin`
- **Email:** `your-email@gmail.com`
- **Password:** `your-pass`

---

## 7: Test Local Server

Run the Django development server:

```bash
python manage.py runserver
```

To access from another device on the same network:

```bash
python manage.py runserver 0.0.0.0:8001
```

Now open your browser at:

- [http://127.0.0.1:8000](http://127.0.0.1:8000)
- or your local IP, e.g.: `http://10.37.129.2:8001/`

---

!!! note

    Celery is used for handling long-running background tasks (like report generation). Start the worker using:

    ```bash
    celery -A ipa_india worker -l INFO
    ```

    To run Celery inside a `screen` session (optional):

    ```bash
    screen -S ipa_celery
    celery -A ipa_india worker -l INFO
    ```

    To detach from the screen session:

    ```bash
    Ctrl + A, then D
    ```

    To reattach:

    ```bash
    screen -r ipa_celery
    ```


??? info "📦 Screen"

    Learn more: [How to Use Linux Screen](https://linuxize.com/post/how-to-use-linux-screen/)

    Use `screen` to manage background processes like Celery or the Django dev server:

    **🔍 Check running screens:**
    ```bash
    screen -r
    ```

    **🔄 Attach to a screen:**
    ```bash
    screen -r <screen_name>
    ```

    **🔙 Detach a screen:**
    ```bash
    screen -d <screen_name>
    ```

    **❌ Delete (terminate) a screen:**
    ```bash
    screen -S <screen_name> -X quit
    ```

    **🆕 Start a new screen session:**
    ```bash
    screen -S <screen_name>
    ```







---

##  Admin Site Setup

When running the server for the first time, visit:

```
http://127.0.0.1:8000/admin
```

Go to the **"Sites"** tab and update the domain to match your current host:

- For local testing: `127.0.0.1:8000`
- For production: your domain name

This ensures correct rendering of templates during report generation.

---

✅ Your development server is now ready!
