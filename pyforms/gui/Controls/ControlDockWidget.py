#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyforms.gui.controls.ControlEmptyWidget import ControlEmptyWidget


class ControlDockWidget(ControlEmptyWidget):
	SIDE_LEFT = 'left'
	SIDE_RIGHT = 'right'
	SIDE_TOP = 'top'
	SIDE_BOTTOM = 'bottom'
	SIDE_DETACHED = 'detached'

	def __init__(self, *args, **kwargs):
		ControlEmptyWidget.__init__(self, *args, **kwargs)
		self.side = kwargs.get('side', 'left')
		self.order = kwargs.get('order',0)
		self.margin = kwargs.get('margin', 0)

		default = kwargs.get('default', None)
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
