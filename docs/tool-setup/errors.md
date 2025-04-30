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
-- unavailable modifier requested: 0 --
-- unavailable modifier requested: 0 --
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


## Monitoring Celery Logs

```bash
tail -f /home/aman/ipa_india/webapp/ipa_india/log/celery/worker1.log

# or all at once:
for file in /home/aman/ipa_india/webapp/ipa_india/log/celery/*.log; do
    echo "Checking $file"
    tail -n 20 $file
done
```

## Monitoring uWSGI log

```bash
tail -f /home/aman/ipa_india/webapp/ipa_india/log/ipa_india.log
```

## Monitoring apache logs

```bash
sudo tail -f /var/log/apache2/ipa_india_error.log
sudo tail -f /var/log/apache2/ipa_india_access.log
```





---


