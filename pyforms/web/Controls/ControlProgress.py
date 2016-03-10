from pyforms.web.Controls.ControlBase import ControlBase
import pyforms.Utils.tools as tools


class ControlProgress(ControlBase):

    _min = 0
    _max = 100

    def __init__(self, label = "%p%", defaultValue = 0, min = 0, max = 100):
        self._updateSlider = True
        self._min = min
        self._max = max
        ControlBase.__init__(self, label, defaultValue)
                
    def initControl(self): return "new ControlProgress('{0}', {1})".format( self._name, str(self.serialize()) )


    @property
    def value(self): return self._value
    @value.setter
    def value(self, value): self._value = value

    @property
    def min(self): return self._min
    @min.setter
    def min(self, value): self._min = value

    @property
    def max(self): return self._max
    @max.setter
    def max(self, value): self._max = value
        