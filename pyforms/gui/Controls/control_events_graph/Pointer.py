# !/usr/bin/python
# -*- coding: utf-8 -*-

from AnyQt.QtGui import QColor
from AnyQt 		 import QtCore

class Pointer(object):
	"""
	
	"""

	def __init__(self, position, parent, scroll):
		"""
		
		:param position: 
		:param parent: 
		:param scroll: 
		"""
		self._position = position
		self._parent = parent
		self._scroll = scroll

	def draw(self, painter, left_shift=0, scale=1):
		"""
		
		:param painter: 
		:param left_shift: 
		:param scale: 
		:return: 
		"""
		x = self.position / scale + left_shift

		painter.setPen(QColor(0, 255, 0))
		painter.setBrush(QColor(0, 255, 0))
		painter.drawLine(x, 8, x, self._parent.height())
		painter.drawEllipse(QtCore.QPoint(x, 8), 5, 5)
		painter.drawText(x + 8, 8 + 4, str(self.position))

	##########################################################################
	#### HELPERS/FUNCTIONS ###################################################
	##########################################################################

	def moveEvent(self):
		"""
		
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
		:rtype: bool 
		"""
		return False

	def canSlideEnd(self, x, y):
		"""
		
		:param x: 
		:param y: 
		:rtype: bool 
		"""
		return False

	def move(self, x, y):
		"""
		
		:param x: 
		:param y: 
		:return: 
		"""
		if (self._position - x) >= 0 and (self._position - x) <= (self._parent.width()):
			self._position += x
			self.moveEvent()

	##########################################################################
	#### PROPERTIES ##########################################################
	##########################################################################

	@property
	def position(self): return self._position

	@position.setter
	def position(self, value):
		self._position = value
		self.moveEvent()

	@property
	def frame(self): return self._position
