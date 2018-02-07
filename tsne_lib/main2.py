#main2.py
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
filenamesDAPI=list(glob.glob('./cell images/*ch1*.tiff'))
filenamesSE=list(glob.glob('./cell images/*ch2*.tiff'))
saved_location='./cropped_and_resized/'



for idx, imageNumber in enumerate(range(len(filenamesDAPI))): 
    #print filenamesSE[imageNumber]
    #if not filenamesSE[imageNumber] == './cell images/r05c05f65p01-ch2sk1fk1fl1.tiff':
    #     continue
    
    # obtains image data
    DAPI = skimage.io.imread(filenamesDAPI[imageNumber]) 
    SE = skimage.io.imread(filenamesSE[imageNumber]) 

    # applys gaussina filter
    DAPIf = mh.gaussian_filter(DAPI, 13)
    SEf = mh.gaussian_filter(SE, 3)

    # finds threshold
    T = mh.thresholding.otsu(np.uint16(SEf))
    SEt= SEf > T/2

    # Finds seeds on the nuclear image
    rmax = mh.regmax(DAPIf)
    pylab.imshow(rmax)
    rmax[np.logical_not(SEt)] = 0

    # Watershed on the cytoplasm image
    seeds,nr_nuclei = mh.label(rmax) # nuclei count
    imagew = mh.cwatershed(-SEf, seeds)

    # Remove areas that aren't nuclei 
    SEn=np.logical_not(SEt)
    imagew[SEn] = 0
    #pylab.imshow(imagew.astype(np.int16)) # convert datatype from int64 to int16 to display labelled value in []

    #prepare names for cropped cells
    filenamesDAPI[idx]= filenamesDAPI[idx][14:38]
    filenames=range(nr_nuclei)
    for x in filenames:
       filenames[x]=filenamesDAPI[idx]+str(filenames[x])

    # crop and label images
    utils.crop_and_save(SE, imagew,'./cropped_and_resized/', filenames= filenames, square=True, resize=70, padding=5)
    utils.crop_and_save(SE, imagew,'./cropped_and_resized/', filenames= filenames, square=True, resize=70, padding=5)


# generating random cell ID for each cropped cells
cellID =[]
filenames=list(glob.glob('./cropped_and_resized/*'))
for imageNumber in range(len(filenames)): 
    cellID.append(str(uuid.uuid4()))
filename="file.csv" 
df = pd.DataFrame (cellID, columns=["CellID"]) # assign unique ID for each cell 
df.to_csv(filename, index=False)



# finding a list of pixels in cell boundries 
cell_boundaries_list=[]
filenames = list(glob.glob('./cropped_and_resized/*')) #load image
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

csv = "file.csv" 
df = utils.read_csv(csv)
print df.shape
df['cell boundary']=pd.Series (cell_boundaries_list)
df['FileName']=pd.Series (filenames)
df.to_csv(csv, index=False)


filenamesch3=list(glob.glob('./cell images/*ch3*.tiff'))
newT= mh.thresholding.otsu(filenamesNEW) # calculate a threshold value
newf = mh.gaussian_filter(filenamesNEW,8) # apply a gaussian filter that smoothen the image
dnat = dnaf > T # do threshold
labelled = mh.label(dnat)[0] #labelling thereshold image
return labelled







