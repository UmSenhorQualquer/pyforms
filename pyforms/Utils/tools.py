#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


import os,sys
import math
from numpy import *
import zipfile
from subprocess import Popen, PIPE
import subprocess

try: 
    import cv2
except:
    print "Warning: It was not possible to import the cv2 library in the Utils.tools package"

    

def getFileInSameDirectory(file, name):
	module_path = os.path.abspath(os.path.dirname(file))
	return os.path.join(module_path, name)

def groupImagesHorizontally( images, color=False ):
	final_width, final_height = sum([ x.shape[1] for x in images ]), max([ x.shape[0] for x in images ])
	if color:
	    final_image = zeros( (final_height, final_width, 3), dtype=uint8 )
	else:
	    final_image = zeros( (final_height, final_width), dtype=uint8 )
	cursor = 0
	for image in images:
	    final_image[0:image.shape[0],cursor:cursor+image.shape[1]] = image
	    cursor += image.shape[1]
	return final_image


def groupImagesVertically( images, color=False ):
	final_width, final_height = max([ x.shape[1] for x in images ]), sum([ x.shape[0] for x in images ])
	if color:
	    final_image = zeros( (final_height, final_width, 3), dtype=uint8 )
	else:
	    final_image = zeros( (final_height, final_width), dtype=uint8 )
	cursor = 0
	for image in images:
	    final_image[cursor:cursor+image.shape[0],0:image.shape[1]] = image
	    cursor += image.shape[0]
	return final_image

def groupImage( images,color=False ):
	himages = []
	for group in images:
	    if isinstance(group, list):
	        himages.append( groupImagesVertically(group,color) )
	    else:
	        himages.append( group )

	return groupImagesHorizontally(himages,color)


def get_object_class_path(obj):
	path = os.path.abspath(sys.modules[obj.__module__].__file__)
	head, tail = os.path.split(path)
	return head


def lin_dist(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def lin_dist3d(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2 + (p0[2] - p1[2])**2)


def zipdir(path, zippath):
    """
    walkfiles = os.walk(path)
    zippath = zipfile.ZipFile(zippath, 'w')
    for root, dirs, files in walkfiles:
        for filename in files: zippath.write(os.path.join(root, filename))
    """
    execStr = ['zip', '-r',zippath, path]
    print ' '.join(execStr)
    proc = subprocess.Popen(execStr, stdout=PIPE, stderr=PIPE)
    (output, error) = proc.communicate()
    if error: print 'error: ', error
    print 'output: ', output
        

def zipfiles(files, zippath):
    zippath = zipfile.ZipFile(zippath, 'w')
    for filename in files: zippath.write( filename)
		
def captureSize(capture):
	return int(capture.get( cv2.cv.CV_CAP_PROP_FRAME_WIDTH )), int(capture.get( cv2.cv.CV_CAP_PROP_FRAME_HEIGHT ))

def points_angle(p1, p2): 
    x1, y1 = p1
    x2, y2 = p2
    rads = math.atan2(-(y2-y1),x2-x1)
    rads %= 2*pi
    return rads


def getTranslationMatrix2d(dx, dy):
    """
    Returns a numpy affine transformation matrix for a 2D translation of
    (dx, dy)
    """
    return matrix([[1, 0, dx], [0, 1, dy], [0, 0, 1]])

def rotate_image(image, angle):
    """
    Rotates the given image about it's centre
    """

    image_size = (image.shape[1], image.shape[0])
    image_center = tuple(array(image_size) / 2)

    rot_mat = vstack([cv2.getRotationMatrix2D(image_center, angle, 1.0), [0, 0, 1]])
    trans_mat = identity(3)

    w2 = image_size[0] * 0.5
    h2 = image_size[1] * 0.5

    rot_mat_notranslate = matrix(rot_mat[0:2, 0:2])

    tl = (array([-w2, h2]) * rot_mat_notranslate).A[0]
    tr = (array([w2, h2]) * rot_mat_notranslate).A[0]
    bl = (array([-w2, -h2]) * rot_mat_notranslate).A[0]
    br = (array([w2, -h2]) * rot_mat_notranslate).A[0]

    x_coords = [pt[0] for pt in [tl, tr, bl, br]]
    x_pos = [x for x in x_coords if x > 0]
    x_neg = [x for x in x_coords if x < 0]

    y_coords = [pt[1] for pt in [tl, tr, bl, br]]
    y_pos = [y for y in y_coords if y > 0]
    y_neg = [y for y in y_coords if y < 0]

    right_bound = max(x_pos)
    left_bound = min(x_neg)
    top_bound = max(y_pos)
    bot_bound = min(y_neg)

    new_w = int(abs(right_bound - left_bound))
    new_h = int(abs(top_bound - bot_bound))
    new_image_size = (new_w, new_h)

    new_midx = new_w * 0.5
    new_midy = new_h * 0.5

    dx = int(new_midx - w2)
    dy = int(new_midy - h2)

    trans_mat = getTranslationMatrix2d(dx, dy)
    affine_mat = (matrix(trans_mat) * matrix(rot_mat))[0:2, :]
    result = cv2.warpAffine(image, affine_mat, new_image_size, flags=cv2.INTER_LINEAR)

    return result


def combinations( l1, l2 ):
    """
    Make combinations between the 2 lists without repeating
    """
    for i in range(len(l1)):
        yield zip( l1,l2)
        l1.insert(0,l1.pop())