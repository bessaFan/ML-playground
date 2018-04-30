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
from flask_thumbnails import Thumbnail


 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
thumb = Thumbnail(app)
app.config['THUMBNAIL_MEDIA_ROOT'] = os.getcwd() + ''
app.config['THUMBNAIL_MEDIA_URL'] = ''
app.config['THUMBNAIL_MEDIA_THUMBNAIL_ROOT'] = os.getcwd() + ''
app.config['THUMBNAIL_MEDIA_THUMBNAIL_URL'] = ''
app.config['THUMBNAIL_STORAGE_BACKEND'] = 'flask_thumbnails.storage_backends.FilesystemStorageBackend'
app.config['THUMBNAIL_DEFAUL_FORMAT'] = 'JPEG'

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024 # Allow 300 MiB maximum upload for all images at once
FILE_SIZE_LIMIT = 3 * 1024 * 1024 # 3 MiB
NUM_IMAGES_LIMIT = 60

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
    # plot_exists = os.path.exists('static/output/%s/*.png' % session_id)
    plot_exists = False
    plot_name=""
    plot_name_no_dir=""
    # files = list(glob.glob('static/output/%s/*.png' % session_id).encode('ascii','ignore') )
    files = list(glob.glob('static/output/%s/*.png' % session_id))
    for x in range(0,len(files)):
      files[x]=files[x].encode('ascii','ignore');

    if (len(files)!=0):
      plot_exists=True
      plot_name= max(files, key=os.path.getctime).encode('ascii','ignore')    #getting the name of the newest file
      plot_name_no_dir=plot_name[51:]

    csv_exists = False
    csv_name=""
    csv_name_no_dir=""

    files = list(glob.glob('static/output/%s/*features*.csv' % session_id))
    for x in range(0,len(files)):
      files[x]=files[x].encode('ascii','ignore');

    if (len(files)!=0):
      csv_exists=True
      csv_name= max(files, key=os.path.getctime).encode('ascii','ignore')    #getting the name of the newest file
      csv_name_no_dir=csv_name[51:]


    # Create list of files organized by colors
    colors = []
    color_names=list(glob.glob('static/uploads/%s/*' % session_id))
    for color_name in color_names:
        color_name = os.path.basename(color_name) # get just the color name, not a long folder path including static/uploads
        images=list(glob.glob('static/uploads/%s/%s/*' % (session_id,color_name)))
        images=[ x for x in images if "100x100" not in x ] # remove thumbnails from list, they will be generated
        colors.append({'hex':color_name,'images':images})
    image_exists = len(colors)
    featureCSV_exists = os.path.exists('static/output/%s/*features*.csv' % session_id)
    return render_template('main.html', files=files, colors=colors, session_id=session_id, plot_exists=plot_exists, featureCSV_exists=featureCSV_exists, image_exists=image_exists, timestamp=str(time.time()), plot_name=plot_name, plot_name_no_dir=plot_name_no_dir, csv_name=csv_name_no_dir)


@app.route("/tsne", methods=['POST', 'GET'])
def tsne():
    session_id=request.args.get('session')
    if not session_id:
        session_id = uuid.uuid4()
        return redirect('/?session=%s' % session_id)

    perplexity = int (request.args.get('perplexity'))
    early_exaggeration = int (request.args.get('early_exaggeration'))
    learning_rate = int (request.args.get('learning_rate'))
    # resolution = int( request.args.get('resolution'))
    resolution = 200 # hard coded this to simplify front-end
    CanvasSize = int (request.args.get('CanvasSize'))
    DotsPerInchs = int (request.args.get('DotsPerInchs'))
    model_name = request.args.get('model_name')

    # Get colors and images information
    colors_text = request.args.get('colors')
    # Convert from badly formatted json to dict
    colors_text = colors_text.replace("'",'"')
    colors_text = colors_text.replace('u"','"')
    colors_dict = json.loads(colors_text)

    colors = [] 
    hex_number = "" 
    for section in range(len(colors_dict)):
      for hex1 in colors_dict[section]['hex']: 
        hex_number+= hex1
      for files in colors_dict[section]['images']:
        colors.append('#'+hex_number.encode('ascii','ignore')) 
      hex_number = "" 

    print 'creating tsne plot'
    tsne_data = tsne_script.tsne_images(session_id, colors_dict, resolution, perplexity,early_exaggeration, learning_rate, DotsPerInchs,CanvasSize, colors, model_name)
    return redirect('/?session=%s#try' % session_id)

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

        # Create folder if necessary
        folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id, hexcolor)
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Check if number of images exceeds the limit
        new_num_images = len(files)
        existing_num_images = len(list(glob.glob('static/uploads/%s/*' % session_id)))
        if new_num_images + existing_num_images > NUM_IMAGES_LIMIT:
          return redirect(request.url)  # TODO: Warn user that this has happened

        for file in files:
          # if user does not select file, browser also submit a empty part without filename
          if file.filename == '':
              print('No selected file')
              return redirect(request.url)

          if file and allowed_file(file.filename):
              # Skip file if too large (>5MB)
              file.seek(0, os.SEEK_END)
              file_size = file.tell()
              if file_size > FILE_SIZE_LIMIT:
                continue # Skip this file it is too big # TODO: Warn user that this has happened
              file.seek(0) # File is allowable size seek back to the beginning of the file. Without this no data would be read because we already seeked to the end of the file to read it's length.
              
              # Save file
              filename = secure_filename(file.filename)
              path = os.path.join(folder, filename)
              file.save(path)

        return redirect(request.url)

if __name__ == "__main__":
    app.run(debug = True, port=3000)
