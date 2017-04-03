#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from pysettings import conf

if conf.PYFORMS_USE_QT5:
	from PyQt5.QtWidgets import QMdiArea
	from PyQt5.QtWidgets import QMdiSubWindow

else:
	from PyQt4.QtGui import QMdiArea
	from PyQt4.QtGui import QMdiSubWindow

from pyforms.gui.Controls.ControlBase import ControlBase

logger = logging.getLogger(__name__)


class ControlMdiArea(ControlBase, QMdiArea):
	"""
	The ControlMdiArea wraps a QMdiArea widget which provides
	 an area in which MDI windows are displayed.
	"""

	def __init__(self, label=""):
		QMdiArea.__init__(self)
		ControlBase.__init__(self, label)
		self._showCloseButton = True

		self.logger = logging.getLogger(__name__)

	def __sub__(self, widget):
		"""
		Remove subwindow and unassigned it from widget
		:param widget:
		:return:
		"""
		widget.close()
		self += widget  # little tweak to temporarily make this widget as the active subwindow
		self.removeSubWindow(widget.subwindow)
		del widget.subwindow

		logger.debug("Widget sub window removed. MDI area sub windows: %s", self.subWindowList())

		return self

	def __add__(self, widget):
		"""
		Show widget on mdi area.

		If widget does not have a subwindow assigned, create a new subwindow without enabling the WA_DeleteOnClose event.
		This will allow subwindow to be hidden instead of destroyed. Otherwise, the closeEvent.accept() will cause
		the "Internal c++ Object Already Deleted" problem.

		If widget already has a subwindow, just show them (both the subwindow and the widget inside)!
		:param widget:
		:return:
		"""

		if not hasattr(widget, 'subwindow'):
			subwindow = QMdiSubWindow()
			subwindow.setWidget(widget)
			rect = widget.geometry()
			# DO NOT SET ATTRIBUTE WA_DeleteOnClose because we want window not to be destroyed
			widget.subwindow = self.addSubWindow(subwindow)
			subwindow.setGeometry(rect)

		widget.subwindow.show()
		widget.show()
		widget.closeEvent = lambda x: self._subWindowClosed(x)
		widget.setFocus()

		logger.debug("Sub window opened. MDI area sub windows: %s", self.subWindowList())

		return self

	def _subWindowClosed(self, closeEvent):
		"""
		Perform actions when subwindow is closed.
		In this case, we don't want subwindow to be removed nor destroyed in order to reutilize later.
		The closeEvent.accept() will just hide the subwindow.
		:param closeEvent:
		:return:
		"""

		window = self.activeSubWindow()
		widget = window.widget()
		# self.removeSubWindow(window) DO NOT REMOVE TO KEEP WINDOW POSITION
		widget.beforeClose()
		closeEvent.accept()

		logger.debug("Sub window closed. MDI area sub windows: %s", self.subWindowList())

	##########################################################################
	############ Properties ##################################################
	##########################################################################

	@property
	def show_subwin_close_button(self): return self._showCloseButton

	@show_subwin_close_button.setter
	def show_subwin_close_button(self, value): self._showCloseButton = value

	@property
	def label(self): return self._label

	@label.setter
	def label(self, value): self._label = value

	@property
	def form(self): return self
