#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlEventTimeline.ControlEventTimeline

"""

import csv
import os
from PyQt4 import QtGui, QtCore
from pyforms.gui.Controls.ControlBase import ControlBase
from pyforms.gui.Controls.ControlEventTimeline.TimelineWidget import TimelineWidget
from pyforms.gui.Controls.ControlEventTimeline.TimelinePopupWindow import TimelinePopupWindow
from pyforms.gui.Controls.ControlEventTimeline.import_window import ImportWindow
from pyforms.gui.Controls.ControlEventTimeline.GraphsProperties import GraphsProperties
from pysettings import conf

__author__ = ["Ricardo Ribeiro", "Hugo Cachitas"]
__credits__ = ["Ricardo Ribeiro", "Hugo Cachitas"]
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = "Ricardo Ribeiro"
__email__ = "ricardojvr@gmail.com"
__status__ = "Development"


class ControlEventTimeline(ControlBase, QtGui.QWidget):
	"""
		Timeline events editor
	"""

	def __init__(self, label="", default=0, max=100):
		QtGui.QWidget.__init__(self)
		ControlBase.__init__(self, label, default)
		self._max = 100
		self._graphs_prop_win = GraphsProperties(self._time, self)


		# Popup menus that only show when clicking on a TIMELINEDELTA object
		self._deltaLockAction = self.add_popup_menu_option("Lock", self.__lockSelected, key='L')
		self._deltaColorAction = self.add_popup_menu_option("Pick a color", self.__pickColor)
		self._deltaRemoveAction = self.add_popup_menu_option("Remove", self.__removeSelected, key='Delete')
		self._deltaActions = [self._deltaLockAction, self._deltaColorAction, self._deltaRemoveAction]
		for action in self._deltaActions:
			action.setVisible(False)

		self.add_popup_menu_option("-")

		# General righ click popup menus
		self.add_popup_menu_option("Set track properties...", self.__setLinePropertiesEvent)
		self.add_popup_menu_option("Set graphs properties", self.show_graphs_properties)
		self.add_popup_menu_option("-")

		clean_menu = self.add_popup_submenu('Clean')

		self.add_popup_menu_option('Current line',function_action=self.__cleanLine, submenu=clean_menu)
		self.add_popup_menu_option('Everything',function_action=self.__clean, submenu=clean_menu)
		self.add_popup_menu_option('Charts',function_action=self.__cleanCharts, submenu=clean_menu)


	def init_form(self):
		# Get the current path of the file
		rootPath = os.path.dirname(__file__)

		vlayout = QtGui.QVBoxLayout()
		hlayout = QtGui.QHBoxLayout()
		# hlayout.setMargin(0)
		vlayout.setMargin(0)
		self.setLayout(vlayout)

		# Add scroll area
		scrollarea = QtGui.QScrollArea()
		scrollarea.setMinimumHeight(140)
		scrollarea.setWidgetResizable(True)
		scrollarea.keyPressEvent = self.__scrollAreaKeyPressEvent
		scrollarea.keyReleaseEvent = self.__scrollAreaKeyReleaseEvent
		vlayout.addWidget(scrollarea)
		#vlayout.setContentsMargins(5, 5, 5, 5)

		# The timeline widget
		widget = TimelineWidget(self)
		widget._scroll = scrollarea
		# widget.setMinimumHeight(1000)
		scrollarea.setWidget(widget)

		# TODO Options buttons
		# btn_1 = QtGui.QPushButton("?")
		# btn_2 = QtGui.QPushButton("?")
		# vlayout_options = QtGui.QVBoxLayout()
		# vlayout_options.addWidget(btn_1)
		# vlayout_options.addWidget(btn_2)
		# hlayout.addLayout(vlayout_options)
		# hlayout.addWidget(btn_1)
		# hlayout.addWidget(btn_2)

		# Timeline zoom slider
		slider = QtGui.QSlider(QtCore.Qt.Horizontal)
		slider.setFocusPolicy(QtCore.Qt.NoFocus)
		slider.setMinimum(1)
		slider.setMaximum(100)
		slider.setValue(10)
		slider.setPageStep(1)
		slider.setTickPosition(QtGui.QSlider.NoTicks)  # TicksBothSides
		slider.valueChanged.connect(self.__scaleSliderChange)
		
		slider_label_zoom_in 	= QtGui.QLabel()
		slider_label_zoom_out 	= QtGui.QLabel()
		slider_label_zoom_in.setPixmap(conf.PYFORMS_PIXMAP_EVENTTIMELINE_ZOOM_IN)
		slider_label_zoom_out.setPixmap(conf.PYFORMS_PIXMAP_EVENTTIMELINE_ZOOM_OUT)
		

		self._zoomLabel = QtGui.QLabel("100%")
		hlayout.addWidget(self._zoomLabel)
		hlayout.addWidget(slider_label_zoom_out)
		hlayout.addWidget(slider)
		hlayout.addWidget(slider_label_zoom_in)
		#hlayout.setContentsMargins(5, 0, 5, 5)
		# Import/Export Buttons
		btn_import = QtGui.QPushButton("Import")
		
		btn_import.setIcon(conf.PYFORMS_ICON_EVENTTIMELINE_IMPORT)
		btn_import.clicked.connect(self.__import)
		btn_export = QtGui.QPushButton("Export")

		btn_export.setIcon(conf.PYFORMS_ICON_EVENTTIMELINE_EXPORT)
		btn_export.clicked.connect(self.__export)
		# importexport_vlayout = QtGui.QVBoxLayout()
		# importexport_vlayout.addWidget(btn_import)
		# importexport_vlayout.addWidget(btn_export)
		# hlayout.addLayout(importexport_vlayout)
		hlayout.addWidget(btn_import)
		hlayout.addWidget(btn_export)

		vlayout.addLayout(hlayout)

		self._time = widget
		self._scrollArea = scrollarea

		

	##########################################################################
	#### HELPERS/PUBLIC FUNCTIONS ############################################
	##########################################################################

	def add_period(self, value, row=0, color=None):
		self._time.addPeriod(value, track, color)
		self._time.repaint()

	def add_graph(self, name, data): self._time.add_chart(name, data)

	def import_graph(self, filename, frame_col=0, val_col=1):
		self.__import()
		self._import_window.import_chart(filename, frame_col, val_col)
		
	def import_graph_file(self, filename, separator=';', ignore_rows=0):
		csvfile = open(filename, 'U')
		spamreader = csv.reader(csvfile, delimiter=separator)
		for i in range(ignore_rows): next(spamreader, None)
		self._time.importchart_csv(spamreader)
		csvfile.close()

	def show_graphs_properties(self):		
		self._graphs_prop_win.show()
		self._time.repaint()

	def import_csv(self, csvfile):
		# If there are annotation in the timeline, show a warning
		if len(self._time._tracks) > 0:  # dict returns True if not empty
			message = ["You are about to import new data. ",
					   "If you proceed, current annotations will be erased. ",
					   "Make sure to export current annotations first to save.",
					   "\n",
					   "Are you sure you want to proceed?"]
			reply = QtGui.QMessageBox.question(self,
											   "Warning!",
											   "".join(message),
											   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
											   QtGui.QMessageBox.No)

			if reply != QtGui.QMessageBox.Yes:
				return

		self._time.import_csv(csvfile)
		

	def export_csv_file(self, filename):
		with open(filename, 'w') as csvfile:
			spamwriter = csv.writer(csvfile, dialect='excel')				
			self._time.export_csv(spamwriter)
				

	def import_csv_file(self, filename):
		with open(filename, 'r') as csvfile:
			spamreader = csv.reader(csvfile, dialect='excel')				
			self._time.import_csv(spamreader)	

	##########################################################################
	#### EVENTS ##############################################################
	##########################################################################

	@property
	def pointer_changed_event(self): return self._time._pointer.moveEvent

	@pointer_changed_event.setter
	def pointer_changed_event(self, value): self._time._pointer.moveEvent = value


	##########################################################################
	#### PROPERTIES ##########################################################
	##########################################################################

	@property
	def value(self): return self._time.position

	@value.setter
	def value(self, value):
		ControlBase.value.fset(self, value)
		self._time.position = value

	@property
	def max(self): return self._time.minimumWidth()

	@max.setter
	def max(self, value):
		self._max = value
		self._time.setMinimumWidth(value)
		self.repaint()

	@property
	def mouse_over_row_index(self):
		globalPos = QtGui.QCursor.pos()
		widgetPos = self._time.mapFromGlobal(globalPos)
		return self._time.trackInPosition(widgetPos.x(), widgetPos.y())

	@property
	def form(self): return self

	@property
	def rows(self): return self._time.tracks

	@property 
	def graphs(self):
		return self._graphs_prop_win.charts


	##########################################################################
	#### PRIVATE FUNCTIONS ###################################################
	##########################################################################


	def about_to_show_contextmenu_event(self):
		for action in self._deltaActions:
			action.setVisible(
				True) if self._time._selected is not None else action.setVisible(False)


	def __setLinePropertiesEvent(self):
		"""
		This controls makes possible the edition of a track in the
		timeline, based on the position of the mouse.

		Updates:
		- Track label
		- Track default color
		"""
		current_track = self.mouseOverLine
		parent = self._time

		# Tracks info dict and index
		i = current_track

		# Save current default color to override with selected track color
		timeline_default_color = parent.color
		try:
			parent.color = self._time._tracks[current_track].color
		except Exception as e:
			error_message = ("You tried to edit an empty track.",
							 "\n",
							 "Initialize it by creating an event first.")
			QtGui.QMessageBox.warning(
				parent, "Attention!", "".join(error_message))
			return e

		# Create dialog
		dialog = TimelinePopupWindow(parent, i)
		dialog.setModal(True)  # to disable main application window

		# If dialog is accepted, update dict info
		if dialog._ui.exec_() == dialog.Accepted:
			# Update label
			if dialog.behavior is not None:
				self._time._tracks[i].title = dialog.behavior

			# Update color
			if self._time._tracks[i].color != dialog.color:
				for delta in self._time._tracks[i].periods:
					delta.color = dialog.color
				self._time._tracks[i].color = dialog.color
			self._time.repaint()
		else:
			pass

		# Restore timeline default color
		parent.color = timeline_default_color

	def __lockSelected(self): self._time.lockSelected()

	def __removeSelected(self): self._time.removeSelected()

	def __import(self):
		"""Import annotations from a file."""
		if not hasattr(self, '_import_window'): self._import_window = ImportWindow(self)
		self._import_window.show()


	def __export(self):
		"""Export annotations to a file."""

		filename, ffilter = QtGui.QFileDialog.getSaveFileNameAndFilter(parent=self,
													 caption="Export annotations file",
													 directory="untitled.csv",
													 filter="CSV Files (*.csv);;CSV Matrix Files (*.csv)",
													 options=QtGui.QFileDialog.DontUseNativeDialog)
		
		filename = str(filename)
		ffilter  = str(ffilter)
		if filename != "":
			with open(filename, 'w') as csvfile:
				spamwriter = csv.writer(csvfile, dialect='excel')
				if ffilter=='CSV Files (*.csv)':
					self._time.export_csv(spamwriter)
				elif ffilter=='CSV Matrix Files (*.csv)':
					self._time.export_2_csv_matrix(spamwriter)



	def __export_2_csv_matrix(self):
		QtGui.QMessageBox.warning(
				self, "Important!",'Please note that this file cannot be imported after.')

		filename = QtGui.QFileDialog.getSaveFileName(parent=self,
													 caption="Export matrix file",
													 directory="untitled.csv",
													 filter="CSV Files (*.csv)",
													 options=QtGui.QFileDialog.DontUseNativeDialog)
		if filename != "":
			with open(filename, 'w') as csvfile:
				spamwriter = csv.writer(csvfile, dialect='excel')
				self._time.export_2_csv_matrix(spamwriter)



	def __cleanLine(self):
		reply = QtGui.QMessageBox.question(self, 'Confirm',
										   "Are you sure you want to clean all the events?", QtGui.QMessageBox.Yes |
										   QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes:
			self._time.cleanLine()

	def __cleanCharts(self):
		reply = QtGui.QMessageBox.question(self, 'Confirm',
										   "Are you sure you want to clean all the charts?", QtGui.QMessageBox.Yes |
										   QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes:
			self._time.cleanCharts()

	def __clean(self):
		reply = QtGui.QMessageBox.question(self, 'Confirm',
										   "Are you sure you want to clean all the events?", QtGui.QMessageBox.Yes |
										   QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes:
			self._time.clean()

	def __pickColor(self):
		self._time.color = QtGui.QColorDialog.getColor(self._time.color)
		if self._time._selected != None:
			self._time._selected.color = self._time.color
			self._time.repaint()

	def __scaleSliderChange(self, value):
		scale = 0.1 * value
		self._time.setMinimumWidth(scale * self._max)
		self._time.scale = scale
		self._zoomLabel.setText(str(value * 10).zfill(3) + "%")

	def __scrollAreaKeyReleaseEvent(self, event):
		modifiers = int(event.modifiers())
		self._time.keyReleaseEvent(event)
		if  modifiers is not QtCore.Qt.ControlModifier and \
				modifiers is not int(QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier) and \
				modifiers is not QtCore.Qt.ShiftModifier:
			QtGui.QScrollArea.keyReleaseEvent(self._scrollArea, event)

	def __scrollAreaKeyPressEvent(self, event):
		modifiers = int(event.modifiers())
		if  modifiers is not QtCore.Qt.ControlModifier and \
				modifiers is not int(QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier) and \
				modifiers is not QtCore.Qt.ShiftModifier:
			QtGui.QScrollArea.keyPressEvent(self._scrollArea, event)