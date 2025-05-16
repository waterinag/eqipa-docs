# 🚀 Deployment in Production

This guide covers how to deploy the **EQIPA Django app** to a production server using **Celery**, **uWSGI**, and **Apache2**.

---

## Celery Worker as a Systemd Service

Celery is used to handle background tasks such as report generation.

### 1: Create PID Directory

```bash
sudo mkdir /var/run/celery/
sudo chown -R $USER:$USER /var/run/celery/
sudo chown -R aman:aman /var/run/celery/
```

---

### 2: Add Celery Service to Systemd

```bash
sudo ln -s /home/aman/ipa_india/webapp/ipa_india/celery_ipa_india.service /etc/systemd/system
```

> Make sure to update the necessary fields in celery_ipa_india.service
.. EnvironmentFile=-/home/aman/ipa_india/webapp/ipa_india/celery.conf
.. WorkingDirectory=/home/aman/ipa_india/webapp/ipa_india/

---

### 3: Reload and Enable Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable celery_ipa_india.service
sudo systemctl start celery_ipa_india.service

# enable the service to be automatically start on boot
sudo systemctl status celery_ipa_india.service
```

??? info "celery_ipa_india.service"

    ```bash
    [Unit]
    Description=Celery Service for ipa_india app
    After=network.target

    [Service]
    Type=forking
    User=aman
    Group=aman
    EnvironmentFile=/home/aman/ipa_india/webapp/ipa_india/celery.conf
    WorkingDirectory=/home/aman/ipa_india/webapp/ipa_india/
    ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} multi start ${CELERYD_NODES} \
        --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
        --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
    ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
        --pidfile=${CELERYD_PID_FILE} --loglevel=${CELERYD_LOG_LEVEL}'
    ExecReload=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} multi restart ${CELERYD_NODES} \
        --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
        --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```


---

### Check Celery Logs

```bash
tail -f /home/aman/ipa_india/webapp/ipa_india/log/celery/worker1.log
```

---

## uWSGI Setup

### Run Django App via uWSGI

Ensure your virtual environment is activated, then run:

```bash
uwsgi --ini ipa_india.ini
```
> Make sure to update the necessary fields in ipa_india.ini


??? info "ipa_india.ini"

    ```bash
    [uwsgi]
    chdir           = /home/aman/ipa_india/webapp/ipa_india
    module          = ipa_india.wsgi
    home            = /home/aman/ipa_india/webapp/venv
    env = DJANGO_SETTINGS_MODULE=ipa_india.settings
    master          = true
    processes       = 5
    threads = 2
    socket          = /home/aman/ipa_india/webapp/ipa_india/ipa_india.sock
    chmod-socket    = 666
    vacuum          = true
    daemonize = /home/aman/ipa_india/webapp/ipa_india/log/ipa_india.log
    post-buffering = True
    route-run = harakiri:180

    ```


This will launch the Django application using your `.ini` configuration.



??? info "uWSGI (Socket Permissions Error)"

    If you encounter this error in the Apache logs:
    ```bash
    (13)Permission denied: AH02454: uwsgi: attempt to connect to Unix domain socket ...
    ```
    It means Apache doesn't have permission to access the .sock file created by uWSGI.

    1. Ensure Apache (www-data) can access the socket directory path:

    ```bash
    # Add Apache user to your Linux user's group
    sudo usermod -a -G vboxuser www-data
    ```

    2.Update directory permissions to allow group (www-data) access:
    ```bash
    sudo chmod 750 /home/vboxuser
    sudo chmod 750 /home/vboxuser/Documents
    sudo chmod 750 /home/vboxuser/Documents/eqipa_india
    sudo chmod 750 /home/vboxuser/Documents/eqipa_india/webapp
    sudo chmod 750 /home/vboxuser/Documents/eqipa_india/webapp/ipa_india

    ```
    These commands ensure only the owner (vboxuser) and group (www-data) can traverse the directory tree securely.
   


---

## Restarting Celery and uWSGI After Code Changes

```bash
# reload the systemd files (this has been done everytime celery_ipa_india.service is changed)
sudo systemctl daemon-reload

#Stop Celery Service
sudo systemctl stop celery_ipa_india.service

#Start Celery Service
sudo systemctl start celery_ipa_india.service

#Verify Celery is Running Correctly
sudo systemctl status celery_ipa_india.service

#Kill Remaining Celery Processes
sudo pkill -9 -f 'celery worker'

#Ensure All Processes Are Stoppedps aux | grep celery
ps aux | grep celery`

#Monitoring Logs
tail -f /home/aman/ipa_india/log/celery/worker1-7.log
tail -f /home/aman/ipa_india/log/celery/worker1-6.log
tail -f /home/aman/ipa_india/log/celery/worker1.log

# or all at once:
for file in /home/aman/ipa_india/log/celery/*.log; do
    echo "Checking $file"
    tail -n 20 $file
done


# check all the running uWSGI workers
ps aux | grep uwsgi

# To stop uWSGI
sudo killall -9 uwsgi

#Restart uWSGI (first activate the venv)
uwsgi --ini ipa_india.ini
```

---

## Summary of Configuration Files

- `celery_ipa_india.service`: systemd unit file for Celery
- `ipa_india.ini`: uWSGI configuration file
- `template_apache.conf`: Apache virtual host config

---

✅ Once both **Celery** and **uWSGI** are running, you're ready to link them to **Apache2** (covered next in [Apache Configuration](apache.md)).
