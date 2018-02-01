# !/usr/bin/python
# -*- coding: utf-8 -*-

from AnyQt.QtGui import QColor
from AnyQt import QtCore

class Track(object):
	"""
	Track
	"""

	DEFAULT_COLOR = QColor(100, 100, 255)

	def __init__(self, parent):
		self._title = ''
		self._color = self.DEFAULT_COLOR
		self._parent = parent
		self._periods = []

	def __len__(self):
		return len(self._periods)

	@staticmethod
	def whichTrack(y):
		return (y - 20) // 34

	@staticmethod
	def whichTop(track):
		return track * 34 + 20

	@property
	def periods(self):
		return self._periods

	@property
	def color(self):
		return self._color

	@color.setter
	def color(self, value):
		self._color = value

	@property
	def title(self):
		return self._title

	@title.setter
	def title(self, value):
		self._title = value

	@property
	def events(self):
		return self._events

	def draw(self, painter, start, end, index):
		"""
		
		:param painter: 
		:param start: 
		:param end: 
		:param index: 
		:return: 
		"""
		y = (index * 34) + 18
		painter.drawLine(start, y, end, y)

	def drawPeriods(self, painter, start, end):
		"""
		
		:param painter: 
		:param start: 
		:param end: 
		:return: 
		"""
		for time in self._periods:
			painter.setBrush(time.color)
			time.draw(painter)

	def drawLabels(self, painter, index):
		"""
		
		:param painter: 
		:param index: 
		:return: 
		"""
		painter.setPen(QtCore.Qt.black)
		painter.setOpacity(0.5)

		x0 = self._parent.visibleRegion().boundingRect().x()
		xmax = self._parent.visibleRegion().boundingRect().width()
		text_length = painter.fontMetrics().width(self.title)
		x = 10
		y = (index * 34) + 30
		painter.drawText(x, y, self.title)

		painter.setOpacity(1.0)

	def selectDelta(self, x, y):
		"""
		
		:param x: 
		:param y: 
		:return: 
		"""
		for delta in self._periods:
			if delta.collide(x, y): return delta
		return None

	def periods_in_range(self, begin, end):
		for delta in self._periods:
			if delta.collide(x, y): return delta

	def clear(self):
		"""
		
		"""
		del self._periods[:]
		self._periods = []

	@property
	def properties(self):
		return ['T', self.title, self.color.name()]

	@properties.setter
	def properties(self, value):
		self.title = value[1]
		self.color = QColor(value[2])

	@property
	def track_index(self):
		for i, track in enumerate(self._parent._tracks):
			if track == self: return i
		return -1
