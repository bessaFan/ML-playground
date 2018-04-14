#!/usr/bin/python
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # disables warning: Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.1 SSE4.2 AVX AVX2 FMA

import time
import glob
import utils 
import csv
import pandas as pd
import skimage
import skimage.io
import scipy
import numpy as np
import mahotas as mh
import tensorflow as tf
import tensorflow.contrib.slim.nets as nets
from tensorflow.contrib.slim.nets import resnet_v2

from PIL import Image
from IPython import embed
from tensorflow.python.tools import inspect_checkpoint as chkp
from sklearn.metrics import average_precision_score

slim = tf.contrib.slim


def resnet(filenames, session_id):
  # Clean up model 
  tf.reset_default_graph()

  # Load images
  images = np.zeros((len(filenames), 224, 224, 3), dtype=np.float32)
  for i, imageName in enumerate(filenames): 
    print i, imageName
    img = skimage.io.imread(imageName)
    if len(img.shape) == 2:
      # we have a 2D, black and white image but  vgg16 needs 3 channels
      img = np.expand_dims(img,2)
      img = np.repeat(img, 3, axis=2)
    img = scipy.misc.imresize(img, (224,224))
    images[i,:,:,:] = img

  in_images = tf.placeholder(tf.float32, images.shape)

  with slim.arg_scope(resnet_v2.resnet_arg_scope()):
    model, intermed = resnet_v2.resnet_v2_101(in_images, None, is_training=False)
    restored_variables = tf.contrib.framework.get_variables_to_restore()
    restorer = tf.train.Saver(restored_variables)

    with tf.Session() as sess:
      img_net_path = 'models/resnet_v2_101.ckpt'
      restorer.restore(sess, img_net_path)
      features = sess.run(model, feed_dict={in_images:images})

  # Clean up model 
  tf.reset_default_graph()

  features = features.squeeze() # remove dimensions that are only 1 long

  #csv stuff
  # features_1d=np.empty(features.shape[0])
  features_1d = [None] * features.shape[0]
  placeholder=""
  for x in range(0, features.shape[0]):
    for y in range(0, features.shape[1]):
        placeholder+=str(features[x][y])+" "
    features_1d[x]=placeholder
    placeholder=""
  


  csv= 'static/output/%s/FeatureVectors.csv' % session_id

  if os.path.isfile(csv):
    df = utils.read_csv(csv)
    df['Resnet_features']=pd.Series (features_1d)
  else:
    df = pd.DataFrame (features_1d, columns=['Resnet_features']) 
  df.to_csv(csv, index=False)

  return features