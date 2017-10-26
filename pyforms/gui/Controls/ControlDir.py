#!/usr/bin/python
# -*- coding: utf-8 -*-

from pysettings import conf

from pyforms.gui.Controls.ControlText import ControlText

import pyforms.utils.tools as tools


from AnyQt 			 import uic
from AnyQt.QtWidgets import QFileDialog


class ControlDir(ControlText):
	def init_form(self):
		control_path = tools.getFileInSameDirectory(__file__, "fileInput.ui")
		self._form = uic.loadUi(control_path)
		self._form.label.setText(self._label)

	def click(self):
		value = str(QFileDialog.getExistingDirectory(self._form, 'Choose a directory', self.value))
		if value: self.value = value

	@property
	def parent(self): return ControlText.parent.fget(self, value)

	@parent.setter
	def parent(self, value):
		ControlText.parent.fset(self, value)
		self._form.pushButton.clicked.connect(self.click)
