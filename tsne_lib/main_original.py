#!/usr/bin/env python
import os
import numpy as np
import pylab
import mahotas as mh
import glob     
import watershed # label image by calling watershed.py
import utils # crop cell by calling utils.py
import plot
# import tsne1
from PIL import Image
import skimage
import skimage.io
import scipy
import pandas as pd
import click
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from IPython import embed
if os.name != 'nt':
  from tsne import bh_sne



def everything():
  '''
  # crop and label images
  for filename in list(glob.glob('*.tif')): 
  	img = skimage.io.imread(filename) # read and save image as an array (img.shape is (1024, 1360))
  	y_value = watershed.label(img) # watershed images; y_value stores the labels
  	utils.crop (img, y_value) #crop image
  '''
  #put together a list of x value for tsne to process
  filenames=list(glob.glob('*.jpg'))
  x_value = np.zeros((4900, len(filenames))) # Dimension of the image: 70*70=4900; x_value will store images in 2d array
  for imageName in filenames : 
  	count = 0
  	image1d = scipy.misc.imresize(skimage.io.imread(imageName), (70,70)) #reshape size to 70,70 for every image
  	image1d = image1d.flatten() #image1d stores a 1d array for each image
  	x_value[:,count] = image1d # add a row of values
  	count += 1

  tsne1.tSNE(x_value) #plot data using tsne




####idk what i did to this code####
@click.command()
@click.option('--csv', help='The csv file that contains single cell data.', required=True)
@click.option('--channel', help='The image channel to crop.', default=1)
@click.option('--resize', help='Size of the image', default=100)
@click.option('--square/--rectangle', help='Crop the cell in into a square box rather than a rectangle.', default=False)
@click.option('--save_location', help='saving location of the image', default="./cropped_and_resize")
@click.option('--image_dir', help='image directory', default='./cell images/*ch1*.tiff')
def crop_images(csv,channel,resize,square,save_location,image_dir):
  #./main.py crop_images  --csv ResultTable\ -\ 2\ wells\,\ 1\ fields\,\ thresh\ 160_with_Traces_full_curated.csv --resize 200
  #./main.py crop_images  --csv file.csv 
  df = utils.read_csv(csv)
  print('Found number of cells: %s' % df.shape[0])
  #image_dir = './images/Ron/'
  #image_dir = './images/LFS images/'
  # Loop by image
  for image_filename in df.FileName.unique():
    cells_in_img = df.loc[df['FileName'] == image_filename]
    cell_ids = []
    # Set the channel number in the image filename to load
    s = list(image_filename)
    s[15]=str(channel)
    ch_image_filename = "".join(s)
    # Load image
    image = skimage.io.imread(image_dir + ch_image_filename)

    # Build labelled image
    labelled = np.zeros(image.shape)
    count = 1
    for row_index, row in cells_in_img.iterrows():
      cyto_px_ids = map(int, row.cyto_boundaries.split()) # get locations of this cell's boundries as a list of ints
      labelled[np.unravel_index(cyto_px_ids, labelled.shape, order='F')] = count # set this cell in the labelled image
      cell_ids.append(row.CellID)
      count+=1

    utils.crop_and_save(image, labelled, save_location, filenames=cell_ids, square=square, resize=resize)
  print('Saved number of cropped cells: %s' % df.shape[0])





