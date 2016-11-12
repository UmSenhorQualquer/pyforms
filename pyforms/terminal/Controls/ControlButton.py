from pyforms.terminal.Controls.ControlBase import ControlBase

class ControlButton(ControlBase):

    @property
    def value(self): return None

    @value.setter
    def value(self, value):  self._value = value
        
