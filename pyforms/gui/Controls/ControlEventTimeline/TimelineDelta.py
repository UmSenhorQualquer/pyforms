# !/usr/bin/python
# -*- coding: utf-8 -*-

from pysettings import conf

if conf.PYFORMS_USE_QT5:
	from PyQt5.QtWidgets import QInputDialog
	from PyQt5.QtGui import QColor

else:
	from PyQt4.QtGui import QColor, QInputDialog

from pyforms.gui.Controls.ControlEventTimeline.Track import Track


class TimelineDelta(object):
	"""
	
	"""

	def __init__(self, begin, end=30, title=None, height=30, top=0, parent=None):
		"""
		
		:param begin: 
		:param end: 
		:param title: 
		:param height: 
		:param top: 
		:param parent: 
		"""
		self._top = top
		self._height = height
		self._parent = parent
		self._title = title
		self._lock = False
		self._begin = begin
		self._end = end

		self.checkNumberOfTracks()

		self._defautcolor = parent._tracks[self.track].color

	##########################################################################
	#### HELPERS/FUNCTIONS ###################################################
	##########################################################################

	def checkNumberOfTracks(self):
		"""
		
		:return: 
		"""
		if self.track >= (self._parent.numberoftracks - 1):
			for i in range(self._parent.numberoftracks - 1, self.track + 1):
				self._parent.addTrack()

	def collide(self, x, y):
		"""
		
		:param x: 
		:param y: 
		:return: 
		"""
		return self.begin <= x <= self.end and self._top <= y <= (self._top + self._height)

	def in_range(self, start, end):
		"""
		:param start: 
		:param end: 
		:return: 
		"""
		return start <= self.begin and end >= self.end or \
			   self.begin <= start <= self.end or \
			   self.begin <= end <= self.end

	def canSlideBegin(self, x, y):
		"""
		
		:param x: 
		:param y: 
		:return: 
		"""
		return not self._lock and x == int(round(self.begin)) and self._top <= y <= (self._top + self._height)

	def canSlideEnd(self, x, y):
		"""
		
		:param x: 
		:param y: 
		:return: 
		"""
		return not self._lock and int(round(self.end)) == x and self._top <= y <= (self._top + self._height)

	def moveEnd(self, x):
		"""
		Move the right edge of the event rectangle.
		:param x: 
		"""

		# Do nothing if locked
		if self._lock:
			return

		# Do nothing if trying to go over the pther edge
		if self._end <= self._begin - x and x < 0:
			return

		# Increment accordingly
		self._end += x / self._parent._scale

		# Minimum begin position is at 0
		if self._end > (self._parent.width() / self._parent._scale):
			self._end = (self._parent.width() / self._parent._scale)

	def moveBegin(self, x):
		"""
		Move the left edge of the event rectangle.
		:param x: 
		"""

		# Do nothing if locked
		if self._lock:
			return

		# Do nothing if trying to go over the other edge
		if self._begin >= self._end - x and x > 0:
			return

		# Increment accordingly
		self._begin += x / self._parent._scale

		# Minimum begin position is at 0
		if self._begin < 0:
			self._begin = 0

	def move(self, x, y):
		"""
		
		:param x: 
		:param y: 
		:return: 
		"""
		if self._lock: return

		if (self.begin + x) >= 0 and (self.end + x) <= self._parent.width():
			self._begin += x / self._parent._scale
			self._end += x / self._parent._scale
		current_track = self.track
		new_track = Track.whichTrack(y)

		if current_track != new_track and new_track >= 0 and new_track <= self._parent.numberoftracks:
			self.track = new_track
			self.checkNumberOfTracks()

	def showEditWindow(self):
		"""
		
		:return: 
		"""
		text, ok = QInputDialog.getText(
			self._parent, 'Edit event', 'Comment:', text=self._title)
		if ok:
			self._title = str(text)
			self._parent.repaint()

	def draw(self, painter, showvalues=False):
		"""
		
		:param painter: 
		:param showvalues: 
		:return: 
		"""
		start, end = self.begin, self.end
		if self._lock:
			transparency = 0.1
		else:
			transparency = 0.5
		painter.setPen(QColor(0, 0, 0))
		painter.setOpacity(transparency)
		painter.drawRoundedRect(
			start, self._top, end - start, self._height, 3, 3)
		painter.setOpacity(1.0)

		painter.drawText(start + 3, self._top + 19, self._title)
		if showvalues:
			painter.drawText(
				start, self._top + 44, "[%d;%d] delta:%d" % (self._begin, self._end, self._end - self._begin))

	def remove(self):
		"""
		
		:return: 
		"""
		try:
			self._parent._tracks[self.track].periods.remove(self)
		except:
			pass

	##########################################################################
	#### PROPERTIES ##########################################################
	##########################################################################

	@property
	def title(self):
		return self._title

	@property
	def lock(self):
		return self._lock

	@lock.setter
	def lock(self, value):
		self._lock = value

	@property
	def begin(self):
		return self._begin * self._parent._scale

	@begin.setter
	def begin(self, value):
		if self._lock: return
		self._begin = value / self._parent._scale
		if self._begin < 0: self._begin = 0

	@property
	def end(self):
		return self._end * self._parent._scale

	@end.setter
	def end(self, value):
		if self._lock: return
		self._end = value / self._parent._scale
		if self._end > (self._parent.width() / self._parent._scale):
			self._end = (self._parent.width() / self._parent._scale)

	@property
	def track(self):
		return Track.whichTrack(self._top)

	@track.setter
	def track(self, value):
		# if the object exists in other track remove it
		if self.track < len(self._parent._tracks) and self in self._parent._tracks[self.track].periods: self.remove()

		# Verify if the new track exists. In case not create it
		self._top = Track.whichTop(value)
		if self.track >= len(self._parent._tracks): self._parent.addTrack()

		# if do not exists in the track add it
		if self not in self._parent._tracks[self.track].periods: self._parent._tracks[self.track].periods.append(self)

	@property
	def color(self):
		return self._defautcolor

	@color.setter
	def color(self, value):
		self._defautcolor = QColor(value) if (type(value) == str) else value

	@property
	def bgrcolor(self):
		return self._defautcolor.blue(), self._defautcolor.green(), self._defautcolor.red()

	@property
	def properties(self):
		return ['P',
		        self._lock,
		        int(round(self._begin)),
		        int(round(self._end)),
		        self._title,
		        self._defautcolor.name(),
		        self.track]

	@properties.setter
	def properties(self, value):
		self._lock = value[1] == 'True'
		self._begin = int(value[2])
		self._end = int(value[3])
		self._title = value[4]
		self._defautcolor = QColor(value[5])
		self.track = int(value[6])

		self.checkNumberOfTracks()
