# !/usr/bin/python
# -*- coding: utf-8 -*-

from AnyQt.QtGui import QColor
from AnyQt import QtCore


class TimelinePointer(object):
	def __init__(self, position, parent):
		"""
        		
		:param position: 
		:param parent: 
		"""
		self._position = position
		self._parent = parent

	def draw(self, painter, showvalues=False):
		"""
		
		:param painter: 
		:param showvalues: 
		:return: 
		"""
		painter.setPen(QColor(0, 255, 0))
		painter.setBrush(QColor(0, 255, 0))
		painter.drawLine(
			self.xposition, 8, self.xposition, self._parent.height())
		painter.drawEllipse(QtCore.QPoint(self.xposition, 8), 5, 5)
		painter.drawText(self.xposition + 8, 8 + 4, str(self._position))

	##########################################################################
	#### HELPERS/FUNCTIONS ###################################################
	##########################################################################

	def moveEvent(self):
		"""
		
		:return: 
		"""
		pass

	def collide(self, x, y):
		"""
		
		:param x: 
		:param y: 
		:return: 
		"""
		return (self.position - 5) <= x <= (self.position + 5) and 3 <= y <= 11

	def canSlideBegin(self, x, y):
		"""
		
		:param x: 
		:param y: 
		:return: 
		"""
		return False

	def canSlideEnd(self, x, y):
		"""
		
		:param x: 
		:param y: 
		:return: 
		"""
		return False

	def move(self, x, y):
		"""
		
		:param x: 
		:param y: 
		:return: 
		"""
		x = int(round(x / self._parent._scale))
		if (self._position - x) >= 0 and (self._position - x) <= (self._parent.width() / self._parent._scale):
			self._position += x
			self.moveEvent()

	##########################################################################
	#### PROPERTIES ##########################################################
	##########################################################################
	@property
	def xposition(self):
		return self._parent.frame2x(self.position)

	@property
	def position(self):
		return self._position

	@position.setter
	def position(self, value):
		self._position = value
		self.moveEvent()

	@property
	def frame(self): return self._position
