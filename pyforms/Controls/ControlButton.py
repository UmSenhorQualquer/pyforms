import pyforms.Utils.tools as tools
from PyQt4 import uic, QtGui
from pyforms.Controls.ControlBase import ControlBase

class ControlButton(ControlBase):

    def initControl(self):
        control_path = tools.getFileInSameDirectory(__file__,"button.ui")
        self._form = uic.loadUi( control_path )
        self._form.pushButton.setText(self._label)

    def load(self, data): pass

    def save(self, data): pass

    ############################################################################

    @property
    def label(self): return ControlBase.lable.fget(self)

    @label.setter
    def label(self, value): 
        ControlBase.label.fset(self, value)
        self._form.pushButton.setText(self._label)

    ############################################################################
    
    @property
    def value(self): return None

    @value.setter
    def value(self, value):
        self._form.pushButton.pressed.connect(value)
