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

import pyforms.Utils.tools as tools
from PyQt4 import QtCore, QtGui
from pyforms.gui.Controls.ControlBase import ControlBase
from PyQt4 import QtCore, QtGui

class ControlLabel(ControlBase, QtGui.QLabel):

    def __init__(self, label='', defaultValue=''):
        QtGui.QLabel.__init__(self)
        ControlBase.__init__(self, label, defaultValue)

    def initForm(self): 
        self.value = self._value

    def load(self, data): pass

    def save(self, data): pass

    @property
    def form(self): return self

    @property
    def value(self):
        return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        ControlBase.value.fset(self, value)
        self.setText(value)
        
        
