#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__      = "Ricardo Ribeiro"
__credits__     = ["Ricardo Ribeiro"]
__license__     = "MIT"
__version__     = "0.0"
__maintainer__  = "Ricardo Ribeiro"
__email__       = "ricardojvr@gmail.com"
__status__      = "Development"


from pyforms.Controls.ControlButton import ControlButton

class ControlToggle(ControlButton):

    def initControl(self):
        ControlToggle.initControl(self)
        self._form.pushButton.setCheckable(True)

    def uncheck(self): self._form.pushButton.setChecked(False)

    def check(self): self._form.pushButton.setChecked(True)

    def isChecked(self): return self._form.pushButton.isChecked()

    @property
    def value(self): return None

    @value.setter
    def value(self, value):
        self._form.pushButton.toggled.connect(value)
