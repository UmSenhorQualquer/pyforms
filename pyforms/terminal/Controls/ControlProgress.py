from pyforms.terminal.Controls.ControlBase import ControlBase

class ControlProgress(ControlBase):

    _min = 0
    _max = 100

    def __init__(self, label = "%p%", defaultValue = 0, min = 0, max = 100, helptext=None):
        self._updateSlider = True
        self._min = min
        self._max = max
        ControlBase.__init__(self, label, defaultValue)
        
        
    @property
    def value(self): return self._value

    @value.setter
    def value(self, value): self._value = value

    @property
    def min(self): return pass

    @min.setter
    def min(self, value): pass

    @property
    def max(self): return pass

    @max.setter
    def max(self, value): pass