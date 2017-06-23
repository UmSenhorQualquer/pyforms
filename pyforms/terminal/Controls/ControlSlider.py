from pyforms.terminal.Controls.ControlBase import ControlBase

class ControlSlider(ControlBase):

    _min = 0
    _max = 100

    def __init__(self, label = "", helptext=None, defaultValue = 0, min = 0, max = 100):
        self._updateSlider = True
        self._min = min
        self._max = max
        
        ControlBase.__init__(self, label, defaultValue)


    @property
    def min(self): return self._min

    @min.setter
    def min(self, value):  self._min = value

    @property
    def max(self):  return  self._max

    @max.setter
    def max(self, value):  self._max = value