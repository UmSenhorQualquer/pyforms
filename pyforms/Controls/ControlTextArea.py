import os
import pickle
import pyforms.Utils.tools as tools
from PyQt4 import uic, QtGui
from pyforms.Controls.ControlBase import ControlBase

class ControlTextArea(ControlBase):

    def initControl(self):
        control_path = tools.getFileInSameDirectory(__file__,"textArea.ui")
        self._form = uic.loadUi( control_path )
        self._form.label.setText(self._label)
        self._form.plainTextEdit.setPlainText(self._value)

    ############################################################################
    ############ Properties ####################################################
    ############################################################################

    @property
    def value(self): 
        self._value = str(self._form.plainTextEdit.toPlainText())
        return self._value

    @value.setter
    def value(self, value):
        ControlBase.value.fset(self,value)
        self._form.plainTextEdit.setPlainText(self._value)