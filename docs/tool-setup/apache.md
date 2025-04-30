# 🌐 Apache Configuration

This section explains how to configure Apache to serve the EQIPA Django project using **uWSGI** and enable **SSL** using Let's Encrypt via **Certbot**.

---

## 1: Copy Apache Virtual Host Configuration

Copy the example configuration to the Apache sites-available directory:

```bash
sudo cp /home/aman/ipa_india/webapp/ipa_india/ipa_india.conf /etc/apache2/sites-available/ipa_india.conf
```

??? info "ipa_india.conf"

    ```bash
    <VirtualHost *:80>
        ServerName eqipa.waterinag.org

    Alias /static/ /home/aman/ipa_india/webapp/ipa_india/static/

        <Directory /home/aman/ipa_india/webapp/ipa_india/ipa_india>
            <Files wsgi.py>
                Require all granted
            </Files>
        </Directory>

    <Location /static>
                    SetHandler none
                    Options -Indexes
            </Location>

            <Location /media>
                    SetHandler none
                    Options -Indexes
            </Location>

            Alias /media/ /home/aman/ipa_india/webapp/ipa_india/media/

            Alias /static/ /home/aman/ipa_india/webapp/ipa_india/static/

            <Directory /home/aman/ipa_india/webapp/ipa_india/>
                    Require all granted
            </Directory>

            <Directory /home/aman/ipa_india/webapp/ipa_india/static>
                    Options FollowSymLinks
                    Order allow,deny
                    Allow from all
            </Directory>

            <Directory /home/aman/ipa_india/webapp/ipa_india/media>
                    Options FollowSymLinks
                    Order allow,deny
                    Allow from all
            </Directory>

        ProxyPass / unix:/home/aman/ipa_india/webapp/ipa_india/ipa_india.sock|uwsgi://localhost/
        # Proxying the connection to uWSGI
        
        # ProxyPass / unix:/home/aman/ipa_india/webapp/ipa_india/ipa_india.sock|uwsgi://localhost/
        ErrorLog ${APACHE_LOG_DIR}/ipa_india_error.log
        CustomLog ${APACHE_LOG_DIR}/ipa_india_access.log combined


    </VirtualHost>

    ```


> Make sure to update paths in the config to match your project directory.

---

##  2: Enable Required Apache Modules

```bash
sudo a2enmod uwsgi
sudo a2enmod ssl
```

---

## 3: Enable the Site

```bash
sudo a2ensite ipa_india.conf
```

---

Verify Apache Configuration

```bash
sudo apachectl configtest
```
You should see: `Syntax OK`

---
Restart Apache to apply changes:

```bash
sudo systemctl reload apache2
sudo systemctl restart apache2
```

---







##  4: Enable SSL with Certbot

Install Certbot:

```bash
sudo apt install certbot python3-certbot-apache
```

Enable HTTPS with your domain:

```bash
sudo certbot --apache -d eqipa.waterinag.org
```

Restart Apache to apply changes:

```bash
sudo systemctl restart apache2
```


---

## 📂 Apache Site Commands Summary

### Enable site

```bash
sudo a2ensite eqipa.waterinag.org.conf
```

### Disable site

```bash
sudo a2dissite eqipa.waterinag.org.conf
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
