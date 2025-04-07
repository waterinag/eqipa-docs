# ❗ Common Errors & Fixes

This page lists common issues encountered while setting up or deploying the EQIPA application, along with tested solutions.

---

## File Permission Errors

### Error

Logs show permission denied when accessing socket or log files.

### Solution

```bash
sudo chown -R www-data:www-data /home/aman/ipa_india/webapp/ipa_india
sudo chown -R aman:aman /home/aman/ipa_india/webapp/ipa_india/log/
sudo chmod -R 755 /home/aman/ipa_india/webapp/ipa_india/log/
```

---

## uWSGI Modifier Error

### Error (in uWSGI logs)

```
-- unavailable modifier requested: 0 --
```

### Solution

```bash
sudo killall -9 uwsgi

sudo chown -R aman:aman /home/aman/ipa_india/webapp/ipa_india/
sudo chmod 755 /home/aman/ipa_india/webapp/ipa_india/

uwsgi --ini ipa_india.ini
```

---

## PostgreSQL Delete Constraint Error

### Error

```
ERROR:  update or delete on table "area" violates foreign key constraint ...
DETAIL:  Key (id)=(X) is still referenced from table "taskhistory"
```

### Solution

1. Delete dependent entries from `taskhistory`:

```sql
DELETE FROM taskhistory WHERE area_id = <id>;
```

2. Then delete from `area`:

```sql
DELETE FROM area WHERE name = 'target_area_name';
```

---

## Screen Issues (Managing Background Sessions)

### Attach to a running screen

```bash
screen -r 392898.django_server
```

### Detach from a screen

```bash
Ctrl + A, then D
```

### Kill a screen session

```bash
screen -S celery_worker -X quit
```

### Start a new screen

```bash
screen -S ipa_server
screen -S ipa_celery
```

---

## Monitoring Celery Logs

```bash
tail -f /home/aman/ipa_india/webapp/ipa_india/log/celery/worker1.log

# or all at once:
for file in /home/aman/ipa_india/webapp/ipa_india/log/celery/*.log; do
    echo "Checking $file"
    tail -n 20 $file
done
```

---

## Restarting Celery and uWSGI After Code Changes

```bash
# Reload systemd
sudo systemctl daemon-reload

# Stop & start Celery
sudo systemctl stop celery_ipa_india.service
sudo systemctl start celery_ipa_india.service
sudo systemctl status celery_ipa_india.service

# Kill stray celery workers
sudo pkill -9 -f 'celery worker'
ps aux | grep celery

# Restart uWSGI
sudo killall -9 uwsgi
uwsgi --ini ipa_india.ini
```

---
