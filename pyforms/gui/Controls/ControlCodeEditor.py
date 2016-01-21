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

class ControlCodeEditor(ControlBase):

	def initForm(self):
		control_path = tools.getFileInSameDirectory(__file__, "code_editor.ui")
		self._form = uic.loadUi(control_path)
		# self.form.label.setText(self._label)
		# self.form.lineEdit.setText(self._value)
		# self.form.setToolTip(self.help)

		super(ControlCodeEditor, self).initForm()
		# self.form.lineEdit.editingFinished.connect(self.finishEditing)

#	def finishEditing(self):
#		"""Function called when the lineEdit widget is edited"""
#		self.changed()
#		self.form.lineEdit.focusNextChild()

	###################################################################
	############ Properties ###########################################
	###################################################################

	@property
	def value(self):
		return self._form.code_area.toPlainText()

	@value.setter
	def value(self, value):
		self._form.code_area.setPlainText(str(value))
