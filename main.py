#!/usr/bin/env python

import sys, argparse
from random import *
import numpy, png


def parseArguments() :

	parser = argparse.ArgumentParser(description = "Simple Identicon generator, written in Python")

	parser.add_argument("name", help = "Define the name of the output file")
	parser.add_argument("-s", "--size", help = "Set the width and height of the picture in pixels, you can set the size of one pixel with the -p flag", type = int, default = 7)
	parser.add_argument("-p", "--pixel-size", help = "The size of one pixel", type = int, default = 50)
	parser.add_argument("-b", "--background-color", help = "Change the background color of the image (RGB values in range 256)", type = int, nargs = 3, default = (240, 240, 240))
	
	args = parser.parse_args()
	
	if not args.name.split(".")[-1] == "png" :
		args.name += ".png"
	
	if args.size <= 2 :
		raise argparse.ArgumentTypeError("Please select a larger picture size")
	
	if args.pixel_size <= 0 :
		raise argparse.ArgumentTypeError("Pixel size has to be greater than 0")
	
	for val in args.background_color :
		if not 0 <= val < 256 :
			raise argparse.ArgumentTypeError("RGB values have to be in range 256")
	
	return vars(args)


def main(params) :
	
    name = params["name"]
    pixel = params["pixel_size"]
    dims = params["size"] - 2
    colors = ( params["background_color"], (randint(0, 255), randint(0, 255), randint(0, 255)) )
    
    matrix = lambda : [[colors[0]]] + [[choice(colors)] for i in range(dims)] + [[colors[0]]]
    matrizen = list()
    
    for i in range(dims // 2 + dims % 2) :
    	matrizen.append(matrix())
    for i in range(dims // 2)[::-1] :
    	matrizen.append(matrizen[i])
    
    matrizen.insert(0, [[colors[0]] for i in range(dims+2)])
    matrizen.append([[colors[0]] for i in range(dims+2)])
    
    array = numpy.concatenate(matrizen, axis=1)
    array = array.repeat(pixel, axis=0).repeat(pixel, axis=1)
    array = numpy.array( [[ val for triple in dim for val in triple] for dim in array] )
    
    img = png.from_array(array, "RGB")
    img.info["bitdepth"] = 8
    img.save(name)


if __name__ == "__main__" :
	args = parseArguments()
	main(args)


