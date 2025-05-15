#  Django Quick Start Guide 
Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.

---

### Key features:
- Ridiculously fast.
- Reassuringly secure.
- Exceedingly scalable.

---

###  Prerequisites

- Python 3.x Installed
- Terminal / Command Line Access
- Basic Python Knowledge


> 📝 **Check Python Version**:
```bash
python --version  # Windows / Ubuntu (if configured)
python3 --version # Recommended on Mac/Linux
```


### Step 1: Create Project Folder & Virtual Environment
```bash
mkdir myproject
cd myproject

# For Ubuntu & Mac
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```


### Step 2:Install Django
```bash
pip install django

```


### Step 3: Start a Django Project
```bash
django-admin startproject mysite
cd mysite


```



### Step 4: Run the Development Server
```bash
p# For Ubuntu & Mac
python3 manage.py runserver

# For Windows
python manage.py runserver

```
Open browser: http://127.0.0.1:8000/


### Step 5: Create a Django App
```bash
python manage.py startapp myapp

```

Project Structure:

```bash
mysite/
    manage.py
    mysite/
    myapp/
```

### Step 6: Register App in Django Settings
Edit mysite/settings.py
```bash
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',  # Add this line
]

```

### Step 7: Add a View in the App
```bash
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, Django!")

```

### Step 8: Update URL Routing
Edit mysite/urls.py:
```bash
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
]


```

### Step 9: Run the Server Again
```bash
# For Ubuntu & Mac
python3 manage.py runserver

# For Windows
python manage.py runserver


```
Visit: http://127.0.0.1:8000/

Expected Output:

```bash
Hello, Django!
```



### Optional: Django Admin Access
```bash
python manage.py createsuperuser



```
Login at: http://127.0.0.1:8000/admin/




### 📚 Learn More

- [Django Official Documentation](https://docs.djangoproject.com/en/5.2/)


