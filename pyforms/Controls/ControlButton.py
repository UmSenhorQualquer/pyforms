#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


import pyforms.Utils.tools as tools
from PyQt4 import uic, QtGui
from pyforms.Controls.ControlBase import ControlBase

class ControlButton(ControlBase):

    def initForm(self):
        control_path = tools.getFileInSameDirectory(__file__,"button.ui")
        self._form = uic.loadUi( control_path )
        self._form.pushButton.setText(self._label)

    def load(self, data): pass

    def save(self, data): pass

    ############################################################################

    @property
    def label(self): return ControlBase.lable.fget(self)

    @label.setter
    def label(self, value): 
        ControlBase.label.fset(self, value)
        self._form.pushButton.setText(self._label)

    ############################################################################
    
    @property
    def value(self): return None

    @value.setter
    def value(self, value):
        self._form.pushButton.pressed.connect(value)
