def setup(img):
	from PIL import Image
	from random import randint

	# creates a black image to draw upon
	width, height = img.size
	new_img = Image.new("RGB",(width,height),"black")

	vectors = []
	for i in range(0, height * 50):

		# mod height in case we want more than 1 point per line
		point = (randint(0,width-1), randint(0,height-1))
		direction = randint(0,7)
		vectors.append((point,direction))

	return(img, new_img, vectors)


def action(img,new_img,moves,x,y,direction):
	# effect works better if the line generation range is increased to 50+
	from random import choice, randint
	from helper import bright_limit, edge_test

	width, height = img.size

	# black out
	new_img.putpixel((x,y),(0,0,0))

	# gets pixel to decide on movement
	pix = img.getpixel((x,y))
	avg_pix = sum(pix) // len(pix)
	if avg_pix < 50: direction = direction + choice((-1,0,1))

	# sets the next position
	x,y = (x + moves[direction % len(moves)][0],
         y + moves[direction % len(moves)][1])

	# moves the vector to random spot if it leaves the boundaries
	if edge_test((x,y),width,height):
		(x,y) = (randint(0,width-1), randint(0,height-1))
		direction = randint(0,7)

	# converts new_img over to pixel from original
	pix = img.getpixel((x,y))
	new_img.putpixel((x,y),pix)

	return((x,y),direction)
