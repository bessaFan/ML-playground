#!/usr/bin/env python
import os
import os.path
import csv
import numpy as np
import pylab
import mahotas as mh
import glob
import watershed # label image by calling watershed.py
import utils # crop cell by calling utils.py
import plot
from PIL import Image
import skimage
import skimage.io
import scipy
import pandas as pd
import click
import matplotlib.patches as mpatches
if os.name != 'nt':
  from tsne import bh_sne
from time import time
from matplotlib.ticker import NullFormatter
from sklearn import manifold, datasets
import sys
from IPython import embed
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.switch_backend('agg')

from get_features_resnet101 import resnet
from get_features_vgg16 import vgg16

 
def tsne_images(session_id,colors_dict, res, perplexity, early_exaggeration, learning_rate, dpi, canvasSize,colour, model_name):

  l = [c['images'] for c in colors_dict]  # pull out image names into list of lists
  filenames = [item for sublist in l for item in sublist] # flatten list

  if not filenames:
    return  # do nothing if there are no files to operate on
  total_res = res**2
  x_value = np.zeros((len(filenames),total_res)) # Dimension of the image: 70*70=4900; x_value will store images in 2d array
  count = 0
  images = []
  for imageName in filenames: 
    image = scipy.misc.imresize(skimage.io.imread(imageName), (res,res)) #reshape size to (70,70) for every image; 70 being the res
    image3d=image[:,:,:3]
    image2d=mh.colors.rgb2grey(image3d)
    image1d = image2d.flatten() #image1d stores a 1d array for each image
    images.append(image3d)
    x_value[count,:] = image1d # add a row of values
    count += 1

  if model_name != 'None':
    if model_name == 'ResNet V2 101':
      x_value = resnet(filenames= filenames, session_id=session_id) 
    if model_name == 'VGG 16':
      x_value = vgg16(filenames=filenames, session_id=session_id) 

  # vis_data = bh_sne(x_value,perplexity=perplexity)# tsne embedding
  tsne = manifold.TSNE(init='pca', random_state=0, early_exaggeration=early_exaggeration, learning_rate=learning_rate,perplexity=perplexity)
  vis_data = tsne.fit_transform(x_value)

  canvas = plot.image_scatter(vis_data[:, 0], vis_data[:, 1], images, colour,res, min_canvas_size=canvasSize )
  plt.imshow(canvas,origin='lower')
  plt.axis('off')
  save_location = 'static/output/%s/output.png' % session_id
  plt.savefig(save_location,dpi=dpi,pad_inches=1,bbox_inches='tight')
  print('Saved image scatter to %s' % save_location)

  #csv stuff
  colours_csv = [None] * len(filenames) #create empty list 
  for x in range (0, len(filenames)): #create a list of colours in the order of the files
    colours_csv[x] =filenames[x][52:58]

  filenames_csv = [None] * len(filenames) #create empty list 
  for x in range (0, len(filenames)): #create a list of filenames in the order of the files
    filenames_csv[x] =filenames[x][59:]

  csv= 'static/output/%s/ReducedFeatures.csv' % session_id # name the csv
  if os.path.isfile(csv):
    df = utils.read_csv(csv)
    df['File Name']=pd.Series (filenames_csv)
  else:
    df = pd.DataFrame (filenames_csv, columns=["File Name"]) 
  # df['FileName']=pd.Series (filenames)
  df['Colour (in Hex)']=pd.Series (colours_csv)
  df['Tsne_1']=pd.Series (vis_data[:, 0])
  df['Tsne_2']=pd.Series (vis_data[:, 1])
  df.to_csv(csv, index=False)

  return vis_data
