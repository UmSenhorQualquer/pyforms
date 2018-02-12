from pyforms.terminal.controls.ControlBase import ControlBase
from sys import stdout

class ControlProgress(ControlBase):

    _min = 0
    _max = 100

    def __init__(self, *args, **kwargs):
        self._updateSlider = True
        self._min = kwargs.get('min', kwargs.get('minimum', 0))
        self._max = kwargs.get('max', kwargs.get('maximum', 100))
        ControlBase.__init__(self, *args, **kwargs)
        
        
    @property
    def value(self): return self._value

    @value.setter
    def value(self, value):
        #diff = self._max-self._min

        if (value % 100 == 0):
            stdout.write( '\rprogress {0}/{1}'.format(value-self._min, self._max) )
        self._value = value

    @property
    def min(self): return self._min

    @min.setter
    def min(self, value): self._min = value

    @property
    def max(self): return self._max

    @max.setter
    def max(self, value): self._max = value