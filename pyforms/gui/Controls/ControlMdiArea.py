#!/usr/bin/python
# -*- coding: utf-8 -*-

""" pyforms.gui.Controls.ControlMdiArea"""

from PyQt4 import QtGui
from pyforms.gui.Controls.ControlBase import ControlBase

__author__ = "Carlos Mão de Ferro"
__copyright__ = ""
__credits__ = "Carlos Mão de Ferro"
__license__ = "MIT"
__version__ = "0.0"
__maintainer__ = ["Ricardo Ribeiro", "Carlos Mão de Ferro"]
__email__ = ["ricardojvr at gmail.com", "cajomferro at gmail.com"]
__status__ = "Development"


class ControlMdiArea(ControlBase):
    """
    The ControlMdiArea wraps a QMdiArea widget which provides
     an area in which MDI windows are displayed.
    """

    def initForm(self):
        self._form = QtGui.QMdiArea()

    ##########################################################################
    ############ Properties ##################################################
    ##########################################################################

    @property
    def value(self): return ControlBase.value.fget(self)

    @value.setter
    def value(self, value):
        if isinstance(self._value, list):
            for w in self._value:
                if w is not None and w is not "":
                    self._form.layout().removeWidget(w._form)
        else:
            if self._value is not None and self._value is not "":
                self._form.layout().removeWidget(self._value._form)

        if isinstance(value, list):
            for w in value:
                self._form.layout().addWidget(w._form)
        else:
            self._form.layout().addWidget(value._form)

        ControlBase.value.fset(self, value)
