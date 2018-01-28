# drunk_renderer
renders image from existing image pixels onto a black canvas

## how to use

takes an existing image 

$ python3 drunk_render.py clint.jpg

and creates out.jpg


## what it does

drunk_render.py uses the Pillow library extensively.
It grabs a point on an existing image, randomly chooses a direction, and may change course when it reaches a dark pixel.
