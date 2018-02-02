def setup(img):
    from PIL import Image
    from random import randint

    # creates a black image to draw upon
    width, height = img.size
    new_img = Image.new("RGB",(width,height),"black")

    vectors = []
    for i in range(0, height * 1):
    	# mod height in case we want more than 1 point per line
    	point = (randint(0,width-1), i % height)
    	direction = randint(0,7)
    	vectors.append((point,direction))

    return(img, new_img, vectors)


def action(img,new_img,moves,x,y,direction):

    from random import choice, randint
    from helper import bright_limit, edge_test

    width, height = img.size

    "continuously brightens and moves in a direction 5 spaces for each line"
    # get pixel info from original image
    pix = img.getpixel((x,y))
    new_pix = new_img.getpixel((x,y))

    for i in range(0,5):

        # combine the pixel values
        new_img.putpixel((x,y),
                        (bright_limit(pix[0] + new_pix[0]),
                         bright_limit(pix[1] + new_pix[1]),
                         bright_limit(pix[2] + new_pix[2])))

		# sets the next position
        x,y = (x + moves[direction % len(moves)][0],
               y + moves[direction % len(moves)][1])

        # avoid losing lines
        if edge_test((x,y), width, height): x,y = randint(0,width - 1), randint(0, height -1)

    avg_min = 15
    avg_max = 255

    avg_pix = sum(pix) // len(pix)
    avg_new_pix = sum(new_pix) // len(new_pix)

    if (avg_pix <= avg_min) or (avg_new_pix >= avg_max):
        direction = direction + choice((-1,0,1,4))

    return((x,y),direction)
