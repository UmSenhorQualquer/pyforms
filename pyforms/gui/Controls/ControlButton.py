#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@author: Ricardo Ribeiro
@credits: Ricardo Ribeiro
@license: MIT
@version: 0.0
@maintainer: Ricardo Ribeiro
@email: ricardojvr@gmail.com
@status: Development
@lastEditedBy: Carlos Mão de Ferro (carlos.maodeferro@neuro.fchampalimaud.org)
'''

from PyQt4 import uic, QtCore, QtGui
from pyforms.gui.Controls.ControlBase import ControlBase


class ControlButton(ControlBase):

	def __init__(self, label='', default=None, checkable=False, helptext=None):
		self._checkable = checkable
		super(ControlButton, self).__init__(label=label, default=default, helptext=helptext)

	def init_form(self):
		self._form = QtGui.QPushButton()
		self._form.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
		self._form.setCheckable(self._checkable)
		self.label = self._label
		self._form.setToolTip(self.help)

	def click(self): self._form.click()

	def load_form(self, data, path=None): pass

	def save_form(self, data, path=None): pass



	##########################################################################

	@property
	def label(self):
		return ControlBase.label.fget(self)

	@label.setter
	def label(self, value):
		ControlBase.label.fset(self, value)
		self._form.setText(self._label)

	@property
	def icon(self): return self._form.icon()

	@icon.setter
	def icon(self, value): 
		if isinstance(value, (str, unicode)):
			self._form.setIcon(QtGui.QIcon(value))
		else:
			self._form.setIcon(value)

	##########################################################################

	@property
	def value(self):
		return None

	@value.setter
	def value(self, value):
		self._form.clicked[bool].connect(value)

	@property
	def checked(self):
		return self._form.isChecked()

	@checked.setter
	def checked(self, value):
		self._form.setChecked(value)

	
