# drunk_renderer
renders image from existing image pixels onto a black canvas

## how to use

takes an existing image 

$ python3 drunk_render.py clint.jpg

and creates out.jpg


## what it does

drunk_render.py uses the Pillow library for image manipulation.
It grabs a point on an existing image, does some stuff, and copies it to a new image. It may change direction when it reaches a dark pixel but most of the time it continues in a particular direction.
