#!/usr/bin/python3

import argparse
from os import mkdir,listdir
from PIL import Image
from random import randint
from shutil import which

from helper import (image_resize, edge_bounce, wall_func, bright_limit,
					edge_test, clean_up_points, make_mp4)

from effects import effects

# argparse
parser = argparse.ArgumentParser()
parser.add_argument("image", help="please include a valid image file")
parser.add_argument("--walls",
					help="vectors bounce off edges instead of disappearing",
					action="store_true")
parser.add_argument("--ani",
					help="creates animation of drawing process. Requires ffmpeg.",
					action="store_true")
parser.add_argument("--steps", type=int,
					help="How many drawing iterations occur. Default is 300")
parser.add_argument("--framerate", type=int,
					help="How many frames per second in animation is --ani is used")

effect_list = []
for file in listdir("effects/"):
	if file.endswith(".py"):
		if file.startswith("__"): pass
		else: effect_list.append(file.split('.')[0])

effects_string = ("image effects:\n\t " + "\n\t".join(sorted(effect_list)))
parser.add_argument("--effect",	default="pink_blue", help=effects_string)

args = parser.parse_args()

image_file_name = args.image

effect = getattr(effects, args.effect)


if args.walls: walls_on = True
else: walls_on = False

if args.steps: steps = args.steps
else: steps = 300

if args.ani:
	if which("ffmpeg") is None:
		print("\n\tError: ffmpeg must be installed to produce animations.")
		exit()
	animate = True
else: animate = False

if args.framerate: framerate = args.framerate
else: framerate = 25

if animate:
	tmp_folder = (".tmp_"+str(randint(0,10000))+"/")
	mkdir(tmp_folder)


# variables

img = Image.open(image_file_name).convert('RGB')
img, width, height = image_resize(img)

# walk directions
up   = ( 0, 1); r_u = ( 1, 1); right = ( 1, 0); r_d = ( 1,-1)
down = ( 0,-1); l_d = (-1,-1); left  = (-1, 0); l_u = (-1, 1)

moves = [up, r_u, right, r_d, down, l_d, down, left, l_u]


# create list of line starting points
img,new_img,vectors = effect.setup(img)

# Main

# steps determines total iterations
for m in range(0,steps):

	# if list empty kill the process
	if len(vectors) <= 0: break
	for i in range(0, len(vectors)):
		# does stuff to vector then returns it
		vectors[i] = effect.action(img, new_img, moves,
						vectors[i][0][0],
						vectors[i][0][1],
						vectors[i][1])

	# make sure vectors are in bounds
	vectors = clean_up_points(vectors, img.size[0], img.size[1])
	# saves image for animation later
	if animate: new_img.save(tmp_folder + str(m).zfill(6) + ".jpg")

# save final result
new_img.save("out.png")

# creates an mp4 that Twitter accepts
if animate: make_mp4(tmp_folder, framerate)
