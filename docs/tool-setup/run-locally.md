# 💻 Running the App Locally

This guide explains how to set up and run the EQIPA Django app locally in a development environment.

---

## 🔧 Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ipa_india.git
cd ipa_india/webapp
```

---

## 🐍 Step 2: Create and Activate a Virtual Environment

Create a Python 3 virtual environment inside the `webapp` folder:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 📦 Step 3: Install Python Dependencies

Install all required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Step 4: Configure Django Settings

Open `ipa_india/settings.py` and update the following:

- `DATABASES` section → add username, password, and DB name
- `GRASS_DB` path → e.g., `/mnt/mapdata/grassdata/ipa_india`

---

## 🔄 Step 5: Apply Migrations & Collect Static Files

Run the following commands to prepare your database and static files:

```bash
python manage.py makemigrations webapp
python manage.py migrate
python manage.py collectstatic
```

---

## 👤 Step 6: Create a Superuser

```bash
python manage.py createsuperuser --username admin
```

Sample credentials:

- **Username:** `admin`
- **Email:** `your-email@gmail.com`
- **Password:** `your-pass`

---

## 🧪 Step 7: Test Local Server

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

## 🖥️ Admin Site Setup

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
