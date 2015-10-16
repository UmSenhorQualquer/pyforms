#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from numpy import *
import cv2, math

def biggestContour(contours, howmany=1):
    biggest = []
    for blob in contours: area = cv2.contourArea(blob); biggest.append( (area, blob) )
    if len(biggest)==0: return None
    biggest = sorted( biggest, key=lambda x: -x[0])
    if howmany==1: return biggest[0][1]
    return [x[1] for x in biggest[:howmany] ]

def getBiggestContour(image, howmany=1):
    (blobs, dummy) = cv2.findContours( image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE )
    return biggestContour(blobs, howmany)

def cutBiggestContour(image, howmany=1):
    contour = getBiggestContour(image)

    mask = zeros_like(image);cv2.drawContours(mask, array([contour]), -1, (255,255,255), -1 )
    tmp = cv2.bitwise_and( image, mask )

    rect = cv2.boundingRect(contour)
    x, y, w, h = rect
    x, y, xx, yy = x,y,x+w,y+h
    return tmp[y:yy, x:xx]


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
