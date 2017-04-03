#!/usr/bin/python
# -*- coding: utf-8 -*-


from pysettings import conf

from pyforms.gui.Controls.ControlBase import ControlBase

if conf.PYFORMS_USE_QT5:
	from PyQt5.QtWidgets import QTreeView
	from PyQt5.QtWidgets import QFileSystemModel
	from PyQt5 import QtCore

else:
	from PyQt4.QtGui import QTreeView
	from PyQt4.QtGui import QFileSystemModel
	from PyQt4 import QtCore


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
