#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyforms.gui.controls.ControlEmptyWidget import ControlEmptyWidget


class ControlDockWidget(ControlEmptyWidget):
	SIDE_LEFT = 'left'
	SIDE_RIGHT = 'right'
	SIDE_TOP = 'top'
	SIDE_BOTTOM = 'bottom'
	SIDE_DETACHED = 'detached'

	def __init__(self, label='', default=None, side='left', order=0, margin=0):
		ControlEmptyWidget.__init__(self, label)
		self.side = side
		self.order = order
		self.margin = margin
		if default is not None: self.value = default
		self._show = True

	@property
	def label(self):
		return self._label

	@label.setter
	def label(self, value):
		self._label = value
		if hasattr(self, 'dock'): self.dock.setWindowTitle(value)

	def save_form(self, data, path=None):
		data['side'] = self.side
		super(ControlDockWidget, self).save_form(data, path=None)

	def load_form(self, data):
		self.side = data['side']
		super(ControlDockWidget, self).load_form(data, path=None)

	def show(self):
		"""
		Show the control
		"""
		self._show = True
		if hasattr(self, 'dock'): self.dock.show()

	def hide(self):
		"""
		Hide the control
		"""
		self._show = False
		if hasattr(self, 'dock'): self.dock.hide()
