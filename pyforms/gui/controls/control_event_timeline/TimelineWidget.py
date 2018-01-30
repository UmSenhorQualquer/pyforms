# !/usr/bin/python
# -*- coding: utf-8 -*-
from AnyQt.QtWidgets import QWidget, QMessageBox
from AnyQt.QtGui 	 import QColor, QPainter, QFont, QCursor
from AnyQt 			 import QtCore

from pyforms.gui.controls.control_event_timeline.Track 			import Track
from pyforms.gui.controls.control_event_timeline.TimelinePointer  import TimelinePointer
from pyforms.gui.controls.control_event_timeline.TimelineDelta 	import TimelineDelta
from pyforms.gui.controls.control_event_timeline.TimelineChart    import TimelineChart


class TimelineWidget(QWidget):
	"""
	Timeline widget definition to be used in the ControlEventTimeline
	"""

	_defautcolor = QColor(100, 100, 255)

	def __init__(self, parent_control):
		super(TimelineWidget, self).__init__()

		self.parent_control = parent_control

		# self.setFocusPolicy(QtCore.Qt.StrongFocus)
		# self.grabKeyboard()
		self.setMouseTracking(True)
		self.setMinimumWidth(300000)
		# self.setMinimumHeight(30)

		# Timeline background color
		palette = self.palette()
		palette.setColor(self.backgroundRole(), QtCore.Qt.white)
		self.setPalette(palette)

		self._chartsColors = [
			QColor(240, 163, 255), QColor(0, 117, 220),
			QColor(153, 63, 0), QColor(76, 0, 92),
			QColor(25, 25, 25), QColor(0, 92, 49),
			QColor(43, 206, 72), QColor(255, 204, 153),
			QColor(128, 128, 128), QColor(148, 255, 181),
			QColor(143, 124, 0), QColor(157, 204, 0),
			QColor(194, 0, 136), QColor(0, 51, 128),
			QColor(255, 164, 5), QColor(255, 168, 187),
			QColor(66, 102, 0), QColor(255, 0, 16),
			QColor(94, 241, 242), QColor(0, 153, 143),
			QColor(116, 10, 255), QColor(153, 0, 0),
			QColor(255, 255, 0), QColor(255, 80, 5)
		]
		self._charts = []
		self._tracks = [Track(parent=self)]

		self._scale = 1.0
		self._lastMouseY = None
		self._mouse_current_pos = None

		self._moving = False
		self._resizingBegin = False
		self._resizingEnd = False
		self._creating_event = False
		self._creating_event_start = None
		self._creating_event_end = None
		self._n_tracks = 1

		self._selected = None
		self._selected_track = 0
		self._pointer = TimelinePointer(0, self)

		# Video playback controls
		self._video_playing = False
		self._video_fps = None
		self._video_fps_min = None
		self._video_fps_max = None
		self._video_fps_inc = None

	##########################################################################
	#### HELPERS/FUNCTIONS ###################################################
	##########################################################################

	def __add__(self, other):
		self.parent_control.__add__(other)
		return self

	def __sub__(self, other):
		self.parent_control.__sub__(other)
		return self

	def x2frame(self, x):
		return int(x / self._scale)

	def frame2x(self, frame):
		return int(frame * self._scale)

	def remove_track(self, track):
		self._tracks.remove(track)
		self.setMinimumHeight(Track.whichTop(len(self._tracks)))

	# self.repaint()

	def rename_graph(self, graph_index, newname):
		self.parent_control.rename_graph(graph_index, newname)
		

	def removeSelected(self):
		if self._selected != None and not self._selected.lock:
			self._selected.remove()
			self._selected = None
			self.repaint()

	def lockSelected(self):
		if self._selected != None:
			self._selected.lock = not self._selected.lock
			self.repaint()

	def selectDelta(self, x, y):
		# Check if the timeline pointer was selected
		if y <= 20:
			if self._pointer.collide(x, y):
				return self._pointer
			else:
				return None
		# Check if the timeline periods were selected
		i = Track.whichTrack(y)
		if i >= len(self._tracks):
			return None

		return self._tracks[i].selectDelta(x, y)

	def __drawTrackLines(self, painter, start, end):
		# Draw only from pixel start to end
		painter.setPen(QtCore.Qt.DashLine)
		painter.setOpacity(0.3)
		# Draw horizontal lines
		# for track in range(0, self.numberoftracks + 1):
		#    y = (track * 34) + 18
		#    painter.drawLine(start, y, end, y)
		for i, track in enumerate(self._tracks):
			track.draw(painter, start, end, i)

		# Draw vertical lines
		for x in range(start - (start % 100), end, 100):
			painter.drawLine(x, 20, x, self.height())
			string = "{0}".format(int(round(x / self._scale)))
			boundtext = painter.boundingRect(QtCore.QRectF(), string)
			painter.drawText(x - boundtext.width() / 2, 15, string)

			if self._video_fps:
				string = "{0}".format(int(round((x / self._scale) * (1000.0 / self._video_fps))))
				boundtext = painter.boundingRect(QtCore.QRectF(), string)
				painter.drawText(x - boundtext.width() / 2, 30, string)

		painter.setOpacity(1.0)

		for index, track in enumerate(self._tracks):
			track.drawLabels(painter, index)



	def add_chart(self, name, data):
		chart = TimelineChart(self, color=self._chartsColors[len(self._charts)], name=name)
		chart.import_data(data)
		self._charts.append(chart)
		self.repaint()

	def importchart_csv(self, csvfileobject):
		chart = TimelineChart(self, color=self._chartsColors[len(self._charts)])
		chart.import_csv(csvfileobject)
		self._charts.append(chart)

		chart.name = "undefined name {0}".format(str(len(self._charts)))
		self.repaint()
		return chart

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
			if len(row) == 0: continue
			if row[0] == "T":
				track = self.addTrack()
				track.properties = row
			elif row[0] == "P":
				period = self.addPeriod([0, 1, '-'])
				period.properties = row

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

	def export_2_csv_matrix(self, csvfileobject):
		for index, track in enumerate(self._tracks):
			_, track_title, _ = track.properties
			for delta in track.periods:
				_, _, begin, end, delta_title, _, _ = delta.properties
				row = [track_title, begin, end, delta_title]

				csvfileobject.writerow(row)

	def cleanCharts(self):
		for graph in self.graphs: self -= 0
		self._charts = []
		self.repaint()

	def clean(self):
		for graph in self.graphs: self -= 0
		self._charts = []
		self._selected = None
		for track in self._tracks: track.clear()
		del self._tracks[:]
		self._tracks = []
		self.repaint()

	def cleanLine(self, track_index=None):
		if track_index is not None or self._selected is not None:
			track_index = track_index if track_index is not None else self._selected.track
			if len(self._tracks) > track_index:
				self._tracks[track_index].clear()
			self._selected = None
			self.repaint()
		else:
			QMessageBox.about(self, "Error", "You must select a timebar first")
			return

	def addTrack(self):
		t = Track(parent=self)
		self._tracks.append(t)
		self.setMinimumHeight(Track.whichTop(len(self._tracks)))
		return t

	def addPeriod(self, value, track=0, color=None):
		"""Adds an annotated interval."""
		begin, end, title = value
		period = TimelineDelta(begin, end, title=title, parent=self, top=Track.whichTop(track))
		self._tracks[period.track].periods.append(period)
		return period

	##########################################################################
	#### EVENTS ##############################################################
	##########################################################################

	def paintEvent(self, e):
		super(TimelineWidget, self).paintEvent(e)

		painter = QPainter()
		painter.begin(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setFont(QFont('Decorative', 8))

		start = self._scroll.horizontalScrollBar().sliderPosition()
		end = start + self.parent().width() + 50

		# Draw graphs ##########################################################
		if len(self._charts) > 0:
			painter.setPen(QtCore.Qt.black)
			middle = self.height() // 2
			painter.setOpacity(0.1)
			painter.drawLine(start, middle, end, middle)

		for chart in self._charts:
			chart.draw(painter, start, end, 0, self.height())
		# End draw graph #######################################################


		self.__drawTrackLines(painter, start, end)

		for track in self._tracks:
			track.drawPeriods(painter, start, end)

		# Draw the selected element
		if self._selected != None:
			painter.setBrush(QColor(255, 0, 0))
			self._selected.draw(painter, showvalues=True)

		# Draw the time pointer
		self._pointer.draw(painter)

		painter.end()

	def mouseDoubleClickEvent(self, event):
		if self._selected is not None and self._selected != self._pointer and self._selected.collide(event.x(),
		                                                                                             event.y()):
			self._selected.showEditWindow()
		elif event.y() > 20:
			top = (event.y() - 20) // 34
			y = top * 34 + 20
			x = event.x() / self._scale
			# time = TimelineDelta(x, x + 50 / self._scale, title='', top=y, parent=self)
			time = TimelineDelta(x, x + 10, title='', top=y, parent=self)
			self._tracks[time.track].periods.append(time)

			self._selected = time
			self._selected_track = self._selected.track
			self.repaint()

	def key_release_event(self, event):
		pass

	def keyReleaseEvent(self, event):
		super(TimelineWidget, self).keyReleaseEvent(event)
		self.key_release_event(event)

		if self._selected is not None:
			modifier = int(event.modifiers())

			# Move the event (or the pointer) left
			if modifier == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Left:
				self._selected.move(-1, 0)
				self.repaint()

			# Move the event (or the pointer) right
			if modifier == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Right:
				self._selected.move(1, 0)
				self.repaint()

			if self._selected != self._pointer:
				# Delete the selected event
				if event.key() == QtCore.Qt.Key_Delete:
					self.removeSelected()

				# Lock or unlock an event
				if event.key() == QtCore.Qt.Key_L:
					self.lockSelected()

				# Move the event up
				if modifier == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Up:
					self._selected.move(0, self._selected._top - 34)
					self.repaint()

				# Move the event down
				if modifier == QtCore.Qt.ControlModifier and event.key() == QtCore.Qt.Key_Down:
					self._selected.move(0, self._selected._top + 34)
					self.repaint()

				# Move the event end left
				if modifier == int(
								QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier) and event.key() == QtCore.Qt.Key_Left:
					self._selected.moveEnd(-1)
					self.repaint()

				# Move the event end right
				if modifier == int(
								QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier) and event.key() == QtCore.Qt.Key_Right:
					self._selected.moveEnd(1)
					self.repaint()

				# Move the event begin left
				if modifier == QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_Left:
					self._selected.moveBegin(-1)
					self.repaint()

				# Move the event begin right
				if modifier == QtCore.Qt.ShiftModifier and event.key() == QtCore.Qt.Key_Right:
					self._selected.moveBegin(1)
					self.repaint()

		else:
			# Keybinds to create an event at current frame
			if event.key() == QtCore.Qt.Key_S and not self._creating_event:
				# Start
				self._creating_event_start = self._pointer.frame
				self._creating_event = True

				# TODO Add some indicator that an event is being recorded, like
				# using the track selector circle to become red

				return

			if event.key() == QtCore.Qt.Key_S and self._creating_event:
				# End, must be followed right after Start key and have no
				# effect otherwise
				self._creating_event_end = self._pointer.frame

				start = self._creating_event_start
				end = self._creating_event_end
				comment = ""

				if end > start:
					self.addPeriod((start, end, comment), self._selected_track)
					self.repaint()
					self._creating_event = False
				else:
					self._creating_event = False

	def mousePressEvent(self, event):
		# Select the track
		selected_track = Track.whichTrack(event.y())
		if selected_track <= len(self._tracks):
			self._selected_track = selected_track

		# Select the period bar
		self._selected = self.selectDelta(event.x(), event.y())
		self._moving = False
		self._resizingBegin = False
		self._resizingEnd = False

		if self._selected is not None:
			# Select the action
			if event.buttons() == QtCore.Qt.LeftButton:
				if self._selected.canSlideEnd(event.x(), event.y()):
					self._resizingEnd = True
				elif self._selected.canSlideBegin(event.x(), event.y()):
					self._resizingBegin = True
				elif self._selected.collide(event.x(), event.y()):
					self._moving = True
		if event.y() <= 20 and not self._moving:
			self._pointer.position = self.x2frame(event.x())

		self.repaint()

	def mouseMoveEvent(self, event):
		super(TimelineWidget, self).mouseMoveEvent(event)
		self.parent_control.mouse_moveover_timeline_event(event)
		
		self._mouse_current_pos = event.x(), event.y()

		

		# Do nothing if no event bar is selected
		if self._selected is None:
			return

		# Set cursors
		if self._selected.canSlideBegin(event.x(), event.y()) or self._selected.canSlideEnd(event.x(), event.y()):
			self.setCursor(QCursor(QtCore.Qt.SizeHorCursor))
		elif self._selected.collide(event.x(), event.y()):
			self.setCursor(QCursor(QtCore.Qt.SizeAllCursor))
		else:
			self.setCursor(QCursor(QtCore.Qt.ArrowCursor))

		if self._selected is None:
			return

		if event.buttons() == QtCore.Qt.LeftButton:
			if self._lastMouseY is not None:
				diff = event.x() - self._lastMouseY
				if diff != 0:
					if self._moving:
						self._selected.move(diff, event.y())
					elif self._resizingBegin:
						self._selected.moveBegin(diff)
					elif self._resizingEnd:
						self._selected.moveEnd(diff)
					self.repaint()
			self._lastMouseY = event.x()

	def mouseReleaseEvent(self, event):
		self._lastMouseY = None

	def trackInPosition(self, x, y):
		return (y - 30) // 34

	def fpsChangeEvent(self):
		pass

	##########################################################################
	#### PROPERTIES ##########################################################
	##########################################################################

	def __checkPositionIsVisible(self, value):
		playerPos = self.frame2x(value)
		scrollLimit = self._scroll.horizontalScrollBar(
		).sliderPosition() + self.parent().width() - 50
		if playerPos > scrollLimit:
			newPos = playerPos - self.parent().width() + 50
			self._scroll.horizontalScrollBar().setSliderPosition(newPos)
		if playerPos < self._scroll.horizontalScrollBar().sliderPosition():
			self._scroll.horizontalScrollBar().setSliderPosition(playerPos)

	@property
	def scroll(self):
		return self._scroll.horizontalScrollBar()

	@property
	def position(self):
		return self._pointer._position

	@position.setter
	def position(self, value):
		self._pointer.position = value
		#######################################################################
		# Check if the player position is inside the scroll
		# if is not in, update the scroll position
		self.__checkPositionIsVisible(value)
		#######################################################################
		self.repaint()

	@property
	def scale(self):
		return self._scale

	@scale.setter
	def scale(self, value):
		self._scale = value
		self.repaint()

	@property
	def color(self):
		return self._defautcolor

	@color.setter
	def color(self, value):
		self._defautcolor = value

	@property
	def tracks(self):
		return self._tracks

	@property
	def numberoftracks(self):
		return len(self._tracks)  # self._n_tracks

	@numberoftracks.setter
	def numberoftracks(self, value):
		# self._n_tracks = value
		if value < len(self._tracks):
			for i in range(value, self._tracks + 1):
				self.addTrack()
		y = value * 34 + 20
		if y + 40 > self.height():
			self.setMinimumHeight(y + 40)

	# Video playback properties
	@property
	def isPlaying(self):
		return self._video_playing

	@property
	def fps(self):
		return self._video_fps

	@fps.setter
	def fps(self, value):
		self._video_fps = value

	@property
	def graphs_properties(self):
		return self.parent_control._graphs_prop_win

	@property
	def current_mouseover_track(self):
		if self._mouse_current_pos is None: return None
		return self.trackInPosition(*self._mouse_current_pos)

	@property
	def graphs(self): return self._charts