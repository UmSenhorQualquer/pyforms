
from pyforms.terminal.Controls.ControlBase import ControlBase

class ControlCheckBox(ControlBase):

    @property
    def value(self): return self._value

    @value.setter
    def value(self, value): ControlBase.value.fset(self, (value=='True' or value==True) )