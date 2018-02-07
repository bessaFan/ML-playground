#for new cell line 
import os
import numpy as np
import pylab
import mahotas as mh
import glob     
import watershed 
import utils 
import plot
import csv
import main
from PIL import Image
import skimage
import skimage.io
import scipy
import pandas as pd
import click
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from IPython import embed
from tsne import bh_sne
import uuid


# Loads both nuclear (DAPI) and cytoplasm (SE) images
filenames=list(glob.glob('./new cellline/original images/*ch3*.tif'))


for idx, imageNumber in enumerate(range(len(filenames))): 

    #print filenamesSE[imageNumber]
    #if not filenamesSE[imageNumber] == './cell images/r05c05f65p01-ch2sk1fk1fl1.tiff':
    #     continue
    
    # obtains image data
    image = skimage.io.imread(filenames[imageNumber]) 

    # applys gaussina filter
    imagef = mh.gaussian_filter(image, 15)

    # finds threshold
    T = mh.thresholding.otsu(np.uint16(imagef))
    imaget= imagef > T+100

    # Finds seeds on the nuclear image
    rmax = mh.regmax(imagef)
    pylab.imshow(rmax)
    rmax[np.logical_not(imaget)] = 0

    # Watershed on the cytoplasm image
    seeds,nr_nuclei = mh.label(rmax) # nuclei count
    imagew = mh.cwatershed(-imagef, seeds)
    # Remove areas that aren't nuclei 
    imagen=np.logical_not(imaget)
    imagew[imagen] = 0
    #pylab.imshow(imagew.astype(np.int16)) # convert datatype from int64 to int16 to display labelled value in []
    #prepare names for cropped cells
    filenames[idx]= filenames[idx][31:-4]
    index = range(nr_nuclei)

    cellNames=[]
    for x in range(nr_nuclei):
        cellNames.append(filenames[idx]+str(index[x]))

    # crop and label images
    utils.crop_and_save(image, imagew,'./new cellline/cropped/', filenames= cellNames, square=True, resize=70, padding=5)


# generating random cell ID for each cropped cells
cellID=[]
filenames=list(glob.glob('./new cellline/cropped/*'))
for imageNumber in range(len(filenames)): 
    cellID.append(str(uuid.uuid4()))
csv="fileNew.csv" 
df = pd.DataFrame (cellID, columns=["CellID"]) # assign unique ID for each cell 
df.to_csv(csv, index=False)



# finding a list of pixels in cell boundries 
cell_boundaries_list=[]
filenames = list(glob.glob('./new cellline/cropped/*')) #load image
for idx,filename in enumerate(filenames):
    targetCell = skimage.io.imread(filenames[idx])
    dimension = targetCell.shape
    # calculating cell boundaries
    boolean_border = mh.bwperim(targetCell, n=4)
    cell_boundaries = np.ravel_multi_index(np.nonzero(boolean_border),dimension)
    # formatting the calculated cell boundaries
    CB_string=map(str, cell_boundaries) # converting all the elements in the array to string
    for x,y in enumerate(CB_string): # add ", " to all the elements so that when they are combined, they are still distinctly recognizable
        CB_string[x]=CB_string[x]+' ' 
    boundaries=''.join(CB_string) # combine all elements in an array to form a single string
    # adding the calculation to the cell_boundaries_list
    cell_boundaries_list.append(boundaries)

df = utils.read_csv(csv)
print df.shape
df['cell boundary']=pd.Series (cell_boundaries_list)
df['FileName']=pd.Series (filenames)
df.to_csv(csv, index=False)

'''
filenamesch3=list(glob.glob('./cell images/*ch3*.tiff'))
newT= mh.thresholding.otsu(filenamesNEW) # calculate a threshold value
newf = mh.gaussian_filter(filenamesNEW,8) # apply a gaussian filter that smoothen the image
dnat = dnaf > T # do threshold
labelled = mh.label(dnat)[0] #labelling thereshold image
return labelled
'''






