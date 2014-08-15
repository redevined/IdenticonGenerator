#!/usr/bin/env python

import sys, argparse
from random import *
import numpy, png


def parseArguments() :

	parser = argparse.ArgumentParser(description = "Color Changer to the IdenticonGenerator, randomizes the color an Identicon again")
	parser.add_argument("name", help = "Define the name of the output file")
	args = parser.parse_args()
	
	if not args.name.split(".")[-1] == "png" :
		args.name += ".png"
	
	return vars(args)


def main(params) :
	
    name = params["name"]
    
    reader = png.Reader(name)
    width, height, array, meta = reader.read_flat()
    
    old_colors = set(array)
    new_colors = ( array[0], randint(0, 255), randint(0, 255), randint(0, 255) )
    cc = dict(zip(old_colors, new_colors))
    
    array = [cc[pix] for pix in array]
    
    writer = png.Writer(width, height, **meta)
    out = open(name, "wb")
    writer.write_array(out, array)
    out.close()


if __name__ == "__main__" :
	args = parseArguments()
	main(args)


