#!/usr/bin/python3
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

from PyQt4 import QtGui
from pyforms.Controls.ControlBase import ControlBase


class ControlEmptyWidget(ControlBase):

    def initControl(self):

        self._form = QtGui.QWidget()
        layout = QtGui.QVBoxLayout()
        layout.setMargin(0)
        self._form.setLayout(layout)

    ##########################################################################
    ############ Properties ##################################################
    ##########################################################################

    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        if isinstance(self._value, list):
            for w in self._value:
                if w is not None and w != "":
                    self._form.layout().removeWidget(w._form)
        else:
            if self._value is not None and self._value != "":
                self._form.layout().removeWidget(self._value._form)

        if isinstance(value, list):
            for w in value:
                self._form.layout().addWidget(w._form)
        else:
            self._form.layout().addWidget(value._form)

        ControlBase.value.fset(self, value)
