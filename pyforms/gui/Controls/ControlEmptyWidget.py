#!/usr/bifn/python
# -*- coding: utf-8 -*-

from pysettings import conf

if conf.PYFORMS_USE_QT5:
	from PyQt5.QtWidgets import QWidget
	from PyQt5.QtWidgets import QVBoxLayout
else:
	from PyQt4.QtGui import QWidget
	from PyQt4.QtGui import QVBoxLayout

from pyforms.gui.Controls.ControlBase import ControlBase
from pyforms.gui.BaseWidget import BaseWidget


class ControlEmptyWidget(ControlBase, QWidget):
	def __init__(self, label='', default=None):
		QWidget.__init__(self)
		layout = QVBoxLayout()
#		layout.setMargin(0)
		self.form.setLayout(layout)

		ControlBase.__init__(self, label)
		self.value = default

	def init_form(self):
		pass

	############################################################################
	############ Properties ####################################################
	############################################################################

	@property
	def value(self):
		return ControlBase.value.fget(self)

	@value.setter
	def value(self, value):
		ControlBase.value.fset(self, value)
		self.__clear_layout()

		if value is None or value == '':  return

		if isinstance(self._value, list):
			for w in self._value:
				if w != None and w != "": self.form.layout().removeWidget(w.form)

		if isinstance(value, list):
			for w in value:
				self.form.layout().addWidget(w.form)
		else:
			self.form.layout().addWidget(value.form)

		# The init_form should be called only for the BaseWidget

		if isinstance(value, BaseWidget) and not value._formLoaded:
			value.init_form()

	@property
	def form(self):
		return self

	def save_form(self, data, path=None):
		if self.value is not None and self.value != '':
			data['value'] = {}
			self.value.save_form(data['value'], path)
		return data

	def load_form(self, data, path=None):
		if 'value' in data and self.value is not None and self.value != '':
			self.value.load_form(data['value'], path)

	def __clear_layout(self):
		if self.form.layout() is not None:
			old_layout = self.form.layout()
			for i in reversed(range(old_layout.count())):
				old_layout.itemAt(i).widget().setParent(None)

	def show(self):
		"""
		Show the control
		"""
		QWidget.show(self)

	def hide(self):
		"""
		Hide the control
		"""
		QWidget.hide(self)
