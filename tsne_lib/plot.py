import numpy as np

def image_scatter(xx, yy, images, colours, min_canvas_size=1000, bg_color=255, lw=10):
    """
    Embeds images into a scatter plot.
    Parameters
    ---------
    images: list or numpy array
        Corresponding images to features. Expects float images with values from (0,1).
    min_canvas_size: float or int  # TODO: change variable name from res to min_canvas_size
        Size of canvas, the minimum size of either x or y
    bg_color: float or numpy array
        Background color value
    lw: int
        Line width of the coloured boxes around cells
    Returns
    ------
    canvas: numpy array
        Image of visualization
    """

    max_width = max([image.shape[0] for image in images])
    max_height = max([image.shape[1] for image in images])

    # Get scatter plot axis limits (min and max)
    x_min, x_max = xx.min(), xx.max()
    y_min, y_max = yy.min(), yy.max()

    # Calculate canvas size
    scale_canvas_x = (x_max-x_min)
    scale_canvas_y = (y_max-y_min)
    if scale_canvas_x > scale_canvas_y:
        canvas_res_x = scale_canvas_x/float(scale_canvas_y)*min_canvas_size
        canvas_res_y = min_canvas_size
    else:
        canvas_res_x = min_canvas_size
        canvas_res_y = scale_canvas_y/float(scale_canvas_x)*min_canvas_size

    # Create canvas by embedding images at the correct positions according it t-sne
    canvas = np.ones((int(canvas_res_x)+max_width+lw, int(canvas_res_y)+max_height+lw, 3),dtype='uint8')*bg_color
    # TODO: Replace this to use a scale factor
    x_coords = np.linspace(x_min, x_max, canvas_res_x) # TODO: Replace this to use a scale factor
    y_coords = np.linspace(y_min, y_max, canvas_res_y) # TODO: Replace this to use a scale factor

    for x, y, image, colour in zip(xx, yy, images, colours):
        w, h = image.shape[:2]
        scaled_x = np.argmin((x - x_coords)**2)+lw # TODO: Replace this to use a scale factor
        scaled_y = np.argmin((y - y_coords)**2)+lw # TODO: Replace this to use a scale factor
        canvas[scaled_x-lw:scaled_x+w+lw, scaled_y-lw:scaled_y+h+lw] = colour # put coloured box around image 
        # from IPython import embed
        # embed() # drop into an IPython session
        canvas[scaled_x:scaled_x+w, scaled_y:scaled_y+h] = image # embed image

    # from PIL import Image
    # image = Image.fromarray(np.uint8(canvas))
    # image.show()
        # inn = raw_input("press enter..")
        # print inn
        # if inn == 'interp':
        #     from IPython import embed
        #     embed() # drop into an IPython session
        
    return canvas

