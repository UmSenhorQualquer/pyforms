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

    def init_form(self):
        control_path = tools.getFileInSameDirectory(__file__,"checkbox.ui")
        self._form = uic.loadUi( control_path )
        self._form.checkBox.setText(self._label)
        self._form.checkBox.stateChanged.connect(self.__checkedToggle)

        if self._value and self._value!='':
            self._form.checkBox.setCheckState( QtCore.Qt.Checked )
        else:
            self._form.checkBox.setCheckState( QtCore.Qt.Unchecked )

        if self.help: self.form.setToolTip(self.help)

    def __checkedToggle(self): self.changed_event()

    def load_form(self, data, path=None):
        if 'value' in data: 
            self._form.checkBox.setChecked( data['value']=='True' )

    def save_form(self, data, path=None):
        data['value'] = str( self._form.checkBox.isChecked() )

 
    @property
    def value(self): return self._form.checkBox.isChecked()

    @value.setter
    def value(self, value):
        ControlBase.value.fset(self,value)
        self._form.checkBox.setChecked(value)