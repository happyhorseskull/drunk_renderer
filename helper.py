def image_resize(img):

    from PIL import Image

    "ffmpeg requires that image dimensions be divisible by 2 because of yuv420"

    # reduce brightness to crawl on white
    width, height = img.size
    max_dimension = 640

    # keeps image size small which emphasizes changes and reduces processing time
    if width > height:
        # float division or else returns 0
        height = int(height * (max_dimension / width))
        width = max_dimension
    else:
        width = int(width * (max_dimension / height))
        height = max_dimension

    if width % 2 > 0: width = width - 1
    if height % 2 > 0: height = height - 1

    img = img.resize((width, height), Image.ANTIALIAS)
    return(img,width,height)


def bright_limit(pix_val):
	"increases brightness of pixels but limits them to the max 255 value"
	# adds a regular amount of brightness that helps dark areas
	if pix_val < 10: pix_val += 10

	if pix_val > 255:
		pix_val = 255
	return(pix_val)


def edge_test(point, width, height):

	off_edge = False

	if (point[0] < 0) or (point[0] >= width):  off_edge = True
	if (point[1] < 0) or (point[1] >= height): off_edge = True

	return(off_edge)


def edge_bounce(img, point, direction):
    "keeps the points within the bounds of the image"

    width,height = img.size

    # edges that keep the renderer within bounds
    # top wall = 0

    if (point[1] >= height):
        point = (point[0], height - 1)
        direction = wall_func(0,direction)

    # right wall = 2
    if (point[0] >= width):
        point = (width - 1, point[1])
        direction = wall_func(2,direction)

    # bottom wall = 4
    if (0 > point[0]):
        point = (0,point[1])
        direction = wall_func(4,direction)

    # left wall = 6
    if (0 > point[1]):
        point = (point[0],0)
        direction = wall_func(6,direction)

    return(point,direction)


def wall_func(wall,direction):
	"determines which way the line will bounce off walls"
	"when line bounces in a clockwise direction 2 is added to the moves variable"
	"and counterclockwise subtracts 2"
	if direction % 2 == 0:
		direction = direction + 4
	else:
		if wall + 1 == direction:
			direction + 2
		else:
			direction - 2

	return(direction)


def clean_up_points(points,width,height):
    "remove points that are off the edge"
    del_list = []

    for i in range(0,len(points)):
        point = points[i][0]
        if edge_test(point, width, height): del_list.append(i)

    for i in range(0,len(del_list)): del points[del_list.pop()]

    return(points)


def make_mp4(tmp_folder, framerate):
    from os import system
    from shutil import rmtree

    system('ffmpeg -loglevel quiet -y -f lavfi -i anullsrc -framerate ' + str(framerate) +
    ' -i ' + tmp_folder + '%06d.jpg -vcodec libx264 -crf 15 -pix_fmt yuv420p -c:a aac ' +
    '-strict -2 -shortest out.mp4')

    rmtree(tmp_folder)
