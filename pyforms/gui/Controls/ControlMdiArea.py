#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlMdiArea"""

import logging

from PyQt4 import QtCore
from PyQt4.QtGui import QMdiArea

from pyforms.gui.Controls.ControlBase import ControlBase

logger = logging.getLogger(__name__)

__author__ = "Ricardo Ribeiro"
__copyright__ = ""
__credits__ = "Carlos Mão de Ferro"
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"


class ControlMdiArea(ControlBase, QMdiArea):
	"""
	The ControlMdiArea wraps a QMdiArea widget which provides
	 an area in which MDI windows are displayed.
	"""

	def __init__(self, label=""):
		QMdiArea.__init__(self)
		ControlBase.__init__(self, label)
		#		self._value = []
		self._showCloseButton = True

		self.logger = logging.getLogger(__name__)

	def __flags(self):
		flags = QtCore.Qt.SubWindow

		flags |= QtCore.Qt.WindowTitleHint
		flags |= QtCore.Qt.WindowMinimizeButtonHint
		flags |= QtCore.Qt.WindowMaximizeButtonHint
		if self._showCloseButton:
			flags |= QtCore.Qt.WindowSystemMenuHint
			flags |= QtCore.Qt.WindowCloseButtonHint

		return flags

	def __sub__(self, window):
		window.close()
		return self

	def __add__(self, widget):

		# if not widget._formLoaded:
		# 	widget.initForm()

		if not hasattr(widget, 'subwindow'):
			widget.subwindow = self.addSubWindow(widget)
			widget.subwindow.overrideWindowFlags(self.__flags())
		else:
			widget.subwindow.show()

		# self.value.append(other)

		widget.show()
		widget.closeEvent = lambda x: self._subWindowClosed(x)

		widget.setFocus()
		logger.debug("Sub window opened. MDI area sub windows: %s", self.subWindowList())
		return self

	def _subWindowClosed(self, closeEvent):

		window = self.activeSubWindow()
		widget = window.widget()

		# self.removeSubWindow(window)

		closeEvent.ignore()
		widget.beforeClose()
		window.hide()

		# If beforeClose return False, will just hide the window.
		# If return True or None remove it from the mdi area
		# res = activeWidget.beforeClose()



		# if res is None or res is True:
		# 	if activeWidget in self._value:
		# 		self._value.remove(activeWidget)

		logger.debug("Sub window closed. MDI area sub windows: %s", self.subWindowList())

	##########################################################################
	############ Properties ##################################################
	##########################################################################

	@property
	def showCloseButton(self):
		return self._showCloseButton

	@showCloseButton.setter
	def showCloseButton(self, value):
		self._showCloseButton = value

	@property
	def label(self):
		return self._label

	@label.setter
	def label(self, value):
		self._label = value

	@property
	def form(self):
		return self

	# @property
	# def value(self):
	# 	return ControlBase.value.fget(self)
	#
	# @value.setter
	# def value(self, value):
	# 	self.closeAllSubWindows()
	# 	self._value = []
	#
	# 	if isinstance(value, list):
	# 		for w in value:
	# 			self += w
	# 	else:
	# 		self += value
	#
	# 	ControlBase.value.fset(self, self._value)
