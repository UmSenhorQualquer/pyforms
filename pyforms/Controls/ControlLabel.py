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
from PyQt4 import uic
from pyforms.Controls.ControlBase import ControlBase


class ControlLabel(ControlBase):

    def initForm(self):
        control_path = tools.getFileInSameDirectory(__file__, "label.ui")
        self._form = uic.loadUi(control_path)
        self._form.label.setText(self._label)

    def load(self, data): pass

    def save(self, data): pass

    ##########################################################################
'''
    @property
    def text(self):
        return ControlBase.label.fget(self)

    @label.setter
    def text(self, value):
        ControlBase.label.fset(self, value)
        self._form.pushButton.setText(self._label)
'''
