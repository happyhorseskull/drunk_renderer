def setup(img):
    from PIL import Image
    from random import randint

    # creates a black image to draw upon
    width, height = img.size
    new_img = img

    vectors = []

    for i in range(0, height * 1):
    	# mod height in case we want more than 1 point per line
    	point = (0, i % height)
    	direction = 2
    	vectors.append((point,direction))

    return(img, new_img, vectors)


def action(img,new_img,moves,x,y,direction):
    from random import choice, randint
    from helper import bright_limit, edge_test

    width, height = img.size

    pix = img.getpixel((x,y))
    avg_pix = sum(pix) // len(pix)
    bright = avg_pix / 255
    if avg_pix > 127:
        new_img.putpixel((x,y),
                            (int(255 * bright),
                             int(105 * bright),
                             int(180 * bright)))
    else: new_img.putpixel((x,y),
                            (int( 30 * bright),
                             int( 70 * bright),
                             int(234 * bright)))

	# sets the next position
    x,y = (x + moves[direction % len(moves)][0],
           y + moves[direction % len(moves)][1])

    if edge_test((x,y), width, height):
        x,y = randint(0,width-1),randint(0,height-1)
    return((x,y),direction)
