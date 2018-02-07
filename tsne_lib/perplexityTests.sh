#!/bin/bash

for (( x=5; x<=100; x+=10 ))
do  
#	./main.py tsne_images  --csv combined.csv --perplexity $x
#	./main.py image_scatter  --csv combined.csv --color-by CellLine -x tsne1 -y tsne2 --dpi 650 --output_filename $x
	./main.py tsne_images  --csv file.csv --perplexity $x
	./main.py image_scatter  --csv file.csv --color-by CellLine -x tsne1 -y tsne2 --dpi 650 --output_filename $x
done
