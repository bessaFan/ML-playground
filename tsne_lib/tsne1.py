# tsne1.py
from PIL import Image
from matplotlib import pyplot as plt
import glob
import numpy as np
from tsne import bh_sne
import code
import imgDisplay

from IPython import embed


def tSNE (x_data, display_plot=False):
    
    vis_data = bh_sne(x_data)# tsne embedding
    vis_x = vis_data[:, 0]
    vis_y = vis_data[:, 1]

    if display_plot:
        plt.scatter(vis_x, vis_y, c = 'black') 
        plt.show()
    
    '''
    images = []
    image_size = 70
    plot_size = 1000
    canvas = imgDisplay.image_scatter(x_data, x_data, image_size, plot_size)
    plt.ion() # maybe not needed? for actually seeing what is imshow'ed
    plt.imshow(canvas)
    plt.show(block=False) # actually show the image
'''


'''
    filenames= glob.glob('croppedCell*.jpg')
    for filename in filenames:
        print filename

        im=Image.open(filenames[0])
        im=np.array(im)

        images.append(im)
        plt.imshow(im)
        code.interact(local=dict(globals(), **locals()))
    
        raw_input("press enter..")

if __name__ == '__main__':
    plt.ion()
    tsne()
'''