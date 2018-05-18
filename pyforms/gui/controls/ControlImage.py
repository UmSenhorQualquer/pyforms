# !/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from confapp import conf

logger = logging.getLogger(__name__)

from pyforms.gui.controls.ControlBase import ControlBase
from pyforms.utils import tools

try:
	import cv2
except:
	logger.debug("OpenCV not available")

import OpenGL.GL  as GL
import OpenGL.GLU as GLU
		
from AnyQt 			 import QtCore, QtOpenGL, uic
from AnyQt.QtWidgets import QWidget

from AnyQt import _api

if _api.USED_API == _api.QT_API_PYQT5:
	try:
		from AnyQt.QtOpenGL import QGLWidget
	except:
		logger.debug("No OpenGL library available")

	import platform
	if platform.system() == 'Darwin':
		from pyforms.gui.controls.control_player.VideoQt5GLWidget import VideoQt5GLWidget as VideoGLWidget
	else:
		from pyforms.gui.controls.control_player.VideoGLWidget import VideoGLWidget

elif _api.USED_API == _api.QT_API_PYQT4:
	try:
		from PyQt4.QtOpenGL import QGLWidget
	except:
		logger.debug("No OpenGL library available")

	from pyforms.gui.controls.control_player.VideoGLWidget import VideoGLWidget

import numpy as np

class ControlImage(ControlBase):
	_imageWidget = None

	def init_form(self):
		control_path = tools.getFileInSameDirectory(__file__, "image.ui")
		self._form = uic.loadUi(control_path)
		self._imageWidget = VideoGLWidget()
		self._form.imageLayout.addWidget(self._imageWidget)

	def save_form(self, data, path=None):
		if type(self.value) is np.ndarray: data['value'] = self._value

	def load_form(self, data, path=None):
		if 'value' in data: self.value = data['value']

	def repaint(self):
		self._imageWidget.repaint()

	@property
	def value(self):
		return ControlBase.value.fget(self)

	@value.setter
	def value(self, value):

		if isinstance(value, str):
			self._value = cv2.imread(value, 1)
		else:
			self._value = value

		if value is not None:
			if isinstance(self._value, list) or isinstance(self._value, tuple):
				self._imageWidget.paint(self._value)
			else:
				self._imageWidget.paint([self._value])

		self.changed_event()
