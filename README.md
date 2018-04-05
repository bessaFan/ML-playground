### Install

```
sudo pip install flask
sudo pip install gunicorn
```

### Run

```
(with flask)
export FLASK_DEBUG=1   # optional
export FLASK_APP=server.py
python -m flask run --host=0.0.0.0

(with gunicorn)
sudo gunicorn server:app -b:8080


```

### Server Setup

```
sudo cp clean_up.py /etc/cron.daily/
sudo chmod +x /etc/cron.daily/clean_up
# modify clean_up.py so that the directory paths to clean are correct for the server
# optionally test that cron successfully runs the clean_up script with:
sudo run-parts -v /etc/cron.daily
```
