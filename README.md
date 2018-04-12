# Introduction

Our web app provides a **"No code. No installation"** platform for researchers to upload images and compare clustering results with popular **machine learning models and manifold learning algorithms**, making experimenting and prototyping with ML less time-consuming. There’s currently no existing app that allows fast organization and visualization of data.

# Website 
[Checkout our awesome website!!](http://23.233.65.16/)


- some points

> some notes

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
