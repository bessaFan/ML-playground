

# Introduction

Our web app provides a **"No code. No installation"** platform for researchers to upload images and compare clustering results with popular **machine learning models and manifold learning algorithms**, making experimenting and prototyping with ML less time-consuming. There’s currently no existing app that allows fast organization and visualization of data.


## Example
<p align="center">
 <img src="https://github.com/bessaFan/ML-playground/blob/master/static/images/animals-example-black.png" height="455px">
</p>


## Project Layout

| Directory or file| Description                                                                                        |
|-------------------------|----------------------------------------------------------------------------------------------------|
| [templates](https://github.com/bessaFan/generate_tsne_plots_online/tree/master/templates "templates") | Main website code folder! (where [main.html](https://github.com/bessaFan/generate_tsne_plots_online/blob/master/templates/main.html "main.html") is found)|
| [static](https://github.com/bessaFan/generate_tsne_plots_online/tree/master/static "static")| Code for front-end styling |
| [tsne_lib](https://github.com/bessaFan/generate_tsne_plots_online/tree/master/tsne_lib "tsne_lib")| Where a bunch of cool backend code is found|
| [clean_up.py](https://github.com/bessaFan/generate_tsne_plots_online/blob/master/clean_up.py "clean_up.py")| Automatically delete the oldest folders, keeping only the 100 most recent ones|
| [server.py](https://github.com/bessaFan/generate_tsne_plots_online/blob/master/server.py "server.py")|Website server|
| [download_models.sh](https://github.com/bessaFan/ML-playground/blob/master/models/download_models.sh "download_models.sh")|Command line download models (move models under models folder after download)|



## Website 
[Checkout our **awesome** website here!!](http://23.233.65.16/)

layout:
<p align="center">

<img src="https://github.com/bessaFan/generate_tsne_plots_online/blob/master/static/images/MLplayground.jpg?raw=true" alt="Website" >
</p>

## Set up

### Installation

```
sudo pip install flask
sudo pip install gunicorn
npm install bootstrap-select
pip install flask-thumbnails==1.0.3

```

### Run

```
(with flask)
export FLASK_DEBUG=1   # optional
export FLASK_APP=server.py
python -m flask run --host=0.0.0.0 --port=5000

(with gunicorn)
sudo gunicorn server:app -b:80 --limit-request-line 0 --timeout 0 --access-logfile -

```

### Server Setup

```
sudo cp clean_up.py /etc/cron.daily/
sudo chmod +x /etc/cron.daily/clean_up
# modify clean_up.py so that the directory paths to clean are correct for the server
# optionally test that cron successfully runs the clean_up script with:
sudo run-parts -v /etc/cron.daily
```

## Helpful Resources
This website contains introsuction to multiple Manifold Learning Models 
-   [http://scikit-learn.org/stable/modules/manifold.html#manifold](http://scikit-learn.org/stable/modules/manifold.html#manifold)

This website has a cool  t-SNE  visualization and discuss multiple misconceptions of t-sne 
-   [https://distill.pub/2016/misread-tsne/](https://distill.pub/2016/misread-tsne/)


More t-SNE reading!!
-  	https://indico.io/blog/visualizing-with-t-sne/
