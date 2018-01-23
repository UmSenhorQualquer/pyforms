# !/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from pysettings      import conf
from AnyQt.QtWidgets import QWidget
from AnyQt.QtGui 	 import QColor, QPainter, QFont
from AnyQt 		     import QtCore

from pyforms.gui.controls.control_events_graph.Track 	 import Track
from pyforms.gui.controls.control_events_graph.Pointer import Pointer
from pyforms.gui.controls.control_events_graph.Event 	 import Event


class EventsWidget(QWidget):
	"""
	Timeline widget definition to be used in the ControlEventTimeline
	"""

	_defautcolor = QColor(100, 100, 255)

	def __init__(self, scroll):
		"""
		
		:param scroll: 
		"""
		self._is_painting = False
		self._break_draw = False  # This variable indicates if should continuing drawing the widget or should move foward

		super(EventsWidget, self).__init__()
		self._scroll = scroll

		# Set the widget background to white ############################
		palette = self.palette()
		palette.setColor(self.backgroundRole(), QtCore.Qt.white)
		self.setPalette(palette)
		#################################################################

		self._max_time = 0
		self._tracks = []  # List of tracks
		self._pointer = Pointer(0, self, scroll)  # Timeline ( greenline )
		self.tracks_height = 30  # Height in pixels
		self.scale = conf.PYFORMS_CONTROL_EVENTS_GRAPH_DEFAULT_SCALE

	##########################################################################
	#### HELPERS/FUNCTIONS ###################################################
	##########################################################################

	def clean(self):
		"""
		Clean all events
		"""
		for track in self._tracks:
			track.clear()
		del self._tracks[:]
		self._tracks = []
		self._break_draw = True and self._is_painting
		self.repaint()

	def add_track(self, title=None):
		"""
		Adds a new track
		:param title: 
		:return: track added 
		"""
		self._tracks.append(Track(parent=self))
		self.setMinimumHeight(self.which_top(len(self._tracks)))
		if title: self._tracks[-1].title = title
		return self._tracks[-1]

	def add_event(self, begin, end, title='', track=0, color="#FFFF00"):
		"""
		Adds an event.		
		:param begin: 
		:param end: 
		:param title: 
		:param track: 
		:param color: 
		:return: 
		"""

		period = Event(begin, end,
		               title=title,
		               parentWidget=self,
		               color=color
		               )

		if self._max_time < end:
			self._max_time = end
		# Create new tracks in case the variable track does not exists
		if len(self._tracks) <= track:
			for i in range(len(self._tracks), track + 1):
				t = self.add_track()
				t.title = title
		#################################################

		end_pixel = end / self._scale
		if end_pixel > self._scroll.maximum():
			self._scroll.setMaximum(end_pixel)

		self._tracks[track].add_period(period)
		return period

	def __check_current_time_is_visible(self, current_time):
		"""
		This function check if the current_time is visible to the user.
		:param current_time: 
		"""
		scroll_limit = (self._scroll.sliderPosition() + self.width()) * self._scale

		if current_time > scroll_limit:
			self._scroll.setMaximum(current_time / self._scale)
			self._scroll.setSliderPosition(current_time / self._scale - self.width())
		if current_time < (self._scroll.sliderPosition() * self._scale):
			self._scroll.setSliderPosition(current_time / self._scale)

	def which_track(self, y):
		"""
		Return the track index which collide with the Y coordenate
		:param y: 
		:return: 
		"""
		return (y - 20) // self.tracks_height

	def which_top(self, track):
		"""
		Return the Y coordenate where the track index start
		:param track: 
		:return: 
		"""
		return track * self.tracks_height + 20

	##########################################################################
	#### DRAW FUNCTIONS ######################################################
	##########################################################################

	def paintEvent(self, e):
		"""
		
		:param e: 
		:return: 
		"""
		self._is_painting = True
		super(EventsWidget, self).paintEvent(e)

		painter = QPainter()
		painter.begin(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setFont(QFont('Decorative', 8))

		slider_pos = self._scroll.sliderPosition()
		start = slider_pos * self._scale
		end = start + self.width() * self._scale

		for i, track in enumerate(self._tracks):
			if self._break_draw:
				break
			track.draw_periods(painter, start, end, track_index=i, left_shift=-self._scroll.sliderPosition(),
			                   scale=self._scale)

		# Draw only from pixel start to end
		painter.setPen(QtCore.Qt.DashLine)
		painter.setOpacity(0.3)

		# print('Draw', start, end, self._scale, self._scroll.sliderPosition(), self.width())

		# Draw vertical lines
		for x in range(start - (start % (100 * self._scale)), end, 100 * self._scale):
			x2draw = (x - slider_pos * self._scale) // self._scale
			painter.drawLine(x2draw, 20, x2draw, self.height())
			string = str(x)
			boundtext = painter.boundingRect(QtCore.QRectF(), string)
			painter.drawText(x2draw - boundtext.width() / 2, 15, string)

		for index, track in enumerate(self._tracks):
			top = self.which_top(index)
			# print(top)
			painter.drawLine(0, top, self.width(), top)
			painter.drawText(10, top + 15, track.title)
		painter.setOpacity(1.0)

		self._pointer.draw(painter, left_shift=-slider_pos, scale=self._scale)  # Draw the time pointer
		painter.end()

		self._break_draw = False
		self._is_painting = False

	##########################################################################
	#### PROPERTIES ##########################################################
	##########################################################################

	@property
	def scale(self):
		return self._scale

	@scale.setter
	def scale(self, value):
		self._scale = value
		self._scroll.setMaximum(self._max_time / self._scale)

	@property
	def scroll(self):
		return self._scroll

	@property
	def position(self):
		return self._pointer._position

	@position.setter
	def position(self, position):
		self._pointer._position = position
		self._break_draw = True and self._is_painting

		if (position / self._scale) >= sys.maxsize:
			self.scale += 1

		#######################################################################
		# Check if the current time position is inside the scroll
		# if is not in, update the scroll position
		self.__check_current_time_is_visible(position)
		#######################################################################
		self.repaint()

	@property
	def color(self):
		return self._defautcolor

	@color.setter
	def color(self, value):
		self._defautcolor = value

	@property
	def tracks_height(self):
		return self._tracks_height

	@tracks_height.setter
	def tracks_height(self, value):
		self._tracks_height = value
		new_height = len(self.tracks) * value + 20
		if new_height > self.height():
			self.setMinimumHeight(new_height)
		self._break_draw = True and self._is_painting
		self.repaint()

	@property
	def tracks(self):
		"""
		Get list of tracks
		:return: 
		"""
		return self._tracks

	##########################################################################
	#### IMPORT AND EXPORT DATA ##############################################
	##########################################################################

	def import_csv(self, csvfileobject):
		"""
		Extracts info from a file object and stores it in memory in
		order to display it on the timeline.

		Refer to the `export` method to learn about input file format
		and structure.
		"""
		# Clear previously stored info
		self._tracks = []
		self._selected = None

		for row in csvfileobject:
			if row[0] == "T":
				track = self.add_track()
				track.properties = row
			elif row[0] == "P":
				event = self.add_event(0, 1, '-')
				event.properties = row

	def export_csv(self, csvfileobject):
		"""
		Processes all timeline data in an arranged format to be written
		in a CSV file.


		Current file structure:
		=======================

		--- CSV FILE BEGIN ---
		Track info line
		Event info line
		Event info line
		...
		Track info line
		Event info line
		Event info line
		...
		Track info line
		Event info line
		Event info line
		...
		--- CSV FILE END ---


		Track info line format:
		=======================

		| T | Total # of events in this track |  |  | Color | Label |


		Event info line format:
		=======================

		| P | Lock status | Begin frame | End frame | Comment | Color |  |
		"""
		for index, track in enumerate(self._tracks):
			csvfileobject.writerow(track.properties)
			for delta in track.periods:
				csvfileobject.writerow(delta.properties)
