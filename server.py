import time
import glob
import os
from tsne_lib import tsne_script
#from IPython import embed
from shutil import copyfile
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import uuid



ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route("/")
def main():
    # Set a session ID
    session_id=request.args.get('session')
    if not session_id:
        session_id = uuid.uuid4()
        return redirect('/?session=%s' % session_id)
    
    # Create folders for this session ID
    images=list(glob.glob('static/uploads/%s/*g' % session_id))    
    if not os.path.exists('static/output/%s/' % session_id):
        os.makedirs('static/output/%s/' % session_id)
    if not os.path.exists('static/uploads/%s/' % session_id):
        os.makedirs('static/uploads/%s/' % session_id)
    plot_exists = os.path.exists('static/output/%s/output.png' % session_id)

    return render_template('main.html', images=images, session_id=session_id, plot_exists=plot_exists)


@app.route("/tsne", methods=['POST', 'GET'])
def tsne():
    # print('test tsne!')
    # print(request)
    # print(vars(request))

    session_id=request.args.get('session')
    if not session_id:
        session_id = uuid.uuid4()
        return redirect('/?session=%s' % session_id)

    perplexity = int (request.args.get('perplexity'))
    x_resolution = int( request.args.get('x_resolution'))
    y_resolution = int (request.args.get('y_resolution'))
    CanvasSize = int (request.args.get('CanvasSize'))
    DotsPerInchs = int (request.args.get('DotsPerInchs'))
    #embed()
    #process variables here
    tsne_data = tsne_script.tsne_images(session_id,x_resolution, perplexity,DotsPerInchs,CanvasSize)
    return redirect('/?session=%s' % session_id)

def allowed_file(filename):
    return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_file():

    session_id=request.args.get('session')
    if not session_id:
      session_id = uuid.uuid4()
      return redirect('/?session=%s' % session_id)

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
              file.save(os.path.join(app.config['UPLOAD_FOLDER'], session_id, filename))
        return redirect(request.url)

if __name__ == "__main__":
    app.run(debug = True, port=200)