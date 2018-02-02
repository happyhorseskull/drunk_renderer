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

    pix = img.getpixel((x,y))
    new_img.putpixel((x,y),(pix[0],pix[1],pix[2]))

    avg_pix = sum(pix) // len(pix)
    if avg_pix < 50: direction = direction + choice((-1,0,1))

	# sets the next position
    x,y = (x + moves[direction % len(moves)][0],
           y + moves[direction % len(moves)][1])

    return((x,y),direction)
