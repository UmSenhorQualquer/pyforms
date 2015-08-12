#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


import os
import pickle
from PyQt4 import uic, QtGui
from PyQt4 import QtCore
import pyforms.Utils.tools as tools
from pyforms.gui.Controls.ControlBase import ControlBase


class ControlHidden(ControlBase):

    _value = None
    _form = None
    _label = None

    def __init__(self, label = "", defaultValue = ""):
        self._value = defaultValue
        self._parent = 1
        self._label = label
        self.initForm()

    def initForm(self): pass

    def finishEditing(self):
        self.changed()

    def changed(self): pass

    def load(self, data):
        if 'value' in data: self.value = data['value']

    def save(self, data):
        if self.value: data['value'] = self.value

   
    def show(self): pass

    def hide(self): pass
    
    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    @property
    def enabled(self): return True

    @enabled.setter
    def enabled(self, value): pass

    ############################################################################

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value):
        oldvalue = self._value
        self._value = value
        if oldvalue!=value: self.changed()

    ############################################################################

    @property
    def label(self): return self._label

    @label.setter
    def label(self, value): self._label = value

    ############################################################################

    @property
    def form(self): return None

    ############################################################################

    @property
    def parent(self): return self._parent

    @parent.setter
    def parent(self, value): self._parent = value



    @property
    def maxWidth(self): return 0

    @maxWidth.setter
    def maxWidth(self, value): 0

    @property
    def minWidth(self): return 0

    @minWidth.setter
    def minWidth(self, value): 0


    @property
    def maxHeight(self): return 0

    @maxHeight.setter
    def maxHeight(self, value): 0

    @property
    def minHeight(self): return 0

    @minHeight.setter
    def minHeight(self, value): 0