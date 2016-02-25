#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


import os
import sys
# import importlib
import math
from numpy import *
import zipfile
from subprocess import Popen, PIPE
import subprocess

# THIS DOESN'T WORK BECAUSE CONF IS IMPORTED WITH PYFORMS
# def load_everything_from(module_names):
#     """
#     Load all
#     :param module_names: modules to be imported
#     :type module_names: list of strings
#     """
#     g = globals()
#     for module_name in module_names:
#         m = importlib.import_module(module_name)
#         names = getattr(m, '__all__', None)
#         if names is None:
#             names = [name for name in dir(m) if not name.startswith('_')]
#         for name in names:
#             g[name] = getattr(m, name)

# THIS DOESN'T WORK BECAUSE CONF IS IMPORTED WITH PYFORMS
# def register_settings_module(module):
#     """
#     Append another settings module to PYFORMS_APP_SETTINGS
#     :param module:
#     :type module:
#     """
#     modules = os.getenv('PYFORMS_APP_SETTINGS', '').split(';')
#     modules.append(module)
#     os.environ['PYFORMS_APP_SETTINGS'] = ';'.join(modules)


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
    print(' '.join(execStr))
    proc = subprocess.Popen(execStr, stdout=PIPE, stderr=PIPE)
    (output, error) = proc.communicate()
    if error: print ('error: '+ error)
    print('output: '+ output)
        

def zipfiles(files, zippath):
    zippath = zipfile.ZipFile(zippath, 'w')
    for filename in files: zippath.write( filename)
		
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



def combinations( l1, l2 ):
    """
    Make combinations between the 2 lists without repeating
    """
    for i in range(len(l1)):
        yield zip( l1,l2)
        l1.insert(0,l1.pop())