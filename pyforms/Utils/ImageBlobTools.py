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
