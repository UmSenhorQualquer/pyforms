from ControlBase import ControlBase
import pyforms.Utils.tools as tools
from PyQt4 import uic
from PyQt4 import QtGui, QtCore

class ControlFilesTree(ControlBase):

    def initControl(self):
        self._form = QtGui.QTreeView()

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value): 
        ControlBase.value.fset(self,value)
        model = QtGui.QFileSystemModel(parent=self._parent)
        self._form.setModel(model)
        model.setRootPath(QtCore.QDir.currentPath())

        self._form.setRootIndex(model.setRootPath(value))

        
        self._form.setIconSize(QtCore.QSize(32,32))