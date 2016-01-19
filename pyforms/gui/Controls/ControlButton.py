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
from PyQt4 import uic, QtCore, QtGui
from pyforms.gui.Controls.ControlBase import ControlBase


class ControlButton(ControlBase):

    def __init__(self, label='', checkable=False):
        self._checkable = checkable
        super(ControlButton, self).__init__(label)

    def initForm(self):
        #control_path = tools.getFileInSameDirectory(__file__, "button.ui")
        #self._form = uic.loadUi(control_path)
        #self._form.pushButton.setText(self._label)
        #self._form.pushButton.setCheckable(self._checkable)

        self._form = QtGui.QPushButton()
        self._form.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self._form.setCheckable(self._checkable)
        self.label = self._label
        self.tooltip = None

    def load(self, data): pass

    def save(self, data): pass

    ##########################################################################

    @property
    def label(self):
        return ControlBase.label.fget(self)

    @label.setter
    def label(self, value):
        ControlBase.label.fset(self, value)
        self._form.setText(self._label)

    ##########################################################################

    @property
    def value(self):
        return None

    @value.setter
    def value(self, value):
        self._form.clicked[bool].connect(value)

    @property
    def checked(self):
        return self._form.isChecked()

    @checked.setter
    def checked(self, value):
        self._form.setChecked(value)

    def click(self):
        self._form.click()
