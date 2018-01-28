#!/usr/bin/python3

import sys
from PIL import Image
from random import choice
from random import randint

img = Image.open(sys.argv[1]).convert('RGB')
width, height = img.size

# creates a black image to draw upon
new_img = Image.new("RGB",(width,height),"black")

# drunk walk directions
up 		= ( 0, 1);	l_u = (-1, 1)
right = ( 1, 0);	r_u = ( 1, 1)
down 	= ( 0,-1);	r_d = ( 1,-1)
left 	= (-1, 0);	l_d = (-1,-1)


moves = [up, r_u, right, r_d, down, l_d, down, left, l_u]

# functions

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


# Main loop

# starts with the Y-axis because it feels more natural??
for j in range(0, height):
	dir = randint(0,7)
	# starting point on the X-axis determined here
	pos = (randint(0,width-1), j)
	# the second value can be any positive int. Determines how long the line will be
	for i in range(0,width*2):

		# get pixel info from original image
		pix = img.getpixel((pos[0],pos[1]))
		# get pixel info from new image
		new_pix = new_img.getpixel((pos[0],pos[1]))

		# combine the pixel values
		new_img.putpixel((pos[0],pos[1]), (bright(pix[0] + new_pix[0]),
																			 bright(pix[1] + new_pix[1]),
																			 bright(pix[2] + new_pix[2])))
                                       
		# movement rules
		avg_pix = sum(pix) // len(pix)
		# drunk walk a choice in direction when it reaches a dark pixel otherwise will continue in straight line
		if avg_pix < 127 - 50: dir = dir + choice((-1,0,1))

		# sets the next position
		pos = (pos[0] + moves[dir % len(moves)][0],
					 pos[1] + moves[dir % len(moves)][1])

		# edges that keep the renderer within bounds. not using this would probably keep the edges from getting 
    # extra bright but I wanted to include it for demonstration purposes
    
		# top wall = 0
		if (pos[1] >= height):
			pos = (pos[0], height - 1)
			wall = 0
			dir = wall_func(wall,dir)

		# right wall = 2
		if (pos[0] >= width):
			pos = (width - 1, pos[1])
			wall = 2
			dir = wall_func(wall,dir)

		# bottom wall = 4
		if (0 > pos[0]):
			pos = (0,pos[1])
			wall = 4
			dir = wall_func(wall,dir)

		# left wall = 6
		if (0 > pos[1]):
			pos = (pos[0],0)
			wall = 6
			dir = wall_func(wall,dir)
      
    # mods the direction back into a number between 0-7 because it feels like a good idea
		dir = dir % len(moves)

new_img.show()
new_img.save("out.jpg")
