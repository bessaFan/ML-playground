import time
import glob
import os
from IPython import embed
from shutil import copyfile
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/")
def hello():
    images=list(glob.glob('static/uploads/*g'))
    return render_template('main.html', images=images)

def allowed_file(filename):
    return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        files = request.files.getlist("file")
        for file in files:
          # if user does not select file, browser also
          # submit a empty part without filename
          if file.filename == '':
              print('No selected file')
              return redirect(request.url)
          if file and allowed_file(file.filename):
              filename = secure_filename(file.filename)
              file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(request.url)

if __name__ == "__main__":
    app.run()
