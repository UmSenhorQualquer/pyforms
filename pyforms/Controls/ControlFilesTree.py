#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from pyforms.Controls.ControlBase import ControlBase
import pyforms.Utils.tools as tools
from PyQt4 import uic
from PyQt4 import QtGui, QtCore

class ControlFilesTree(ControlBase):

    def initForm(self):
        self._form = QtGui.QTreeView()

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value): 
        ControlBase.value.fset(self,value)
        model = QtGui.QFileSystemModel(parent=None)
        self._form.setModel(model)
        model.setRootPath(QtCore.QDir.currentPath())

        self._form.setRootIndex(model.setRootPath(value))

        
        self._form.setIconSize(QtCore.QSize(32,32))