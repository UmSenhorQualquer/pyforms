from pyforms.terminal.Controls.ControlBase import ControlBase

class ControlSlider(ControlBase):


    def __init__(self, *args, **kwargs):
        self._min = kwargs.get('minimum', 0)
        self._max = kwargs.get('maximum', 100)
        if 'default' not in kwargs: kwargs['default'] = 0
        ControlBase.__init__(self, *args, **kwargs)
        

    @property
    def min(self): return self._min

    @min.setter
    def min(self, value):  self._min = value

    @property
    def max(self):  return  self._max

    @max.setter
    def max(self, value):  self._max = value