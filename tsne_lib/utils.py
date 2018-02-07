# utils.py
import numpy as np
import pylab
import mahotas as mh
import skimage
from IPython import embed
from skimage.measure import regionprops 
from matplotlib import pyplot as plt
import scipy.misc
import pandas as pd


def crop_and_save(image, labelled, save_location, filenames=None, square=False, resize=70, padding=5):
  nr_objects=int(np.max(labelled))
  stats = skimage.measure.regionprops(labelled.astype(int))

  for index in range(nr_objects):
    stat = stats[index]
    x_px_size = int(stat.bbox[2]-stat.bbox[0])
    y_px_size = int(stat.bbox[3]-stat.bbox[1])

    if square:
      max_resolution = np.maximum(x_px_size,y_px_size)
      x_px_size = max_resolution
      y_px_size = max_resolution

    x_px_size += padding
    y_px_size += padding
    centroidValue=stat.centroid
    y,x = labelled.shape
    startx = centroidValue[0]-x_px_size/2
    starty = centroidValue[1]-y_px_size/2
    if (centroidValue[0]<x_px_size/2):
      startx = centroidValue[0]
    if (centroidValue[1]<y_px_size/2):
      starty = centroidValue[0]

    # Black out everything except the cell
    labelled1=labelled==index+1 # get boundry of one cell indentified by it's index (1,2,3,etc. note: 0 is background)
    labelled1=scipy.ndimage.binary_fill_holes(labelled1).astype(int) # fill interior of cell
    image1 = image.copy() # create a copy of the image without blackout
    image1[labelled1==0]=0 # set everything other than the cell to black

    # Crop the cell
    result = image1[int(startx):int(startx+x_px_size), int(starty):int(starty+y_px_size)]
    if resize:
      result = scipy.misc.imresize(result, (resize,resize)) 
    if result.size == 0:
      print('[WARN] image size is 0')
      continue

    name = filenames[index] if filenames else index # Use a given filename for this crop or use the index when saving
    filename = '%s%s.png' % (save_location, name)
    print('Saving cropped cell to file: %s' % filename)
    scipy.misc.imsave(filename, result)


def read_csv(filename):
  df = pd.read_csv(filename)
  return df

def gray_to_color(img):
    if len(img.shape) == 2:
        # img = np.invert(img)
        img = np.dstack((img, img, img))
    return img

def get_colors(n, cmap='gist_rainbow'):
    color_list = []
    color_map = plt.cm.get_cmap(cmap, n)
    for i in range(n):
      color_list.append(color_map(i))

    print color_list
    return color_list
