# watershed.py
import numpy as np
import pylab
import mahotas as mh

def label(images):
	T = mh.thresholding.otsu(images) # calculate a threshold value
	dnaf = mh.gaussian_filter(images,8) # apply a gaussian filter that smoothen the image
	dnat = dnaf > T # do threshold
	labelled = mh.label(dnat)[0] #labelling thereshold image
	return labelled