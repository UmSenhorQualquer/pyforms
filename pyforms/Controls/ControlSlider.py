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

class ControlSlider(ControlBase):

    _min = 0
    _max = 100

    def __init__(self, label = "", defaultValue = 0, min = 0, max = 100):
        self._updateSlider = True
        self._min = min
        self._max = max
        
        ControlBase.__init__(self, label, defaultValue)
        self._form.value.setText( str(defaultValue) )
        self._form.horizontalSlider.valueChanged.connect( self.valueChanged )
        
    def initControl(self):
        control_path = tools.getFileInSameDirectory(__file__,"sliderInput.ui")
        self._form = uic.loadUi( control_path )
        self._form.label.setText(self._label)
        self._form.horizontalSlider.setMinimum(self._min)
        self._form.horizontalSlider.setMaximum(self._max)
        self._form.horizontalSlider.setValue( self._value )

    def valueChanged(self, value):
        self._updateSlider = False
        self.value = value
        self._updateSlider = True

    def load(self, data):
        if 'value' in data: self.value = data['value']
        

    def save(self, data):
        if self.value: data['value'] = self.value        

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value):
        ControlBase.value.fset(self, value)
        if self._updateSlider and self._value!=None:  self._form.horizontalSlider.setValue( int(value) )
        self._form.value.setText( str(value) )
        

    @property
    def min(self): return self._form.horizontalSlider.minimum()

    @min.setter
    def min(self, value): self._form.horizontalSlider.setMinimum(value)

    @property
    def max(self): return self._form.horizontalSlider.maximum()

    @max.setter
    def max(self, value): self._form.horizontalSlider.setMaximum(value)