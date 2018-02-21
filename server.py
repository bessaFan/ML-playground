import json
import time
import glob
import os
from tsne_lib import tsne_script
from shutil import copyfile
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import uuid
from IPython import embed



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
    if not os.path.exists('static/output/%s/' % session_id):
        os.makedirs('static/output/%s/' % session_id)
    if not os.path.exists('static/uploads/%s/' % session_id):
        os.makedirs('static/uploads/%s/' % session_id)

    # Check if plot exists, the front-end will display different things
    plot_exists = os.path.exists('static/output/%s/output.png' % session_id)

    # Create list of files organized by colors
    colors = []
    color_names=list(glob.glob('static/uploads/%s/*' % session_id))
    for color_name in color_names:
        color_name = os.path.basename(color_name) # get just the color name, not a long folder path including static/uploads
        images=list(glob.glob('static/uploads/%s/%s/*' % (session_id,color_name)))
        colors.append({'hex':color_name,'images':images})

    return render_template('main.html', colors=colors, session_id=session_id, plot_exists=plot_exists)


@app.route("/tsne", methods=['POST', 'GET'])
def tsne():
    session_id=request.args.get('session')
    if not session_id:
        session_id = uuid.uuid4()
        return redirect('/?session=%s' % session_id)

    perplexity = int (request.args.get('perplexity'))
    early_exaggeration = int (request.args.get('early_exaggeration'))
    learning_rate = int (request.args.get('learning_rate'))
    resolution = int( request.args.get('resolution'))
    CanvasSize = int (request.args.get('CanvasSize'))
    DotsPerInchs = int (request.args.get('DotsPerInchs'))

    # Get colors and images information
    colors_text = request.args.get('colors')
    # Convert from badly formatted json to dict
    colors_text = colors_text.replace("'",'"')
    colors_text = colors_text.replace('u"','"')
    colors_dict = json.loads(colors_text)

    tsne_data = tsne_script.tsne_images(session_id, colors_dict, resolution, perplexity,early_exaggeration, learning_rate, DotsPerInchs,CanvasSize)
    return redirect('/?session=%s' % session_id)

def allowed_file(filename):
    return '.' in filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def upload_file():

    session_id=request.args.get('session')
    hexcolor=request.form.get('hexcolor')
    hexcolor=hexcolor[1:] # remove # from #FFFFFF
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
              folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id, hexcolor)
              if not os.path.exists(folder):
                  os.makedirs(folder)
              path = os.path.join(folder, filename)
              file.save(path)
        return redirect(request.url)

if __name__ == "__main__":
    app.run(debug = True, port=200)