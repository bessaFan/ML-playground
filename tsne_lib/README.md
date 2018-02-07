# Visualize Single Cells Using t-SNE

t-SNE Result Plot:

![tsne output](https://raw.githubusercontent.com/Kafri-Lab/Cell-t-SNE/master/readme_images/output-tsne-full%20resolution.jpg "tsne output")

Color Legend (Ground Truth)
- ![#00dd0e](https://placehold.it/15/00dd0e/000000?text=+) Green cells are cytoplasm stained only and are correctly grouped by t-SNE.
- ![#ff0000](https://placehold.it/15/ff0000/000000?text=+) Red cells are peroxisome stained only and are correctly grouped by t-SNE.
- ![#7c7c7c](https://placehold.it/15/7c7c7c/000000?text=+) Gray cells are nucleus stained only and are correctly grouped by t-SNE.
- ![#0f6afc](https://placehold.it/15/0f6afc/000000?text=+) Blue cells are whole cell stained and the sample size is too small to see a t-SNE group.

## Project Layout

| Directory or file            | Description                                                                                        |
|------------------------------|----------------------------------------------------------------------------------------------------|
| "Visualizing with t-SNE.ipynb" | Main code file! Contains lots of practice and a final section which produces the above t-SNE image |
| "barcode_images/"              | 1,571 cropped, rotated, and masked single cell images used in t-SNE. Each cell is barcoded with a different stain localization within the cell  |

## Project Status

I'm hoping to clean up the code. Open an issue if you need help.


## Futher reading about t-SNE...

- http://distill.pub/2016/misread-tsne/
- https://indico.io/blog/visualizing-with-t-sne/
