#!/usr/bin/python3

import sys
import argparse
from os import mkdir, system
from PIL import Image
from random import choice
from random import randint
from shutil import rmtree, which

parser = argparse.ArgumentParser()
parser.add_argument("image", help="please include a valid image file")
parser.add_argument("--walls",
		                help="lines bounce off edges instead of disappearing",
		                action="store_true")
parser.add_argument("--ani",
								    help="creates animation of drawing process. Requires ffmpeg.",
										action="store_true")
parser.add_argument("--steps", type=int,
										help="How many drawing iterations occur. Default is 1000")

args = parser.parse_args()

image_file_name = args.image

if args.walls:
	walls_on = True
else:
	walls_on = False

if args.ani:
	if which("ffmpeg") is None:
		print("\n\tError: ffmpeg must be installed on your system to produce animations.")
		exit()
	animate = True
else:
	animate = False

if args.steps:
	steps = args.steps
else:
	steps = 1000

tmp_folder = ("tmp_"+str(randint(0,10000))+"/")
mkdir(tmp_folder)

# drunk walk directions
up   = ( 0, 1); r_u = ( 1, 1); right = ( 1, 0); r_d = ( 1,-1)
down = ( 0,-1); l_d = (-1,-1); left  = (-1, 0); l_u = (-1, 1)

moves = [up, r_u, right, r_d, down, l_d, down, left, l_u]

# functions

def image_resize(img):
	"ffmpeg requires that image dimensions be divisible by 2 because of yuv420"
	width, height = img.size
	if width % 2 > 0: width = width - 1
	if height % 2 > 0: height = height - 1

	img = img.resize((width, height), Image.ANTIALIAS)
	return(img,width,height)

def bright(pix_val):
	"increases brightness of pixels but limits them to the max 255 value"
	# adds a regular amount of brightness that helps dark areas
	pix_val += 10

	if pix_val > 255:
		pix_val = 255
	return(pix_val)

def wall_func(wall,direction):
	"determines which way the line will bounce off walls"
	"when the line bounces in a clockwise direction 2 is added to the moves variable and counterclockwise subtracts 2"
	if direction % 2 == 0:
		direction = direction + 4
	else:
		if wall + 1 == direction:
			direction + 2
		else:
			direction - 2

	return(direction)

def edges(position, direction):
	"keeps the points within the bounds of the image"
	# edges that keep the renderer within bounds
	# top wall
	if (position[1] >= height):
		position = (position[0], height - 1)
		top_wall = 0
		direction = wall_func(top_wall,direction)

	# right wall
	if (position[0] >= width):
		position = (width - 1, position[1])
		right_wall = 2
		direction = wall_func(right_wall,direction)

	# bottom wall
	if (0 > position[0]):
		position = (0,position[1])
		bottom_wall = 4
		direction = wall_func(bottom_wall,direction)

	# left wall = 6
	if (0 > position[1]):
		position = (position[0],0)
		left_wall = 6
		direction = wall_func(left_wall,direction)

	return(position,direction)


def no_edges(position):

	off_edge = False

	if position[0] < 0: 			off_edge = True
	if position[0] >= width: 	off_edge = True
	if position[1] < 0: 			off_edge = True
	if position[1] >= height: off_edge = True

	return(off_edge)


def clean_up():
	"remove points that are off the edge"
	del_list = []

	for i in range(0,len(lines)):
		point = lines[i][0]
		direction = lines[i][1]
		if walls_on:
			lines[i] = edges(point, direction)
		else:
			if no_edges(point): del_list.append(i)

	for i in range(0,len(del_list)):
		del lines[del_list.pop()]


# Main

img = Image.open(image_file_name).convert('RGB')
width, height = img.size

if (width  % 2 > 0) or (height % 2 > 0):
	img, width, height = image_resize(img)

# creates a black image to draw upon
new_img = Image.new("RGB",(width,height),"black")

# create list of line starting points
lines = []
for i in range(0, height):
	pos = (randint(0,width-1),i)
	dir = randint(0,7)
	lines.append((pos,dir))

# determines total iterations through
for m in range(0,steps):

	# if list empty kill the process
	if len(lines) <= 0: break

	for i in range(0, len(lines)):

		x   = lines[i][0][0]
		y   = lines[i][0][1]
		dir = lines[i][1]

		# get pixel info from original image
		pix = img.getpixel((x,y))

		# get pixel info from new image
		new_pix = new_img.getpixel((x,y))

		# combine the pixel values
		new_img.putpixel((x,y), (bright(pix[0] + new_pix[0]),
					 bright(pix[1] + new_pix[1]),
					 bright(pix[2] + new_pix[2])))

		# movement rules
		avg_pix = sum(pix) // len(pix)
		# drunk walk a choice in direction when it reaches a dark area otherwise will continue in straight line
		if avg_pix < 127 - 50: dir = dir + choice((-1,0,1))
		if avg_pix > 250: pos = (randint(0,width-1),randint(0,height-1))

		# sets the next position
		pos = (x + moves[dir % len(moves)][0],
					 y + moves[dir % len(moves)][1])

		lines[i] = (pos,dir)

	clean_up()

	if animate: new_img.save(tmp_folder + str(m).zfill(6) + ".jpg")

new_img.save("out.png")
if animate: system('ffmpeg -loglevel quiet -y -f lavfi -i anullsrc -framerate 60 -i ' + tmp_folder +
			             '%06d.jpg -vcodec libx264 -crf 15 -pix_fmt yuv420p -c:a aac -strict -2 -shortest out.mp4')

rmtree(tmp_folder)