@click.command()
@click.option('--csv', help='The csv file that contains single cell data.', required=True)
@click.option('--color-by', help='The measurement name to color the boxes by.', default='Trace')
@click.option('-x', help='The measurement name on the X axis.', required=True)
@click.option('-y', help='The measurement name on the Y axis.', required=True)
@click.option('--dpi', help='The resolution to save the output image.', default=200)
@click.option('--channel', help='The image channel to display.', default=1)
def image_scatter(csv,color_by,x,y,dpi,channel):
  #./main.py image_scatter  --csv ResultTable\ -\ 2\ wells\,\ 1\ fields\,\ thresh\ 160_with_Traces_full_curated.csv -x tsne1 -y tsne2 --color-by CellLine --dpi 650
  #./main.py image_scatter  --csv file.csv --color-by CellID -x tsne1 -y tsne2 --dpi 650
  df = utils.read_csv(csv)
  print('Found number of cells: %s' % df.shape[0])
  #image_dir = './images/cropped_images/Ron/'
  #image_dir = './images/cropped_images/'
  #image_dir = './cropped/'

  '''
    filenamesDAPI[idx]= filenamesDAPI[idx][14:38]
    filenames=range(nr_nuclei)
    for x in filenames:
       filenames[x]=filenamesDAPI[idx]+str(filenames[x])
  '''
  cell_imgs = []
  colors = []
  xx = np.array([])
  yy = np.array([])

  cmap='gist_rainbow'
  color_list = utils.get_colors(len(np.unique(df[color_by])),cmap=cmap)

  # blue is better when there are only 3 colours
  if len(color_list) == 3 and cmap == 'gist_rainbow':
    color_list[2] = (0.05, 0.529, 1, 1.0)

  images = df["FileName"]

  for row_id, row in df.iterrows():
    cell_id = row.CellID
    '''
    image_filename = image_dir + 'ch' + str(channel) + '-' + cell_id + '.jpg'
    if not os.path.exists(image_filename):
      print('[WARN] no image found %s'% image_filename)
      continue
    print('Loading image %s' % image_filename)
    '''
    image_filename = images[row_id]

    image = skimage.io.imread(image_filename)
    image = utils.gray_to_color(image)
    cell_imgs.append(image)
    xx = np.append(xx,row[x])
    yy = np.append(yy,row[y])
    color_id = np.where(np.unique(df[color_by])==row[color_by])[0][0] # find position where this value appears
    c = color_list[color_id]
    c = (int(c[0]*255),int(c[1]*255),int(c[2]*255)) # convert value range, ex. 1.0 -> 255 or 0.0 -> 0
    colors.append(c)

  if len(cell_imgs)==0:
    print('[ERROR] 0 cropped single cell images found.')
    return

  canvas = plot.image_scatter(yy, xx, cell_imgs, colors, min_canvas_size=4000)
  plt.imshow(canvas,origin='lower')
  plt.title('%s vs %s' % (x,y))
  plt.xlabel('%s' % x)
  plt.ylabel('%s' % y)
  #plt.xticks([])
  #plt.yticks([])
  patches=[]
  '''
  for i in range(len(np.unique(df[color_by]))):
    label = '%s %s' % (color_by, np.unique(df[color_by])[i])
    if color_by == 'Dend.cat':
      label = 'Detected Category %s' % (i+1)
    # Plot additional data that can't be in the main csv
    # extra_datafile = 'PCaxes.csv'
    # if os.path.exists(extra_datafile):
    #   df_extra = utils.read_csv(extra_datafile)
    #   from IPython import embed
    #   embed() # drop into an IPython session
    #   plt.scatter(avg_x, avg_y,c=color,marker='*')
    patch = mpatches.Patch(color=color_list[i], label=label)
    patches.append(patch)
  '''
  plt.legend(handles=patches,bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0, frameon=False)
  save_location = './images/%s_image_scatter_by_%s_dpi%s.png' % (csv, color_by, dpi)
  plt.savefig(save_location,dpi=dpi,pad_inches=1,bbox_inches='tight')
  # plt.show()
  print('Saved image scatter to %s' % save_location)




@click.command()
@click.option('--csv', help='The csv file that contains single cell data.', required=True)
@click.option('--res', help='The resolution of image.', default=70)
@click.option('--perplexity', help='The perplexcity of tsne plot.', default=5)
def tsne_images(csv,res,perplexity):
  #./main.py tsne_images  --csv file.csv --perplexity 1
  image_dir = './cropped_and_resized/'
  filenames=list(glob.glob(image_dir+'*'))
  '''
  x_value = np.zeros((4900, len(filenames))) # Dimension of the image: 70*70=4900; x_value will store images in 2d array
  for imageName in filenames: 
    count = 0
    image1d = scipy.misc.imresize(skimage.io.imread(imageName), (70,70)) #reshape size to 70,70 for every image
    image1d = image1d.flatten() #image1d stores a 1d array for each image
    x_value[:,count] = image1d # add a row of values
    count += 1
  '''
  total_res = res**2
  x_value = np.zeros((len(filenames),total_res)) # Dimension of the image: 70*70=4900; x_value will store images in 2d array
  print filenames
  count = 0
  for imageName in filenames: 
    image1d = scipy.misc.imresize(skimage.io.imread(imageName), (res,res)) #reshape size to 70,70 for every image
    image1d = image1d.flatten() #image1d stores a 1d array for each image
    x_value[count,:] = image1d # add a row of values
    #embed()
    count += 1
    if count>50:
      break

  print x_value.shape
  vis_data = bh_sne(x_value,perplexity=perplexity)# tsne embedding
  print vis_data.shape
  vis_x = vis_data[:, 0]
  vis_y = vis_data[:, 1]

  df = utils.read_csv(csv)
  print df.shape
  df['tsne1']=pd.Series (vis_x)
  df['tsne2']=pd.Series (vis_y)
  df.to_csv(csv, index=False)


# Setup group of command line commands
@click.group()
def cli():
    pass
cli.add_command(crop_images)
cli.add_command(image_scatter)
cli.add_command(tsne_images)

if __name__ == '__main__':
  cli()  # make command line commands available
  # everything()


# import pylab
# pylab.imshow(labelled);pylab.show()