#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyforms.utils.tools as tools

from AnyQt 							  import uic
from pyforms.gui.controls.ControlBase import ControlBase


class ControlSlider(ControlBase):

	def __init__(self, *args, **kwargs):
		self._updateSlider = True
		self._min = kwargs.get('minimum', 0)
		self._max = kwargs.get('maximum', 100)
		if 'default' not in kwargs: kwargs['default'] = 0
		ControlBase.__init__(self, *args, **kwargs)
		
		self._form.value.setText(str(kwargs['default']))
		self._form.horizontalSlider.valueChanged.connect(self.valueChanged)

	

	def init_form(self):
		control_path = tools.getFileInSameDirectory(__file__, "sliderInput.ui")
		self._form = uic.loadUi(control_path)
		self._form.label.setText(self._label)
		self.form.label.setAccessibleName('ControlSlider-label')

		self._form.horizontalSlider.setMinimum(self._min)
		self._form.horizontalSlider.setMaximum(self._max)
		self._form.horizontalSlider.setValue(self._value)

	def valueChanged(self, value):
		self._updateSlider = False
		self.value = value
		self._updateSlider = True

	def load_form(self, data, path=None):
		if 'value' in data: self.value = int(data['value'])

	def save_form(self, data, path=None):
		data['value'] = self.value

	@property
	def value(self):
		return self._value

	@value.setter
	def value(self, value):
		ControlBase.value.fset(self, value)
		if self._updateSlider and self._value != None:  self._form.horizontalSlider.setValue(int(value))
		self._form.value.setText(str(value))

	@property
	def min(self):
		return self._form.horizontalSlider.minimum()

	@min.setter
	def min(self, value):
		self._form.horizontalSlider.setMinimum(value)

	@property
	def max(self):
		return self._form.horizontalSlider.maximum()

	@max.setter
	def max(self, value):
		self._form.horizontalSlider.setMaximum(value)
