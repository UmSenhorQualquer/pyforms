#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = ["Ricardo Ribeiro", "Hugo Cachitas"]
__credits__     = ["Ricardo Ribeiro", "Hugo Cachitas"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"



from PyQt4 import QtCore, QtGui

class TimelineChart(object):

	def __init__(self, timeLineWidget, csvfileobject, color=QtGui.QColor(255,0,0) ):
		self._data 		 = []
		self._firstFrame = None
		self._graphMax   = None
		self._graphMin   = None
		self._widget     = timeLineWidget
		self._color = color

		data = [map(float, row) for row in csvfileobject]
		
		self._graphMax = 0
		self._graphMin = 100000000000
		self._data = []
		lastX = 0
		for x,y in data:
			if y>self._graphMax: self._graphMax=y
			if y<self._graphMin: self._graphMin=y

			if int(x-lastX)>1: 
				for i in range(0, int(x-lastX)+1 ):
					self._data.append( (lastX+i,y) )
					#self._data.append( None )
			self._data.append( (x,y) )

			lastX = x
		#If the first frame of the data i not 0 fill the data array with Nones
		#for i in range( int(data[0][0]) ): self._data.append(None)

		#self._data 	+= data
		

	def draw(self,  painter, left, right, top, bottom):
		painter.setPen(self._color)
		painter.setOpacity(0.7)
		
		maxHeight 	= (bottom-top)
		start 		= self._widget.x2frame(left)
		end   		= self._widget.x2frame(right)
		end   		= len(self._data) if end>len(self._data) else end

		diff = self._graphMax - self._graphMin
		if diff<=0: diff=1
		

		yMiddle = self._graphMin+diff/2
		for pos1, pos2 in zip(self._data[start+1:end], self._data[start:end]):
			if pos1 and pos2: 
				x ,y  	= pos1
				xx,yy 	= pos2

				y -= self._graphMin
				yy -= self._graphMin

				y  		=  (y*maxHeight)  // diff #+ yMiddle
				yy 		=  (yy*maxHeight) // diff #+ yMiddle

				painter.drawLine(self._widget.frame2x(xx), yy, self._widget.frame2x(x), y );

		painter.setOpacity(1.0)