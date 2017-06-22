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
import pyforms.utils.tools as tools
from PyQt4 import QtGui
from PyQt4 import uic
from PyQt4.QtGui import QCompleter, QStringListModel

class ControlText(ControlBase):

	def initForm(self):
		control_path = tools.getFileInSameDirectory(__file__, "textInput.ui")
		self._form = uic.loadUi(control_path)
		self.form.label.setText(self._label)
		self.form.lineEdit.setText(self._value)
		self.form.setToolTip(self.help)

		super(ControlText, self).initForm()

		self.form.label.setAccessibleName('ControlText-label')
		self.form.lineEdit.editingFinished.connect(self.finishEditing)
		self.form.lineEdit.keyPressEvent = self.__key_pressed
		self.form.lineEdit._autoCompleteList = []
		self.form.lineEdit._completer = QCompleter(parent=self.form.lineEdit)
		self.form.lineEdit._completer.setCaseSensitivity(0)
		self.form.lineEdit._autoCompleteModel = QStringListModel(self.form.lineEdit._autoCompleteList, parent=self.form.lineEdit)
		self.form.lineEdit._completer.setModel(self.form.lineEdit._autoCompleteModel)
		self.form.lineEdit.setCompleter(self.form.lineEdit._completer)
		self.form.lineEdit._changedFname = None


	def finishEditing(self):
		"""Function called when the lineEdit widget is edited"""
		func_name = self.form.lineEdit._changedFname
		if callable(func_name):
			try:
				func_name()
			except:
				import sys
				print sys.exc_info()[0]
		self.changed()

	def __key_pressed(self, event): 
		QtGui.QLineEdit.keyPressEvent(self.form.lineEdit, event)

		self.key_pressed(event)

	def key_pressed(self, evt):
		pass
		
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

	@property
	def autoCompleteText(self):
		return self.form.lineEdit._autoCompleteList

	@autoCompleteText.setter
	def autoCompleteText(self, valueList):
		self.form.lineEdit._autoCompleteList = list(valueList)
		self.form.lineEdit._autoCompleteModel.setStringList(list(valueList))

	@property
	def dataChangedFunction(self):
		return self.form.lineEdit._changedFname

	@dataChangedFunction.setter
	def dataChangedFunction(self, value):
		self.form.lineEdit._changedFname = value

	@property
	def autoCompleteMode(self, value):
		return self.form.lineEdit._completer.completionMode()

	@autoCompleteMode.setter
	def autoCompleteMode(self, value):
		self.form.lineEdit._completer.setCompletionMode(value)

