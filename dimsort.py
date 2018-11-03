#!/usr/bin/env python3
"""
dimsort.py

Python script that sorts images into folders by dimensions
in terms of resolution: 'height'x'width' in pixels
"""

import os
import sys
import shutil
import fnmatch
from PIL import Image

# set working directory where folders, named by dimension, will be created
workingDir = os.getcwd()

# move file from src to dest
def move(src,dest):
    shutil.move(src, dest)

# iterate through all files and folders in a directory
def pywalker(dirPath):
    for root, dirs, files in os.walk(dirPath):
        for file_ in files:
            nestedPath = workingDir+"/"+ os.path.join(root, file_)
            dimsort(nestedPath)

def dimsort(imgPath):
    """ Parse image dimensions 'height'<x>'width' in pixels
        and sort into directory of the same name """
    
    # if ext is an image format
    if fnmatch.fnmatch(imgPath, '*.jpg') or \
        fnmatch.fnmatch(imgPath, '*.jpeg') or \
        fnmatch.fnmatch(imgPath, '*.png'):

        try:
            # attempt to open image with PIL
            with Image.open(imgPath) as img:

                # create string and dir from dimensions, ex: (1080x1920)
                imgName = img.filename.lstrip(workingDir)
                imgWidth,imgHeigth = img.size
                heightByWidth = str(imgHeigth) +"x"+ str(imgWidth)
                dimPath = workingDir +"/"+ heightByWidth

                # create dir of same name unless prexisting
                if not os.path.isdir(dimPath):
                    try:
                        os.mkdir(dimPath)
                    except OSError as e:
                        sys.exit("Unable to create directory {}".format(heightByWidth))

                # sort image into folder if not already present
                if os.path.exists(dimPath+"/"+imgName):
                    print("Skipping '{}', file already present in {}".format(imgName, heightByWidth))
                else:
                    move(imgPath,dimPath)
                    print("{} moved to {}".format(imgName,heightByWidth))    

        except Exception as e:
            print(e)


if __name__=="__main__":

    # ensure user gives imgPath to <image> or <dir with images>
    if len(sys.argv) != 2:
        sys.exit("usage: python3 dimsort.py </imgPath/to/[dir]> or <[image.jpg|png|etc]>")

    if len(sys.argv) == 2:
        try:
            tryPath = sys.argv[1]

            # simplest case: imgPath to a single file
            if os.path.isfile(tryPath):
                dimsort(tryPath)

            # recursive case: imgPath is to a directory
            elif os.path.isdir(tryPath):
                pywalker(tryPath)

            # catch error
            else:
                sys.exit("Please check Path: {}".format(tryPath))

        except Exception as e:
            print("Error: {}".format(e))
