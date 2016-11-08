#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlLabel"""

import pyforms.utils.tools as tools
from PyQt4 import uic
from pyforms.gui.Controls.ControlBase import ControlBase

__author__ = "Carlos Mão de Ferro"
__copyright__ = ""
__credits__ = "Carlos Mão de Ferro"
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"


class ControlLabel(ControlBase):

    def __init__(self, label=''):
        super(ControlLabel, self).__init__(label=label, defaultValue=label)

    def init_form(self):
        control_path = tools.getFileInSameDirectory(__file__, "label.ui")
        self._form = uic.loadUi(control_path)
        self._form.label.setText(self._label)

    def load(self, data): pass

    def save(self, data): pass

    def changed(self):
        self._form.label.setText(self._value)

    @property
    def form(self): return self._form
