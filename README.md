# drunk_renderer
renders image from existing image pixels onto a black canvas

## how to use

takes an existing image 

$ python3 drunk_render.py clint.jpg

and creates out.png

--ani

causes it to also create out.mp4

--steps

determines the number of iterations that will be drawn.

--effect

there are multiple image effects. current list: drunk_walk, pink_blue, retina_bleed, static

## what it does

drunk_render.py uses the Pillow library for image manipulation.
It grabs a point from an existing image array, does some stuff, and copies it to a new image array.
