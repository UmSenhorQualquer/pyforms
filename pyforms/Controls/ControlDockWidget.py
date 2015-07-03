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
from PyQt4 import uic, QtGui,QtCore
from pyforms.Controls.ControlBase import ControlBase

class ControlDockWidget(ControlBase):

    def initControl(self):
        self._form = QtGui.QDockWidget()
        self._form.setFeatures(QtGui.QDockWidget.DockWidgetFloatable | QtGui.QDockWidget.DockWidgetClosable | QtGui.QDockWidget.DockWidgetMovable ) 
        self._form.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        
    ############################################################################


    @property
    def label(self): return self._form.windowTitle()

    @label.setter
    def label(self, value): ControlBase.label.fset(self, value); self._form.setWindowTitle(value)

    ############################################################################
    
    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value): 
        ControlBase.label.fset(self, value);
        self._form.setWidget(value.form)