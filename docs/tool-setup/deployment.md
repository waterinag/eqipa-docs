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

> Make sure to update paths if your project is located elsewhere.
.. EnvironmentFile=-/home/aman/ipa_india/webapp/ipa_india/celery.conf
.. WorkingDirectory=/home/aman/ipa_india/webapp/ipa_india/

---

### 3: Reload and Enable Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable celery_ipa_india.service
sudo systemctl start celery_ipa_india.service
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

---

## Summary of Configuration Files

- `celery_ipa_india.service`: systemd unit file for Celery
- `ipa_india.ini`: uWSGI configuration file
- `template_apache.conf`: Apache virtual host config

---

✅ Once both **Celery** and **uWSGI** are running, you're ready to link them to **Apache2** (covered next in [Apache Configuration](apache.md)).
