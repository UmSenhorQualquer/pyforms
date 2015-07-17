#!/usr/bifn/python
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
from pyforms.BaseWidget import BaseWidget


class ControlEmptyWidget(ControlBase, QtGui.QWidget):

    def __init__(self, label=''):
        ControlBase.__init__(self, label)
        QtGui.QWidget.__init__(self)

        layout = QtGui.QVBoxLayout()
        layout.setMargin(0)
        self.form.setLayout(layout)

    def initForm(self):
        pass

    ##########################################################################
    ############ Properties ##################################################
    ##########################################################################

    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        ControlBase.value.fset(self, value)
        if value is None:
            return

        if isinstance(self._value, list):
            for w in self._value:
                if w != None and w != "":
                    self.form.layout().removeWidget(w.form)
        else:
            if self._value != None and self._value != "":
                self.form.layout().removeWidget(self._value.form)

        if isinstance(value, list):
            for w in value:
                self.form.layout().addWidget(w.form)
        else:
            self.form.layout().addWidget(value.form)

        # The initForm should be called only for the BaseWidget
        if isinstance(value, BaseWidget):
            value.initForm()

    @property
    def form(self): return self

    def save(self, data):
        if self.value != '':
            data['value'] = {}
            self.value.save(data['value'])

    def load(self, data):
        if 'value' in data:
            self.value.load(data['value'])
