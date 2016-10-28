#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


import pyforms.utils.tools as tools
from PyQt4 import uic, QtGui, QtCore
from pyforms.gui.Controls.ControlBase import ControlBase

class ControlCheckBox(ControlBase):

    def initForm(self):
        control_path = tools.getFileInSameDirectory(__file__,"checkbox.ui")
        self._form = uic.loadUi( control_path )
        self._form.checkBox.setText(self._label)
        self._form.checkBox.stateChanged.connect(self.__checkedToggle)
	self._form.checkBox.stateChangedFname = None

        if self._value and self._value!='':
            self._form.checkBox.setCheckState( QtCore.Qt.Checked )
        else:
            self._form.checkBox.setCheckState( QtCore.Qt.Unchecked )

    def __checkedToggle(self): 
	func_name = self._form.checkBox.stateChangedFname
	if callable(func_name):
		try:
			func_name()
		except:
			import sys
			print sys.exc_info()[0]
	self.changed()

    def load(self, data):
        if 'value' in data: 
            self._form.checkBox.setChecked( data['value']=='True' )

    def save(self, data):
        data['value'] = str( self.isChecked() )

 
    @property
    def value(self): return self._form.checkBox.isChecked()

    @value.setter
    def value(self, value):
        ControlBase.value.fset(self,value)
        self._form.checkBox.setChecked(value)

    @property
    def stateChangedFunction(self):
	return self._form.checkBox.stateChangedFname

    @stateChangedFunction.setter
    def stateChangedFunction(self, value):
	self._form.checkBox.stateChangedFname = value


