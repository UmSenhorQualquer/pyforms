# !/usr/bin/python
# -*- coding: utf-8 -*-

import csv
from pyforms.gui.controls.ControlBase 					  import ControlBase
from pyforms.gui.controls.control_events_graph.EventsWidget import EventsWidget
from AnyQt.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QScrollBar, QFileDialog
from AnyQt 			 import QtCore


class ControlEventsGraph(ControlBase, QWidget):
	"""
		Timeline events editor
	"""

	def __init__(self, label="", default=0, min=0, max=100, **kwargs):
		"""
		
		:param label: 
		:param default: 
		:param min: 
		:param max: 
		:param kwargs: 
		"""
		QWidget.__init__(self)
		ControlBase.__init__(self, label, default, **kwargs)
		self.add_popup_menu_option('Export to CSV', self.__export)

	def init_form(self):
		vlayout = QVBoxLayout()

		if _api.USED_API == _api.QT_API_PYQT5:
			vlayout.setContentsMargins(0,0,0,0)
		elif _api.USED_API == _api.QT_API_PYQT4:
			vlayout.setMargin(0)

		self.setLayout(vlayout)

		self._scroll = QScrollBar(QtCore.Qt.Horizontal)

		scrollarea = QScrollArea()
		scrollarea.setMinimumHeight(140)
		scrollarea.setWidgetResizable(True)

		self._events_widget = EventsWidget(scroll=self._scroll)
		scrollarea.setWidget(self._events_widget)

		self._scroll.actionTriggered.connect(self.__scroll_changed)

		vlayout.addWidget(scrollarea)  # The timeline widget
		vlayout.addWidget(self._scroll)  # Add scroll

		self._scroll.setMaximum(0)
		self._scroll.setSliderPosition(0)

	##########################################################################
	#### HELPERS/PUBLIC FUNCTIONS ############################################
	##########################################################################

	def add_track(self, title=None):
		"""
		
		:param title: 
		"""
		self._events_widget.add_track(title)

	def add_event(self, begin, end, title='', track=0, color='#FFFF00'):
		"""
		
		:param begin: 
		:param end: 
		:param title: 
		:param track: 
		:param color: 
		:return: 
		"""
		return self._events_widget.add_event(begin, end, title, track, color)

	##########################################################################
	#### EVENTS ##############################################################
	##########################################################################

	def __scroll_changed(self, change): self.repaint()

	def get_export_filename(self): return "untitled.csv"

	def __export(self):
		"""Export annotations to a file."""
		filename = QFileDialog.getSaveFileName(parent=self,
		                                       caption="Export annotations file",
		                                       directory=self.get_export_filename(),
		                                       filter="CSV Files (*.csv)",
		                                       options=QFileDialog.DontUseNativeDialog)
		if filename != '':
			self.export_csv(filename)

	def export_csv(self, filename):
		"""
		Export annotations to a file.
		:param str filename: filename to open 
		"""
		with open(filename, 'wb') as csvfile:
			spamwriter = csv.writer(csvfile, dialect='excel')
			self._events_widget.export_csv(spamwriter)

	def repaint(self):
		"""
		
		"""
		self._events_widget.repaint()

	##########################################################################
	#### PROPERTIES ##########################################################
	##########################################################################
	"""
	Overwrite the changed event from the ControlBase
	"""

	@property
	def changed_event(self): return self._events_widget._pointer.moveEvent

	@changed_event.setter
	def changed_event(self, value): self._events_widget._pointer.moveEvent = value

	@property
	def value(self): return self._events_widget.position

	@value.setter
	def value(self, value): self._events_widget.position = value

	@property
	def form(self): return self

	@property
	def tracks(self): return self._events_widget.tracks

	@property
	def tracks_height(self): return self._events_widget.tracks_height

	@tracks_height.setter
	def tracks_height(self, value): self._events_widget.tracks_height = value

	@property
	def scale(self): return self._events_widget.scale

	@scale.setter
	def scale(self, value): self._events_widget.scale = value
