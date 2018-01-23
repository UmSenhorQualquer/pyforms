#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from pyforms.gui.controls.ControlBase import ControlBase
from AnyQt 			 import uic
from AnyQt.QtWidgets import QApplication

class ControlProgress(ControlBase):
	def __init__(self, label="%p%", default=0, min=0, max=100):
		self._updateSlider = True
		self._min = min
		self._max = max

		ControlBase.__init__(self, label, default)

	def init_form(self):
		module_path = os.path.abspath(os.path.dirname(__file__))
		control_path = os.path.join(module_path, "progressInput.ui")
		self._form = uic.loadUi(control_path)
		self._form.horizontalSlider.setMinimum(self._min)
		self._form.horizontalSlider.setMaximum(self._max)
		self._form.horizontalSlider.setValue(self._value)
		self._form.horizontalSlider.setFormat(self._label)

	@property
	def label(self): return self._label

	@label.setter
	def label(self, value):
		self._label = value
		self._form.horizontalSlider.setFormat(self._label)

	@property
	def value(self): return self._form.horizontalSlider.value()

	@value.setter
	def value(self, value):
		self._form.horizontalSlider.setValue(value)
		QApplication.processEvents()

	def __add__(self, other):
		self.value = self.value + other
		return self

	def __sub__(self, other):
		self.value = self.value - other
		return self

	@property
	def min(self): return self._form.horizontalSlider.minimum()

	@min.setter
	def min(self, value): self._form.horizontalSlider.setMinimum(value)

	@property
	def max(self): return self._form.horizontalSlider.maximum()

	@max.setter
	def max(self, value): self._form.horizontalSlider.setMaximum(value)
