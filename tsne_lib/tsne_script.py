#!/usr/bin/env python
import os
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

#from get_features_resnet101 import resnet
#from get_features_vgg16 import vgg16

 
def tsne_images(session_id,colors_dict, res, perplexity, early_exaggeration, learning_rate, dpi, canvasSize,colour, model_name):

  l = [c['images'] for c in colors_dict]  # pull out image names into list of lists
  filenames = [item for sublist in l for item in sublist] # flatten list

  if not filenames:
    return  # do nothing if there are no files to operate on
  total_res = res**2
  x_value = np.zeros((len(filenames),total_res)) # Dimension of the image: 70*70=4900; x_value will store images in 2d array
  count = 0
  images = []
  # colour = np.zeros(len(filenames))
  for imageName in filenames: 
    image = scipy.misc.imresize(skimage.io.imread(imageName), (res,res)) #reshape size to (70,70) for every image; 70 being the res
    image3d=image[:,:,:3]
    image2d=mh.colors.rgb2grey(image3d)
    image1d = image2d.flatten() #image1d stores a 1d array for each image
    images.append(image3d)
    x_value[count,:] = image1d # add a row of values
    count += 1

  if model_name == 'ResNet V2 101':
    x_value = resnet(filenames) 
  if model_name == 'VGG 16':
    x_value = vgg16(filenames) 

  # vis_data = bh_sne(x_value,perplexity=perplexity)# tsne embedding
  tsne = manifold.TSNE(init='pca', random_state=0, early_exaggeration=early_exaggeration, learning_rate=learning_rate,perplexity=perplexity)
  vis_data = tsne.fit_transform(x_value)

  canvas = plot.image_scatter(vis_data[:, 0], vis_data[:, 1], images, colour,res, min_canvas_size=canvasSize )
  plt.imshow(canvas,origin='lower')
  plt.axis('off')
  #plt.title('%s vs %s' % (x,y))
  #plt.xlabel('%s' % x)
  #plt.ylabel('%s' % y)
  #patches=[]  
  #plt.legend(handles=patches,bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0, frameon=False)
  save_location = 'static/output/%s/output.png' % session_id
  plt.savefig(save_location,dpi=dpi,pad_inches=1,bbox_inches='tight')
  # plt.show()
  print('Saved image scatter to %s' % save_location)
  return vis_data
