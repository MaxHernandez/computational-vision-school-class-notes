#! /usr/bin/python
from time import time
from sys import argv
from math import fabs
from PIL import Image, ImageOps, ImageDraw
from subprocess import call

def horizontal_histogram(image, output = 'horizontal.dat'):
    hist = list()
    pic = image.load()
    fl = open(output, 'w')

    for x in range(image.size[0]):
        suma = 0
        for y in range(image.size[1]):
            suma += pic[x, y]
        fl.write(str(x)+' '+str(suma)+'\n')
        hist.append(suma)

    fl.close()
    return hist

def vertical_histogram(image, output = 'vertical.dat'):
    hist = list()
    pic = image.load()
    fl = open(output, 'w')

    for y in range(image.size[1]):
        suma = 0
        for x in range(image.size[0]):
            suma += pic[x, y]
        fl.write(str(y)+' '+str(suma)+'\n')
        hist.append(suma)

    fl.close()
    return hist

def median_filter(image):
    pic = image.load()
    pic_copy = (image.copy()).load()

    for i in range(image.size[0]):
        for j in range(image.size[1]):

            temp = []
            for h in range(i-1, i+2):
                for l in range(j-1, j+2):
                    if h >= 0 and l >= 0 and h < image.size[0] and l < image.size[1]:
                        temp.append(pic_copy[h, l])
            temp.sort()
            pic[i,j] = int(temp[int(len(temp)/2)])
    return pic

def find_local_minimums(histogram):
    cosa = list()
    for i in range(1, len(histogram)-1):
        if histogram[i-1] > histogram[i] and histogram[i+1] > histogram[i]:
            yield i

def hole_detection(image_name, output="output.png", size=(128, 128)):
    image = Image.open(image_name)
    original_image = image.copy()
    image.thumbnail(size, Image.ANTIALIAS)
    
    image = ImageOps.grayscale(image)
    median_filter(image)

    horizontal_hist = horizontal_histogram(image)
    vertical_hist = vertical_histogram(image)
    
    horizontal = [ y for y in find_local_minimums(horizontal_hist)]
    vertical = [ x for x in find_local_minimums(vertical_hist)] 

    call(['gnuplot', 'hole.plot'])
 
    razon = image.size
    image = original_image
    razon = (float(image.size[0])/razon[0], float(image.size[1])/razon[1])
    draw = ImageDraw.Draw(image)
    
    for x in horizontal:
        x = int(x*razon[0])
        draw.line((x, 0, x, image.size[1]), fill=(0, 255, 0))

    for y in vertical:
        y = int(y*razon[1])
        draw.line((0, y, image.size[0], y), fill=(0, 0, 255))

    image.save(output)

def main():
    before = time()
    hole_detection(argv[1])
    print "Tiempo de corrida:", (time() - before)

main()
