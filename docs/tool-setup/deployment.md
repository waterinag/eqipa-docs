# 🚀 Deployment in Production

This guide covers how to deploy the **EQIPA Django app** to a production server using **Celery**, **uWSGI**, and **Apache2**.

---

## 🧵 Celery Worker as a Systemd Service

Celery is used to handle background tasks such as report generation.

### 📁 Step 1: Create PID Directory

```bash
sudo mkdir /var/run/celery/
sudo chown -R $USER:$USER /var/run/celery/
```

---

### 🔗 Step 2: Add Celery Service to Systemd

```bash
sudo ln -s /home/aman/ipa_india/webapp/ipa_india/celery_ipa_india.service /etc/systemd/system
```

> Make sure to update paths if your project is located elsewhere.

---

### ⚙️ Step 3: Reload and Enable Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable celery_ipa_india.service
sudo systemctl start celery_ipa_india.service
```

---

### 📊 Check Celery Logs

```bash
tail -f /home/aman/ipa_india/webapp/ipa_india/log/celery/worker1.log
```

---

## 🌀 uWSGI Setup

### ▶️ Run Django App via uWSGI

Ensure your virtual environment is activated, then run:

```bash
uwsgi --ini ipa_india.ini
```

This will launch the Django application using your `.ini` configuration.

---

## 📝 Summary of Configuration Files

- `celery_ipa_india.service`: systemd unit file for Celery
- `ipa_india.ini`: uWSGI configuration file
- `template_apache.conf`: Apache virtual host config

---

✅ Once both **Celery** and **uWSGI** are running, you're ready to link them to **Apache2** (covered next in [Apache Configuration](apache.md)).
