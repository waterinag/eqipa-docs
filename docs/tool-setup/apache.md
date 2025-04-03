# 🌐 Apache Configuration

This section explains how to configure Apache to serve the EQIPA Django project using **uWSGI** and enable **SSL** using Let's Encrypt via **Certbot**.

---

## 📝 Step 1: Copy Apache Virtual Host Configuration

Copy the example configuration to the Apache sites-available directory:

```bash
sudo cp ipa_india/template_apache.conf /etc/apache2/sites-available/ipa_india.conf
```

> Make sure to update paths in the config to match your project directory.

---

## 🔌 Step 2: Enable Required Apache Modules

```bash
sudo a2enmod uwsgi
sudo a2enmod ssl
```

---

## 🔧 Step 3: Enable the Site

```bash
sudo a2ensite ipa_india.conf
```

Restart Apache to apply changes:

```bash
sudo systemctl reload apache2
sudo systemctl restart apache2
```

---

## ✅ Verify Apache Configuration

```bash
sudo apachectl configtest
```

You should see: `Syntax OK`

---

## 🛡️ Step 4: Enable SSL with Certbot

Install Certbot:

```bash
sudo apt install certbot python3-certbot-apache
```

Enable HTTPS with your domain:

```bash
sudo certbot --apache -d ipa.waterinag.org
```

You can enable multiple domains if needed:

```bash
sudo certbot --apache -d ipa.waterinag.org -d eqipa.waterinag.org
```

---

## 📂 Apache Site Commands Summary

### Enable site

```bash
sudo a2ensite ipa.waterinag.org.conf
```

### Disable site

```bash
sudo a2dissite ipa.waterinag.org.conf
```

### List enabled sites

```bash
ls -l /etc/apache2/sites-enabled
```

---

## 🔎 Logs and Troubleshooting

### View Apache error log

```bash
sudo tail -f /var/log/apache2/ipa_india_error.log
```

### Check uWSGI log

```bash
tail -f /home/aman/ipa_india/webapp/ipa_india/log/ipa_india.log
```

> Ensure Apache's config is pointing to the correct uWSGI socket and the socket file has proper read/write permissions.

---

✅ Apache is now configured and serving your EQIPA application securely over HTTPS!
