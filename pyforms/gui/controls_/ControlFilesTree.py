#!/usr/bin/python
# -*- coding: utf-8 -*-


from pysettings import conf

from pyforms.gui.controls.ControlBase import ControlBase

from AnyQt 			 import QtCore
from AnyQt.QtWidgets import QTreeView, QFileSystemModel

class ControlFilesTree(ControlBase):
	def init_form(self):
		self._form = QTreeView()

	@property
	def value(self): return self._value

	@value.setter
	def value(self, value):
		ControlBase.value.fset(self, value)
		model = QFileSystemModel(parent=None)
		self._form.setModel(model)
		model.setRootPath(QtCore.QDir.currentPath())

		self._form.setRootIndex(model.setRootPath(value))

		self._form.setIconSize(QtCore.QSize(32, 32))
