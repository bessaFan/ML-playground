Inspiration from: https://onepagelove.com/isis-cocco

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


