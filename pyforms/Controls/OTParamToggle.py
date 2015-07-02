import os
import pickle
from PyQt4 import uic, QtGui
import opentrackerlib.utils.tools as tools
from opentrackerlib.modules.formcontrols.OTParamButton import OTParamButton

class OTParamToggle(OTParamButton):

    def initControl(self):
        OTParamButton.initControl(self)
        self._form.pushButton.setCheckable(True)

    def uncheck(self): self._form.pushButton.setChecked(False)

    def check(self): self._form.pushButton.setChecked(True)

    def isChecked(self): return self._form.pushButton.isChecked()

    @property
    def value(self): return None

    @value.setter
    def value(self, value):
        self._form.pushButton.toggled.connect(value)
