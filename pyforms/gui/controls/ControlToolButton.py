#!/usr/bin/python
# -*- coding: utf-8 -*-



from confapp import conf

from AnyQt.QtCore 	 import Qt
from AnyQt 			 import uic
from AnyQt.QtWidgets import QToolButton, QSizePolicy
from AnyQt.QtGui 	 import QIcon

from pyforms.gui.controls.ControlBase import ControlBase


class ControlToolButton(ControlBase):
	def __init__(self, *args, **kwargs):
		self._checkable = kwargs.get('checkable', False)
		self._maxheight = kwargs.get('maxheight', None)
		self._maxwidth = kwargs.get('maxwidth', None)
		super(ControlToolButton, self).__init__(*args, **kwargs)

		default = kwargs.get('default', None)
		if default: self.value = default

		icon = kwargs.get('icon', None)
		if icon: self.icon = icon

		

	def init_form(self):
		self._form = QToolButton()
		if self._maxwidth: self._form.setMaximumWidth(self._maxwidth)
		if self._maxheight: self._form.setMaximumHeight(self._maxheight)
		self._form.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
		self._form.setCheckable(self._checkable)
		self.label = self._label
		self._form.setToolTip(self.help)

	def click(self):
		self._form.click()

	def load_form(self, data, path=None):
		pass

	def save_form(self, data, path=None):
		pass

	##########################################################################

	@property
	def label(self):
		return ControlBase.label.fget(self)

	@label.setter
	def label(self, value):
		ControlBase.label.fset(self, value)
		if value is None:
			self._form.setToolButtonStyle(Qt.ToolButtonIconOnly)
		else:
			self._form.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
			self._form.setText(self._label)

	@property
	def icon(self):
		return self._form.icon()

	@icon.setter
	def icon(self, value):
		if isinstance(value, (str, bytes)):
			self._form.setIcon(QIcon(value))
		else:
			self._form.setIcon(value)

	##########################################################################

	@property
	def value(self):
		return None

	@value.setter
	def value(self, value):
		try:
			self._form.clicked.disconnect()  # ignore previous signals if any
		except TypeError as err:
			# http://stackoverflow.com/questions/21586643/pyqt-widget-connect-and-disconnect
			pass
		self._form.clicked[bool].connect(value)

	@property
	def checked(self):
		return self._form.isChecked()

	@checked.setter
	def checked(self, value):
		self._form.setChecked(value)
