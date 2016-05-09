#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyforms.Utils.tools as tools
from PyQt4 import uic
from pyforms.gui.Controls.ControlBase import ControlBase

__author__ = "Ricardo Ribeiro"
__credits__ = ["Ricardo Ribeiro"]
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = "Ricardo Ribeiro"
__email__ = "ricardojvr@gmail.com"
__status__ = "Development"


class ControlTextArea(ControlBase):

    def initForm(self):
        control_path = tools.getFileInSameDirectory(__file__, "textArea.ui")
        self._form = uic.loadUi(control_path)
        self._form.label.setText(self._label)
        self._form.plainTextEdit.setPlainText(str(self._value))

        super(ControlTextArea, self).initForm()
        self.form.plainTextEdit.textChanged.connect(self.finishEditing)

    def __add__(self, other):
        self._form.plainTextEdit.appendPlainText(str(other))
        return self

    def finishEditing(self):
        """Function called when the lineEdit widget is edited"""
        self.changed()
        

    @property
    def value(self):
        return self._form.plainTextEdit.toPlainText()

    @value.setter
    def value(self, value):
        self._form.plainTextEdit.setPlainText(str(value))

    @property
    def readOnly(self):
        return self._form.plainTextEdit.isReadOnly()

    @readOnly.setter
    def readOnly(self, value):
        self._form.plainTextEdit.setReadOnly(value)
