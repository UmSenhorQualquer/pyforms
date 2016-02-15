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

from pyforms.gui.Controls.ControlBase import ControlBase
import pyforms.Utils.tools as tools
from PyQt4 import uic

class ControlText(ControlBase):

	def initForm(self):
		control_path = tools.getFileInSameDirectory(__file__, "textInput.ui")
		self._form = uic.loadUi(control_path)
		self.form.label.setText(self._label)
		self.form.lineEdit.setText(self._value)
		self.form.setToolTip(self.help)

		super(ControlText, self).initForm()
		self.form.lineEdit.editingFinished.connect(self.finishEditing)

	def finishEditing(self):
		"""Function called when the lineEdit widget is edited"""
		self.changed()
		
	###################################################################
	############ Properties ###########################################
	###################################################################

	@property
	def value(self):
		self._value = str(self._form.lineEdit.text())
		return self._value

	@value.setter
	def value(self, value):
		self._form.lineEdit.setText(value)
		ControlBase.value.fset(self, value)

	@property
	def label(self): return self.form.label.text()

	@label.setter
	def label(self, value):
		self.form.label.setText(value)
		ControlBase.label.fset(self, value)
