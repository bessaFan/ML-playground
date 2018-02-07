#!/usr/bin/env python
from time import time
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from sklearn import manifold, datasets
import numpy as np
import skimage.io
import glob
import scipy
import plot
import sys
import mahotas as mh
from IPython import embed



def tsne_images(res,perplexity):
  filenames=list(glob.glob('static/uploads/*g'))
  total_res = res**2
  x_value = np.zeros((len(filenames),total_res)) # Dimension of the image: 70*70=4900; x_value will store images in 2d array
  count = 0
  images = []
  colour = []
  for imageName in filenames: 
    image = scipy.misc.imresize(skimage.io.imread(imageName), (res,res)) #reshape size to (70,70) for every image; 70 being the res
    images.append(image)
    image3d=image[:,:,:3]
    image2d=mh.colors.rgb2grey(image3d)
    image1d = image2d.flatten() #image1d stores a 1d array for each image
    x_value[count,:] = image1d # add a row of values
    count += 1
    colour.append(0)
  embed()
  # vis_data = bh_sne(x_value,perplexity=perplexity)# tsne embedding
  tsne = manifold.TSNE( init='pca', random_state=0, perplexity=perplexity)
  vis_data = tsne.fit_transform(x_value)





  return vis_data




def image_scatter(csv,color_by,x,y,dpi,channel,output_filename):

  df = utils.read_csv(csv)
  print('Found number of cells: %s' % df.shape[0])

  cell_imgs = []
  colors = []
  xx = np.array([])
  yy = np.array([])

  cmap='gist_rainbow'
  color_list = utils.get_colors(len(np.unique(df[color_by])),cmap=cmap)

  # blue is better when there are only 3 colours
  if len(color_list) == 3 and cmap == 'gist_rainbow':
    color_list[2] = (0.05, 0.529, 1, 1.0)
  # blue is better when there are only 2 colours
  if len(color_list) == 2 and cmap == 'gist_rainbow':
    color_list[1] = (0.05, 0.529, 1, 1.0)

  images = df["FileName"]

  for row_id, row in df.iterrows():
    cell_id = row.CellID
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
  patches=[]
  plt.legend(handles=patches,bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0, frameon=False)
  save_location = './images/%s_image_scatter_by_%s_dpi%s_%s.png' % (csv, color_by, dpi, output_filename)
  plt.savefig(save_location,dpi=dpi,pad_inches=1,bbox_inches='tight')
  # plt.show()
  print('Saved image scatter to %s' % save_location)













  hgfghjk





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